/**
 * Google Apps Script - Integração OSP Docs
 * 
 * Este script roda dentro do Google Workspace e:
 * 1. Compartilha documentos com a Service Account
 * 2. Lista documentos e seus IDs reais
 * 3. Envia dados para nossa API Python
 * 
 * Instalação:
 * 1. Abra Google Drive
 * 2. Clique em "+ Novo" > "Google Apps Script"
 * 3. Cole este código
 * 4. Execute a função setup()
 */

// Configuração
const SERVICE_ACCOUNT_EMAIL = "ga4-api-access@site-2026.iam.gserviceaccount.com";
const API_URL = "http://localhost:5000/api/v2"; // Sua API Python
const WEBHOOK_TOKEN = "seu_token_seguro_aqui"; // Para validar requisições

// ============================================================================
// COMPARTILHAMENTO DE DOCUMENTOS
// ============================================================================

/**
 * Compartilha um documento com a Service Account
 * @param {String} fileId - ID do arquivo
 * @param {String} role - 'viewer', 'commenter' ou 'editor'
 */
function shareWithServiceAccount(fileId, role = 'editor') {
  try {
    const file = DriveApp.getFileById(fileId);
    file.addEditor(SERVICE_ACCOUNT_EMAIL);
    
    Logger.log(`✅ Compartilhado: ${file.getName()}`);
    return {
      success: true,
      fileName: file.getName(),
      fileId: fileId,
      role: role
    };
  } catch (e) {
    Logger.log(`❌ Erro ao compartilhar: ${e}`);
    return {
      success: false,
      fileId: fileId,
      error: e.toString()
    };
  }
}

/**
 * Compartilha uma pasta inteira com a Service Account
 * @param {String} folderId - ID da pasta
 */
function shareFolder(folderId) {
  try {
    const folder = DriveApp.getFolderById(folderId);
    const files = folder.getFiles();
    const results = [];
    
    Logger.log(`📁 Compartilhando pasta: ${folder.getName()}`);
    
    while (files.hasNext()) {
      const file = files.next();
      results.push(shareWithServiceAccount(file.getId(), 'editor'));
    }
    
    Logger.log(`✅ ${results.length} documentos compartilhados`);
    return results;
  } catch (e) {
    Logger.log(`❌ Erro ao compartilhar pasta: ${e}`);
    return { error: e.toString() };
  }
}

/**
 * Compartilha múltiplos documentos
 * @param {Array} fileIds - Array de IDs de arquivo
 */
function shareMultiple(fileIds) {
  const results = [];
  for (let fileId of fileIds) {
    results.push(shareWithServiceAccount(fileId, 'editor'));
  }
  return results;
}

// ============================================================================
// LISTAGEM DE DOCUMENTOS
// ============================================================================

/**
 * Lista todos os documentos de uma pasta com seus IDs
 * @param {String} folderId - ID da pasta
 * @returns {Array} Lista de documentos com metadados
 */
function listFolderDocuments(folderId) {
  try {
    const folder = DriveApp.getFolderById(folderId);
    const files = folder.getFiles();
    const documents = [];
    
    while (files.hasNext()) {
      const file = files.next();
      const mimeType = file.getMimeType();
      
      documents.push({
        name: file.getName(),
        id: file.getId(),
        type: getMimeTypeLabel(mimeType),
        mimeType: mimeType,
        owner: file.getOwner().getEmail(),
        url: file.getUrl(),
        lastModified: file.getLastUpdated(),
        shared: file.isSharedWithMe()
      });
    }
    
    return documents;
  } catch (e) {
    Logger.log(`❌ Erro ao listar pasta: ${e}`);
    return { error: e.toString() };
  }
}

/**
 * Lista documentos recursivamente (incluindo subpastas)
 * @param {String} folderId - ID da pasta
 * @param {Array} results - Acumulador (não passar)
 * @returns {Array} Lista completa de documentos
 */
function listFolderDocumentsRecursive(folderId, results = []) {
  try {
    const folder = DriveApp.getFolderById(folderId);
    const files = folder.getFiles();
    const subFolders = folder.getFolders();
    
    // Arquivos
    while (files.hasNext()) {
      const file = files.next();
      results.push({
        name: file.getName(),
        id: file.getId(),
        type: getMimeTypeLabel(file.getMimeType()),
        mimeType: file.getMimeType(),
        owner: file.getOwner().getEmail(),
        url: file.getUrl(),
        lastModified: file.getLastUpdated(),
        folderPath: folder.getName()
      });
    }
    
    // Subpastas (recursivo)
    while (subFolders.hasNext()) {
      const subFolder = subFolders.next();
      listFolderDocumentsRecursive(subFolder.getId(), results);
    }
    
    return results;
  } catch (e) {
    Logger.log(`❌ Erro ao listar recursivo: ${e}`);
    return { error: e.toString() };
  }
}

/**
 * Busca documentos por nome
 * @param {String} searchTerm - Termo de busca
 * @returns {Array} Documentos encontrados
 */
function searchDocuments(searchTerm) {
  try {
    const files = DriveApp.getFilesByName(searchTerm);
    const results = [];
    
    while (files.hasNext()) {
      const file = files.next();
      results.push({
        name: file.getName(),
        id: file.getId(),
        type: getMimeTypeLabel(file.getMimeType()),
        url: file.getUrl()
      });
    }
    
    return results;
  } catch (e) {
    Logger.log(`❌ Erro ao buscar: ${e}`);
    return { error: e.toString() };
  }
}

