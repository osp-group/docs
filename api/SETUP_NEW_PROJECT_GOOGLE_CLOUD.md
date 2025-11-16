# 🚀 Setup Google Cloud Project - osp-docs-validator

Guia passo a passo para criar novo projeto Google Cloud.

**Tempo total**: ~10 minutos

---

## 📋 Passo 1: Criar Novo Projeto (2 min)

### 1.1 Abrir Google Cloud Console

Vá para: https://console.cloud.google.com/

### 1.2 Criar novo projeto

1. No topo, clique no seletor de projeto (próximo ao logo Google Cloud)
2. Clique em **"NEW PROJECT"** (ou "NOVO PROJETO" em português)
3. Preencha:
   - **Project name**: `osp-docs-validator`
   - **Organization**: (deixe em branco ou selecione sua organização)
   - **Billing account**: Selecione sua conta de cobrança
4. Clique em **"CREATE"**
5. Aguarde ~30 segundos

### 1.3 Selecionar o novo projeto

Depois que criado:
1. Clique novamente no seletor de projeto
2. Procure por `osp-docs-validator`
3. Clique para selecionar

**Confirmação**: No topo deve aparecer "osp-docs-validator" como projeto ativo

---

## 📚 Passo 2: Habilitar Google Drive API (2 min)

### 2.1 Ir para biblioteca de APIs

1. No menu esquerdo, vá para: **APIs & Services** → **Library**
2. Ou abra direto: https://console.cloud.google.com/apis/library

### 2.2 Procurar Google Drive API

1. Na caixa de busca, digite: `Google Drive API`
2. Clique no resultado

### 2.3 Habilitar API

1. Clique no botão azul **"ENABLE"** (topo da página)
2. Aguarde ~10 segundos

**Confirmação**: Botão agora diz "MANAGE" em vez de "ENABLE"

---

## 🔐 Passo 3: Criar OAuth 2.0 Credentials (4 min)

### 3.1 Ir para Credenciais

1. No menu esquerdo: **APIs & Services** → **Credentials**
2. Ou abra direto: https://console.cloud.google.com/apis/credentials

### 3.2 Criar OAuth Consent Screen

**Importante**: Faça isso ANTES de criar o Client ID

1. Na seção esquerda, clique em **"OAuth consent screen"**
2. Selecione **"External"** (para desenvolvimento)
3. Clique em **"CREATE"**

**Preencha o formulário**:
- **App name**: `OSP Drive Validator`
- **User support email**: (seu email)
- **Developer contact**: (seu email)
- Clique **"SAVE AND CONTINUE"**

**Próximas telas**:
- Clique **"ADD OR REMOVE SCOPES"**
- Procure: `drive.readonly`
- Selecione **"Google Drive API - .../auth/drive.readonly"**
- Clique **"UPDATE"**
- Clique **"SAVE AND CONTINUE"**
- Clique **"SAVE AND CONTINUE"** novamente
- Clique **"BACK TO DASHBOARD"**

### 3.3 Criar OAuth Client ID

1. Clique **"+ CREATE CREDENTIALS"** (topo)
2. Selecione **"OAuth client ID"**
3. Tipo de aplicação: **"Desktop application"**
4. Nome: `OSP Drive Validator`
5. Clique **"CREATE"**

**Resultado**: Uma janela pop-up com:
- Client ID
- Client Secret
- Download button

### 3.4 Download do arquivo JSON

1. Clique no botão **⬇️ DOWNLOAD** (ou "Download JSON")
2. Arquivo baixa como: `client_secret_XXXXX.json`
3. Guarde em local seguro (seu Downloads)

---

## 💾 Passo 4: Copiar Arquivo para o Projeto (1 min)

### 4.1 Abrir Terminal

```bash
# Terminal na sua máquina
cd /Users/gpagotto/osp-website/docs
```

### 4.2 Copiar arquivo JSON

```bash
# Copie o arquivo baixado para a pasta api/
cp ~/Downloads/client_secret_*.json api/oauth_credentials.json

# Verificar se copiou
ls -la api/oauth_credentials.json
```

