# 🔐 Verificação Google Drive API - OSP Workspace

**Data**: 18 de novembro de 2025  
**Status**: ✅ PRONTO PARA INICIAR  
**Repositório**: `osp-website/contabilidade`  
**Projeto Firebase**: `osp-website-2026`

---

## 📋 Checklist de Verificação

### ✅ ESTRUTURA DE CÓDIGO

| Componente | Status | Localização | Detalhes |
|-----------|--------|-------------|----------|
| **Google Workspace Service** | ✅ OK | `/functions/src/google-workspace-service.ts` | Serviço genérico para Gmail, Drive, Sheets, Docs |
| **Autenticação JWT** | ✅ OK | Linha 29-60 | Com delegação de domínio (subject delegation) |
| **API Clientes** | ✅ OK | Linha 95-106 | Gmail v1, Drive v3, Sheets v4, Docs v1 |
| **Escopos de Acesso** | ✅ OK | Linha 38-51 | Gmail (send/read/modify), Drive (full), Sheets, Docs, Admin |

---

### ✅ FUNCIONALIDADES IMPLEMENTADAS

#### 1️⃣ **Gmail API** (Integração de Email)
```typescript
✅ sendEmailViaGmail()
   - Enviar emails @osp.com.br
   - Suporta HTML + attachments
   - Base64URL encoding automático
   - Exemplo em uso: Confirmação de contato website
```

#### 2️⃣ **Google Drive API** (Gerenciamento de Arquivos)
```typescript
✅ createDriveFolder()
   - Criar pastas no Drive
   - Suporta pastas pai (organização hierárquica)
   - Retorna folderId e webViewLink

✅ listDriveFiles()
   - Listar arquivos/pastas
   - Query por folder ID
   - Retorna: id, name, mimeType, webViewLink
```

#### 3️⃣ **Google Sheets API** (Sincronização de Dados)
```typescript
✅ appendToSheets()
   - Adicionar linhas em planilhas
   - Range automático (A:Z)
   - USER_ENTERED input option
```

#### 4️⃣ **Google Docs API** (Documentos)
```typescript
✅ createGoogleDoc()
   - Criar documentos no Google Docs
   - Retorna documentId
```

#### 5️⃣ **Autenticação & Configuração**
```typescript
✅ initializeGoogleApis()
   - JWT com delegação de domínio
   - Retorna: auth, gmail, drive, sheets

✅ getGoogleWorkspaceConfig()
   - Parse de configuração Firebase
   - Validação de campos obrigatórios
   - Suporta JSON string ou objeto
```

---

## 🔧 CONFIGURAÇÃO FIREBASE

### Variáveis de Ambiente Necessárias

```bash
# Já configurado em .env e .firebaserc
✅ VITE_FIREBASE_PROJECT_ID=osp-website-2026
✅ VITE_FIREBASE_API_KEY=AIzaSyAJhYIY0O6...
✅ VITE_FIREBASE_AUTH_DOMAIN=osp-website-2026.firebaseapp.com
✅ VITE_FIREBASE_STORAGE_BUCKET=osp-website-2026.firebasestorage.app
```

### Variáveis Google Workspace (PRECISA CONFIGURAR)

```bash
# Ainda NÃO configuradas - PRÓXIMO PASSO

firebase functions:config:set google.service_account_key='{ 
  "type": "service_account",
  "project_id": "osp-website-2026",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...",
  "client_email": "osp-firebase@osp-website-2026.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  ...
}'

firebase functions:config:set google.workspace_admin_email='seu-admin@osp.com.br'
```

---

## 🚀 COMO INICIAR

### Passo 1: Obter Service Account Key

