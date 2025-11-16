#!/usr/bin/env python3
"""
Google Drive Validator API - Enhanced with OAuth Support

Suporta dois modos de autenticação:
  1. Service Account (arquivo JSON com credenciais)
  2. OAuth 2.0 (autenticação com conta pessoal, ex: mkt@osp.com.br)

Usage:
  # Modo OAuth (recomendado com conta pessoal)
  python3 api/google_drive_validator_api.py

  # Modo Service Account (se preferir)
  export GOOGLE_CREDENTIALS=/path/to/service-account.json
  python3 api/google_drive_validator_api.py
"""

import os
import json
import pickle
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from flask import Flask, jsonify, request
from flask_cors import CORS
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as OAuth2Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state
class ValidatorState:
    def __init__(self):
        self.service = None
        self.auth_method = None  # 'oauth' or 'service_account'
        self.authenticated_email = None
        self.links_cache = {}
        self.last_validation = None
        self.validation_in_progress = False
        self.error = None

state = ValidatorState()

# Hub locations
HUBS = {
    "VENDAS": "VENDAS/templates/README.md",
    "CONHECIMENTO": "CONHECIMENTO/solucoes/INDEX.md",
    "DADOS_INTELIGENCIA": "DADOS_INTELIGENCIA/dashboards/README.md",
    "MARKETING": "MARKETING/campanhas/README.md",
}


def init_oauth_service() -> bool:
    """Initialize Google Drive API with OAuth 2.0"""
    
    token_file = "api/google_drive_token.pickle"
    credentials_file = "api/oauth_credentials.json"
    
    try:
        # Try loading existing token
        if os.path.exists(token_file):
            logger.info("📦 Loading existing OAuth token...")
            with open(token_file, 'rb') as f:
                credentials = pickle.load(f)
            
            # Refresh if expired
            if credentials.expired and credentials.refresh_token:
                logger.info("🔄 Refreshing expired token...")
                credentials.refresh(Request())
                with open(token_file, 'wb') as f:
                    pickle.dump(credentials, f)
            
            state.service = build('drive', 'v3', credentials=credentials)
            state.auth_method = 'oauth'
            
            # Get authenticated user email
            about = state.service.about().get(fields='user').execute()
            state.authenticated_email = about['user'].get('emailAddress', 'unknown')
            
            logger.info(f"✅ OAuth authenticated as: {state.authenticated_email}")
            return True
        
        # No existing token
        logger.info("⚠️ No OAuth token found")
        logger.info("Run: python3 api/google_drive_oauth_setup.py")
        return False
    
    except Exception as e:
        logger.error(f"❌ OAuth initialization failed: {e}")
        return False