**Esperado**:
```
-rw-r--r--  1 gpagotto  staff  XXXX Nov 16 19:00 api/oauth_credentials.json
```

---

## ✅ Passo 5: Verificar Configuração (1 min)

### 5.1 Instalar dependências (se ainda não tem)

```bash
cd /Users/gpagotto/osp-website/docs
pip install -r api/requirements.txt
```

### 5.2 Executar setup script

```bash
python3 api/google_drive_oauth_setup.py
```

**Esperado na primeira execução**:
```
🔐 Configuração do Google Drive OAuth
...
🔐 Abrindo navegador para autorizar...
Você será solicitado a fazer login com mkt@osp.com.br
```

### 5.3 No navegador

1. Navegador abrirá em `http://localhost:8080`
2. Faça login com: **mkt@osp.com.br**
3. Clique em **"Permitir"** (quando pergunta permissões)

**Resultado no terminal**:
```
✅ Token carregado com sucesso
✅ Conexão bem-sucedida!
Primeiros 5 arquivos encontrados:
  📄 Dashboard...
  📄 ...

======================================================================
✅ CONFIGURAÇÃO COMPLETA!
======================================================================
```

---

## 🚀 Passo 6: Iniciar API (1 min)

```bash
cd /Users/gpagotto/osp-website/docs
python3 api/google_drive_validator_api_enhanced.py
```

**Esperado**:
```
======================================================================
🚀 Starting Google Drive Validator API...
======================================================================

✅ Drive API ready
   Authentication: oauth
   Authenticated as: mkt@osp.com.br

🔗 Server starting at http://localhost:5000
======================================================================
```

---

## ✅ Passo 7: Testar (1 min)

**Em novo terminal:**

```bash
# Health check
curl http://localhost:5000/health | jq .

# Esperado:
{
  "status": "healthy",
  "authenticated_as": "mkt@osp.com.br"
}
```

---

## 🎉 Pronto!

API está agora conectada ao Google Drive de **mkt@osp.com.br** com projeto `osp-docs-validator`!

### Próximos passos:

```bash
# Ver todos os 64 links
curl http://localhost:5000/api/v1/links | jq '.summary'

# Ver permissões
curl http://localhost:5000/api/v1/permissions | jq .

# Ver links de um hub
curl http://localhost:5000/api/v1/links/VENDAS | jq '.links[] | {text, status}'
```

---

## 📋 Checklist

- [ ] Criou projeto `osp-docs-validator`
- [ ] Habilitou Google Drive API
- [ ] Criou OAuth 2.0 Credentials
- [ ] Downloaded `client_secret_*.json`
- [ ] Copiou para `api/oauth_credentials.json`
- [ ] Executou `python3 api/google_drive_oauth_setup.py`
- [ ] Autorizou com mkt@osp.com.br
- [ ] Iniciou API com `python3 api/google_drive_validator_api_enhanced.py`
- [ ] Testou `/health` endpoint ✅

---

## 🐛 Problemas?

### ❌ "Projeto não aparece no seletor"

Aguarde ~1 minuto e recarregue a página

### ❌ "ENABLE button não aparece"

Certifique-se de estar no projeto correto (seletor no topo)

### ❌ "OAuth consent screen error"

Volte e complete todos os campos obrigatórios (*)

### ❌ "Arquivo não copiou"

```bash
# Verifique localização
ls -la ~/Downloads/client_secret_*.json

# Se não achar, procure em:
find ~/Downloads -name "*secret*.json" 2>/dev/null
```

### ❌ "Browser não abriu no setup"

```bash
# Abra manualmente:
# http://localhost:8080

# Ou remova token e tente novamente:
rm api/google_drive_token.pickle
python3 api/google_drive_oauth_setup.py
```

---

## 🔒 Segurança

```bash
# Proteja credenciais
chmod 600 api/oauth_credentials.json
chmod 600 api/google_drive_token.pickle

# Adicione ao .gitignore
echo "api/oauth_credentials.json" >> .gitignore
echo "api/google_drive_token.pickle" >> .gitignore
```

---

**Data**: 16 de novembro de 2025  
**Status**: 🆕 READY TO EXECUTE
