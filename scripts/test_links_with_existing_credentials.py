#!/usr/bin/env python3
"""
Google Drive Links Validator - Using Existing GA4 Service Account

Testa todos os 64 links do Google Drive usando as credenciais já configuradas.

Usage:
    python3 scripts/test_links_with_existing_credentials.py
"""

import os
import json
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import re

# Credenciais existentes
CREDENTIALS_PATH = os.path.expanduser("~/.credentials/ga4-api-key.json")

# Hubs com links
HUBS = {
    "VENDAS": "VENDAS/templates/README.md",
    "CONHECIMENTO": "CONHECIMENTO/solucoes/INDEX.md",
    "DADOS_INTELIGENCIA": "DADOS_INTELIGENCIA/dashboards/README.md",
    "MARKETING": "MARKETING/campanhas/README.md",
}


def load_credentials():
    """Carrega credenciais do GA4 Service Account"""
    try:
        credentials = Credentials.from_service_account_file(
            CREDENTIALS_PATH,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        print(f"✅ Credenciais carregadas: {credentials.service_account_email}")
        return credentials
    except Exception as e:
        print(f"❌ Erro ao carregar credenciais: {e}")
        return None


def build_drive_service(credentials):
    """Cria serviço Google Drive"""
    try:
        service = build('drive', 'v3', credentials=credentials)
        print("✅ Google Drive service inicializado")
        return service
    except Exception as e:
        print(f"❌ Erro ao inicializar Drive service: {e}")
        return None


def extract_doc_id(url):
    """Extrai Document ID da URL do Google Drive"""
    patterns = [
        r'/d/([a-zA-Z0-9-_]+)',
        r'id=([a-zA-Z0-9-_]+)',
        r'key=([a-zA-Z0-9-_]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def check_document_access(service, doc_id):
    """Verifica se documento é acessível via API"""
    try:
        file_metadata = service.files().get(
            fileId=doc_id,
            fields='id, name, mimeType, owners, lastModifiedTime, webViewLink, permissions'
        ).execute()
        
        permissions = file_metadata.get('permissions', [])
        shared_with_osp = any(
            p.get('emailAddress', '').endswith('@osp-group') 
            for p in permissions
        )
        
        public = any(
            p.get('type') == 'anyone'
            for p in permissions
        )
        
        owners = file_metadata.get('owners', [])
        owner_email = owners[0].get('emailAddress', 'unknown') if owners else 'unknown'
        
        return {
            "accessible": True,
            "title": file_metadata.get('name'),
            "mime_type": file_metadata.get('mimeType'),
            "owner": owner_email,
            "shared_with_osp_group": shared_with_osp,
            "public": public,
            "last_modified": file_metadata.get('lastModifiedTime'),
            "web_view_link": file_metadata.get('webViewLink'),
            "error": None
        }
    
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            error = "Document not found (may be deleted)"
        elif "403" in error_msg or "permission denied" in error_msg.lower():
            error = "Access denied (not shared with this account)"
        else:
            error = error_msg
        
        return {
            "accessible": False,
            "error": error,
            "title": None,
            "mime_type": None,
            "owner": None,
            "shared_with_osp_group": False,
            "public": False,
            "last_modified": None,
            "web_view_link": None
        }


def load_hub_links():
    """Carrega links dos arquivos markdown"""
    
    links_by_hub = {
        "VENDAS": [],
        "CONHECIMENTO": [],
        "DADOS_INTELIGENCIA": [],
        "MARKETING": []
    }
    
    link_pattern = r'\[([^\]]+)\]\((https://docs\.google\.com/[^)]+)\)'
    
    for hub_name, file_path in HUBS.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for match in re.finditer(link_pattern, content):
                    text = match.group(1)
                    url = match.group(2)
                    doc_id = extract_doc_id(url)
                    
                    if doc_id:
                        links_by_hub[hub_name].append({
                            "text": text,
                            "url": url,
                            "doc_id": doc_id,
                            "hub": hub_name
                        })
            except Exception as e:
                print(f"⚠️  Erro ao ler {file_path}: {e}")
    
    return links_by_hub


def validate_all_links(service):
    """Valida todos os links"""
    
    print("\n🔍 Carregando links dos hubs...")
    links_by_hub = load_hub_links()
    
    total_links = sum(len(links) for links in links_by_hub.values())
    print(f"✅ {total_links} links encontrados")
    
    print("\n📊 Validando links...")
    print("=" * 80)
    
    results = {
        "total": total_links,
        "accessible": 0,
        "inaccessible": 0,
        "by_hub": {},
        "errors": []
    }
    
    for hub_name, links in links_by_hub.items():
        print(f"\n📁 {hub_name}")
        print("-" * 80)
        
        hub_results = {
            "total": len(links),
            "accessible": 0,
            "inaccessible": 0,
            "links": []
        }
        
        for idx, link in enumerate(links, 1):
            validation = check_document_access(service, link['doc_id'])
            
            if validation['accessible']:
                status = "✅"
                hub_results['accessible'] += 1
                results['accessible'] += 1
            else:
                status = "❌"
                hub_results['inaccessible'] += 1
                results['inaccessible'] += 1
                results['errors'].append({
                    "text": link['text'],
                    "hub": hub_name,
                    "error": validation['error']
                })
            
            link['validation'] = validation
            link['status'] = status
            hub_results['links'].append(link)
            
            print(f"  {status} [{idx}/{len(links)}] {link['text'][:50]}")
            if not validation['accessible']:
                print(f"     ⚠️  {validation['error']}")
        
        results['by_hub'][hub_name] = hub_results
    
    return results


def print_summary(results):
    """Imprime resumo de resultados"""
    
    print("\n" + "=" * 80)
    print("📊 RESUMO DE VALIDAÇÃO")
    print("=" * 80)
    
    print(f"\n✅ Acessíveis: {results['accessible']}/{results['total']}")
    print(f"❌ Inacessíveis: {results['inaccessible']}/{results['total']}")
    
    if results['total'] > 0:
        pct = round(100 * results['accessible'] / results['total'], 1)
        print(f"📈 Taxa de acesso: {pct}%")
    
    print("\n📁 Por Hub:")
    for hub_name, hub_results in results['by_hub'].items():
        accessible = hub_results['accessible']
        total = hub_results['total']
        status = "✅" if hub_results['inaccessible'] == 0 else "⚠️"
        print(f"  {status} {hub_name}: {accessible}/{total}")
    
    if results['errors']:
        print("\n⚠️  Links com Problemas:")
        for error in results['errors']:
            print(f"  ❌ {error['text']} ({error['hub']})")
            print(f"     {error['error']}")
    
    print("\n" + "=" * 80)


def save_report(results):
    """Salva relatório em Markdown"""
    
    report_path = "testing/GOOGLE_DRIVE_VALIDATION_EXISTING_CREDENTIALS.md"
    
    content = f"""# 📊 Google Drive Links Validation Report

**Data**: {Path('').resolve().name}  
**Método**: Usando credenciais GA4 Service Account  
**Credencial**: ga4-api-access@site-2026.iam.gserviceaccount.com

---

## 📈 Resumo

| Métrica | Valor |
|---------|-------|
| Total de Links | {results['total']} |
| Acessíveis ✅ | {results['accessible']} |
| Inacessíveis ❌ | {results['inaccessible']} |
| Taxa de Acesso | {round(100 * results['accessible'] / results['total'], 1)}% |

---

## 📁 Por Hub

"""
    
    for hub_name, hub_results in results['by_hub'].items():
        content += f"\n### {hub_name}\n\n"
        content += f"- **Total**: {hub_results['total']}\n"
        content += f"- **Acessíveis**: {hub_results['accessible']}\n"
        content += f"- **Inacessíveis**: {hub_results['inaccessible']}\n"
        
        if hub_results['links']:
            content += "\n**Links:**\n"
            for link in hub_results['links']:
                status = link['status']
                text = link['text']
                content += f"- {status} {text}\n"
    
    if results['errors']:
        content += "\n---\n\n## ⚠️ Links com Problemas\n\n"
        for error in results['errors']:
            content += f"- **{error['text']}** ({error['hub']})\n"
            content += f"  - {error['error']}\n\n"
    
    content += "\n---\n\n## ℹ️ Notas\n\n"
    content += "- Validação realizada usando Google Drive API\n"
    content += "- Credencial: Service Account (GA4)\n"
    content += "- Projeto: site-2026\n"
    
    # Criar diretório se não existir
    os.makedirs("testing", exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Relatório salvo em: {report_path}")


def main():
    """Função principal"""
    
    print("\n" + "=" * 80)
    print("🚀 Google Drive Links Validator")
    print("   Usando credenciais GA4 Service Account")
    print("=" * 80)
    
    # Carregar credenciais
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"\n❌ Arquivo de credenciais não encontrado: {CREDENTIALS_PATH}")
        return
    
    credentials = load_credentials()
    if not credentials:
        return
    
    # Construir serviço
    service = build_drive_service(credentials)
    if not service:
        return
    
    # Validar links
    results = validate_all_links(service)
    
    # Exibir resumo
    print_summary(results)
    
    # Salvar relatório
    save_report(results)
    
    print("\n✅ Validação completa!")


if __name__ == "__main__":
    main()
