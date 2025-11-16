# 🔐 Google Drive API Setup Guide

**Data**: 16 de novembro de 2025  
**Objetivo**: Configurar validação avançada dos links Google Drive com permissões

---

## 🎯 O que você consegue com a validação API

✅ Verificar se documentos existem  
✅ Testar acesso real (@osp-group)  
✅ Ver permissões compartilhadas  
✅ Confirmar proprietários  
✅ Validar tipos de documentos  
✅ Rastrear últimas modificações  

---

## 📋 Pré-requisitos

- ✅ Conta Google com acesso ao Google Cloud Console
- ✅ Python 3.8+
- ✅ Terminal/Console
- ✅ Acesso aos arquivos Google Drive a validar

---

## 🚀 Passo a Passo (5 minutos)

### 1️⃣ Criar Google Cloud Project

1. Vá para [Google Cloud Console](https://console.cloud.google.com/project)
2. Clique em **"Criar Projeto"** (canto superior)
3. Nome: `osp-docs-validation` (ou qualquer nome)
4. Clique em **"Criar"**
5. Aguarde criação (leva ~30 segundos)

### 2️⃣ Habilitar Google Drive API

1. No console, vá para **"APIs & Serviços"** → **"Biblioteca"**
2. Procure por: `Google Drive API`
3. Clique em **"Google Drive API"**
4. Clique em **"Ativar"** (azul, topo)
5. Aguarde ativação (~10 segundos)

### 3️⃣ Criar Service Account

1. Vá para **"APIs & Serviços"** → **"Credenciais"**
2. Clique em **"+ CRIAR CREDENCIAIS"** (topo)
3. Selecione **"Service Account"**
4. Preencha:
   - **Nome da conta de serviço**: `osp-docs-validator`
   - **ID da conta de serviço**: (preenchido automaticamente)
   - **Descrição**: `Validator para arquivos Google Drive`
5. Clique em **"Criar e Continuar"**
6. Na próxima tela: deixe em branco, clique em **"Continuar"**
7. Clique em **"Concluído"**

### 4️⃣ Gerar Chave JSON

1. Clique na conta de serviço criada (`osp-docs-validator`)
2. Vá para aba **"Chaves"**
3. Clique em **"+ ADICIONAR CHAVE"** → **"Criar nova chave"**
4. Selecione **"JSON"**
5. Clique em **"Criar"**
6. Um arquivo `XXX-XXXXX.json` será baixado automaticamente
7. **Guarde este arquivo** em local seguro

### 5️⃣ Copiar arquivo JSON

1. O arquivo foi baixado em Downloads (ex: `osp-docs-validator-xxxxx.json`)
2. Copie para a pasta do projeto:
   ```bash
   cp ~/Downloads/osp-docs-validator-*.json /Users/gpagotto/osp-website/docs/
   mv /Users/gpagotto/osp-website/docs/*.json /Users/gpagotto/osp-website/docs/credentials.json
   ```

### 6️⃣ Compartilhar Arquivos Google Drive

**Importante**: Os arquivos devem ser compartilhados com o email da Service Account

1. No console Google Cloud, vá para **"Credenciais"**
2. Clique na conta de serviço (`osp-docs-validator`)
3. Copie o **"Email da conta de serviço"** (algo como `osp-docs-validator@xxxxx.iam.gserviceaccount.com`)
4. Em cada arquivo Google Drive que quer validar:
   - Clique em **"Compartilhar"** (canto superior direito)
   - Cole o email da service account
   - Permissão: **"Visualizador"** (é suficiente)
   - Clique em **"Compartilhar"**

**Dica**: Para compartilhar em massa:
- Crie uma pasta no Drive com todos os documentos
- Compartilhe a pasta com a service account
- Todos os documentos dentro serão acessíveis

### 7️⃣ Instalar Dependências Python

```bash
cd /Users/gpagotto/osp-website/docs
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 8️⃣ Executar Validação

```bash
python3 scripts/validate_google_drive_links_api.py credentials.json
```

---

## ✅ Resultado Esperado

Se tudo funcionar:

```
✅ Google Drive API initialized successfully

🔍 Scanning hubs and validating with API...
  📄 VENDAS...
  📄 CONHECIMENTO...
  📄 DADOS_INTELIGENCIA...
  📄 MARKETING...

📋 Scanning audit file...
  Found 83 links in audit file

✅ Advanced report generated: /Users/gpagotto/osp-website/docs/testing/QA_GOOGLE_DRIVE_LINKS_ADVANCED_P6.md

================================================
📊 VALIDATION SUMMARY
================================================

Total Links Checked: 64
Accessible: 64 ✅
Inaccessible: 0 ⚠️
Access Rate: 100.0%
```

---

## 🆘 Troubleshooting

### ❌ "Module not found" error

**Solução**:
```bash
pip install --upgrade google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### ❌ "Credentials not found"

**Solução**:
```bash
# Verifique se o arquivo existe
ls -la /Users/gpagotto/osp-website/docs/credentials.json

# Se não existir, execute novamente o setup
```

### ❌ "Access denied (403)"

**Solução**:
1. Verifique se os arquivos foram compartilhados com o email da service account
2. Re-compartilhe com permissão "Visualizador"
3. Aguarde ~1 minuto e tente novamente

### ❌ "Document not found (404)"

**Solução**:
- O link é inválido ou foi deletado
- Verifique a URL no arquivo markdown
- Atualize com o link correto

### ❌ "401 Unauthorized"

**Solução**:
1. Gere uma nova chave JSON (delete a antiga no console)
2. Atualize o arquivo `credentials.json`
3. Tente novamente

---

## 🔒 Segurança

**Importante**: Proteja o arquivo `credentials.json`

```bash
# Definir permissões restritivas
chmod 600 /Users/gpagotto/osp-website/docs/credentials.json

# Adicionar ao .gitignore (NÃO commit no repo)
echo "credentials.json" >> /Users/gpagotto/osp-website/docs/.gitignore
```

**Nunca**:
- ❌ Compartilhe o arquivo `credentials.json`
- ❌ Faça commit no GitHub
- ❌ Envie por email
- ❌ Deixe em local público

---

## 📊 O que o Script Gera

Após executar, você terá:

📄 `testing/QA_GOOGLE_DRIVE_LINKS_ADVANCED_P6.md`
- Relatório completo de validação
- Permissões verificadas
- Status de acesso por documento
- Recomendações de segurança

---

## 🔄 Automação (Futuro)

Para validação mensal automática:

```bash
# Cron job (executar todo 1º do mês)
0 9 1 * * cd /Users/gpagotto/osp-website/docs && python3 scripts/validate_google_drive_links_api.py credentials.json
```

---

## 📞 Suporte

- **Erro no setup?** Contate `platform@ospalavancagem.com.br`
- **Problema com API?** Veja [Google Drive API Docs](https://developers.google.com/drive/api/reference/rest)
- **Question?** Abra issue em `osp-group/docs`

---

## 📎 Referências

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Drive API Docs](https://developers.google.com/drive/api)
- [Service Account Auth](https://developers.google.com/identity/protocols/oauth2/service-account)
- [Python Google Client Library](https://github.com/googleapis/google-api-python-client)

---

**Próximas ações**:
1. ✅ Setup concluído
2. ⏳ Executar script: `python3 scripts/validate_google_drive_links_api.py credentials.json`
3. ⏳ Revisar relatório gerado
4. ⏳ Corrigir qualquer link inválido
5. ⏳ Atualizar compartilhamentos conforme necessário

---

**Setup Guide Version**: 1.0  
**Date**: 16 de novembro de 2025  
**Status**: Ready to use
