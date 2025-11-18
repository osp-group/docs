# 🚀 Como Usar Google Drive API - Estrutura Pronta

**Data**: 18 de novembro de 2025  
**Status**: ✅ **PRONTO PARA USAR - API já está em `/contabilidade`**  
**Estrutura**: Reutilizável via import

---

## 📍 LOCALIZAÇÃO DA API

```
/osp-website/contabilidade/
  └── functions/
      └── src/
          └── google-workspace-service.ts  ← API PRONTA
```

**Arquivo**: 476 linhas - Totalmente implementado e testado

---

## 🔧 COMO USAR

### 1️⃣ Importar o Serviço

```typescript
import {
  getGoogleWorkspaceConfig,
  createDriveFolder,
  listDriveFiles,
  appendToSheets,
  sendEmailViaGmail,
  createGoogleDoc,
  initializeGoogleApis,
  EmailOptions
} from './google-workspace-service';
```

---

### 2️⃣ Obter Configuração

```typescript
// Carrega automaticamente de Firebase functions config
const config = getGoogleWorkspaceConfig();

// config contém:
// - serviceAccountKey: { client_email, private_key, ... }
// - workspaceAdminEmail: "seu-admin@osp.com.br"
```

---

### 3️⃣ CASOS DE USO

#### 📁 Criar Pasta no Google Drive

```typescript
const folderId = await createDriveFolder(
  'Candidatos MKT 2025',
  config,
  'seu-admin@osp.com.br',
  'parent_folder_id_optional'
);

console.log(`✅ Pasta criada: ${folderId}`);
// Resultado: "1a2b3c4d5e6f7g8h9i0j"
```

#### 📋 Listar Arquivos em Pasta

```typescript
const files = await listDriveFiles(
  config,
  'seu-admin@osp.com.br',
  'parent_folder_id'
);

// Resultado:
// [
//   { id: '...', name: 'CV.pdf', mimeType: 'application/pdf', webViewLink: '...' },
//   { id: '...', name: 'Prova.pdf', mimeType: 'application/pdf', webViewLink: '...' },
// ]

files.forEach(file => console.log(`📄 ${file.name}: ${file.webViewLink}`));
```

#### 📊 Adicionar Dados em Google Sheets

```typescript
await appendToSheets(
  '1a2b3c4d5e6f7g8h9i0j',  // Spreadsheet ID
  'Candidatos',              // Sheet name
  [
    ['Giulia Attolini', '78/100', 'R$ 5.000', 'Aprovada'],
    ['Jonathan Rodrigues', '58→Tier1', 'R$ 4.500', 'Tier 1'],
    ['Raissa Costa', '76/100', 'R$ 5.000', 'Aprovada'],
  ],
  config,
  'seu-admin@osp.com.br'
);

console.log(`✅ Dados sincronizados com Google Sheets`);
```

#### 📧 Enviar Email @osp.com.br

```typescript
const emailOptions: EmailOptions = {
  to: 'destinatario@example.com',
  subject: 'Resultado do Processo Seletivo MKT 2025',
  htmlContent: `
    <h1>🎉 Parabéns!</h1>
    <p>Você foi aprovado para a próxima fase.</p>
    <p><a href="https://drive.google.com/...">Acesse a pasta de candidatos</a></p>
  `,
  attachments: [
    {
      filename: 'ranking.pdf',
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

console.log(`✅ Email enviado de seu-admin@osp.com.br`);
```

#### 📄 Criar Google Doc

```typescript
const docId = await createGoogleDoc(
  'Relatório MKT 2025 - Candidatos',
  config,
  'seu-admin@osp.com.br'
);

console.log(`✅ Google Doc criado: https://docs.google.com/document/d/${docId}/edit`);
```

---

## 🎯 EXEMPLO COMPLETO: Sincronizar Candidatos MKT

```typescript
import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
import {
  getGoogleWorkspaceConfig,
  createDriveFolder,
  appendToSheets,
  sendEmailViaGmail,
  EmailOptions
} from './google-workspace-service';

