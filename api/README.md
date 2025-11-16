# 🔗 Google Drive Validator API

REST API para validar e monitorar os 83 links Google Drive integrados nos hubs OSP.

---

## 🎯 Features

✅ **Validação em Tempo Real**: Verifica se documentos estão acessíveis  
✅ **Auditoria de Permissões**: Monitora quem tem acesso (@osp-group, público, etc)  
✅ **Metadados**: Extrai título, proprietário, tipo de documento  
✅ **Cache Inteligente**: Resultados cacheados para performance  
✅ **REST API**: Fácil integração com dashboards e ferramentas  
✅ **Python Client**: SDK pronto para usar  

---

## 📋 Pré-requisitos

- Python 3.8+
- Google Cloud Service Account (com JSON credentials)
- Arquivos Google Drive compartilhados com a service account

---

## 🚀 Quick Start

### 1. Instalar Dependências

```bash
cd /Users/gpagotto/osp-website/docs
pip install -r api/requirements.txt
```

### 2. Configurar Google Drive API

Siga o guia completo em: `scripts/GOOGLE_DRIVE_API_SETUP.md`

**Resumido**:
```bash
# Definir credenciais
export GOOGLE_CREDENTIALS=/caminho/para/credentials.json

# Ou criar arquivo .env
echo "GOOGLE_CREDENTIALS=/caminho/para/credentials.json" > api/.env
```

### 3. Iniciar o Servidor

```bash
python3 api/google_drive_validator_api.py
```

**Esperado**:
```
🚀 Starting Google Drive Validator API...
✅ Drive API ready

📚 API Endpoints:
  GET  /health                           - Health check
  GET  /api/v1/status                    - Overall status
  GET  /api/v1/links                     - All links
  GET  /api/v1/links/<hub_name>          - Hub links
  POST /api/v1/validate                  - Validate URL
  POST /api/v1/validate/all              - Validate all
  GET  /api/v1/permissions               - Permission audit

🔗 Server starting at http://localhost:5000
```

---

## 📡 API Endpoints

### Health Check

```bash
curl http://localhost:5000/health
```

**Response**:
```json
{
  "status": "healthy",
  "api_version": "1.0",
  "drive_api": "connected",
  "cached_results": true,
  "last_validation": "2025-11-16T19:30:00.123456"
}
```

### Get Overall Status

```bash
curl http://localhost:5000/api/v1/status
```

**Response**:
```json
{
  "status": "ok",
  "validation": {
    "total": 64,
    "accessible": 64,
    "inaccessible": 0
  },
  "last_validated": "2025-11-16T19:30:00.123456",
  "validation_in_progress": false
}
```

### Get All Links

```bash
curl http://localhost:5000/api/v1/links
```

**Response**:
```json
{
  "validated_at": "2025-11-16T19:30:00.123456",
  "hubs": {
    "VENDAS": [
      {
        "text": "Contabilidade Mensal",
        "url": "https://docs.google.com/document/d/1LH8JcQftRWcKjxB4nCiKpSzOWE22E4DcS4XA84wQ6xI/edit",
        "doc_id": "1LH8JcQftRWcKjxB4nCiKpSzOWE22E4DcS4XA84wQ6xI",
        "hub": "VENDAS",
        "validation": {
          "accessible": true,
          "title": "Contabilidade Mensal",
          "mime_type": "application/vnd.google-apps.document",
          "owner": "Admin User",
          "shared_with_osp_group": true,
          "public": false,
          "last_modified": "2025-11-16T10:00:00.000Z",
          "web_view_link": "https://docs.google.com/...",
          "error": null
        },
        "status": "✅ Accessible"
      }
    ]
  },
  "summary": {
    "total": 64,
    "accessible": 64,
    "inaccessible": 0
  }
}
```

### Get Hub Links

```bash
curl http://localhost:5000/api/v1/links/VENDAS
```

### Get Link Details

```bash
curl http://localhost:5000/api/v1/links/VENDAS/1LH8JcQftRWcKjxB4nCiKpSzOWE22E4DcS4XA84wQ6xI
```

### Validate Single URL

```bash
curl -X POST http://localhost:5000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.google.com/document/d/..."}'
```

### Trigger Full Validation

```bash
curl -X POST http://localhost:5000/api/v1/validate/all
```

### Get Permissions Audit

```bash
curl http://localhost:5000/api/v1/permissions
```

**Response**:
```json
{
  "total": 64,
  "shared_with_osp_group": 62,
  "not_shared_with_osp_group": 2,
  "public": 1,
  "private": 63,
  "by_hub": {
    "VENDAS": {
      "total": 29,
      "shared_with_osp_group": 28,
      "public": 0
    },
    "CONHECIMENTO": {
      "total": 20,
      "shared_with_osp_group": 20,
      "public": 0
    },
    "DADOS_INTELIGENCIA": {
      "total": 12,
      "shared_with_osp_group": 12,
      "public": 1
    },
    "MARKETING": {
      "total": 3,
      "shared_with_osp_group": 2,
      "public": 0
    }
  }
}
```

---

## 🐍 Python Client Usage

### Setup

```python
from api.google_drive_client import GoogleDriveValidatorClient

# Initialize client
client = GoogleDriveValidatorClient("http://localhost:5000")

# Health check
health = client.health_check()
print(health['status'])
```

