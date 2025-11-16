# 📘 Guia Passo a Passo - Google Drive Validator API

Instruções detalhadas para usar a API do início ao fim.

---

## 🎯 Objetivo Final

Validar que todos os 64 links do Google Drive integrados nos hubs estão:
- ✅ Acessíveis (documentos existem)
- ✅ Compartilhados com @osp-group
- ✅ Com permissões corretas

---

## ⏱️ Tempo Total: ~30 minutos

---

## 🔧 PASSO 1: Verificar Pré-requisitos (2 min)

### Verificar Python

```bash
python3 --version
# Esperado: Python 3.8 ou maior
# Exemplo: Python 3.9.13
```

Se não tiver Python 3.8+, instale de https://www.python.org/

### Verificar que você está no diretório correto

```bash
cd /Users/gpagotto/osp-website/docs
pwd
# Esperado: /Users/gpagotto/osp-website/docs
```

---

## 📦 PASSO 2: Instalar Dependências (3 min)

### Instalar todas as bibliotecas necessárias

```bash
pip install -r api/requirements.txt
```

**Esperado:**
```
Collecting Flask==2.3.3
  Using cached Flask-2.3.3-py3-none-any.whl
...
Successfully installed Flask-2.3.3 Flask-CORS-4.0.0 google-api-python-client-2.108.0 ...
```

### Verificar instalação

```bash
python3 -c "import flask; import google.auth; print('✅ All dependencies installed')"
```

---

## 🔐 PASSO 3: Configurar Google Drive API (10 min)

### 3a. Criar arquivo de credenciais

Siga o guia completo em: `scripts/GOOGLE_DRIVE_API_SETUP.md`

**Resumido:**

1. Ir para https://console.cloud.google.com/
2. Criar novo projeto (ou usar existente)
3. Ativar "Google Drive API"
4. Criar "Service Account"
5. Gerar JSON key
6. Compartilhar arquivos Drive com o email do service account

### 3b. Colocar arquivo no local correto

```bash
# Copiar credentials.json para a pasta api/
cp ~/Downloads/credentials.json /Users/gpagotto/osp-website/docs/api/credentials.json

# Verificar se existe
ls -la api/credentials.json
# Esperado: -rw-r--r--  1 user  staff  XXX Nov 16 19:00 api/credentials.json
```

### 3c. Definir variável de ambiente

```bash
export GOOGLE_CREDENTIALS=/Users/gpagotto/osp-website/docs/api/credentials.json

# Verificar se foi definida
echo $GOOGLE_CREDENTIALS
# Esperado: /Users/gpagotto/osp-website/docs/api/credentials.json
```

---

## 🚀 PASSO 4: Iniciar o Servidor (1 min)

### Iniciar API

```bash
python3 api/google_drive_validator_api.py
```

**Esperado:**
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
 * Serving Flask app 'google_drive_validator_api'
 * Debug mode: on
 * Running on http://localhost:5000
