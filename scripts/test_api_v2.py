#!/usr/bin/env python3
"""
Script de teste para API Google Drive v2
Encontra e valida links reais no Drive
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

# Adicionar API ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from google_drive_client_v2 import GoogleDriveClient


def find_google_drive_urls(directory: str = ".") -> dict:
    """Encontra URLs do Google Drive em arquivos markdown"""
    urls_by_hub = {
        'VENDAS': [],
        'CONHECIMENTO': [],
        'DADOS_INTELIGENCIA': [],
        'MARKETING': [],
        'OPERACOES': [],
        'OTHER': []
    }
    
    # Padrão de URL do Google Drive
    url_pattern = r'https://docs\.google\.com/[a-zA-Z/]+/d/[a-zA-Z0-9-_]+(?:/[a-zA-Z0-9\-_?=&]*)?'
    
    markdown_files = Path(directory).rglob('*.md')
    
    for file_path in markdown_files:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Encontrar todas as URLs
        for match in re.finditer(url_pattern, content):
            url = match.group(0)
            
            # Determinar qual hub
            hub = 'OTHER'
            if 'VENDAS' in str(file_path):
                hub = 'VENDAS'
            elif 'CONHECIMENTO' in str(file_path):
                hub = 'CONHECIMENTO'
            elif 'DADOS_INTELIGENCIA' in str(file_path):
                hub = 'DADOS_INTELIGENCIA'
            elif 'MARKETING' in str(file_path):
                hub = 'MARKETING'
            elif 'OPERACOES' in str(file_path):
                hub = 'OPERACOES'
            
            urls_by_hub[hub].append({
                'url': url,
                'file': str(file_path),
                'line': content[:content.find(url)].count('\n') + 1
            })
    
    return urls_by_hub


def extract_doc_id(url: str) -> str:
    """Extrai ID do documento da URL"""
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    return match.group(1) if match else None


def main():
    """Executa testes"""
    print("\n" + "="*70)
    print("🧪 Google Drive API v2 - Script de Teste")
    print("="*70)
    
    # 1. Conectar à API
    print("\n1️⃣ Conectando à API...")
    client = GoogleDriveClient()
    
    if not client.health_check():
        print("❌ API não está rodando!")
        print("\n   Para iniciar a API, execute em outro terminal:")
        print("   $ python3 api/google_drive_api_v2.py")
        return
    
    print("✅ API online")
    
    # 2. Inicializar serviço
    print("\n2️⃣ Inicializando serviço...")
    status = client.init_service()
    if 'error' in status:
        print(f"❌ Erro: {status['error']}")
        return
    
    print(f"   Auth: {status.get('auth_method')}")
    print(f"   Email: {status.get('authenticated_email')}")
    
    # 3. Encontrar URLs
    print("\n3️⃣ Procurando URLs nos arquivos...")
    urls_by_hub = find_google_drive_urls()
    
    total_urls = sum(len(urls) for urls in urls_by_hub.values())
    print(f"   Total encontrado: {total_urls} URLs")
    
    for hub, urls in urls_by_hub.items():
        if urls:
            print(f"   • {hub}: {len(urls)} URLs")
    
    if total_urls == 0:
        print("   ⚠️  Nenhuma URL encontrada!")
        return
    
    # 4. Validar URLs
    print("\n4️⃣ Validando URLs...")
    all_urls = [item['url'] for urls in urls_by_hub.values() for item in urls]
    
    # Validar em lotes (para não sobrecarregar)
    batch_size = 10
    all_results = []
    
    for i in range(0, len(all_urls), batch_size):
        batch = all_urls[i:i+batch_size]
        print(f"   Validando lote {i//batch_size + 1} de {(len(all_urls)-1)//batch_size + 1}...")
        
        result = client.validate_urls(batch)
        if 'error' in result:
            print(f"   ❌ Erro: {result['error']}")
            continue
        
        all_results.extend(result.get('results', []))
    
    # 5. Gerar relatório
    print("\n5️⃣ Gerando relatório...")
    
    accessible = [r for r in all_results if r.get('accessible')]
    inaccessible = [r for r in all_results if not r.get('accessible') and r.get('valid')]
    invalid_format = [r for r in all_results if not r.get('valid')]
    
    print(f"\n   📊 RESUMO")
    print(f"   {'─'*50}")
    print(f"   ✅ Acessíveis:       {len(accessible)}/{total_urls}")
    print(f"   ⚠️  Inacessíveis:     {len(inaccessible)}/{total_urls}")
    print(f"   ❌ Formato inválido: {len(invalid_format)}/{total_urls}")
    
    # 6. Detalhes por hub
    print(f"\n   📁 Por Hub:")
    print(f"   {'─'*50}")
    for hub, urls in urls_by_hub.items():
        if urls:
            hub_accessible = sum(1 for url_item in urls if any(r['url'] == url_item['url'] and r.get('accessible') for r in all_results))
            print(f"   {hub:20} {hub_accessible:2}/{len(urls):2} acessíveis")
    
    # 7. Salvar relatório
    report_file = "testing/GOOGLE_DRIVE_VALIDATION_V2.md"
    print(f"\n6️⃣ Salvando relatório em {report_file}...")
    
    os.makedirs("testing", exist_ok=True)
    
    with open(report_file, 'w') as f:
        f.write(f"# 📊 Google Drive Links - Relatório de Validação v2\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"**Total de URLs:** {total_urls}\n")
        f.write(f"**Acessíveis:** {len(accessible)}\n")
        f.write(f"**Inacessíveis:** {len(inaccessible)}\n")
        f.write(f"**Formato inválido:** {len(invalid_format)}\n\n")
        
        f.write("## 📈 Resumo por Hub\n\n")
        for hub, urls in urls_by_hub.items():
            if urls:
                hub_accessible = sum(1 for url_item in urls if any(r['url'] == url_item['url'] and r.get('accessible') for r in all_results))
                f.write(f"### {hub}\n")
                f.write(f"- Acessíveis: {hub_accessible}/{len(urls)}\n")
                f.write(f"- Taxa: {100*hub_accessible/len(urls):.1f}%\n\n")
        
        f.write("## ✅ URLs Acessíveis\n\n")
        for result in accessible:
            f.write(f"- [{result['access_info'].get('title', 'Sem título')}]({result['url']})\n")
            f.write(f"  - ID: {result['doc_id']}\n")
            f.write(f"  - Tipo: {result['access_info'].get('mime_type', 'Desconhecido')}\n\n")
        
        f.write("## ⚠️ URLs Inacessíveis\n\n")
        for result in inaccessible:
            f.write(f"- {result['url']}\n")
            f.write(f"  - ID: {result['doc_id']}\n")
            f.write(f"  - Erro: {result['access_info'].get('error', 'Desconhecido')}\n\n")
        
        f.write("## ❌ URLs com Formato Inválido\n\n")
        for result in invalid_format:
            f.write(f"- {result['url']}\n")
            f.write(f"  - Erro: {result.get('error', 'Formato inválido')}\n\n")
    
    print(f"✅ Relatório salvo!")
    
    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    main()