### Common Operations

```python
# Get overall status
status = client.get_status()
print(f"Accessible: {status['validation']['accessible']}")

# Get all links
all_links = client.get_all_links()

# Get specific hub
vendas_links = client.get_hub_links("VENDAS")
print(f"VENDAS has {vendas_links['total']} links")
print(f"Accessible: {vendas_links['accessible']}")

# Validate single URL
result = client.validate_url("https://docs.google.com/document/d/...")

# Get accessible links only
accessible = client.get_accessible_links()

# Get inaccessible links (to fix)
inaccessible = client.get_inaccessible_links()

# Get links NOT shared with @osp-group
not_shared = client.get_not_shared_with_osp_group()
for link in not_shared:
    print(f"Fix permission: {link['text']}")

# Get public links (security review)
public_links = client.get_public_links()

# Get permission summary
permissions = client.get_permissions_summary()
print(f"Public: {permissions['public']}")
```

---

## 📊 Dashboards & Monitoring

### Real-time Status

```python
from api.google_drive_client import GoogleDriveValidatorClient
import time

client = GoogleDriveValidatorClient()

while True:
    status = client.get_status()
    
    total = status['validation']['total']
    accessible = status['validation']['accessible']
    inaccessible = status['validation']['inaccessible']
    
    pct = round(100 * accessible / max(1, total), 1)
    
    print(f"[{status['last_validated']}] Access: {accessible}/{total} ({pct}%)")
    
    if inaccessible > 0:
        inaccessible_links = client.get_inaccessible_links()
        for link in inaccessible_links:
            error = link.get('validation', {}).get('error', 'unknown')
            print(f"  ⚠️ {link['text']}: {error}")
    
    time.sleep(300)  # Check every 5 minutes
```

### Permission Audit Report

```python
from api.google_drive_client import GoogleDriveValidatorClient

client = GoogleDriveValidatorClient()

# Get links not shared with @osp-group
not_shared = client.get_not_shared_with_osp_group()

print("🔐 Links NOT shared with @osp-group:")
print("=" * 60)
for link in not_shared:
    print(f"\n📄 {link['text']}")
    print(f"   Hub: {link['hub']}")
    print(f"   URL: {link['url']}")
    print(f"   Owner: {link['validation']['owner']}")
    print(f"   Recommendation: Share with @osp-group as Viewer")

# Get public links
public_links = client.get_public_links()

print("\n\n🌍 Public Links (Security Review):")
print("=" * 60)
for link in public_links:
    print(f"\n📄 {link['text']}")
    print(f"   Hub: {link['hub']}")
    print(f"   Recommendation: Consider restricting to @osp-group only")
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Credentials path
export GOOGLE_CREDENTIALS=/path/to/credentials.json

# API Configuration
export API_HOST=0.0.0.0
export API_PORT=5000
export API_DEBUG=false
```

### .env File

```bash
# Create api/.env
GOOGLE_CREDENTIALS=/Users/gpagotto/osp-website/docs/credentials.json
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=true
```

---

## 🧪 Testing

### Test Health Check

```bash
curl http://localhost:5000/health
```

### Test Validation

```bash
curl -X POST http://localhost:5000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.google.com/document/d/1Nejr3BNKV6mf77fl61eezGqhY3QHGJY6_LQJCynYtvs/edit"
  }'
```

### Run Python Tests

```bash
python3 -m pytest api/tests/
```

---

## 🚨 Troubleshooting

### ❌ "API connection refused"

```bash
# Verify API is running
curl http://localhost:5000/health

# If error, restart API
python3 api/google_drive_validator_api.py
```

### ❌ "GOOGLE_CREDENTIALS not set"

```bash
# Set environment variable
export GOOGLE_CREDENTIALS=/path/to/credentials.json

# Or create api/.env
echo "GOOGLE_CREDENTIALS=/path/to/credentials.json" > api/.env
```

### ❌ "Document not found (404)"

- Verifique se o arquivo foi compartilhado com o service account
- Aguarde ~1 minuto após compartilhar
- Tente validar novamente

### ❌ "Access denied (403)"

- Verifique permissões na service account
- Re-compartilhe arquivo com "Viewer" (não precisa de "Editor")
- Verifique se credentials.json está correto

---

## 📈 Performance

- **Cache**: Resultados cacheados por 1 hora
- **Concurrent**: Suporta múltiplas requisições simultâneas
- **Timeout**: 30 segundos por documento
- **Batch**: Validar todos os 64 links leva ~2-3 minutos

---

## 🔒 Security

- ✅ HTTPS recomendado em produção
- ✅ Proteja `credentials.json` (chmod 600)
- ✅ Use variáveis de ambiente
- ✅ CORS habilitado para localhost
- ✅ Não fazer log de URLs completas

---

## 📎 Referências

- [Google Drive API Docs](https://developers.google.com/drive/api/reference/rest)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Auth Python Client](https://github.com/googleapis/google-auth-library-python)

---

## 🎯 Next Steps

1. ✅ API criada
2. ⏳ Python client pronto
3. ⏳ Setup credentials
4. ⏳ Start servidor
5. ⏳ Integrar com dashboards

---

**API Version**: 1.0  
**Date**: 16 de novembro de 2025  
**Status**: Ready for production