// ============================================================================
// COMUNICAÇÃO COM API
// ============================================================================

/**
 * Envia dados para a API Python
 * @param {Object} data - Dados a enviar
 * @param {String} endpoint - Endpoint da API
 */
function sendToAPI(data, endpoint = '/documents/found') {
  try {
    const options = {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify({
        ...data,
        token: WEBHOOK_TOKEN,
        timestamp: new Date().toISOString()
      }),
      muteHttpExceptions: true
    };
    
    const response = UrlFetchApp.fetch(API_URL + endpoint, options);
    const result = JSON.parse(response.getContentText());
    
    Logger.log(`📤 API Response: ${response.getResponseCode()}`);
    return result;
  } catch (e) {
    Logger.log(`❌ Erro ao enviar para API: ${e}`);
    return { error: e.toString() };
  }
}

/**
 * Sincroniza documentos com a API
 * @param {String} folderId - ID da pasta para sincronizar
 */
function syncFolderWithAPI(folderId) {
  Logger.log(`🔄 Sincronizando pasta com API...`);
  
  // Listar documentos
  const documents = listFolderDocumentsRecursive(folderId);
  
  if (documents.error) {
    Logger.log(`❌ Erro: ${documents.error}`);
    return documents;
  }
  
  Logger.log(`📊 ${documents.length} documentos encontrados`);
  
  // Enviar para API
  const response = sendToAPI({
    action: 'sync_documents',
    folderName: DriveApp.getFolderById(folderId).getName(),
    folderId: folderId,
    documents: documents,
    count: documents.length
  }, '/documents/sync');
  
  return {
    success: true,
    documentsFound: documents.length,
    apiResponse: response
  };
}

// ============================================================================
// UTILITÁRIOS
// ============================================================================

/**
 * Converte MIME type em label legível
 */
function getMimeTypeLabel(mimeType) {
  const labels = {
    'application/vnd.google-apps.spreadsheet': 'Planilha',
    'application/vnd.google-apps.document': 'Documento',
    'application/vnd.google-apps.presentation': 'Apresentação',
    'application/vnd.google-apps.form': 'Formulário',
    'application/vnd.google-apps.folder': 'Pasta',
    'application/pdf': 'PDF',
    'text/plain': 'Texto'
  };
  
  return labels[mimeType] || mimeType;
}

/**
 * Cria um relatório e o envia por email
 */
function generateAndEmailReport(folderId) {
  const documents = listFolderDocumentsRecursive(folderId);
  const folder = DriveApp.getFolderById(folderId);
  
  let html = `
    <h1>📊 Relatório de Documentos - ${folder.getName()}</h1>
    <p><strong>Data:</strong> ${new Date().toLocaleString()}</p>
    <p><strong>Total de documentos:</strong> ${documents.length}</p>
    
    <h2>Documentos Encontrados:</h2>
    <table border="1" cellpadding="10">
      <tr>
        <th>Nome</th>
        <th>Tipo</th>
        <th>ID</th>
        <th>Proprietário</th>
        <th>Última modificação</th>
      </tr>
  `;
  
  for (let doc of documents) {
    html += `
      <tr>
        <td><a href="${doc.url}">${doc.name}</a></td>
        <td>${doc.type}</td>
        <td><code>${doc.id}</code></td>
        <td>${doc.owner}</td>
        <td>${doc.lastModified}</td>
      </tr>
    `;
  }
  
  html += `</table>`;
  
  // Enviar email
  const userEmail = Session.getActiveUser().getEmail();
  GmailApp.sendEmail(userEmail, `Relatório: ${folder.getName()}`, '', {
    htmlBody: html
  });
  
  Logger.log(`📧 Relatório enviado para ${userEmail}`);
}

// ============================================================================
// SETUP & TESTES
// ============================================================================

/**
 * Função de setup - executar uma vez
 */
function setup() {
  Logger.log("✅ Script OSP Docs configurado!");
  Logger.log(`   Service Account: ${SERVICE_ACCOUNT_EMAIL}`);
  Logger.log(`   API URL: ${API_URL}`);
  Logger.log("");
  Logger.log("Funções disponíveis:");
  Logger.log("  1. shareWithServiceAccount(fileId)");
  Logger.log("  2. shareFolder(folderId)");
  Logger.log("  3. listFolderDocuments(folderId)");
  Logger.log("  4. listFolderDocumentsRecursive(folderId)");
  Logger.log("  5. searchDocuments(searchTerm)");
  Logger.log("  6. syncFolderWithAPI(folderId)");
  Logger.log("  7. generateAndEmailReport(folderId)");
  Logger.log("");
  Logger.log("Exemplos:");
  Logger.log("  shareFolder('sua_folder_id')");
  Logger.log("  syncFolderWithAPI('sua_folder_id')");
}

/**
 * Teste: listar documentos de uma pasta
 */
function testListDocuments() {
  // Substitua pela ID da sua pasta
  const folderId = "1234567890"; // Coloque a ID real aqui
  const docs = listFolderDocumentsRecursive(folderId);
  
  Logger.log("📊 Documentos encontrados:");
  for (let doc of docs) {
    Logger.log(`  • ${doc.name} (${doc.type})`);
    Logger.log(`    ID: ${doc.id}`);
  }
}

/**
 * Teste: compartilhar com Service Account
 */
function testShare() {
  // Substitua pela ID do arquivo
  const fileId = "1234567890"; // Coloque a ID real aqui
  const result = shareWithServiceAccount(fileId, 'editor');
  Logger.log(JSON.stringify(result, null, 2));
}
