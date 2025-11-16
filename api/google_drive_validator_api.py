#!/usr/bin/env python3
"""
Google Drive Validator API - REST API for validating OSP Drive links

Purpose:
  - Expose Google Drive link validation via HTTP API
  - Check document accessibility and permissions
  - Provide real-time status for all 83 links
  - Enable integration with dashboards and monitoring

Usage:
  1. Set GOOGLE_CREDENTIALS environment variable:
     export GOOGLE_CREDENTIALS=/path/to/credentials.json
  
  2. Run the server:
     python3 api/google_drive_validator_api.py
  
  3. API will start at: http://localhost:5000

Requirements:
  pip install flask google-auth-oauthlib google-auth-httplib2 google-api-python-client

Endpoints:
  GET  /health                           - Health check
  GET  /api/v1/status                    - Overall validation status
  GET  /api/v1/links                     - List all links with status
  GET  /api/v1/links/<hub_name>          - Links for specific hub
  GET  /api/v1/links/<hub_name>/<doc_id> - Specific link details
  POST /api/v1/validate                  - Validate a URL
  GET  /api/v1/permissions               - Permission audit summary
"""

import os
import json
import logging
from datetime import datetime
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

from flask import Flask, jsonify, request
from flask_cors import CORS

try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    from google.api_errors import HttpError
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state
class ValidatorState:
    def __init__(self):
        self.service = None
        self.links_cache = {}
        self.last_validation = None
        self.validation_in_progress = False
        self.error = None

state = ValidatorState()


