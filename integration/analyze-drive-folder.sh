#!/bin/bash

# Script para analisar pasta Comercial do Google Drive usando Google Drive API
# Folder ID: 13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT

# ⚠️ ANTES DE EXECUTAR:
# 1. Instalar Google CLI: brew install google-cloud-sdk
# 2. Autenticar: gcloud auth application-default login
# 3. Ter permissão de acesso à pasta

FOLDER_ID="13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT"

# Função para listar arquivos em uma pasta
list_folder_contents() {
  local folder_id=$1
  local indent=$2
  
  echo "$indent📁 Folder ID: $folder_id"
  
  # Usar Google Drive API via curl (requer token de acesso)
  # Para agora, documentar manualmente
}

# Instruções para acesso via API
cat << 'EOF'

🔐 Para acessar via API Google Drive:

1. Abrir Google Cloud Console: https://console.cloud.google.com/
2. Projeto: osp-website-2026
3. Ativar Google Drive API
4. Criar credencial de acesso
5. Executar query:

curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q='FOLDER_ID'+in+parents&pageSize=1000"

Alternativamente, usar o script Python incluído neste arquivo.

EOF
