#!/usr/bin/env python3
"""
🔐 Google Drive OAuth Setup - Autenticação com mkt@osp.com.br

Este script configura a autenticação OAuth 2.0 para usar a conta Google Drive
de mkt@osp.com.br sem expor a senha.

Uso:
    python3 api/google_drive_oauth_setup.py
"""

import os
import json
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials as OAuth2Credentials

# Scopes necessários para acessar Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class GoogleDriveOAuthSetup:
    """Configura autenticação OAuth para Google Drive"""
    
    def __init__(self, credentials_file="api/oauth_credentials.json", 
                 token_file="api/google_drive_token.pickle"):
        self.credentials_file = credentials_file
        self.token_file = token_file
    
    def create_oauth_credentials(self):
        """
        Cria arquivo de credenciais OAuth 2.0
        
        Este arquivo é gerado pelo Google Cloud Console e permite
        autenticar com a conta pessoal de mkt@osp.com.br
        
        Passos:
        1. Ir para: https://console.cloud.google.com/
        2. Criar OAuth 2.0 Client ID (Tipo: Desktop app)
        3. Baixar JSON
        4. Salvar como api/oauth_credentials.json
        """
        
        if os.path.exists(self.credentials_file):
            print(f"✅ Arquivo de credenciais encontrado: {self.credentials_file}")
            return True
        
        print("❌ Arquivo de credenciais OAuth não encontrado!")
        print("\nPassos para criar:")
        print("=" * 60)
        print("1. Vá para: https://console.cloud.google.com/apis/credentials")
        print("2. Clique em: '+ CRIAR CREDENCIAIS' → 'ID do cliente OAuth'")
        print("3. Tipo de aplicativo: 'Aplicativo de desktop'")
        print("4. Clique em 'Criar'")
        print("5. Clique no botão de download (⬇️)")
        print("6. Salve como: api/oauth_credentials.json")
        print("=" * 60)
        
        return False
    
    def get_authenticated_service(self):
        """
        Obtém serviço Google Drive autenticado
        
        Na primeira execução, abre o navegador para autorizar.
        Depois, usa token salvo (válido por ~1 hora).
        """
        
        # Tentar carregar token existente
        if os.path.exists(self.token_file):
            print(f"📦 Carregando token existente: {self.token_file}")
            with open(self.token_file, 'rb') as token:
                credentials = pickle.load(token)
            
            # Verificar se token está válido
            if credentials.expired and credentials.refresh_token:
                print("🔄 Atualizando token expirado...")
                credentials.refresh(Request())
                # Salvar token atualizado
                with open(self.token_file, 'wb') as token:
                    pickle.dump(credentials, token)
            
            print("✅ Token carregado com sucesso")
            return credentials
        
        # Primeira vez: precisa de credenciais OAuth
        if not self.create_oauth_credentials():
            return None
        
        print("\n🔐 Abrindo navegador para autorizar...")
        print("Você será solicitado a fazer login com mkt@osp.com.br")
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file,
                SCOPES
            )
            credentials = flow.run_local_server(port=8080)
            
            # Salvar token para reutilizar
            with open(self.token_file, 'wb') as token:
                pickle.dump(credentials, token)
            
            print(f"✅ Token salvo em: {self.token_file}")
            return credentials
        
        except Exception as e:
            print(f"❌ Erro ao autenticar: {e}")
            return None
    
    def test_connection(self, credentials):
        """Testa conexão com Google Drive"""
        try:
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            service = build('drive', 'v3', credentials=credentials)
            
            # Tentar listar primeiros 5 arquivos
            results = service.files().list(
                pageSize=5,
                fields="files(id, name, mimeType, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                print("\n✅ Conexão bem-sucedida!")
                print("\nPrimeiros 5 arquivos encontrados:")
                for file in files:
                    print(f"  📄 {file['name']} ({file['mimeType']})")
                return True
            else:
                print("⚠️ Nenhum arquivo encontrado no Drive")
                return True
        
        except Exception as e:
            print(f"❌ Erro ao testar conexão: {e}")
            return False
    
    def setup_step_by_step(self):
        """Guia passo a passo de configuração"""
        
        print("\n" + "=" * 70)
        print("🔐 Configuração do Google Drive OAuth - mkt@osp.com.br")
        print("=" * 70)
        
        # Passo 1: OAuth Credentials
        print("\n📋 PASSO 1: Criar Arquivo de Credenciais OAuth")
        print("-" * 70)
        
        if not os.path.exists(self.credentials_file):
            print("\n⚠️  Arquivo oauth_credentials.json não encontrado!")
            print("\nVocê precisa:")
            print("1. Ir para: https://console.cloud.google.com/apis/credentials")
            print("2. Criar novo OAuth 2.0 Client ID (tipo: Desktop)")
            print("3. Download JSON")
            print("4. Salvar como: api/oauth_credentials.json")
            print("5. Re-executar este script")
            return False
        
        print("✅ oauth_credentials.json encontrado")
        
        # Passo 2: Autenticar
        print("\n📋 PASSO 2: Autenticar com mkt@osp.com.br")
        print("-" * 70)
        
        credentials = self.get_authenticated_service()
        if not credentials:
            print("❌ Falha na autenticação")
            return False
        
        # Passo 3: Testar conexão
        print("\n📋 PASSO 3: Testar Conexão")
        print("-" * 70)
        
        if not self.test_connection(credentials):
            print("❌ Falha ao testar conexão")
            return False
        
        # Passo 4: Guardar credenciais para API
        print("\n📋 PASSO 4: Guardar Credenciais para API")
        print("-" * 70)
        
        # Criar arquivo de configuração com credenciais
        config = {
            "oauth_type": "user",
            "email": "mkt@osp.com.br",
            "token_file": self.token_file,
            "credentials_file": self.credentials_file,
            "status": "ready"
        }
        
        config_file = "api/oauth_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuração salva em: {config_file}")
        
        print("\n" + "=" * 70)
        print("✅ CONFIGURAÇÃO COMPLETA!")
        print("=" * 70)
        print(f"\n✅ Token OAuth salvo em: {self.token_file}")
        print(f"✅ Configuração salva em: {config_file}")
        print("\n🚀 Próximos passos:")
        print("1. Iniciar API com: python3 api/google_drive_validator_api.py")
        print("2. A API usará automaticamente suas credenciais OAuth")
        print("\n💡 Dica: O token é renovado automaticamente quando expira")
        
        return True

def main():
    """Função principal"""
    setup = GoogleDriveOAuthSetup()
    success = setup.setup_step_by_step()
    
    if not success:
        print("\n❌ Configuração não completada")
        print("\nResolva os problemas acima e tente novamente.")
        exit(1)
    else:
        print("\n✅ Tudo pronto para usar!")

if __name__ == "__main__":
    main()
