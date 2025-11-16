#!/usr/bin/env python3
"""
Extensão da API v2 - Endpoints para receber dados do Google Apps Script
Adicione este código ao arquivo google_drive_api_v2.py
"""

# Adicione estas rotas à sua app Flask (após os imports)

# ============================================================================
# ENDPOINTS - INTEGRAÇÃO COM GOOGLE WORKSPACE
# ============================================================================

WEBHOOK_TOKEN = "seu_token_seguro_aqui"  # Mesmo token do Apps Script

def verify_webhook_token(request):
    """Verifica token de segurança"""
    token = request.get_json().get('token')
    return token == WEBHOOK_TOKEN


@app.route('/api/v2/documents/sync', methods=['POST'])
def sync_documents():
    """Recebe documentos sincronizados do Google Workspace"""
    if not verify_webhook_token(request):
        return jsonify({'error': 'Token inválido'}), 401
    
    data = request.get_json()
    
    # Extrair documentos
    documents = data.get('documents', [])
    folder_name = data.get('folderName', 'Unknown')
    folder_id = data.get('folderId', '')
    
    logger.info(f"📥 Sincronizando {len(documents)} documentos de {folder_name}")
    
    # Armazenar em cache/BD
    cache_key = f"folder_{folder_id}"
    set_cached(cache_key, {
        'folder_name': folder_name,
        'documents': documents,
        'count': len(documents),
        'synced_at': datetime.now().isoformat()
    })
    
    # Processar cada documento
    results = []
    for doc in documents:
        doc_result = {
            'id': doc['id'],
            'name': doc['name'],
            'type': doc['type'],
            'url': doc['url'],
            'processed': True
        }
        
        # Tentar validar acesso
        access_info = check_document_access(doc['id'])
        doc_result['accessible'] = access_info['accessible']
        doc_result['access_info'] = access_info
        
        results.append(doc_result)
    
    response = {
        'status': 'success',
        'folder': folder_name,
        'total_documents': len(documents),
        'processed': len(results),
        'timestamp': datetime.now().isoformat(),
        'results': results
    }
    
    logger.info(f"✅ Sincronização concluída: {len(results)}/{len(documents)}")
    
    return jsonify(response), 200


@app.route('/api/v2/documents/found', methods=['POST'])
def documents_found():
    """Recebe notificação de documentos encontrados"""
    if not verify_webhook_token(request):
        return jsonify({'error': 'Token inválido'}), 401
    
    data = request.get_json()
    documents = data.get('documents', [])
    
    logger.info(f"📨 {len(documents)} documentos encontrados pelo Workspace")
    
    # Compilar lista de IDs
    doc_ids = [doc['id'] for doc in documents]
    
    # Validar todos
    validation_results = []
    accessible_count = 0
    
    for doc_id, doc_name in [(d['id'], d['name']) for d in documents]:
        access = check_document_access(doc_id)
        validation_results.append({
            'id': doc_id,
            'name': doc_name,
            'accessible': access['accessible'],
            'error': access.get('error')
        })
        if access['accessible']:
            accessible_count += 1
    
    # Salvar em cache
    cache_key = f"workspace_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    set_cached(cache_key, {
        'documents': documents,
        'validation': validation_results,
        'stats': {
            'total': len(documents),
            'accessible': accessible_count,
            'inaccessible': len(documents) - accessible_count
        }
    })
    
    return jsonify({
        'status': 'received',
        'total_documents': len(documents),
        'accessible': accessible_count,
        'validation_results': validation_results,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/v2/documents/list', methods=['GET'])
def list_cached_documents():
    """Lista documentos em cache sincronizados do Workspace"""
    cached_docs = {}
    
    for key in state.cache:
        if key.startswith('folder_') or key.startswith('workspace_'):
            cached_docs[key] = state.cache[key]
    
    return jsonify({
        'total_batches': len(cached_docs),
        'documents': cached_docs,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/v2/workspace/status', methods=['GET'])
def workspace_status():
    """Status de sincronização com Google Workspace"""
    return jsonify({
        'status': 'connected',
        'webhook_endpoint': '/api/v2/documents/sync',
        'last_sync': state.last_validated,
        'cached_batches': sum(1 for k in state.cache if 'folder_' in k or 'workspace_' in k),
        'timestamp': datetime.now().isoformat()
    }), 200


# ============================================================================
# ENDPOINTS - GERAÇÃO DE RELATÓRIOS
# ============================================================================

@app.route('/api/v2/reports/validation', methods=['GET'])
def validation_report():
    """Gera relatório de validação em HTML"""
    html = """
    <html>
    <head>
        <title>Relatório de Validação - Google Drive API</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            h1 { color: #1f2937; }
            .stats { display: flex; gap: 20px; margin: 20px 0; }
            .stat-box { 
                border: 1px solid #e5e7eb; 
                padding: 15px; 
                border-radius: 8px; 
                flex: 1;
                text-align: center;
            }
            .stat-value { font-size: 24px; font-weight: bold; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { text-align: left; padding: 12px; border-bottom: 1px solid #e5e7eb; }
            th { background-color: #f3f4f6; }
            .accessible { color: green; }
            .inaccessible { color: red; }
        </style>
    </head>
    <body>
        <h1>📊 Relatório de Validação - Google Drive API</h1>
        <p>Gerado em: {timestamp}</p>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{total}</div>
                <div>Total de Links</div>
            </div>
            <div class="stat-box">
                <div class="stat-value accessible">{accessible}</div>
                <div>Acessíveis</div>
            </div>
            <div class="stat-box">
                <div class="stat-value inaccessible">{inaccessible}</div>
                <div>Inacessíveis</div>
            </div>
        </div>
        
        <h2>Estatísticas por Hub</h2>
        <table>
            <tr>
                <th>Hub</th>
                <th>Acessíveis</th>
                <th>Inacessíveis</th>
                <th>Taxa (%)</th>
            </tr>
            {hub_stats}
        </table>
        
        <h2>Links Inacessíveis</h2>
        <table>
            <tr>
                <th>Nome</th>
                <th>Erro</th>
                <th>Hub</th>
            </tr>
            {inaccessible_links}
        </table>
    </body>
    </html>
    """
    
    # Calcular estatísticas
    total = state.validation_stats.get('total', 0)
    accessible = state.validation_stats.get('accessible', 0)
    inaccessible = total - accessible
    
    html = html.format(
        timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        total=total,
        accessible=accessible,
        inaccessible=inaccessible,
        hub_stats="",  # Preenchido dinamicamente
        inaccessible_links=""  # Preenchido dinamicamente
    )
    
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}


@app.route('/api/v2/reports/export', methods=['GET'])
def export_report():
    """Exporta relatório em formato CSV"""
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Nome', 'URL', 'Hub', 'Acessível', 'Tipo', 'Erro'])
    
    # Dados (vazio por enquanto, preencher com dados reais)
    
    response = app.response_class(
        response=output.getvalue(),
        status=200,
        mimetype='text/csv'
    )
    response.headers['Content-Disposition'] = 'attachment; filename="relatorio_validacao.csv"'
    
    return response