/**
 * Cloud Function: Sincronizar candidatos com Google Drive
 * Trigger: Quando novo documento é criado em candidates/{candidateId}
 */
export const syncCandidateToGoogleDrive = functions.firestore
  .document('candidates/{candidateId}')
  .onCreate(async (snap, context) => {
    const candidateId = context.params.candidateId;
    const candidateData = snap.data() as {
      name: string;
      email: string;
      score: number;
      cvUrl: string;
      provaUrl: string;
    };

    try {
      const config = getGoogleWorkspaceConfig();
      const adminEmail = 'seu-admin@osp.com.br';

      // 1. Criar pasta para candidato
      const folderId = await createDriveFolder(
        `${candidateData.name}`,
        config,
        adminEmail,
        'PARENT_FOLDER_ID_MKT_2025'  // Pasta pai
      );

      console.log(`✅ Pasta criada para ${candidateData.name}: ${folderId}`);

      // 2. Adicionar dados em Google Sheets
      await appendToSheets(
        'SPREADSHEET_ID_MKT',
        'Candidatos',
        [[
          candidateData.name,
          `${candidateData.score}/100`,
          candidateData.email,
          new Date().toLocaleDateString('pt-BR'),
          `https://drive.google.com/drive/folders/${folderId}`,
        ]],
        config,
        adminEmail
      );

      console.log(`✅ Dados adicionados em Google Sheets`);

      // 3. Enviar email de confirmação
      const emailOptions: EmailOptions = {
        to: candidateData.email,
        subject: `Candidatura Recebida - ${candidateData.name}`,
        htmlContent: `
          <h2>Olá ${candidateData.name}!</h2>
          <p>Obrigado por se candidatar ao processo seletivo MKT 2025.</p>
          <p>Sua avaliação inicial: <strong>${candidateData.score}/100</strong></p>
          <p>Seus documentos foram organizados em: 
            <a href="https://drive.google.com/drive/folders/${folderId}">Google Drive</a>
          </p>
          <p>Entraremos em contato em breve!</p>
        `
      };

      await sendEmailViaGmail(emailOptions, config, adminEmail);
      console.log(`✅ Email enviado para ${candidateData.email}`);

      // 4. Atualizar Firestore com links
      await snap.ref.update({
        googleDriveFolderId: folderId,
        driveLink: `https://drive.google.com/drive/folders/${folderId}`,
        synced: true,
        syncedAt: admin.firestore.FieldValue.serverTimestamp(),
      });

      return { success: true, folderId };
    } catch (error) {
      console.error(`❌ Erro ao sincronizar ${candidateId}:`, error);
      
      // Marcar como erro em Firestore
      await snap.ref.update({
        syncError: error instanceof Error ? error.message : 'Erro desconhecido',
        synced: false,
      });

      throw error;
    }
  });
```

---

## 🔐 CONFIGURAÇÃO NECESSÁRIA

A API do contabilidade já está rodando. Você precisa apenas:

### 1. Verificar se as variáveis estão configuradas:

```bash
cd ~/osp-website/contabilidade

# Verificar configuração
firebase functions:config:get
```

**Você deve ver**:
```json
{
  "google": {
    "service_account_key": "{ ... json ... }",
    "workspace_admin_email": "seu-admin@osp.com.br"
  }
}
```

### 2. Se não estiverem configuradas:

```bash
# Setar service account key (obter do Google Cloud Console)
firebase functions:config:set \
  google.service_account_key='{ "type": "service_account", ... }' \
  google.workspace_admin_email='seu-admin@osp.com.br'

# Deploy
firebase deploy --only functions
```

---

## 📝 VARIÁVEIS NECESSÁRIAS NO SEU CÓDIGO

Adicione estas constantes com valores reais:

```typescript
// ⚠️ OBTER ESTES VALORES PRIMEIRO

// 1. Folder ID da pasta "Candidatos MKT 2025" no Google Drive
const PARENT_FOLDER_ID_MKT_2025 = 'paste_aqui_folder_id';

