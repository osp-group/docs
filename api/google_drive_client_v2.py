#!/usr/bin/env python3
"""
Cliente Python para Google Drive API v2
"""

import requests
import json
from typing import Dict, List, Optional, Tuple

class GoogleDriveClient:
    """Cliente para Google Drive API v2"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.initialized = False
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Tuple[bool, Dict]:
        """Faz requisição HTTP"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method == 'GET':
                response = self.session.get(url, **kwargs, timeout=30)
            elif method == 'POST':
                response = self.session.post(url, **kwargs, timeout=30)
            else:
                return False, {'error': f'Método {method} não suportado'}
            
            if response.status_code >= 400:
                return False, {
                    'error': f'HTTP {response.status_code}',
                    'details': response.text
                }
            
            return True, response.json()
        except requests.ConnectionError:
            return False, {'error': 'Conexão recusada - API não está rodando?'}
        except Exception as e:
            return False, {'error': str(e)}
    
    # ========================================================================
    # STATUS
    # ========================================================================
    
    def health_check(self) -> bool:
        """Verifica se API está online"""
        success, _ = self._make_request('GET', '/health')
        return success
    
    def get_status(self) -> Dict:
        """Obtém status da API"""
        success, data = self._make_request('GET', '/api/v2/status')
        return data if success else {'error': 'Falha ao obter status'}
    
    def init_service(self) -> Dict:
        """Inicializa serviço de Drive"""
        success, data = self._make_request('POST', '/api/v2/init')
        if success:
            self.initialized = True
        return data
    
    # ========================================================================
    # VALIDAÇÃO
    # ========================================================================
    
    def validate_url(self, url: str) -> Dict:
        """Valida uma URL do Google Drive"""
        success, data = self._make_request('POST', '/api/v2/validate/url', 
                                           json={'url': url})
        return data if success else {'error': 'Falha ao validar URL'}
    
    def validate_urls(self, urls: List[str]) -> Dict:
        """Valida múltiplas URLs"""
        success, data = self._make_request('POST', '/api/v2/validate/urls',
                                           json={'urls': urls})
        return data if success else {'error': 'Falha ao validar URLs'}
    
    def validate_urls_from_file(self, filepath: str) -> Dict:
        """Valida URLs de um arquivo (uma por linha)"""
        try:
            with open(filepath, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
            return self.validate_urls(urls)
        except Exception as e:
            return {'error': f'Erro ao ler arquivo: {e}'}
    
    # ========================================================================
    # BUSCA
    # ========================================================================
    
    def search(self, query: str, max_results: int = 10) -> Dict:
        """Busca documentos no Google Drive"""
        success, data = self._make_request('GET', '/api/v2/search',
                                           params={'q': query, 'max_results': max_results})
        return data if success else {'error': 'Falha ao buscar'}


# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

if __name__ == '__main__':
    client = GoogleDriveClient()
    
    print("\n" + "="*60)
    print("📊 Google Drive Client v2 - Exemplo")
    print("="*60)
    
    # Verificar status
    print("\n1️⃣ Verificando conexão...")
    if client.health_check():
        print("✅ API online")
    else:
        print("❌ API offline - execute: python3 api/google_drive_api_v2.py")
        exit(1)
    
    # Inicializar
    print("\n2️⃣ Inicializando serviço...")
    status = client.init_service()
    print(f"   Status: {status.get('status')}")
    print(f"   Auth: {status.get('auth_method')}")
    print(f"   Email: {status.get('authenticated_email')}")
    
    # Testar validação
    print("\n3️⃣ Testando validação de URL...")
    test_url = "https://docs.google.com/spreadsheets/d/1invalid/edit"
    result = client.validate_url(test_url)
    print(f"   URL: {result.get('url')}")
    print(f"   Válida: {result.get('valid')}")
    print(f"   Acessível: {result.get('accessible')}")
    
    # Buscar documentos
    print("\n4️⃣ Buscando documentos...")
    search_result = client.search("OKR", max_results=5)
    print(f"   Query: {search_result.get('query')}")
    print(f"   Resultados: {search_result.get('count')}")
    
    print("\n" + "="*60 + "\n")
