#!/usr/bin/env python3
"""
Script para acessar e analisar pasta COMERCIAL via Google Drive API
Usa Service Account do Firebase para autenticação

Uso:
    python3 list_comercial_drive.py

⚠️ REQUER:
1. Arquivo service-account-key.json no mesmo diretório
   (Obter de: Google Cloud Console → Credentials → Service Account)
2. Service Account com delegação configurada no Google Admin Console
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Bibliotecas Google não encontradas!")
    print("Instale com: pip install google-auth google-api-python-client")
    sys.exit(1)

@dataclass
class FileInfo:
    """Informação sobre arquivo no Drive"""
    id: str
    name: str
    type: str  # 'folder' ou 'file'
    mime_type: str
    size: int  # em bytes
    modified_time: str
    created_time: str
    web_view_link: str
    path: str = ""

class GoogleDriveAnalyzer:
    """Analisador de pastas Google Drive com autenticação Service Account"""
    
    FOLDER_ID_COMERCIAL = "13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT"
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    
    def __init__(self, service_account_file: Optional[str] = None):
        """
        Inicializar analisador com Service Account
        
        Args:
            service_account_file: Caminho para arquivo service-account-key.json
        """
        self.service_account_file = service_account_file or self._find_service_account()
        self.service = None
        self.credentials = None
        self.files_list: List[FileInfo] = []
        
    def _find_service_account(self) -> Optional[str]:
        """Procurar arquivo service-account-key.json ou usar Firebase config"""
        # Procurar em vários locais
        paths = [
            Path.cwd() / "service-account-key.json",
            Path.home() / ".config/google/service-account-key.json",
            Path(__file__).parent / "service-account-key.json",
            Path(__file__).parent.parent / "contabilidade" / "service-account-key.json",
        ]
        
        for path in paths:
            if path.exists():
                print(f"✅ Service Account encontrado (arquivo): {path}")
                return str(path)
        
        # Tentar obter do Firebase config
        return "firebase:workspace"  # Marcador especial para usar Firebase
    
    def authenticate(self) -> bool:
        """
        Autenticar com Google Drive API usando Service Account
        Tenta: 1) Arquivo JSON local, 2) Firebase config
        
        Returns:
            True se autenticação bem-sucedida, False caso contrário
        """
        try:
            service_account_info = None
            source = None
            
            # Opção 1: Arquivo JSON local
            if self.service_account_file and self.service_account_file != "firebase:workspace":
                try:
                    with open(self.service_account_file) as f:
                        service_account_info = json.load(f)
                        source = f"arquivo ({self.service_account_file})"
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"⚠️  Não conseguiu ler arquivo local: {e}")
                    service_account_info = None
            
            # Opção 2: Firebase config
            if not service_account_info:
                service_account_info = self._get_firebase_config()
                if service_account_info:
                    source = "Firebase config (contabilidade)"
            
            # Se ainda não temos credenciais, erro
            if not service_account_info:
                print("❌ Arquivo service-account-key.json não encontrado!")
                print("❌ Firebase config também não encontrado!")
                print("\n📍 Locais onde procurei:")
                paths = [
                    "service-account-key.json (diretório atual)",
                    "~/.config/google/service-account-key.json",
                    "./service-account-key.json",
                    "../contabilidade/service-account-key.json",
                    "Firebase functions:config:get (contabilidade)",
                ]
                for path in paths:
                    print(f"   - {path}")
                
                print("\n💡 Para configurar:")
                print("1. Ir a: https://console.cloud.google.com/")
                print("2. Projeto: osp-website-2026")
                print("3. Credenciais → Criar Credencial → Conta de Serviço")
                print("4. Download JSON key")
                print("5. Salvar como: service-account-key.json")
                return False
            
            # Criar credenciais
            self.credentials = Credentials.from_service_account_info(
                service_account_info,
                scopes=self.SCOPES
            )
            
            # Construir serviço Google Drive
            self.service = build('drive', 'v3', credentials=self.credentials)
            
            print(f"✅ Autenticação bem-sucedida!")
            print(f"   Fonte: {source}")
            print(f"   Service Account: {service_account_info.get('client_email')}")
            print(f"   Projeto: {service_account_info.get('project_id')}")
            return True
            
        except Exception as e:
            print(f"❌ Erro de autenticação: {e}")
            return False
    
    def _get_firebase_config(self) -> Optional[dict]:
        """
        Obter credenciais do Firebase config do repositório contabilidade
        Executa: firebase functions:config:get --project osp-website-2026
        
        Returns:
            Dict com service account info ou None
        """
        import subprocess
        import json
        
        try:
            # Ir para diretório contabilidade
            contabilidade_path = Path(__file__).parent.parent.parent / "contabilidade"
            
            if not contabilidade_path.exists():
                print(f"⚠️  Diretório contabilidade não encontrado: {contabilidade_path}")
                return None
            
            # Executar firebase config get
            result = subprocess.run(
                ["firebase", "functions:config:get", "--project", "osp-website-2026"],
                cwd=str(contabilidade_path),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print(f"⚠️  Firebase CLI error: {result.stderr[:200]}")
                return None
            
            # Parse do JSON
            config = json.loads(result.stdout)
            
            # Extrair service account da config
            service_account = config.get('google', {}).get('workspace', {}).get('service_account_key')
            
            if service_account:
                if isinstance(service_account, dict):
                    return service_account
                elif isinstance(service_account, str):
                    return json.loads(service_account)
            
            return None
            
        except subprocess.TimeoutExpired:
            print("⚠️  Firebase config request timeout")
            return None
        except FileNotFoundError:
            print("⚠️  Firebase CLI não instalado")
            return None
        except Exception as e:
            print(f"⚠️  Erro ao obter Firebase config: {e}")
            return None
    
    def format_size(self, size_bytes: int) -> str:
        """Converter bytes para formato legível"""
        if not size_bytes:
            return "0B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f}TB"
    
    def get_mime_icon(self, mime_type: str) -> str:
        """Obter ícone baseado no MIME type"""
        mime_icons = {
            "application/vnd.google-apps.folder": "📁",
            "application/pdf": "📄",
            "application/vnd.google-apps.document": "📝",
            "application/vnd.google-apps.spreadsheet": "📊",
            "application/vnd.google-apps.presentation": "🎯",
            "text/csv": "📊",
            "application/vnd.ms-excel": "📊",
            "text/plain": "📝",
            "image/png": "🖼️",
            "image/jpeg": "🖼️",
            "application/zip": "📦",
        }
        return mime_icons.get(mime_type, "📋")
    
    def list_folder_recursive(self, folder_id: str, depth: int = 0, path: str = "") -> List[FileInfo]:
        """
        Listar arquivos em uma pasta recursivamente
        
        Args:
            folder_id: ID da pasta Google Drive
            depth: Profundidade de recursão (para indentação)
            path: Caminho acumulado
        
        Returns:
            Lista de FileInfo com todos os arquivos e pastas
        """
        if not self.service:
            print("❌ Não autenticado! Execute authenticate() primeiro.")
            return []
        
        try:
            # Query para listar itens da pasta
            query = f"'{folder_id}' in parents and trashed=false"
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, mimeType, modifiedTime, createdTime, size, webViewLink, parents)',
                pageSize=1000,
                orderBy='name'
            ).execute()
            
            items = results.get('files', [])
            indent = "  " * depth
            
            if not items:
                print(f"{indent}  (vazio)")
                return []
            
            for item in items:
                mime_type = item.get('mimeType', '')
                name = item.get('name', 'Sem nome')
                file_id = item.get('id', '')
                size = int(item.get('size', 0)) if item.get('size') else 0
                modified = item.get('modifiedTime', '')
                created = item.get('createdTime', '')
                web_link = item.get('webViewLink', '')
                
                is_folder = mime_type == 'application/vnd.google-apps.folder'
                icon = self.get_mime_icon(mime_type)
                type_str = "folder" if is_folder else "file"
                
                # Criar objeto FileInfo
                file_info = FileInfo(
                    id=file_id,
                    name=name,
                    type=type_str,
                    mime_type=mime_type,
                    size=size,
                    modified_time=modified,
                    created_time=created,
                    web_view_link=web_link,
                    path=f"{path}/{name}"
                )
                
                self.files_list.append(file_info)
                
                # Imprimir item
                size_str = self.format_size(size) if size else "N/A"
                print(f"{indent}{icon} {name} ({size_str})")
                
                # Se é pasta, recursivamente listar conteúdo
                if is_folder:
                    self.list_folder_recursive(file_id, depth + 1, f"{path}/{name}")
            
            return self.files_list
            
        except HttpError as e:
            print(f"❌ Erro HTTP {e.resp.status}: {e.content}")
            return []
        except Exception as e:
            print(f"❌ Erro ao listar pasta: {e}")
            return []
    
    def generate_markdown_report(self) -> str:
        """Gerar relatório em Markdown"""
        report = []
        
        # Cabeçalho
        report.append("# 📊 ANÁLISE PASTA COMERCIAL - GOOGLE DRIVE")
        report.append(f"\n**Data da Análise**: {datetime.now().strftime('%d de %B de %Y às %H:%M')}")
        report.append(f"**Folder ID**: `{self.FOLDER_ID_COMERCIAL}`")
        report.append(f"**Autenticação**: Service Account (Firebase)")
        report.append("\n---\n")
        
        # Resumo
        total_files = len([f for f in self.files_list if f.type == 'file'])
        total_folders = len([f for f in self.files_list if f.type == 'folder'])
        total_size = sum(f.size for f in self.files_list)
        
        report.append("## 📈 RESUMO EXECUTIVO\n")
        report.append(f"- **Total de Arquivos**: {total_files}")
        report.append(f"- **Total de Pastas**: {total_folders}")
        report.append(f"- **Tamanho Total**: {self.format_size(total_size)}")
        report.append(f"- **Total de Itens**: {len(self.files_list)}")
        report.append("\n")
        
        # Categorias por tipo
        report.append("## 📁 DISTRIBUIÇÃO POR TIPO\n")
        mime_types = {}
        for file_info in self.files_list:
            mime = file_info.mime_type
            if mime not in mime_types:
                mime_types[mime] = {'count': 0, 'size': 0}
            mime_types[mime]['count'] += 1
            mime_types[mime]['size'] += file_info.size
        
        for mime_type in sorted(mime_types.keys()):
            icon = self.get_mime_icon(mime_type)
            count = mime_types[mime_type]['count']
            size = self.format_size(mime_types[mime_type]['size'])
            report.append(f"- {icon} {mime_type}: {count} arquivo(s) ({size})")
        
        report.append("\n---\n")
        
        # Estrutura hierárquica
        report.append("## 🗂️ ESTRUTURA COMPLETA\n\n")
        report.append("```")
        report.append("COMERCIAL/")
        
        # Agrupar por pastas principais (depth 1)
        main_folders = [f for f in self.files_list if f.type == 'folder' and f.path.count('/') == 1]
        
        for folder in sorted(main_folders, key=lambda x: x.name):
            report.append(f"├── {folder.name}/")
            
            # Arquivos nesta pasta
            files_in_folder = [
                f for f in self.files_list 
                if f.path.startswith(f"{folder.path}/") and f.type == 'file' and f.path.count('/') == 2
            ]
            
            for file_info in sorted(files_in_folder, key=lambda x: x.name):
                icon = self.get_mime_icon(file_info.mime_type)
                size = self.format_size(file_info.size)
                report.append(f"│   ├── {icon} {file_info.name} ({size})")
            
            # Subpastas
            subfolders = [
                f for f in self.files_list 
                if f.path.startswith(f"{folder.path}/") and f.type == 'folder' and f.path.count('/') == 2
            ]
            
            for subfolder in sorted(subfolders, key=lambda x: x.name):
                report.append(f"│   ├── 📁 {subfolder.name}/")
        
        report.append("```\n")
        
        # Arquivos na raiz
        root_files = [f for f in self.files_list if f.path.count('/') == 1 and f.type == 'file']
        if root_files:
            report.append("## 📄 ARQUIVOS NA RAIZ\n")
            for file_info in sorted(root_files, key=lambda x: x.name):
                icon = self.get_mime_icon(file_info.mime_type)
                size = self.format_size(file_info.size)
                modified = file_info.modified_time.split('T')[0] if file_info.modified_time else 'N/A'
                report.append(f"- {icon} **{file_info.name}** ({size}) - Modificado: {modified}")
                report.append(f"  - [Abrir no Drive]({file_info.web_view_link})")
            report.append("\n")
        
        # Principais pastas
        report.append("## 📂 PASTAS PRINCIPAIS\n")
        for folder in sorted(main_folders, key=lambda x: x.name):
            files_count = len([f for f in self.files_list if f.path.startswith(f"{folder.path}/") and f.type == 'file'])
            subfolders_count = len([f for f in self.files_list if f.path.startswith(f"{folder.path}/") and f.type == 'folder' and f.path.count('/') > 1])
            
            report.append(f"\n### 📁 {folder.name}\n")
            report.append(f"- Arquivos: {files_count}")
            report.append(f"- Subpastas: {subfolders_count}")
            report.append(f"- [Abrir no Drive]({folder.web_view_link})")
        
        return "\n".join(report)

def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🔍 ANALISADOR PASTA COMERCIAL - GOOGLE DRIVE API")
    print("="*60 + "\n")
    
    # Criar analisador
    analyzer = GoogleDriveAnalyzer()
    
    # Autenticar
    print("🔐 Autenticando...")
    if not analyzer.authenticate():
        print("\n❌ Falha na autenticação. Não foi possível continuar.")
        return 1
    
    # Listar conteúdo
    print(f"\n📂 Listando pasta COMERCIAL ({analyzer.FOLDER_ID_COMERCIAL})...\n")
    
    files = analyzer.list_folder_recursive(analyzer.FOLDER_ID_COMERCIAL)
    
    print(f"\n✅ Análise concluída!")
    print(f"   Total de itens: {len(files)}")
    
    # Gerar relatório
    print("\n📊 Gerando relatório Markdown...")
    report = analyzer.generate_markdown_report()
    
    # Salvar para arquivo
    output_file = Path(__file__).parent / "COMERCIAL_STRUCTURE.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Relatório salvo em: {output_file}")
    
    # Mostrar primeira parte do relatório
    print("\n" + "="*60)
    print(report[:1000] + "\n...")
    print("="*60 + "\n")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