// 2. Spreadsheet ID onde adicionar dados
const SPREADSHEET_ID_MKT = 'paste_aqui_spreadsheet_id';

// 3. Email admin do Workspace
const ADMIN_EMAIL = 'seu-admin@osp.com.br';

// 4. Email para receber notificações
const NOTIFICATION_EMAIL = 'leo@osp.com.br';
```

---

## 🎯 COMO OBTER OS IDs

### Folder ID do Google Drive

```
URL: https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j?usp=sharing
                                          └─ Folder ID: 1a2b3c4d5e6f7g8h9i0j
```

### Spreadsheet ID

```
URL: https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j/edit#gid=0
                                          └─ Spreadsheet ID: 1a2b3c4d5e6f7g8h9i0j
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

Para começar a usar com Candidatos MKT:

- [ ] Verificar que `firebase functions:config:get` mostra `google.service_account_key`
- [ ] Criar pasta "Candidatos MKT 2025" no Google Drive
- [ ] Obter Folder ID e adicionar ao código
- [ ] Criar Google Sheet "Ranking MKT 2025"
- [ ] Obter Spreadsheet ID e adicionar ao código
- [ ] Importar `google-workspace-service` no seu código
- [ ] Implementar a Cloud Function (exemplo acima)
- [ ] Testar: Criar novo candidato em Firestore
- [ ] Verificar que pasta foi criada no Drive
- [ ] Verificar que dados foram adicionados em Sheets
- [ ] Verificar que email foi enviado

---

## 🔗 INTEGRAÇÃO COM PROJETO ATUAL

### Para Candidatos MKT 2025

```
1. Candidato criado em Firestore: candidates/{id}
   ↓
2. Cloud Function dispara (onCreate)
   ↓
3. Criar pasta no Drive: /Candidatos MKT 2025/{Nome Candidato}/
   ↓
4. Adicionar linha em Google Sheets
   ↓
5. Enviar email de confirmação @osp.com.br
   ↓
6. Atualizar Firestore com links Drive
```

---

## 📊 EXEMPLOS DE RETORNO

### Criar Pasta
```
✅ Pasta criada: 1a2b3c4d5e6f7g8h9i0j
Link: https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j
```

### Adicionar Dados
```
✅ Dados sincronizados com Google Sheets
Range: Candidatos!A:Z
Linhas adicionadas: 1
```

### Enviar Email
```
✅ Email sent via Gmail: CADcHthYfkL9x...
From: seu-admin@osp.com.br
To: candidato@example.com
Subject: Candidatura Recebida - Giulia Attolini
```

---

## ⚠️ TRATAMENTO DE ERROS

```typescript
try {
  const folderId = await createDriveFolder(...);
} catch (error) {
  console.error('❌ Erro ao criar pasta:', error);
  // Erros comuns:
  // - "Google configuration not found" → Firebase config não foi setado
  // - "Access Denied" → Service account não tem permissão
  // - "Invalid parent folder ID" → Folder ID não existe ou inválido
}
```

---

## 🚀 PRÓXIMOS PASSOS

1. **Hoje**: Verificar que Google API está configurada em `/contabilidade`
2. **Hoje**: Criar pasta "Candidatos MKT 2025" no Google Drive
3. **Hoje**: Obter Folder ID e Spreadsheet ID
4. **Amanhã**: Implementar Cloud Function para sincronizar candidatos
5. **Amanhã**: Testar com novo candidato
6. **Próx. semana**: Expandir para P6 DATOS_INTELIGENCIA

---

## 📞 REFERÊNCIAS

- ✅ Arquivo principal: `/contabilidade/functions/src/google-workspace-service.ts`
- ✅ Cloud Function exemplo: `/contabilidade/functions/src/index.ts` (linhas 1-600)
- ✅ Docs: `/integration/GOOGLE_DRIVE_API_VERIFICATION.md`

---

**Status**: 🟢 **PRONTO PARA USAR**  
**Estrutura**: Reutilizável entre projetos  
**Tempo para primeira integração**: ~1 hora  

Qualquer dúvida, consulte o arquivo de verificação completo! 🚀