def init_drive_service(credentials_path: Optional[str] = None) -> bool:
    """Initialize Google Drive API service."""
    if not GOOGLE_API_AVAILABLE:
        state.error = "Google API libraries not installed"
        return False

    cred_path = credentials_path or os.environ.get("GOOGLE_CREDENTIALS")
    
    if not cred_path:
        state.error = "GOOGLE_CREDENTIALS environment variable not set"
        return False

    if not os.path.exists(cred_path):
        state.error = f"Credentials file not found: {cred_path}"
        return False

    try:
        credentials = Credentials.from_service_account_file(
            cred_path,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        state.service = build('drive', 'v3', credentials=credentials)
        logger.info("✅ Google Drive API initialized")
        return True
    except Exception as e:
        state.error = f"Failed to initialize Drive API: {str(e)}"
        logger.error(state.error)
        return False


def extract_doc_id(url: str) -> Optional[str]:
    """Extract document ID from Google Drive URL."""
    import re
    
    patterns = [
        r'https://docs\.google\.com/document/d/([a-zA-Z0-9_-]+)',
        r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)',
        r'https://docs\.google\.com/presentation/d/([a-zA-Z0-9_-]+)',
        r'https://drive\.google\.com/.*[?&]id=([a-zA-Z0-9_-]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def check_document_access(doc_id: str) -> Tuple[bool, Dict]:
    """Check if document is accessible."""
    result = {
        "id": doc_id,
        "accessible": False,
        "title": None,
        "mime_type": None,
        "owner": None,
        "shared_with_osp_group": False,
        "public": False,
        "last_modified": None,
        "web_view_link": None,
        "error": None,
    }

    if not state.service:
        result["error"] = "Drive API not initialized"
        return False, result

    try:
        file_metadata = state.service.files().get(
            fileId=doc_id,
            fields='id,name,mimeType,owners,permissions,lastModifiedTime,webViewLink,shared'
        ).execute()

        result["title"] = file_metadata.get("name")
        result["mime_type"] = file_metadata.get("mimeType")
        result["last_modified"] = file_metadata.get("lastModifiedTime")
        result["web_view_link"] = file_metadata.get("webViewLink")
        result["accessible"] = True

        owners = file_metadata.get("owners", [])
        if owners:
            result["owner"] = owners[0].get("displayName")

        permissions = file_metadata.get("permissions", [])
        for perm in permissions:
            role = perm.get("role")
            type_ = perm.get("type")
            email = perm.get("emailAddress", "")

            if type_ == "group" and "@osp" in email.lower():
                result["shared_with_osp_group"] = True

            if type_ == "anyone":
                result["public"] = True

        return True, result

    except HttpError as error:
        if error.resp.status == 404:
            result["error"] = "Document not found"
        elif error.resp.status == 403:
            result["error"] = "Access denied (no permission)"
        else:
            result["error"] = f"HTTP {error.resp.status}: {error.resp.reason}"
        return False, result
    except Exception as e:
        result["error"] = str(e)
        return False, result


def load_hub_links() -> Dict[str, List[Dict]]:
    """Load all hub links from markdown files."""
    import re
    from pathlib import Path

    hub_files = {
        "VENDAS": "DADOS_INTELIGENCIA/VENDAS/templates/README.md",
        "CONHECIMENTO": "DADOS_INTELIGENCIA/CONHECIMENTO/solucoes/INDEX.md",
        "DADOS_INTELIGENCIA": "DADOS_INTELIGENCIA/dashboards/README.md",
        "MARKETING": "DADOS_INTELIGENCIA/MARKETING/campanhas/README.md",
    }

    docs_root = Path(__file__).parent.parent
    links = {}

    for hub_name, file_path in hub_files.items():
        full_path = docs_root / file_path
        hub_links = []

        if full_path.exists():
            try:
                content = full_path.read_text(encoding="utf-8")
                markdown_links = re.findall(
                    r'\[([^\]]+)\]\((https://docs\.google\.com/[^\)]+)\)',
                    content
                )

                for text, url in markdown_links:
                    doc_id = extract_doc_id(url)
                    hub_links.append({
                        "text": text,
                        "url": url,
                        "doc_id": doc_id,
                        "hub": hub_name,
                    })
            except Exception as e:
                logger.error(f"Error reading {file_path}: {str(e)}")

        links[hub_name] = hub_links

    return links


def validate_all_links() -> Dict:
    """Validate all links and cache results."""
    state.validation_in_progress = True
    
    try:
        hub_links = load_hub_links()
        results = {
            "validated_at": datetime.now().isoformat(),
            "hubs": {},
            "summary": {
                "total": 0,
                "accessible": 0,
                "inaccessible": 0,
            }
        }

        for hub_name, links in hub_links.items():
            hub_results = []
            
            for link in links:
                doc_id = link.get("doc_id")
                if doc_id:
                    accessible, details = check_document_access(doc_id)
                    link["validation"] = details
                    link["status"] = "✅ Accessible" if accessible else "❌ Inaccessible"
                    hub_results.append(link)
                    
                    results["summary"]["total"] += 1
                    if accessible:
                        results["summary"]["accessible"] += 1
                    else:
                        results["summary"]["inaccessible"] += 1

            results["hubs"][hub_name] = hub_results

        state.links_cache = results
        state.last_validation = datetime.now()
        return results

    except Exception as e:
        logger.error(f"Error validating links: {str(e)}")
        return {"error": str(e)}
    finally:
        state.validation_in_progress = False


# API Routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "api_version": "1.0",
        "drive_api": "connected" if state.service else "disconnected",
        "cached_results": bool(state.links_cache),
        "last_validation": state.last_validation.isoformat() if state.last_validation else None,
    })


@app.route('/api/v1/status', methods=['GET'])
def get_status():
    """Get overall validation status."""
    if not state.links_cache:
        validate_all_links()

    return jsonify({
        "status": "ok",
        "validation": state.links_cache.get("summary", {}),
        "last_validated": state.last_validation.isoformat() if state.last_validation else None,
        "validation_in_progress": state.validation_in_progress,
    })


@app.route('/api/v1/links', methods=['GET'])
def get_all_links():
    """Get all links with validation status."""
    if not state.links_cache:
        validate_all_links()

    return jsonify(state.links_cache)


