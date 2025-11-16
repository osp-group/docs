# 🚀 Google Drive API v2 - Documentação Completa

**Status:** ✅ Pronto para uso  
**Versão:** 2.0.0  
**Data:** 16 de novembro de 2025

---

## 📋 Índice

1. [Quick Start](#quick-start)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Uso](#uso)
5. [API Endpoints](#api-endpoints)
6. [Cliente Python](#cliente-python)
7. [Exemplos](#exemplos)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1️⃣ Instalar dependências
```bash
cd /Users/gpagotto/osp-website/docs
pip3 install flask flask-cors google-api-python-client google-auth-oauthlib google-auth-httplib2 -q
```

### 2️⃣ Iniciar a API
```bash
python3 api/google_drive_api_v2.py
```

Você verá:
```
🚀 Iniciando Google Drive API v2
   Auth: service_account
   Email: ga4-api-access@site-2026.iam.gserviceaccount.com
   Acessível em: http://localhost:5000
```

### 3️⃣ Testar em outro terminal
```bash
# Verificar saúde
curl http://localhost:5000/health

# Validar uma URL
curl -X POST http://localhost:5000/api/v2/validate/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.google.com/spreadsheets/d/YOUR_ID/edit"}'
```

---

## Instalação

### Pré-requisitos
- Python 3.8+
- pip
- Google Cloud credentials (Service Account ou OAuth)

### Packages

```bash
pip3 install \
  flask==2.3.3 \
  flask-cors==4.0.0 \
  google-api-python-client==2.108.0 \
  google-auth-oauthlib==1.1.0 \
  google-auth-httplib2==0.2.0 \
  requests==2.31.0
```

---

## Configuração

### Opção A: Service Account (Recomendado para produção)

**Arquivo:** `~/.credentials/ga4-api-key.json`

A API detecta automaticamente se este arquivo existe e o usa.

```bash
# Verificar se arquivo existe
ls -la ~/.credentials/ga4-api-key.json
```

Se não existir, crie um Google Cloud Service Account:

1. Vá para [Google Cloud Console](https://console.cloud.google.com)
2. Selecione o projeto `site-2026`
3. Navegue para **Service Accounts**
4. Crie uma chave JSON
5. Salve em `~/.credentials/ga4-api-key.json`

### Opção B: OAuth 2.0 (Para desenvolvimento com sua conta)

**Arquivo:** `oauth_credentials.json` (na raiz do projeto)

1. Vá para [Google Cloud Console](https://console.cloud.google.com)
2. Crie um **OAuth 2.0 Client ID** (Desktop application)
3. Salve o JSON em `oauth_credentials.json`
4. A API solicitará permissão na primeira vez

---

## Uso

### Via Cliente Python

```python
from api.google_drive_client_v2 import GoogleDriveClient

# Criar cliente
client = GoogleDriveClient(base_url="http://localhost:5000")

# Status
status = client.get_status()
print(status['authenticated_email'])

# Validar uma URL
result = client.validate_url("https://docs.google.com/spreadsheets/d/ID/edit")
print(result['accessible'])  # True ou False

# Validar múltiplas
urls = ["https://docs.google.com/spreadsheets/d/ID1/edit", "..."]
results = client.validate_urls(urls)

# Buscar documentos
search = client.search("OKR 2025", max_results=5)
for doc in search['results']:
    print(f"{doc['name']} ({doc['id']})")
```

### Via REST API

#### GET /health
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "ok",
  "timestamp": "2025-11-16T10:30:00"
}
```

#### GET /api/v2/status
```bash
curl http://localhost:5000/api/v2/status
```

Response:
```json
{
  "status": "operational",
  "auth_method": "service_account",
  "authenticated_email": "ga4-api-access@site-2026.iam.gserviceaccount.com",
  "cache_size": 42,
  "validation_stats": { ... }
}
```

---

## API Endpoints

### Validação

#### POST /api/v2/validate/url
Valida uma URL do Google Drive

**Request:**
```json
{
  "url": "https://docs.google.com/spreadsheets/d/ID/edit"
}
```

**Response:**
```json
{
  "url": "https://docs.google.com/spreadsheets/d/ID/edit",
  "valid": true,
  "doc_id": "ID",
  "accessible": true,
  "access_info": {
    "accessible": true,
    "title": "OKRs 2025",
    "owner": "Admin",
    "mime_type": "application/vnd.google-apps.spreadsheet",
    "shared_with_service_account": true,
    "last_modified": "2025-11-15T15:30:00Z",
    "web_view_link": "https://docs.google.com/spreadsheets/d/ID/edit"
  }
}
```

#### POST /api/v2/validate/urls
Valida múltiplas URLs

**Request:**
```json
{
  "urls": [
    "https://docs.google.com/spreadsheets/d/ID1/edit",
    "https://docs.google.com/document/d/ID2/edit"
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "url": "...",
      "valid": true,
      "doc_id": "ID1",
      "accessible": true,
      "access_info": { ... }
    },
    ...
  ],
  "stats": {
    "total": 2,
    "valid_format": 2,
    "accessible": 2,
    "errors": 0
  }
}
```

### Busca

#### GET /api/v2/search?q=OKR&max_results=10
Busca documentos no Drive

**Response:**
```json
{
  "query": "OKR",
  "results": [
    {
      "id": "1qCYg7nCz5v0k_8W2pL_7mN9qRx_4hJ5sA_bT2uV1wXy",
      "name": "OKRs 2025",
      "mime_type": "application/vnd.google-apps.spreadsheet",
      "owner": "Admin",
      "web_view_link": "https://docs.google.com/spreadsheets/d/ID/edit",
      "modified_time": "2025-11-15T15:30:00Z"
    }
  ],
  "count": 1
}
```

---

## Cliente Python

### Inicialização

```python
from api.google_drive_client_v2 import GoogleDriveClient

client = GoogleDriveClient(
    base_url="http://localhost:5000"  # URL da API (padrão)
)
```

### Métodos

#### `health_check() -> bool`
Verifica se API está online
```python
if client.health_check():
    print("API está rodando")
```

#### `get_status() -> dict`
Obtém status da API
```python
status = client.get_status()
print(status['authenticated_email'])
```

#### `init_service() -> dict`
Inicializa serviço de Drive
```python
result = client.init_service()
if 'error' not in result:
    print("Serviço inicializado")
```

#### `validate_url(url: str) -> dict`
Valida uma URL
```python
result = client.validate_url("https://docs.google.com/spreadsheets/d/ID/edit")
if result['accessible']:
    print(f"Documento: {result['access_info']['title']}")
```

#### `validate_urls(urls: list) -> dict`
Valida múltiplas URLs
```python
urls = ["url1", "url2", "url3"]
results = client.validate_urls(urls)
print(f"Acessíveis: {results['stats']['accessible']}")
```

#### `validate_urls_from_file(filepath: str) -> dict`
Valida URLs de um arquivo (uma por linha)
```python
results = client.validate_urls_from_file("links.txt")
```

#### `search(query: str, max_results: int = 10) -> dict`
Busca documentos
```python
results = client.search("OKR 2025", max_results=5)
for doc in results['results']:
    print(f"{doc['name']}: {doc['web_view_link']}")
```

---

## Exemplos

### Exemplo 1: Validar links de um arquivo

```bash
# Criar arquivo de links
cat > links.txt << 'EOF'
https://docs.google.com/spreadsheets/d/1qCYg7nCz5v0k_8W2pL_7mN9qRx_4hJ5sA_bT2uV1wXy/edit
https://docs.google.com/document/d/1aB3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX4yZ5aB6c/edit
EOF

# Executar cliente
python3 << 'PYTHON'
from api.google_drive_client_v2 import GoogleDriveClient

client = GoogleDriveClient()
result = client.validate_urls_from_file("links.txt")

print(f"Acessíveis: {result['stats']['accessible']}")
print(f"Inacessíveis: {result['stats']['errors']}")

for r in result['results']:
    status = "✅" if r['accessible'] else "❌"
    print(f"{status} {r['url']}")
PYTHON
```

### Exemplo 2: Buscar documentos e validar

```python
from api.google_drive_client_v2 import GoogleDriveClient

client = GoogleDriveClient()

# Buscar documentos com "OKR" no nome
search_result = client.search("OKR", max_results=10)

# Validar cada um
for doc in search_result['results']:
    # Construir URL
    url = f"https://docs.google.com/spreadsheets/d/{doc['id']}/edit"
    
    # Validar
    result = client.validate_url(url)
    status = "✅" if result['accessible'] else "❌"
    
    print(f"{status} {doc['name']}")
    print(f"   {doc['web_view_link']}")
    print(f"   Última modificação: {doc['modified_time']}")
```

### Exemplo 3: Executar teste automático

```bash
# Com API rodando em outro terminal
python3 scripts/test_api_v2.py
```

---

## Troubleshooting

### "API offline - execute: python3 api/google_drive_api_v2.py"

**Problema:** Cliente não consegue se conectar à API  
**Solução:** Inicie a API em outro terminal

```bash
python3 api/google_drive_api_v2.py
```

### "Acesso negado (não compartilhado com esta conta)"

**Problema:** Service Account não tem permissão  
**Solução:** Compartilhe o documento com:
```
ga4-api-access@site-2026.iam.gserviceaccount.com
```

Role: **Editor** (ou Visualizador se só ler)

### "ID do documento não encontrado na URL"

**Problema:** URL tem formato inválido  
**Solução:** URLs válidas:
- `https://docs.google.com/spreadsheets/d/{ID}/edit`
- `https://docs.google.com/document/d/{ID}/edit`
- `https://docs.google.com/presentation/d/{ID}/edit`

### "Serviço não inicializado"

**Problema:** Nenhum método de autenticação disponível  
**Solução:** Configure Service Account ou OAuth (veja [Configuração](#configuração))

---

## Performance

- **Cache:** 1 hora por padrão
- **Timeout:** 30 segundos por requisição
- **Batch size:** Máximo 10 URLs por validação

---

## Logs

A API escreve logs no console:

```
INFO - ✅ Service Account inicializado: ga4-api-access@site-2026.iam.gserviceaccount.com
INFO - POST /api/v2/validate/url 200
INFO - Documento cacheado: 1qCYg7nCz5v0k_8W2pL_7mN9qRx_4hJ5sA_bT2uV1wXy
```

Para usar logs em produção, configure um handler de arquivo:

```python
import logging
logging.basicConfig(
    filename='google_drive_api.log',
    level=logging.INFO
)
```

---

## Próximos Passos

1. ✅ Instalar dependências
2. ✅ Iniciar API
3. ✅ Validar links
4. ⏳ Integrar com dashboard
5. ⏳ Configurar monitoramento automático
