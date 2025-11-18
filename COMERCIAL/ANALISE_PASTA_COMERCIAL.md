# 📊 Análise Pasta Comercial - Google Drive

**Data**: 18 de novembro de 2025  
**Folder ID**: `13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT`  
**URL**: https://drive.google.com/drive/folders/13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT

---

## 🎯 OBJETIVO

Mapear todos os documentos da pasta **COMERCIAL** e subpastas para:
- ✅ Identificar que tipos de documentos estão lá
- ✅ Estruturar conforme P6 Phase 2
- ✅ Sincronizar com repositório `docs`
- ✅ Criar automação via Google Drive API

---

## 📋 COMO FAZER A ANÁLISE

### Opção 1: Manual (Rápido - 10 min)

1. Abrir: https://drive.google.com/drive/folders/13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT
2. Ver todas as pastas e arquivos (scrollar)
3. Documentar estrutura abaixo

### Opção 2: Via Google Drive API (Automático)

```python
# Executar script Python para listar tudo
python3 analyze_drive.py --folder-id 13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT --recursive
```

---

## 📁 ESTRUTURA ESPERADA

Baseado em padrões de pasta Comercial, esperamos encontrar:

```
COMERCIAL/
├── 📊 Propostas/
│   ├── 2024/
│   ├── 2025/
│   └── Templates/
├── 📈 Apresentações/
│   ├── Pitch Deck
│   ├── Case Studies
│   └── Webinars
├── 📄 Contratos/
│   ├── Modelos
│   ├── Assinados
│   └── Em Negociação
├── 👥 Leads & Prospects/
│   ├── Base de Dados
│   ├── Segmentação
│   └── Pipeline
├── 📞 Contatos/
│   ├── Clientes
│   ├── Parceiros
│   └── Referências
├── 📈 Relatórios/
│   ├── Mensal
│   ├── Trimestral
│   └── Anual
└── 📝 Documentos Internos/
    ├── Processos
    ├── Guias
    └── Templates
```

---

## 🔍 INSTRUÇÕES PASSO-A-PASSO

### PASSO 1: Visualizar Estrutura

Abra: https://drive.google.com/drive/folders/13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT

**Anote**:
- [ ] Quantas pastas principais?
- [ ] Quantos arquivos na raiz?
- [ ] Tipos de arquivos (PDF, Sheets, Docs, etc)?
- [ ] Datas dos documentos?
- [ ] Quem é o criador/editor?

### PASSO 2: Mapear Subpastas

Para cada pasta principal:
1. Abrir pasta
2. Anotar nome e quantidade de itens
3. Verificar se tem subpastas
4. Se sim, repetir processo

### PASSO 3: Documentar Conteúdo

Para cada arquivo importante:
- [ ] Nome do arquivo
- [ ] Tipo (PDF, Spreadsheet, Document, etc)
- [ ] Tamanho aproximado
- [ ] Data de criação/modificação
- [ ] Descrição breve do conteúdo

---

## 📝 TEMPLATE DE ANÁLISE

Preencher este template após explorar a pasta:

```markdown
# Pasta Comercial - Conteúdo Documentado

## 📊 RESUMO EXECUTIVO

- **Total de Pastas**: [número]
- **Total de Arquivos**: [número]
- **Tamanho Total**: [GB/MB]
- **Último Update**: [data]
- **Principais Categorias**: [lista]

## 📁 ESTRUTURA COMPLETA

### 1️⃣ [Nome da Pasta Principal]
- Descrição: [breve]
- Arquivos: [quantidade]
- Subpastas: [quantidade]
- Conteúdo:
  - [ ] [Nome do arquivo 1]
  - [ ] [Nome do arquivo 2]

### 2️⃣ [Nome da Pasta Principal]
...

## 💡 INSIGHTS

- Padrões identificados: [...]
- Documentos críticos: [...]
- Gaps/Faltando: [...]
- Oportunidades de organização: [...]

## 🚀 PRÓXIMAS AÇÕES

- [ ] Sincronizar com repositório docs
- [ ] Criar automação de backup
- [ ] Estruturar conforme P6
- [ ] Compartilhar com time
```

---

## 🔐 ACESSO VIA API (Automático)

Se quiser fazer análise automática via Python:

### 1. Setup

```bash
# Instalar biblioteca
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Autenticar
gcloud auth application-default login
```

### 2. Script Python

```python
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_core.client_options import ClientOptions
from googleapiclient.discovery import build

def list_folder_recursive(folder_id, depth=0):
    """Lista todos os arquivos em uma pasta recursivamente"""
    
    service = build('drive', 'v3')
    indent = "  " * depth
    
    try:
        # Listar itens na pasta
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='files(id, name, mimeType, modifiedTime, size, webViewLink)',
            pageSize=1000
        ).execute()
        
        items = results.get('files', [])
        
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                print(f"{indent}📁 {item['name']}/")
                list_folder_recursive(item['id'], depth + 1)
            else:
                size = item.get('size', 0)
                size_str = f"{int(size) / 1024 / 1024:.1f}MB" if size else "N/A"
                print(f"{indent}📄 {item['name']} ({size_str})")
    
    except Exception as e:
        print(f"{indent}❌ Erro: {e}")

# Executar
list_folder_recursive('13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT')
```

### 3. Executar

```bash
python3 analyze_drive.py > comercial_structure.txt
```

---

## 🎯 O QUE PROCURAR

### 🔴 CRÍTICOS (Prioridade Alta)
- Propostas ativas
- Contratos assinados
- Pipeline de vendas
- Leads quentes

### 🟡 IMPORTANTES (Prioridade Média)
- Apresentações e case studies
- Relatórios de performance
- Templates e modelos
- Documentos de processo

### 🟢 ÚTEIS (Prioridade Baixa)
- Documentos antigos
- Arquivos de referência
- Histórico de projetos

---

## 📤 COMO SINCRONIZAR COM REPOSITÓRIO

Após análise, os documentos podem ser:

1. **Exportados para PDF** (se Docs/Sheets)
2. **Compactados em arquivo** (se muitos arquivos)
3. **Listados em markdown** (índice)
4. **Commitar no repositório docs**

Exemplo:
```bash
# Criar pasta no repositório
mkdir -p /DADOS_INTELIGENCIA/COMERCIAL/

# Copiar/exportar documentos
# Fazer commit
git add DADOS_INTELIGENCIA/COMERCIAL/
git commit -m "COMERCIAL: Importar documentos do Google Drive"
```

---

## 🚀 PRÓXIMOS PASSOS

1. **HOJE**: 
   - [ ] Abrir pasta Comercial
   - [ ] Explorar e anotar estrutura
   - [ ] Preencher template acima

2. **AMANHÃ**:
   - [ ] Criar script Python para análise automática
   - [ ] Exportar estrutura completa
   - [ ] Criar índice markdown

3. **PRÓX. SEMANA**:
   - [ ] Sincronizar documentos críticos com repositório
   - [ ] Configurar automação via Cloud Function
   - [ ] Compartilhar com time comercial

---

## 📞 INFORMAÇÕES ÚTEIS

- **Folder ID**: `13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT`
- **URL Direta**: https://drive.google.com/drive/folders/13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT
- **API Docs**: https://developers.google.com/drive/api/guides/folder-contents
- **Google Drive API Service**: Já pronto em `/contabilidade/functions/src/google-workspace-service.ts`

---

**Status**: 🟡 Aguardando análise manual ou automática  
**Data**: 18 de novembro de 2025  
**Próximo**: Preencher estrutura e documentar conteúdo
