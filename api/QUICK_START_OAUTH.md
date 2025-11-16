# 🚀 Quick Start - Google Drive OAuth com mkt@osp.com.br

Integração rápida em 3 passos (5 minutos).

---

## 📋 Pré-requisitos

- ✅ Google Chrome ou Firefox
- ✅ Acesso à conta mkt@osp.com.br
- ✅ Python 3.8+ instalado
- ✅ Este repositório clonado

---

## ⚡ 3 Passos Rápidos

### Passo 1: Gerar OAuth Credentials (2 min)

```bash
# Abrir link no navegador
open https://console.cloud.google.com/apis/credentials

# OU copie e cole em novo tab:
# https://console.cloud.google.com/apis/credentials
```

**No Google Cloud Console:**

1. Clique: **"+ CRIAR CREDENCIAIS"**
2. Selecione: **"ID do cliente OAuth"**
3. Tipo: **"Aplicativo de desktop"**
4. Nome: `OSP Drive` (ou qualquer nome)
5. Clique: **"Criar"**
6. Clique no ícone **⬇️** para baixar JSON

**No terminal:**

```bash
cp ~/Downloads/client_secret_*.json /Users/gpagotto/osp-website/docs/api/oauth_credentials.json
```

### Passo 2: Executar Setup (2 min)

```bash
cd /Users/gpagotto/osp-website/docs

python3 api/google_drive_oauth_setup.py
```

**Na primeira execução:**
- Navegador abrirá automaticamente
- Faça login com: **mkt@osp.com.br**
- Clique em **"Permitir"**
- Terminal confirmará sucesso ✅

### Passo 3: Iniciar API (1 min)

```bash
python3 api/google_drive_validator_api_enhanced.py
```

**Esperado:**

```
======================================================================
🚀 Starting Google Drive Validator API...
======================================================================

✅ Drive API ready
   Authentication: oauth
   Authenticated as: mkt@osp.com.br

📚 API Endpoints:
  GET  /health                           - Health check
  ...

🔗 Server starting at http://localhost:5000
======================================================================
```

---

## ✅ Verificar Integração

**Em novo terminal:**

```bash
# Teste 1: Health check
curl http://localhost:5000/health | jq .

# Teste 2: Status geral
curl http://localhost:5000/api/v1/status | jq .

# Teste 3: Ver todos os links
curl http://localhost:5000/api/v1/links | jq '.summary'
```

**Esperado:**

```json
{
  "total": 64,
  "accessible": 64,
  "inaccessible": 0
}
```

---

## 🎯 Pronto!

Sua API está agora conectada ao Google Drive de **mkt@osp.com.br** 🎉

### Próximos passos:

```bash
# Ver todos os 64 links
curl http://localhost:5000/api/v1/links | jq .

# Ver permissões
curl http://localhost:5000/api/v1/permissions | jq .

# Validar URL específica
curl -X POST http://localhost:5000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.google.com/document/d/..."}'
```

---

## 📚 Documentação Completa

Para guias mais detalhados:

- **OAuth Setup**: `api/OAUTH_SETUP.md`
- **API README**: `api/README.md`
- **Step-by-Step**: `api/STEP_BY_STEP.md`

---

## 🐛 Problemas?

### ❌ "oauth_credentials.json not found"

```bash
# Você pulou Passo 1
# Vá para: https://console.cloud.google.com/apis/credentials
# Baixe o arquivo JSON
# Copie para: api/oauth_credentials.json
```

### ❌ "Browser didn't open"

```bash
# Abra manualmente no navegador:
# http://localhost:8080

# Ou remova token antigo e tente novamente:
rm api/google_drive_token.pickle
python3 api/google_drive_oauth_setup.py
```

### ❌ "Access denied (403)"

O arquivo no Google Drive não está compartilhado com mkt@osp.com.br:

1. No Google Drive: Abra o arquivo
2. Clique em "Compartilhar" (canto superior direito)
3. Adicione: mkt@osp.com.br
4. Permissão: "Visualizador"
5. Clique "Compartilhar"

---

## 🔒 Segurança

```bash
# Seus tokens estão protegidos:
ls -la api/google_drive_token.pickle
# Resultado: -rw-r--r-- (apenas sua conta acessa)

# Configure .gitignore:
cat >> .gitignore << 'EOF'
api/oauth_credentials.json
api/google_drive_token.pickle
api/credentials.json
EOF
```

---

**Status**: ✅ Pronto para usar!

Próximo: Integrar links nos hubs 📚