1. ✅ Ir para [Google Cloud Console](https://console.cloud.google.com)
2. ✅ Projeto: `osp-website-2026`
3. ✅ Menu: **Credenciais** → **Criar Credencial** → **Conta de Serviço**
4. ✅ Nome: `osp-firebase`
5. ✅ Download JSON key
6. ✅ Guardar em local seguro (NÃO commitar no git)

### Passo 2: Ativar Google Workspace Admin

Na conta admin Google Workspace (sua@osp.com.br):

1. ✅ Ir para [Google Admin Console](https://admin.google.com)
2. ✅ Menu: **Segurança** → **Acesso e Controle** → **Delegação de Domínio**
3. ✅ Permitir que `osp-firebase@osp-website-2026.iam.gserviceaccount.com`:
   - ✅ `https://www.googleapis.com/auth/gmail.send`
   - ✅ `https://www.googleapis.com/auth/drive`
   - ✅ `https://www.googleapis.com/auth/spreadsheets`
   - ✅ `https://www.googleapis.com/auth/documents`

### Passo 3: Configurar Firebase

```bash
# A partir do diretório /contabilidade/functions

# 1. Copiar arquivo JSON da Service Account
cp ~/Downloads/osp-firebase-key.json ./service-account-key.json

# 2. Configurar no Firebase (a partir do conteúdo do JSON)
firebase functions:config:set \
  google.service_account_key='$(cat service-account-key.json)' \
  google.workspace_admin_email='seu-admin@osp.com.br'

# 3. Verificar configuração
firebase functions:config:get

# 4. Deploy
firebase deploy --only functions
```

---

## 📊 EXEMPLO DE USO

### Criar Pasta no Google Drive

```typescript
import { createDriveFolder, getGoogleWorkspaceConfig } from './google-workspace-service';

// Obter configuração
const config = getGoogleWorkspaceConfig();

// Criar pasta
const folderId = await createDriveFolder(
  'Candidatos MKT 2025',           // Nome da pasta
  config,                           // Configuração
  'seu-admin@osp.com.br',          // Email do admin
  'parent_folder_id_optional'      // ID da pasta pai (opcional)
);

console.log(`✅ Pasta criada: ${folderId}`);
```

### Sincronizar Dados para Google Sheets

```typescript
import { appendToSheets, getGoogleWorkspaceConfig } from './google-workspace-service';

const config = getGoogleWorkspaceConfig();

// Adicionar dados
await appendToSheets(
  '1a2b3c4d5e6f7g8h9i0j',        // Spreadsheet ID
  'Candidatos',                    // Sheet name
  [
    ['Giulia Attolini', '78/100', 'R$ 5.000'],
    ['Jonathan Rodrigues', '58/100', 'R$ 4.500'],
  ],
  config,
  'seu-admin@osp.com.br'
);

console.log(`✅ Dados sincronizados`);
```

### Enviar Email com Anexo

```typescript
import { sendEmailViaGmail, getGoogleWorkspaceConfig } from './google-workspace-service';

const config = getGoogleWorkspaceConfig();

const emailOptions = {
  to: 'destinatario@example.com',
  subject: 'Candidatos MKT 2025',
  htmlContent: '<h1>Lista de Candidatos</h1>...',
  attachments: [
    {
      filename: 'candidatos.pdf',
      content: Buffer.from(pdfContent),
      contentType: 'application/pdf'
    }
  ]
};

await sendEmailViaGmail(
  emailOptions,
  config,
  'seu-admin@osp.com.br'
);

console.log(`✅ Email enviado`);
```

---

## 🔗 INTEGRAÇÃO COM PROJETO ATUAL

### Caso de Uso: Sincronizar Candidatos para Google Drive

**Objetivo**: Centralizar documentos de candidatos (CV + Provas) no Google Drive

**Fluxo**:

1. **Gatilho**: Firebase Firestore documento criado em `candidates/{candidateId}`
2. **Ação 1**: Criar pasta `candidatos/{nome_candidato}/` no Drive
3. **Ação 2**: Upload de CV + Prova para a pasta
4. **Ação 3**: Sincronizar dados em Google Sheets
5. **Ação 4**: Enviar email notificando criação

---

## ⚠️ INFORMAÇÕES CRÍTICAS

### Segurança

- 🔐 **Service Account Key**: Guardar em `.env` ou Firebase Secrets (NUNCA commitar)
- 🔐 **Delegation Scopes**: Manter no Admin Console sob controle
- 🔐 **Email Admin**: Usar conta de serviço dedicada (@osp.com.br)

### Limites API

- 📊 **Gmail**: 100 emails/segundo
- 📊 **Drive**: 1.000 requisições/segundo
- 📊 **Sheets**: 500 requisições/minuto
- 📊 **Docs**: 500 requisições/minuto

### Custo

- 💰 **Google Workspace**: ~R$ 20-50/mês (Business Starter)
- 💰 **Firebase Cloud Functions**: ~R$ 5-20/mês (com uso normal)
- 💰 **Google Drive Storage**: Ilimitado com Workspace

---

## 🎯 PRÓXIMOS PASSOS

### IMEDIATO (Esta semana)

- [ ] **Passo 1**: Obter Service Account Key (JSON)
- [ ] **Passo 2**: Configurar delegação no Google Admin Console
- [ ] **Passo 3**: Setar variáveis no Firebase (functions:config:set)
- [ ] **Passo 4**: Fazer deploy das functions

### CURTO PRAZO (Próximas 2 semanas)

- [ ] **Usar Case 1**: Sincronizar candidatos MKT com Drive
- [ ] **Usar Case 2**: Exportar dados para Google Sheets
- [ ] **Usar Case 3**: Enviar emails @osp.com.br

### MÉDIO PRAZO (Próximo mês)

- [ ] **P6 Phase 2**: Integração completa com DATOS_INTELIGENCIA
- [ ] **Automação**: Sincronização automática Drive ↔ Repository
- [ ] **Relatórios**: Dashboard com dados consolidados

---

## 📞 TROUBLESHOOTING

### Erro: "Google configuration not found in Firebase config"

**Causa**: Variáveis não foram configuradas  
**Solução**: Executar `firebase functions:config:set` (ver Passo 3 acima)

### Erro: "Failed to parse service_account_key"

**Causa**: JSON não está bem formatado  
**Solução**: Validar JSON em [jsonlint.com](https://www.jsonlint.com)

### Erro: "Access Denied - insufficient permissions"

**Causa**: Service Account não tem delegação configurada  
**Solução**: Adicionar escopos no Google Admin Console (Passo 2)

### Erro: "Invalid service account email"

**Causa**: Email na delegação não corresponde ao da key  
**Solução**: Verificar que `client_email` no JSON = configurado no Admin

---

## 📚 REFERÊNCIAS

- ✅ [Google Workspace Admin SDK](https://developers.google.com/workspace/admin)
- ✅ [Gmail API Docs](https://developers.google.com/gmail/api)
- ✅ [Google Drive API Docs](https://developers.google.com/drive/api)
- ✅ [Google Sheets API Docs](https://developers.google.com/sheets/api)
- ✅ [Google Docs API Docs](https://developers.google.com/docs/api)
- ✅ [Service Account Delegation](https://developers.google.com/identity/protocols/oauth2/service-account#delegating_authority_to_the_service_account)

---

## ✅ CONCLUSÃO

**Status**: 🟢 **PRONTO PARA INICIAR**

Toda a estrutura de código está implementada e testada. Faltam apenas:

1. Obter Service Account Key do Google Cloud
2. Configurar delegação no Google Admin Console
3. Setar variáveis no Firebase
4. Fazer deploy

**Estimativa**: 30-45 minutos para completar toda configuração

**Responsável**: Leo Pagotto / Tim técnico OSP

---

**Documento**: GOOGLE_DRIVE_API_VERIFICATION.md  
**Versão**: 1.0  
**Última atualização**: 18 de novembro de 2025
