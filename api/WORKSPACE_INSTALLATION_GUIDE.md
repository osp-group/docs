# 🚀 Google Workspace Integration - Guia Completo

**Status:** ✅ Pronto para instalar  
**Data:** 16 de novembro de 2025

---

## 📋 O que é?

Um **Google Apps Script** que roda dentro do Google Workspace e:
- ✅ Compartilha documentos **automaticamente** com a Service Account
- ✅ Lista **todos os documentos** de uma pasta (com IDs reais)
- ✅ Comunica com nossa **API Python** via webhooks
- ✅ Sincroniza dados em **tempo real**

**Resultado:** Nenhuma ação manual necessária!

---

## 🛠 Instalação em 5 minutos

### Passo 1: Criar o Script

1. Abra [Google Drive](https://drive.google.com)
2. Clique em **"+ Novo"** → **"Mais"** → **"Google Apps Script"**

![Step 1](screenshots/step1.png)

3. Copie o conteúdo de `api/google_workspace_integration.gs`
4. Cole no editor (substitua tudo)
5. Salve com o nome: **"OSP Docs Integration"**

### Passo 2: Configurar Credenciais

Edite estas linhas no topo do script:

```javascript
const SERVICE_ACCOUNT_EMAIL = "ga4-api-access@site-2026.iam.gserviceaccount.com";
const API_URL = "http://localhost:5000/api/v2";  // Sua API Python
const WEBHOOK_TOKEN = "seu_token_super_seguro_aqui";  // Gere um token aleatório
```

Para gerar um token seguro:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Passo 3: Autorizar o Script

1. No editor Google Apps Script, clique em **"Executar"**
2. Clique na função **"setup"**
3. Autorize as permissões (pode estar em uma aba separada)
4. Veja o resultado no Log (ícone 🔽)

### Passo 4: Configurar a API

Na sua API Python (`api/google_drive_api_v2.py`), atualize o token:

```python
WEBHOOK_TOKEN = "seu_token_super_seguro_aqui"  # MESMO token do Apps Script
```

### Passo 5: Testar

No Google Apps Script:

1. Clique em **"Selecionar função"** (topo)
2. Escolha **"testListDocuments"**
3. Modifique a função para adicionar o ID de uma pasta real

```javascript
const folderId = "1234567890";  // Coloque ID real
```

4. Clique em **"Executar"**
5. Veja no Log os documentos encontrados

---

## 📖 Como Usar

### Opção 1: Compartilhar Uma Pasta

```javascript
// No Google Apps Script
shareFolder("seu_folder_id");
```

### Opção 2: Sincronizar Com API

```javascript
// Sincroniza tudo automaticamente
syncFolderWithAPI("seu_folder_id");

// Você verá na API:
// 📥 Sincronizando 42 documentos de DADOS_INTELIGENCIA
// ✅ Sincronização concluída: 42/42
```

### Opção 3: Buscar Documentos

```javascript
// Busca pelo nome
const results = searchDocuments("OKR");

// Resultado:
// [{
//   name: "OKRs 2025",
//   id: "1qCYg7nCz5v0k_8W2pL_7mN9qRx_4hJ5sA_bT2uV1wXy",
//   type: "Planilha",
//   url: "https://docs.google.com/spreadsheets/d/..."
// }]
```

### Opção 4: Gerar Relatório

```javascript
// Cria relatório e envia por email
generateAndEmailReport("seu_folder_id");
```

---

## 🔄 Fluxo de Funcionamento

```
┌─────────────────────────┐
│   Google Workspace      │
│  (Apps Script runs)     │
└────────────┬────────────┘
             │
             │ 1. Encontra documentos
             │ 2. Obtém IDs reais
             │ 3. Compartilha com Service Account
             │
             ▼
┌─────────────────────────┐
│   Google Drive API      │
│  (Recebe documentos)    │
└────────────┬────────────┘
             │
             │ Webhook POST para:
             │ /api/v2/documents/sync
             │
             ▼
┌─────────────────────────┐
│  API Python (v2)        │
│  (localhost:5000)       │
└────────────┬────────────┘
             │
             │ Processa:
             │ - Valida acesso
             │ - Armazena em cache
             │ - Gera relatório
             │
             ▼
┌─────────────────────────┐
│  Relatório Gerado       │
│  ✅ 42 documentos       │
│  🎯 40 acessíveis       │
│  ❌ 2 inacessíveis      │
└─────────────────────────┘
```

---

## 📍 Encontrar ID da Pasta

### Método 1: De uma URL

Se a URL é:
```
https://drive.google.com/drive/folders/1Bw8V9G-1a2b3c4d5e6f7g8h9i0j1k2l
```

O ID é: `1Bw8V9G-1a2b3c4d5e6f7g8h9i0j1k2l`

### Método 2: No Google Apps Script

```javascript
// Abra a pasta no Drive
// Cole este código no console:
function getSelectedFolders() {
  const folder = DriveApp.getRootFolder();
  Logger.log(folder.getId());  // Ver no Log
}
```

---

## 🧪 Testes

### Teste 1: Listar documentos

```bash
# Na API rodando
curl http://localhost:5000/api/v2/documents/list
```

Response:
```json
{
  "total_batches": 3,
  "documents": {
    "folder_abc123": {
      "folder_name": "DADOS_INTELIGENCIA",
      "documents": [...],
      "count": 42
    }
  }
}
```

### Teste 2: Status de Workspace

```bash
curl http://localhost:5000/api/v2/workspace/status
```

Response:
```json
{
  "status": "connected",
  "webhook_endpoint": "/api/v2/documents/sync",
  "last_sync": "2025-11-16T10:30:00",
  "cached_batches": 3
}
```

### Teste 3: Validação Completa

```bash
curl http://localhost:5000/api/v2/reports/validation
```

Abre relatório em HTML no navegador

---

## 🐛 Troubleshooting

### "Erro de autorização"

**Causa:** Você não deu permissão ao script  
**Solução:**
1. Clique em "Executar"
2. Aceite as permissões na aba que abrir
3. Se não aparecer, clique em seu avatar > "Revisar permissões"

### "Webhook não recebido"

**Causa:** API não está rodando ou token está errado  
**Solução:**
```bash
# Verificar se API está rodando
curl http://localhost:5000/health

# Se não responde, inicie:
python3 api/google_drive_api_v2.py

# Verificar token
echo $WEBHOOK_TOKEN  # Ver token configurado
```

### "Pasta não encontrada"

**Causa:** ID inválido ou você não tem acesso  
**Solução:**
1. Abra a pasta no Drive
2. Copie o ID da URL corretamente
3. Teste com uma pasta que você criou

### "Documentos não compartilhados"

**Causa:** Service Account não foi adicionado  
**Solução:**
1. No Apps Script, execute `shareFolder(folderID)`
2. Aguarde 30 segundos
3. Tente validar novamente

---

## 🔐 Segurança

### Token do Webhook

- **Nunca** commite o token real no git
- Use variáveis de ambiente:

```python
# Na API
import os
WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN', 'token_padrao_para_testes')
```

```bash
# Ao iniciar
export WEBHOOK_TOKEN="seu_token_aqui"
python3 api/google_drive_api_v2.py
```

### Permissões do Service Account

A conta `ga4-api-access@site-2026.iam.gserviceaccount.com` terá:
- ✅ Editor em todas as pastas compartilhadas
- ❌ Não pode deletar documentos
- ❌ Não pode mudar proprietário

---

## 📊 Casos de Uso

### Caso 1: Sincronizar DADOS_INTELIGENCIA

```javascript
// Executar no Apps Script
syncFolderWithAPI("ID_DA_PASTA_DADOS_INTELIGENCIA");

// Resultado na API:
// ✅ 42 documentos sincronizados
// 🎯 40 acessíveis
// ❌ 2 inacessíveis (investigar permissões)
```

### Caso 2: Encontrar Todos os "OKRs"

```javascript
const results = searchDocuments("OKR");
const response = sendToAPI({
  action: 'found_documents',
  search_term: 'OKR',
  results: results
});
```

### Caso 3: Relatório Automático Diário

1. No Google Apps Script, crie um **trigger**:
   - Clique em ⏰ (Acionadores)
   - **"Criar um novo acionador"**
   - Função: `syncFolderWithAPI`
   - Evento: **"Cada dia"** às 08:00
   - Zona: Seu fuso horário

2. Todo dia às 8h, a sincronização roda automaticamente!

---

## 📚 Referências

- [Google Apps Script Documentation](https://developers.google.com/apps-script)
- [DriveApp Reference](https://developers.google.com/apps-script/reference/drive)
- [UrlFetchApp (para webhooks)](https://developers.google.com/apps-script/reference/url-fetch)

---

## ✅ Checklist de Implementação

- [ ] Script criado no Google Drive
- [ ] Credenciais configuradas
- [ ] Autorização concedida
- [ ] Teste básico funcionando
- [ ] API rodando em localhost:5000
- [ ] Token do webhook configurado
- [ ] Sincronização testada
- [ ] Relatório gerado
- [ ] Trigger diário criado (opcional)

---

## 🎯 Próximos Passos

1. ✅ Instalar e testar script
2. ⏳ Sincronizar DADOS_INTELIGENCIA
3. ⏳ Gerar relatório de validação
4. ⏳ Integrar com dashboard
5. ⏳ Configurar monitoramento automático

---

## 📞 Suporte

Se tiver dúvidas:

1. Verifique os Logs no Google Apps Script (Ctrl+Enter)
2. Teste cada função individualmente
3. Verifique se a API está rodando
4. Confirme que o token está correto
