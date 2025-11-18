#!/usr/bin/env python3
"""
Script para extrair metadados dos 19 links Google Drive não integrados
Lê títulos, tipos e informações relevantes dos documentos e planilhas
"""

import json
import subprocess
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import io
import sys

class LinkMetadataExtractor:
    """Extrator de metadados de links Google Drive"""
    
    # 19 links não integrados
    LINKS = {
        # COMERCIAL (17 links)
        "comercial": [
            {"id": "1Nd7lnrhIkNwY8Foqoi1fOMBqe46r9pU7e4iEnf-mxw0", "name": "Recurso Comercial 01"},
            {"id": "12svc2pU6uexH6jcfhKr9xfun8TRjMGxxJ5OPevzIY_U", "name": "Recurso Comercial 02"},
            {"id": "1O9mdc93o4evHyyzvtrrA9EWuygzUGsavsjCf8yEbDKk", "name": "Recurso Comercial 03"},
            {"id": "1xiSGb1brogSgI_zZdOau85rXkOj3B4z8KZFd7N7cu8o", "name": "Recurso Comercial 04"},
            {"id": "1LH8JcQftRWcKjxB4nCiKpSzOWE22E4DcS4XA84wQ6xI", "name": "Recurso Comercial 05"},
            {"id": "1ueqFBXFujBHBmJOjzKUiDn38qN6ipQeCoTNBsI8utgE", "name": "Recurso Comercial 06"},
            {"id": "1J5GIpqjC5xDOGTVVk4lNBmUWs4-UfF0MI56ncZMb2ec", "name": "Recurso Comercial 07"},
            {"id": "1TeuYivbHhWL9Zn0lziKbOQQI-yQZateoQULl7l0GI-g", "name": "Recurso Comercial 08"},
            {"id": "1otUt7ZBnTtXWCZXFzh_lXedJ1DOyMddeWejr7QrUSY0", "name": "Recurso Comercial 09"},
            {"id": "1tWwyvCSnyuTHj2DyNLW1nSdrh9gRNdpASWH2UQsIadQ", "name": "Recurso Comercial 10"},
            {"id": "173mFVUyLT0j9a8kbORCZVH-_n-ot9xl2bEhu8hN0qEE", "name": "Recurso Comercial 11"},
            {"id": "1xzv-x4LNDfYjFrphRJYM0zhlUJov0CBqO70o97wPqO8", "name": "Recurso Comercial 12"},
            {"id": "1i_xoVQcHtKp5wC6ZYSP_8EqcOobUdznmc9AYhip_jyg", "name": "Recurso Comercial 13"},
            {"id": "1SRkFoBV2mxWs32W6P-jpP7jLfw1nfD6Z534AJC0gats", "name": "Recurso Comercial 14"},
            {"id": "1RBgiL9Hodry7LEApDJNUWcVJWOeH8ltXltkuY3BpiF8", "name": "Recurso Comercial 15"},
            {"id": "1AAjr5hJvCW4uFS5or8z5dsAtfDyXTvzEhAXYSqFmMJM", "name": "Recurso Comercial 16"},
            {"id": "1AtBjqmDBrfipycUPuM12infjQMKZbpE9g2olArS29R0", "name": "Recurso Comercial 17"},
        ],
        # GESTÃO/Relatórios (2 links)
        "gestao": [
            {"id": "1CTjl6Y4VKB1NYjyVE-aVvds05cxFa5-go91Qk7FaFHo", "name": "Dados Consolidados"},
            {"id": "1dACqlBghNEJlkZvX8J9pSQ_4Sz-f-fryCe4xW5J9YSQ", "name": "Forecast"},
        ]
    }
    
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Autenticar com Firebase Service Account"""
        print("🔐 Autenticando com Firebase...")
        try:
            # Pegar config do Firebase
            result = subprocess.run(
                ['firebase', 'functions:config:get', '--project', 'osp-website-2026'],
                capture_output=True,
                text=True,
                cwd=Path.home() / 'osp-website' / 'contabilidade'
            )
            
            if result.returncode != 0:
                raise Exception("Firebase config não encontrado")
            
            # Parse JSON config
            config = json.loads(result.stdout)
            service_account_info = config['google']['workspace']['service_account_key']
            
            # Criar credenciais
            credentials = Credentials.from_service_account_info(
                service_account_info,
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            
            self.service = build('drive', 'v3', credentials=credentials)
            print("✅ Autenticação bem-sucedida!")
            
        except Exception as e:
            print(f"❌ Erro de autenticação: {e}")
            sys.exit(1)
    
    def get_file_metadata(self, file_id):
        """Obter metadados de um arquivo"""
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='name,mimeType,description,webViewLink,createdTime,modifiedTime,size,owners'
            ).execute()
            return file
        except Exception as e:
            print(f"⚠️  Erro ao obter metadados de {file_id}: {e}")
            return None
    
    def get_document_title(self, file_id):
        """Obter título de um Google Doc"""
        try:
            from googleapiclient.discovery import build as build_docs
            docs_service = build_docs('docs', 'v1', credentials=self.service._http.credentials)
            doc = docs_service.documents().get(documentId=file_id).execute()
            return doc.get('title', 'Sem título')
        except:
            return None
    
    def extract_metadata(self):
        """Extrair metadados de todos os 19 links"""
        print("\n📂 Extraindo metadados dos 19 links...\n")
        
        results = {
            "comercial": [],
            "gestao": []
        }
        
        # COMERCIAL
        print("📁 COMERCIAL (17 links)")
        for i, link in enumerate(self.LINKS["comercial"], 1):
            file_id = link["id"]
            print(f"  [{i:2d}/17] Lendo {link['name']}...", end=" ")
            
            metadata = self.get_file_metadata(file_id)
            if metadata:
                results["comercial"].append({
                    "id": file_id,
                    "nome": link["name"],
                    "titulo": metadata.get('name', 'Sem título'),
                    "tipo": metadata.get('mimeType', 'Unknown'),
                    "descricao": metadata.get('description', ''),
                    "link": metadata.get('webViewLink', f'https://docs.google.com/document/d/{file_id}'),
                    "tamanho": metadata.get('size', 0),
                    "modificado": metadata.get('modifiedTime', '')
                })
                print("✅")
            else:
                print("❌")
        
        # GESTÃO
        print("\n📊 GESTÃO/Relatórios (2 links)")
        for i, link in enumerate(self.LINKS["gestao"], 1):
            file_id = link["id"]
            print(f"  [{i:2d}/2] Lendo {link['name']}...", end=" ")
            
            metadata = self.get_file_metadata(file_id)
            if metadata:
                results["gestao"].append({
                    "id": file_id,
                    "nome": link["name"],
                    "titulo": metadata.get('name', 'Sem título'),
                    "tipo": metadata.get('mimeType', 'Unknown'),
                    "descricao": metadata.get('description', ''),
                    "link": metadata.get('webViewLink', f'https://docs.google.com/spreadsheets/d/{file_id}'),
                    "tamanho": metadata.get('size', 0),
                    "modificado": metadata.get('modifiedTime', '')
                })
                print("✅")
            else:
                print("❌")
        
        return results
    
    def generate_markdown(self, results):
        """Gerar markdown com os resultados"""
        
        md = """# 📚 Recursos Google Drive - Informações Extraídas

