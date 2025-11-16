# 🔐 Setup OAuth com mkt@osp.com.br

Guia rápido para integrar Google Drive da conta mkt@osp.com.br com a API.

---

## ⏱️ Tempo: 5 minutos

---

## 🎯 Objetivo

Conectar a API ao Google Drive de mkt@osp.com.br sem expor a senha.

---

## 📋 Passo 1: Criar OAuth Credentials (3 min)

### 1.1 Vá para Google Cloud Console

https://console.cloud.google.com/apis/credentials

### 1.2 Criar novo OAuth 2.0 Client ID

1. Clique em **"+ CRIAR CREDENCIAIS"** (topo)
2. Selecione **"ID do cliente OAuth"**
3. Se pergunta tipo: escolha **"Aplicativo de desktop"**
4. Nome: `OSP Drive Validator`
5. Clique em **"Criar"**

### 1.3 Download do arquivo JSON

1. Na lista de "Aplicativos de desktop", veja `OSP Drive Validator`
2. Clique no ícone de **download** (⬇️) 
3. Arquivo baixa em `~/Downloads/client_secret_XXXXX.json`

### 1.4 Copiar para projeto

```bash
cp ~/Downloads/client_secret_*.json /Users/gpagotto/osp-website/docs/api/oauth_credentials.json
```

### 1.5 Verificar

```bash
ls -la /Users/gpagotto/osp-website/docs/api/oauth_credentials.json
```

**Esperado:**
```
-rw-r--r--  1 user  staff  XXX Nov 16 19:00 oauth_credentials.json
```

---

## 🔐 Passo 2: Executar Setup Script (1 min)

```bash
cd /Users/gpagotto/osp-website/docs

python3 api/google_drive_oauth_setup.py
```

**Esperado:**
```
======================================================================
🔐 Configuração do Google Drive OAuth - mkt@osp.com.br
======================================================================

📋 PASSO 1: Criar Arquivo de Credenciais OAuth
----------------------------------------------------------------------
✅ oauth_credentials.json encontrado

📋 PASSO 2: Autenticar com mkt@osp.com.br
----------------------------------------------------------------------
🔐 Abrindo navegador para autorizar...
Você será solicitado a fazer login com mkt@osp.com.br
```

### 2.1 Autorizar no navegador

1. Uma aba do navegador abrirá automaticamente
2. Clique em **"Entrar com Google"**
3. Faça login com: **mkt@osp.com.br**
4. Clique em **"Permitir"** (quando pergunta permissões)

### 2.2 Volta automática

Após autorizar, o terminal mostrará:

```
✅ Token carregado com sucesso

📋 PASSO 3: Testar Conexão
----------------------------------------------------------------------
✅ Conexão bem-sucedida!

Primeiros 5 arquivos encontrados:
  📄 Dashboard Vendas (application/vnd.google-apps.spreadsheet)
  📄 Templates (application/vnd.google-apps.folder)
  📄 ...

📋 PASSO 4: Guardar Credenciais para API
----------------------------------------------------------------------
✅ Configuração salva em: api/oauth_config.json

======================================================================
✅ CONFIGURAÇÃO COMPLETA!
======================================================================

✅ Token OAuth salvo em: api/google_drive_token.pickle
✅ Configuração salva em: api/oauth_config.json

🚀 Próximos passos:
1. Iniciar API com: python3 api/google_drive_validator_api.py
2. A API usará automaticamente suas credenciais OAuth
```

---

## 🚀 Passo 3: Iniciar API com OAuth

```bash
python3 api/google_drive_validator_api.py
```

**A API agora usará** as credenciais OAuth de mkt@osp.com.br!

---

## ✅ Verificar Integração

### Testar em novo terminal:

```bash
curl http://localhost:5000/health
```

**Esperado:**
```json
{
  "status": "healthy",
  "drive_api": "connected",
  "authenticated_as": "mkt@osp.com.br"
}
```

---

## 📋 Arquivos Criados

- `api/oauth_credentials.json` - OAuth Client ID (DO NOT COMMIT)
- `api/google_drive_token.pickle` - Token de acesso (DO NOT COMMIT)
- `api/oauth_config.json` - Configuração (seguro, pode commitar)

### Adicionar ao .gitignore:

```bash
cat >> /Users/gpagotto/osp-website/docs/.gitignore << 'EOF'

# Google Drive OAuth
api/oauth_credentials.json
api/google_drive_token.pickle
api/credentials.json

EOF
```

---

## 🔄 Renovação de Token

- **Válido por**: ~1 hora de uso
- **Renovação**: Automática (sem ação necessária)
- **Compartilhável**: Não - é específico de mkt@osp.com.br

---

## 🐛 Troubleshooting

### ❌ "oauth_credentials.json not found"

```bash
# Você pulou o Passo 1
# Siga: Passo 1: Criar OAuth Credentials
```

### ❌ "Browser didn't open"

```bash
# Abra manualmente:
# https://localhost:8080

# Ou faça login novamente:
rm api/google_drive_token.pickle
python3 api/google_drive_oauth_setup.py
```

### ❌ "Token expired"

```bash
# Token é renovado automaticamente
# Se problema persiste:
rm api/google_drive_token.pickle
python3 api/google_drive_oauth_setup.py
```

### ❌ "Access denied"

Verifique permissões:
1. Vá para o arquivo/pasta no Google Drive
2. Clique em "Compartilhar"
3. Certifique que mkt@osp.com.br tem acesso

---

## 🎯 Próximos Passos

1. ✅ OAuth Credentials criado
2. ✅ Setup script executado
3. ✅ Token obtido
4. ✅ API conectada

**Agora você pode:**
- ✅ Validar todos os 64 links do mkt@osp.com.br
- ✅ Verificar permissões em tempo real
- ✅ Gerar relatórios de acesso
- ✅ Integrar com dashboards

---

**Data**: 16 de novembro de 2025  
**Status**: 🆕 PRONTO PARA USAR