def init_service_account_service(credentials_path: Optional[str] = None) -> bool:
    """Initialize Google Drive API with Service Account"""
    
    cred_path = credentials_path or os.environ.get("GOOGLE_CREDENTIALS")
    
    if not cred_path or not os.path.exists(cred_path):
        logger.info("⚠️ No Service Account credentials found")
        return False
    
    try:
        credentials = Credentials.from_service_account_file(
            cred_path,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        
        state.service = build('drive', 'v3', credentials=credentials)
        state.auth_method = 'service_account'
        state.authenticated_email = credentials.service_account_email
        
        logger.info(f"✅ Service Account authenticated as: {state.authenticated_email}")
        return True
    
    except Exception as e:
        logger.error(f"❌ Service Account initialization failed: {e}")
        return False


def init_drive_service() -> bool:
    """Initialize Google Drive API (tries OAuth first, then Service Account)"""
    
    logger.info("🚀 Initializing Google Drive API...")
    
    # Try OAuth first (preferred for personal accounts)
    if init_oauth_service():
        return True
    
    # Fall back to Service Account
    if init_service_account_service():
        return True
    
    state.error = "No authentication method available (OAuth or Service Account)"
    logger.error(state.error)
    return False


def extract_doc_id(url: str) -> Optional[str]:
    """Extract document ID from Google Drive URL"""
    
    patterns = [
        r'/d/([a-zA-Z0-9-_]+)',  # /d/ID/
        r'id=([a-zA-Z0-9-_]+)',   # ?id=ID
        r'key=([a-zA-Z0-9-_]+)',  # ?key=ID
    ]
    
    import re
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def check_document_access(doc_id: str) -> Dict:
    """Check if document is accessible via API"""
    
    try:
        file_metadata = state.service.files().get(
            fileId=doc_id,
            fields='id, name, mimeType, owners, lastModifiedTime, webViewLink, permissions'
        ).execute()
        
        # Check if shared with @osp-group
        permissions = file_metadata.get('permissions', [])
        shared_with_osp = any(
            p.get('emailAddress', '').endswith('@osp-group') 
            for p in permissions
        )
        
        # Check if public
        public = any(
            p.get('type') == 'anyone'
            for p in permissions
        )
        
        owners = file_metadata.get('owners', [])
        owner_email = owners[0].get('emailAddress', 'unknown') if owners else 'unknown'
        
        return {
            "accessible": True,
            "title": file_metadata.get('name', 'unknown'),
            "mime_type": file_metadata.get('mimeType', 'unknown'),
            "owner": owner_email,
            "shared_with_osp_group": shared_with_osp,
            "public": public,
            "last_modified": file_metadata.get('lastModifiedTime', ''),
            "web_view_link": file_metadata.get('webViewLink', ''),
            "error": None
        }
    
    except HttpError as e:
        error_code = e.resp.status
        if error_code == 404:
            error_msg = "Document not found (may be deleted)"
        elif error_code == 403:
            error_msg = "Access denied (not shared with authenticated account)"
        else:
            error_msg = f"HTTP {error_code}"
        
        return {
            "accessible": False,
            "error": error_msg,
            "title": None,
            "mime_type": None,
            "owner": None,
            "shared_with_osp_group": False,
            "public": False,
            "last_modified": None,
            "web_view_link": None
        }
    
    except Exception as e:
        return {
            "accessible": False,
            "error": str(e),
            "title": None,
            "mime_type": None,
            "owner": None,
            "shared_with_osp_group": False,
            "public": False,
            "last_modified": None,
            "web_view_link": None
        }


def load_hub_links() -> Dict[str, List[Dict]]:
    """Load and parse links from hub markdown files"""
    
    import re
    
    links_by_hub = {
        "VENDAS": [],
        "CONHECIMENTO": [],
        "DADOS_INTELIGENCIA": [],
        "MARKETING": []
    }
    
    link_pattern = r'\[([^\]]+)\]\((https://docs\.google\.com/[^)]+)\)'
    
    for hub_name, file_path in HUBS.items():
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all links
                for match in re.finditer(link_pattern, content):
                    text = match.group(1)
                    url = match.group(2)
                    doc_id = extract_doc_id(url)
                    
                    if doc_id:
                        links_by_hub[hub_name].append({
                            "text": text,
                            "url": url,
                            "doc_id": doc_id,
                            "hub": hub_name
                        })
        
        except Exception as e:
            logger.warning(f"Error reading {file_path}: {e}")
    
    return links_by_hub


def validate_all_links() -> Dict:
    """Validate all links"""
    
    if state.validation_in_progress:
        return {"error": "Validation already in progress"}
    
    state.validation_in_progress = True
    
    try:
        hub_links = load_hub_links()
        
        for hub_name in hub_links:
            for link in hub_links[hub_name]:
                validation = check_document_access(link['doc_id'])
                link['validation'] = validation
                link['status'] = "✅ Accessible" if validation['accessible'] else "❌ Inaccessible"
        
        state.links_cache = hub_links
        state.last_validation = datetime.now().isoformat()
        
        return {"status": "ok", "validated_at": state.last_validation}
    
    finally:
        state.validation_in_progress = False


# ============================================================================
# API Routes
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "api_version": "1.0",
        "drive_api": "connected" if state.service else "disconnected",
        "auth_method": state.auth_method,
        "authenticated_as": state.authenticated_email,
        "cached_results": bool(state.links_cache),
        "last_validation": state.last_validation
    })


@app.route('/api/v1/status', methods=['GET'])
def get_status():
    """Get overall validation status"""
    
    if not state.links_cache:
        validate_all_links()
    
    total = sum(len(links) for links in state.links_cache.values())
    accessible = sum(
        1 for links in state.links_cache.values()
        for link in links
        if link.get('validation', {}).get('accessible')
    )
    inaccessible = total - accessible
    
    return jsonify({
        "status": "ok",
        "validation": {
            "total": total,
            "accessible": accessible,
            "inaccessible": inaccessible
        },
        "last_validated": state.last_validation,
        "validation_in_progress": state.validation_in_progress
    })


@app.route('/api/v1/links', methods=['GET'])
def get_all_links():
    """Get all links"""
    
    if not state.links_cache:
        validate_all_links()
    
    total = sum(len(links) for links in state.links_cache.values())
    accessible = sum(
        1 for links in state.links_cache.values()
        for link in links
        if link.get('validation', {}).get('accessible')
    )
    
    return jsonify({
        "validated_at": state.last_validation,
        "hubs": state.links_cache,
        "summary": {
            "total": total,
            "accessible": accessible,
            "inaccessible": total - accessible
        }
    })