**Data de Extração**: 18 de novembro de 2025  
**Status**: ✅ Extraído e Catalogado  
**Total de recursos**: 19

---

## 📊 Resumo

- **COMERCIAL**: 17 recursos
- **GESTÃO/Relatórios**: 2 recursos
- **Total**: 19 links catalogados

---

## 📁 COMERCIAL (17 recursos)

"""
        
        for item in results.get("comercial", []):
            md += f"""### {item['nome']}

**Título Real**: {item['titulo']}  
**Tipo**: {item['tipo']}  
**Link**: [{item['titulo']}]({item['link']})  
**Modificado**: {item['modificado']}  
**Tamanho**: {item['tamanho']} bytes  

---

"""
        
        md += """## 📊 GESTÃO/Relatórios (2 recursos)

"""
        
        for item in results.get("gestao", []):
            md += f"""### {item['nome']}

**Título Real**: {item['titulo']}  
**Tipo**: {item['tipo']}  
**Link**: [{item['titulo']}]({item['link']})  
**Modificado**: {item['modificado']}  
**Tamanho**: {item['tamanho']} bytes  

---

"""
        
        md += """## 🔄 Próximos Passos

- [ ] Revisar títulos extraídos
- [ ] Categorizar recursos por tipo
- [ ] Integrar nas seções apropriadas
- [ ] Atualizar índices

---

**Gerado por**: extract_metadata_links.py  
**Timestamp**: 18 de novembro de 2025
"""
        
        return md

def main():
    extractor = LinkMetadataExtractor()
    results = extractor.extract_metadata()
    
    # Salvar JSON com resultados
    output_json = Path(__file__).parent / "link_metadata.json"
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ JSON salvo em: {output_json}")
    
    # Gerar e salvar markdown
    markdown = extractor.generate_markdown(results)
    output_md = Path(__file__).parent / "RECURSOS_EXTRAIDOS.md"
    with open(output_md, 'w') as f:
        f.write(markdown)
    
    print(f"✅ Markdown salvo em: {output_md}")
    print("\n✅ Extração concluída!")

if __name__ == "__main__":
    main()