@app.route('/api/v1/links/<hub_name>', methods=['GET'])
def get_hub_links(hub_name: str):
    """Get links for specific hub."""
    if not state.links_cache:
        validate_all_links()

    hub_data = state.links_cache.get("hubs", {}).get(hub_name)
    
    if hub_data is None:
        return jsonify({"error": f"Hub '{hub_name}' not found"}), 404

    return jsonify({
        "hub": hub_name,
        "links": hub_data,
        "total": len(hub_data),
        "accessible": sum(1 for l in hub_data if l.get("validation", {}).get("accessible")),
    })


@app.route('/api/v1/links/<hub_name>/<doc_id>', methods=['GET'])
def get_link_details(hub_name: str, doc_id: str):
    """Get details for specific link."""
    if not state.links_cache:
        validate_all_links()

    hub_data = state.links_cache.get("hubs", {}).get(hub_name, [])
    
    for link in hub_data:
        if link.get("doc_id") == doc_id:
            return jsonify(link)

    return jsonify({"error": f"Link not found: {doc_id} in {hub_name}"}), 404


@app.route('/api/v1/validate', methods=['POST'])
def validate_link():
    """Validate a single URL."""
    data = request.get_json()
    
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    url = data["url"]
    doc_id = extract_doc_id(url)

    if not doc_id:
        return jsonify({"error": "Invalid Google Drive URL"}), 400

    accessible, details = check_document_access(doc_id)

    return jsonify({
        "url": url,
        "doc_id": doc_id,
        "status": "✅ Accessible" if accessible else "❌ Inaccessible",
        "details": details,
    })


@app.route('/api/v1/permissions', methods=['GET'])
def get_permissions_summary():
    """Get permission audit summary."""
    if not state.links_cache:
        validate_all_links()

    summary = {
        "total": 0,
        "shared_with_osp_group": 0,
        "not_shared_with_osp_group": 0,
        "public": 0,
        "private": 0,
        "by_hub": {},
    }

    for hub_name, links in state.links_cache.get("hubs", {}).items():
        hub_summary = {
            "total": len(links),
            "shared_with_osp_group": 0,
            "public": 0,
        }

        for link in links:
            validation = link.get("validation", {})
            if validation.get("accessible"):
                summary["total"] += 1
                
                if validation.get("shared_with_osp_group"):
                    summary["shared_with_osp_group"] += 1
                    hub_summary["shared_with_osp_group"] += 1
                else:
                    summary["not_shared_with_osp_group"] += 1

                if validation.get("public"):
                    summary["public"] += 1
                else:
                    summary["private"] += 1

        summary["by_hub"][hub_name] = hub_summary

    return jsonify(summary)


@app.route('/api/v1/validate/all', methods=['POST'])
def validate_all():
    """Trigger full validation of all links."""
    if state.validation_in_progress:
        return jsonify({"error": "Validation already in progress"}), 409

    results = validate_all_links()
    
    return jsonify({
        "status": "validation_complete",
        "results": results,
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


def main():
    """Start the API server."""
    print("🚀 Starting Google Drive Validator API...")
    
    # Initialize Drive service
    if not init_drive_service():
        print(f"⚠️  Warning: {state.error}")
        print("API will still run but without Drive API features")
    else:
        print("✅ Drive API ready")

    print("\n📚 API Endpoints:")
    print("  GET  /health                           - Health check")
    print("  GET  /api/v1/status                    - Overall status")
    print("  GET  /api/v1/links                     - All links")
    print("  GET  /api/v1/links/<hub_name>          - Hub links")
    print("  POST /api/v1/validate                  - Validate URL")
    print("  POST /api/v1/validate/all              - Validate all")
    print("  GET  /api/v1/permissions               - Permission audit")

    print("\n🔗 Server starting at http://localhost:5000")
    print("Press CTRL+C to stop\n")

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
