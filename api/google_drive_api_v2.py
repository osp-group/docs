#!/usr/bin/env python3
"""
Google Drive API v2 - REST API para validação e gerenciamento de links
Suporta OAuth 2.0 e Service Account
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from functools import wraps
import re

from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google.oauth2.credentials import Credentials as OAuthCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
SERVICE_ACCOUNT_EMAIL = "ga4-api-access@site-2026.iam.gserviceaccount.com"
CACHE_DURATION = 3600  # 1 hora

# ============================================================================
# ESTADO GLOBAL
# ============================================================================

class APIState:
    """Estado compartilhado da API"""
    def __init__(self):
        self.service = None
        self.auth_method = None  # 'service_account' ou 'oauth'
        self.authenticated_email = None
        self.cache = {}
        self.cache_timestamps = {}
        self.last_validated = None
        self.validation_stats = {
            'total': 0,
            'accessible': 0,
            'inaccessible': 0,
            'last_run': None
        }

state = APIState()


# ============================================================================
# AUTENTICAÇÃO
# ============================================================================

def init_service_account():
    """Inicializa com Service Account"""
    try:
        creds_path = os.path.expanduser("~/.credentials/ga4-api-key.json")
        if not os.path.exists(creds_path):
            logger.error(f"Service Account não encontrado: {creds_path}")
            return None
        
        creds = ServiceAccountCredentials.from_service_account_file(
            creds_path,
            scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=creds)
        state.auth_method = 'service_account'
        state.authenticated_email = SERVICE_ACCOUNT_EMAIL
        logger.info(f"✅ Service Account inicializado: {SERVICE_ACCOUNT_EMAIL}")
        return service
    except Exception as e:
        logger.error(f"Erro ao inicializar Service Account: {e}")
        return None


def init_oauth():
    """Inicializa com OAuth 2.0"""
    try:
        oauth_creds_path = "oauth_credentials.json"
        if not os.path.exists(oauth_creds_path):
            logger.warning(f"OAuth credentials não encontrado: {oauth_creds_path}")
            return None
        
        # Se tiver token salvo, usar
        if os.path.exists("oauth_token.json"):
            with open("oauth_token.json", "r") as f:
                token_data = json.load(f)
                creds = OAuthCredentials.from_authorized_user_info(token_data, SCOPES)
        else:
            # Criar novo fluxo OAuth
            flow = InstalledAppFlow.from_client_secrets_file(
                oauth_creds_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
            
            # Salvar token para próximas vezes
            with open("oauth_token.json", "w") as f:
                f.write(creds.to_json())
        
        service = build('drive', 'v3', credentials=creds)
        state.auth_method = 'oauth'
        state.authenticated_email = creds.client_id
        logger.info(f"✅ OAuth inicializado")
        return service
    except Exception as e:
        logger.error(f"Erro ao inicializar OAuth: {e}")
        return None


def init_drive_service():
    """Inicializa Drive service - tenta OAuth primeiro, depois Service Account"""
    # Tentar OAuth primeiro
    service = init_oauth()
    if service:
        state.service = service
        return service
    
    # Fallback para Service Account
    service = init_service_account()
    if service:
        state.service = service
        return service
    
    logger.error("❌ Nenhum método de autenticação disponível")
    return None


# ============================================================================
# CACHE
# ============================================================================

def get_cached(key: str) -> Optional[Dict]:
    """Obtém valor do cache se ainda válido"""
    if key not in state.cache:
        return None
    
    timestamp = state.cache_timestamps.get(key, 0)
    if datetime.now().timestamp() - timestamp > CACHE_DURATION:
        del state.cache[key]
        del state.cache_timestamps[key]
        return None
    
    return state.cache[key]


def set_cached(key: str, value: Dict):
    """Armazena valor no cache"""
    state.cache[key] = value
    state.cache_timestamps[key] = datetime.now().timestamp()


# ============================================================================
# VALIDAÇÃO DE LINKS
# ============================================================================

def extract_doc_id(url: str) -> Optional[str]:
    """Extrai ID do documento de uma URL do Google Drive"""
    patterns = [
        r'/d/([a-zA-Z0-9-_]+)',  # /d/ID/edit
        r'[?&]id=([a-zA-Z0-9-_]+)',  # ?id=ID
        r'#gid=([a-zA-Z0-9-_]+)',  # #gid=ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def validate_url_format(url: str) -> Tuple[bool, str]:
    """Valida formato da URL do Google Drive"""
    if not url.startswith('https://docs.google.com/'):
        return False, "URL não é do Google Drive"
    
    if not any(x in url for x in ['document', 'spreadsheets', 'presentation', 'forms']):
        return False, "Tipo de documento não suportado"
    
    if not extract_doc_id(url):
        return False, "ID do documento não encontrado na URL"
    
    return True, "OK"


def check_document_access(doc_id: str) -> Dict:
    """Verifica acesso a um documento específico"""
    cache_key = f"doc_{doc_id}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    
    try:
        if not state.service:
            return {
                'accessible': False,
                'error': 'Serviço não inicializado',
                'title': None,
                'owner': None,
                'shared_with_service_account': False,
                'mime_type': None,
                'last_modified': None
            }
        
        file = state.service.files().get(
            fileId=doc_id,
            fields='name, mimeType, owners, permissions, webViewLink, modifiedTime',
            supportsAllDrives=True
        ).execute()
        
        # Verifica se Service Account tem acesso
        shared_with_service_account = any(
            perm.get('emailAddress') == SERVICE_ACCOUNT_EMAIL 
            for perm in file.get('permissions', [])
        )
        
        result = {
            'accessible': True,
            'error': None,
            'title': file.get('name'),
            'owner': file.get('owners', [{}])[0].get('displayName'),
            'shared_with_service_account': shared_with_service_account,
            'mime_type': file.get('mimeType'),
            'last_modified': file.get('modifiedTime'),
            'web_view_link': file.get('webViewLink')
        }
        
        set_cached(cache_key, result)
        return result
        
    except HttpError as e:
        error_code = e.resp.status
        
        if error_code == 404:
            error_msg = "Documento não encontrado (ID inválido?)"
        elif error_code == 403:
            error_msg = "Acesso negado (não compartilhado com esta conta)"
        else:
            error_msg = f"Erro HTTP {error_code}"
        
        result = {
            'accessible': False,
            'error': error_msg,
            'title': None,
            'owner': None,
            'shared_with_service_account': False,
            'mime_type': None,
            'last_modified': None
        }
        
        set_cached(cache_key, result)
        return result


def search_documents(query: str, max_results: int = 10) -> List[Dict]:
    """Busca documentos no Google Drive"""
    try:
        if not state.service:
            return []
        
        results = state.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType, owners, webViewLink, modifiedTime)',
            pageSize=max_results,
            supportsAllDrives=True
        ).execute()
        
        files = results.get('files', [])
        return [
            {
                'id': f['id'],
                'name': f['name'],
                'mime_type': f['mimeType'],
                'owner': f.get('owners', [{}])[0].get('displayName'),
                'web_view_link': f.get('webViewLink'),
                'modified_time': f.get('modifiedTime')
            }
            for f in files
        ]
    except Exception as e:
        logger.error(f"Erro ao buscar documentos: {e}")
        return []


# ============================================================================
# ROTAS - STATUS & HEALTH
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/v2/status', methods=['GET'])
def status():
    """Status da API"""
    return jsonify({
        'status': 'operational' if state.service else 'not_configured',
        'auth_method': state.auth_method,
        'authenticated_email': state.authenticated_email,
        'cache_size': len(state.cache),
        'validation_stats': state.validation_stats,
        'timestamp': datetime.now().isoformat()
    }), 200


# ============================================================================
# ROTAS - VALIDAÇÃO DE URLS
# ============================================================================

@app.route('/api/v2/validate/url', methods=['POST'])
def validate_url_endpoint():
    """Valida uma URL do Google Drive"""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL é obrigatória'}), 400
    
    # Validar formato
    is_valid, format_msg = validate_url_format(url)
    if not is_valid:
        return jsonify({
            'url': url,
            'valid': False,
            'format_error': format_msg,
            'access_info': None
        }), 400
    
    # Extrair ID e validar acesso
    doc_id = extract_doc_id(url)
    access_info = check_document_access(doc_id)
    
    return jsonify({
        'url': url,
        'valid': True,
        'doc_id': doc_id,
        'accessible': access_info['accessible'],
        'access_info': access_info
    }), 200


@app.route('/api/v2/validate/urls', methods=['POST'])
def validate_urls_endpoint():
    """Valida múltiplas URLs do Google Drive"""
    data = request.get_json()
    urls = data.get('urls', [])
    
    if not urls:
        return jsonify({'error': 'URLs é obrigatória'}), 400
    
    results = []
    stats = {
        'total': len(urls),
        'valid_format': 0,
        'accessible': 0,
        'errors': 0
    }
    
    for url in urls:
        is_valid, format_msg = validate_url_format(url)
        
        if not is_valid:
            results.append({
                'url': url,
                'valid': False,
                'error': format_msg
            })
            stats['errors'] += 1
            continue
        
        stats['valid_format'] += 1
        
        doc_id = extract_doc_id(url)
        access_info = check_document_access(doc_id)
        
        if access_info['accessible']:
            stats['accessible'] += 1
        
        results.append({
            'url': url,
            'valid': True,
            'doc_id': doc_id,
            'accessible': access_info['accessible'],
            'access_info': access_info
        })
    
    return jsonify({
        'results': results,
        'stats': stats,
        'timestamp': datetime.now().isoformat()
    }), 200


# ============================================================================
# ROTAS - BUSCA
# ============================================================================

@app.route('/api/v2/search', methods=['GET'])
def search_endpoint():
    """Busca documentos no Google Drive"""
    query = request.args.get('q', '')
    max_results = int(request.args.get('max_results', 10))
    
    if not query:
        return jsonify({'error': 'Query é obrigatória'}), 400
    
    results = search_documents(query, max_results)
    
    return jsonify({
        'query': query,
        'results': results,
        'count': len(results),
        'timestamp': datetime.now().isoformat()
    }), 200


# ============================================================================
# ROTAS - INICIALIZAÇÃO
# ============================================================================

@app.route('/api/v2/init', methods=['POST'])
def init_endpoint():
    """Inicializa o serviço de Drive"""
    service = init_drive_service()
    
    if not service:
        return jsonify({
            'status': 'error',
            'message': 'Não foi possível inicializar serviço de Drive'
        }), 500
    
    return jsonify({
        'status': 'ok',
        'auth_method': state.auth_method,
        'authenticated_email': state.authenticated_email,
        'message': 'Serviço inicializado com sucesso'
    }), 200


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Inicializar serviço
    init_drive_service()
    
    # Rodar app
    logger.info("🚀 Iniciando Google Drive API v2")
    logger.info(f"   Auth: {state.auth_method}")
    logger.info(f"   Email: {state.authenticated_email}")
    logger.info("   Acessível em: http://localhost:5000")
    
    app.run(debug=True, port=5000)