@app.route('/api/v1/links/<hub_name>', methods=['GET'])
def get_hub_links(hub_name):
    """Get links for specific hub"""
    
    if not state.links_cache:
        validate_all_links()
    
    if hub_name not in state.links_cache:
        return jsonify({"error": f"Hub '{hub_name}' not found"}), 404
    
    links = state.links_cache[hub_name]
    accessible = sum(1 for link in links if link.get('validation', {}).get('accessible'))
    
    return jsonify({
        "hub": hub_name,
        "total": len(links),
        "accessible": accessible,
        "inaccessible": len(links) - accessible,
        "links": links
    })


@app.route('/api/v1/links/<hub_name>/<doc_id>', methods=['GET'])
def get_link_details(hub_name, doc_id):
    """Get details for specific link"""
    
    if not state.links_cache:
        validate_all_links()
    
    if hub_name not in state.links_cache:
        return jsonify({"error": f"Hub '{hub_name}' not found"}), 404
    
    for link in state.links_cache[hub_name]:
        if link['doc_id'] == doc_id:
            return jsonify(link)
    
    return jsonify({"error": "Link not found"}), 404


@app.route('/api/v1/validate', methods=['POST'])
def validate_url():
    """Validate single URL"""
    
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL required"}), 400
    
    doc_id = extract_doc_id(url)
    if not doc_id:
        return jsonify({"error": "Invalid Google Drive URL"}), 400
    
    validation = check_document_access(doc_id)
    
    return jsonify({
        "url": url,
        "doc_id": doc_id,
        "validation": validation
    })


@app.route('/api/v1/validate/all', methods=['POST'])
def validate_all():
    """Trigger full validation"""
    
    result = validate_all_links()
    return jsonify(result)


@app.route('/api/v1/permissions', methods=['GET'])
def get_permissions():
    """Get permission audit summary"""
    
    if not state.links_cache:
        validate_all_links()
    
    summary = {
        "total": 0,
        "shared_with_osp_group": 0,
        "not_shared_with_osp_group": 0,
        "public": 0,
        "private": 0,
        "by_hub": {}
    }
    
    for hub_name, links in state.links_cache.items():
        hub_summary = {
            "total": len(links),
            "shared_with_osp_group": 0,
            "not_shared_with_osp_group": 0,
            "public": 0,
            "private": 0
        }
        
        for link in links:
            validation = link.get('validation', {})
            
            if validation.get('accessible'):
                summary['total'] += 1
                hub_summary['total'] = len(links)
                
                if validation.get('shared_with_osp_group'):
                    summary['shared_with_osp_group'] += 1
                    hub_summary['shared_with_osp_group'] += 1
                else:
                    summary['not_shared_with_osp_group'] += 1
                    hub_summary['not_shared_with_osp_group'] += 1
                
                if validation.get('public'):
                    summary['public'] += 1
                    hub_summary['public'] += 1
                else:
                    summary['private'] += 1
                    hub_summary['private'] += 1
        
        summary['by_hub'][hub_name] = hub_summary
    
    return jsonify(summary)


# ============================================================================
# Main
# ============================================================================

def main():
    """Main entry point"""
    
    print("\n" + "=" * 70)
    print("🚀 Starting Google Drive Validator API...")
    print("=" * 70)
    
    # Initialize API
    if not init_drive_service():
        print("\n❌ Failed to initialize Google Drive API")
        print("\nOptions:")
        print("1. OAuth: Run 'python3 api/google_drive_oauth_setup.py'")
        print("2. Service Account: Set GOOGLE_CREDENTIALS environment variable")
        return
    
    print(f"\n✅ Drive API ready")
    print(f"   Authentication: {state.auth_method}")
    print(f"   Authenticated as: {state.authenticated_email}")
    
    print("\n📚 API Endpoints:")
    print("  GET  /health                           - Health check")
    print("  GET  /api/v1/status                    - Overall status")
    print("  GET  /api/v1/links                     - All links")
    print("  GET  /api/v1/links/<hub_name>          - Hub links")
    print("  GET  /api/v1/links/<hub_name>/<doc_id> - Link details")
    print("  POST /api/v1/validate                  - Validate URL")
    print("  POST /api/v1/validate/all              - Validate all")
    print("  GET  /api/v1/permissions               - Permission audit")
    
    print("\n🔗 Server starting at http://localhost:5000")
    print("=" * 70)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