```

**ℹ️ Deixe este terminal aberto!** Abra outro terminal para os próximos passos.

---

## ✅ PASSO 5: Testar Health Check (1 min)

### Em novo terminal:

```bash
curl http://localhost:5000/health
```

**Esperado:**
```json
{
  "status": "healthy",
  "api_version": "1.0",
  "drive_api": "connected",
  "cached_results": true,
  "last_validation": "2025-11-16T19:30:00.123456"
}
```

Se receber erro, volte ao Passo 3 (credentials).

---

## 📊 PASSO 6: Verificar Status Geral (1 min)

### Obter resumo da validação

```bash
curl http://localhost:5000/api/v1/status
```

**Esperado:**
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

---

## 🔗 PASSO 7: Ver Todos os Links (2 min)

### Obter lista completa de 64 links

```bash
curl http://localhost:5000/api/v1/links | jq '.'
```

**Esperado:**
```json
{
  "validated_at": "2025-11-16T19:30:00.123456",
  "hubs": {
    "VENDAS": [
      {
        "text": "Contabilidade Mensal",
        "url": "https://docs.google.com/...",
        "doc_id": "1LH8JcQftRWcKjxB4nCiKpSzOWE22E4DcS4XA84wQ6xI",
        "hub": "VENDAS",
        "validation": {
          "accessible": true,
          "title": "Contabilidade Mensal",
          "owner": "Admin User",
          "shared_with_osp_group": true,
          "public": false,
          "last_modified": "2025-11-16T10:00:00.000Z",
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

---

## 🎯 PASSO 8: Filtrar por Hub (1 min)

### Ver apenas links do VENDAS

```bash
curl http://localhost:5000/api/v1/links/VENDAS | jq '.hubs.VENDAS[] | {text, accessible: .validation.accessible}'
```

**Esperado:**
```json
{
  "text": "Contabilidade Mensal",
  "accessible": true
}
{
  "text": "Template de Proposta",
  "accessible": true
}
...
```

### Outros hubs:

```bash
# CONHECIMENTO
curl http://localhost:5000/api/v1/links/CONHECIMENTO | jq '.hubs.CONHECIMENTO | length'

# DADOS_INTELIGENCIA
curl http://localhost:5000/api/v1/links/DADOS_INTELIGENCIA | jq '.hubs.DADOS_INTELIGENCIA | length'

# MARKETING
curl http://localhost:5000/api/v1/links/MARKETING | jq '.hubs.MARKETING | length'
```

---

## 🔐 PASSO 9: Auditoria de Permissões (2 min)

### Verificar quem tem acesso

```bash
curl http://localhost:5000/api/v1/permissions | jq '.'
```

**Esperado:**
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

### ⚠️ Se houver problemas:

Se `not_shared_with_osp_group > 0`, você precisa:

1. Entrar no Google Drive
2. Abrir o arquivo
3. Compartilhar → Adicionar "osp-group@..." → Salvar

---

## 🐍 PASSO 10: Usar Python Client (3 min)

### 10a. Criar arquivo de teste

```bash
cat > /tmp/test_api.py << 'EOF'
import sys
sys.path.insert(0, '/Users/gpagotto/osp-website/docs')

from api.google_drive_client import GoogleDriveValidatorClient

# Conectar à API
client = GoogleDriveValidatorClient("http://localhost:5000")

# Health check
print("1️⃣  Health Check:")
health = client.health_check()
print(f"   Status: {health['status']}\n")

# Status geral
print("2️⃣  Overall Status:")
status = client.get_status()
print(f"   Total: {status['validation']['total']}")
print(f"   Accessible: {status['validation']['accessible']}")
print(f"   Inaccessible: {status['validation']['inaccessible']}\n")

# Links por hub
print("3️⃣  Links por Hub:")
for hub in ["VENDAS", "CONHECIMENTO", "DADOS_INTELIGENCIA", "MARKETING"]:
    hub_data = client.get_hub_links(hub)
    print(f"   {hub}: {hub_data['total']} links ({hub_data['accessible']} accessible)")
print()

# Links inacessíveis
print("4️⃣  Links Inaccessíveis:")
inaccessible = client.get_inaccessible_links()
if inaccessible:
    for link in inaccessible:
        print(f"   ❌ {link['text']} - {link['validation']['error']}")
else:
    print("   ✅ Todos os links estão acessíveis!")
print()

# Permissões
print("5️⃣  Permissões:")
perms = client.get_permissions_summary()
print(f"   Compartilhado com @osp-group: {perms['shared_with_osp_group']}/{perms['total']}")
print(f"   Público: {perms['public']}/{perms['total']}")
print()

# Links públicos (revisar)
print("6️⃣  Links Públicos (revisar):")
public_links = client.get_public_links()
if public_links:
    for link in public_links:
        print(f"   🌍 {link['text']} - {link['hub']}")
else:
    print("   ✅ Nenhum link público")
print()

# Links não compartilhados com @osp-group
print("7️⃣  Links NÃO compartilhados com @osp-group:")
not_shared = client.get_not_shared_with_osp_group()
if not_shared:
    for link in not_shared:
        print(f"   🔒 {link['text']} - {link['hub']}")
        print(f"      ↳ Ação: Compartilhe com @osp-group como 'Viewer'")
else:
    print("   ✅ Todos os links estão compartilhados com @osp-group")

EOF
```

### 10b. Executar teste

```bash
python3 /tmp/test_api.py
```

**Esperado:**
```
1️⃣  Health Check:
   Status: healthy

2️⃣  Overall Status:
   Total: 64
   Accessible: 64
   Inaccessible: 0

3️⃣  Links por Hub:
   VENDAS: 29 links (29 accessible)
   CONHECIMENTO: 20 links (20 accessible)
   DADOS_INTELIGENCIA: 12 links (12 accessible)
   MARKETING: 3 links (3 accessible)

4️⃣  Links Inaccessíveis:
   ✅ Todos os links estão acessíveis!

5️⃣  Permissões:
   Compartilhado com @osp-group: 62/64
   Público: 1/64

6️⃣  Links Públicos (revisar):
   🌍 Dashboard Público - DADOS_INTELIGENCIA

7️⃣  Links NÃO compartilhados com @osp-group:
   🔒 Template Provisório - VENDAS
      ↳ Ação: Compartilhe com @osp-group como 'Viewer'
```

---

## 📋 PASSO 11: Gerar Relatório Completo (1 min)

### Criar relatório em JSON

```bash
curl http://localhost:5000/api/v1/links > /tmp/links_report.json

# Verificar tamanho
wc -l /tmp/links_report.json
```

### Ou gerar relatório em Markdown

```bash
python3 << 'EOF'
import sys, json
sys.path.insert(0, '/Users/gpagotto/osp-website/docs')
from api.google_drive_client import GoogleDriveValidatorClient

client = GoogleDriveValidatorClient("http://localhost:5000")

# Gerar relatório
print("# 📊 Relatório de Validação - Google Drive Links\n")

status = client.get_status()
print(f"**Data:** {status['last_validated']}\n")
print(f"**Total de Links:** {status['validation']['total']}")
print(f"**Acessíveis:** {status['validation']['accessible']}")
print(f"**Inacessíveis:** {status['validation']['inaccessible']}\n")

print("## 📍 Links por Hub\n")
for hub in ["VENDAS", "CONHECIMENTO", "DADOS_INTELIGENCIA", "MARKETING"]:
    hub_data = client.get_hub_links(hub)
    pct = round(100 * hub_data['accessible'] / hub_data['total']) if hub_data['total'] > 0 else 0
    print(f"### {hub}")
    print(f"- Total: {hub_data['total']}")
    print(f"- Acessíveis: {hub_data['accessible']} ({pct}%)")
    print(f"- Status: {'✅ OK' if hub_data['inaccessible'] == 0 else '⚠️ PROBLEMAS'}\n")

print("## 🔐 Permissões\n")
perms = client.get_permissions_summary()
print(f"- Compartilhado com @osp-group: {perms['shared_with_osp_group']}/{perms['total']}")
print(f"- Público: {perms['public']}/{perms['total']}")
print(f"- Privado: {perms['private']}/{perms['total']}\n")

inaccessible = client.get_inaccessible_links()
if inaccessible:
    print("## ⚠️ Links Problematicos\n")
    for link in inaccessible:
        print(f"- **{link['text']}** ({link['hub']})")
        print(f"  - Error: {link['validation']['error']}\n")

EOF
```

---

## 🛑 PASSO 12: Parar o Servidor (1 min)

### Quando terminar:

```bash
# No terminal onde a API está rodando:
# Pressione: Ctrl + C

# Esperado:
# KeyboardInterrupt
# Shutting down...
```

---

## 🐛 TROUBLESHOOTING

### ❌ "Connection refused"

```bash
# Verificar se API está rodando
curl http://localhost:5000/health

# Se não conectar, restart a API:
# 1. Ctrl+C no terminal da API
# 2. python3 api/google_drive_validator_api.py
```

### ❌ "GOOGLE_CREDENTIALS not set"

```bash
# Definir variável:
export GOOGLE_CREDENTIALS=/Users/gpagotto/osp-website/docs/api/credentials.json

# Verificar:
echo $GOOGLE_CREDENTIALS
```

### ❌ "Document not found (404)"

- Arquivo foi deletado no Google Drive
- Ou URL está incorreta
- ↳ Verificar em: `curl http://localhost:5000/api/v1/permissions`

### ❌ "Access denied (403)"

- Arquivo não foi compartilhado com o service account
- ↳ No Google Drive: Compartilhe com o email do service account (Viewer)

### ❌ "ModuleNotFoundError: No module named 'flask'"

```bash
# Reinstalar dependências:
pip install -r api/requirements.txt
```

---

## 📈 Próximos Passos

Depois que confirmar que tudo funciona:

1. **Guardar relatório** → `testing/QA_GOOGLE_DRIVE_LINKS_API_VALIDATION.md`
2. **Compartilhar permissões** → Se houver links não compartilhados
3. **Integrar com dashboard** → API pronta para consumo
4. **Agendar validações** → Cron job para validar diariamente

---

## 📞 Checklist Final

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install -r api/requirements.txt`)
- [ ] credentials.json no diretório api/
- [ ] Variável GOOGLE_CREDENTIALS definida
- [ ] API iniciada (`python3 api/google_drive_validator_api.py`)
- [ ] Health check respondendo
- [ ] Todos os 64 links validados
- [ ] Relatório gerado
- [ ] Permissões auditadas

---

**✅ Fim!** 

Sua API Google Drive Validator está pronta para uso em produção.

Qualquer dúvida, consulte `api/README.md` para documentação completa.
