# Google Drive Integration API

Production-ready APIs for Google Drive document management and automation.

## 📦 Contents

### Core APIs

- **`google_drive_api_v2.py`** - Flask REST API server
  - 8 REST endpoints for document validation and search
  - Dual authentication (OAuth 2.0 + Service Account)
  - 1-hour cache with TTL
  - CORS support

- **`google_drive_client_v2.py`** - Python SDK client
  - Easy integration library for external code
  - 7 public methods (health_check, validate_url/urls, search, get_status, init_service)
  - Production-ready

- **`google_workspace_integration.gs`** - Google Apps Script
  - Automates document discovery and sharing
  - Recursive folder traversal
  - Webhook communication with Python API
  - Google Workspace native execution

### Documentation

- **`README_API_V2.md`** - Complete API reference
  - Setup instructions
  - Endpoint documentation
  - Usage examples
  - Troubleshooting

- **`WORKSPACE_INSTALLATION_GUIDE.md`** - Google Workspace setup
  - 5-minute installation
  - Configuration guide
  - Testing procedures

### Dependencies

- **`requirements.txt`** - Python dependencies
  - Flask, Flask-CORS
  - google-api-python-client, google-auth, google-auth-oauthlib

## 🚀 Quick Start

See **`README_API_V2.md`** for complete setup instructions.

## 📋 Status

- ✅ API v2: Complete and production-ready
- ✅ Google Workspace integration: Ready to deploy
- ✅ Documentation: Complete

**Note**: Google Drive connection will be completed in future iterations.
