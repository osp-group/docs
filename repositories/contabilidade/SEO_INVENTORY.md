# 🔍 SEO Inventory - OSP Contabilidade WordPress Migration

**Site Atual:** www.ospcontabilidade.com.br (WordPress)  
**Site Novo:** osp-website-2026.web.app → osp.com.br (React/Firebase)  
**Data:** 16 de Outubro de 2025

---

## 📊 PASSO 1: Exportar Dados do Google Analytics 4

### 1.1 Páginas Mais Visitadas (Últimos 6 Meses)

**Como fazer:**
1. Acesse: https://analytics.google.com
2. Selecione a propriedade OSP Contabilidade
3. Vá em: **Relatórios** → **Engajamento** → **Páginas e telas**
4. Configure o período: **Últimos 6 meses**
5. Clique em **Exportar** (canto superior direito) → **Google Sheets** ou **CSV**

**Colunas importantes:**
- Nome da página (URL)
- Visualizações de página
- Usuários
- Taxa de engajamento
- Conversões (se configurado)

### 1.2 Fontes de Tráfego

**Relatório:** **Aquisição** → **Aquisição de tráfego**
- Origem / Mídia
- Usuários
- Sessões
- Conversões

### 1.3 Eventos de Conversão

**Relatório:** **Engajamento** → **Conversões**
- Quais eventos estão configurados? (ex: form_submit, contact, lead)
- Páginas que mais convertem

---

## 📊 PASSO 2: Exportar Dados do Google Search Console

### 2.1 Páginas com Melhor Performance Orgânica

**Como fazer:**
1. Acesse: https://search.google.com/search-console
2. Selecione: www.ospcontabilidade.com.br
3. Vá em: **Desempenho** → **Páginas**
4. Configure: **Últimos 6 meses**
5. Clique em **Exportar** → **Google Sheets**

**Métricas importantes:**
- URL
- Cliques totais
- Impressões totais
- CTR médio
- Posição média

### 2.2 Consultas (Keywords) que Geram Tráfego

**Relatório:** **Desempenho** → **Consultas**
- Palavras-chave que trazem visitantes
- Posição no Google
- CTR

---

## 🗺️ PASSO 3: Mapear Todas as URLs do WordPress

### Opção A: Plugin WordPress (Mais Fácil)

**Instale um destes plugins:**
- **Export All URLs** (gratuito)
- **Simple URLs List** (gratuito)
- **Screaming Frog SEO Spider** (ferramenta externa, versão gratuita até 500 URLs)

**Passos:**
1. WordPress Admin → Plugins → Adicionar novo
2. Buscar "Export All URLs"
3. Instalar e ativar
4. Ferramentas → Export URLs
5. Exportar lista completa em CSV

### Opção B: Screaming Frog (Recomendado para análise completa)

**Download:** https://www.screamingfrogseosuite.com/

**Como usar:**
1. Abrir Screaming Frog
2. Modo: **Spider**
3. Digite: `https://www.ospcontabilidade.com.br`
4. Clique **Start**
5. Aguarde o crawl completo
6. Exportar: **Internal → All**

**Dados que você terá:**
- Todas as URLs do site
- Status Code (200, 301, 404)
- Títulos de página (Title Tags)
- Meta Descriptions
- H1, H2
- Word Count
- Links internos/externos

---

## 📋 PASSO 4: Criar Planilha Master de Migração

**Abra Google Sheets e crie estas colunas:**

| URL Antiga (WordPress) | URL Nova (React) | Tipo de Página | Tráfego Mensal | Conversões | Prioridade | Status 301 | Notas |
|------------------------|------------------|----------------|----------------|------------|------------|------------|-------|
| /contabilidade-para-industrias/ | /solucoes/industrias | Solução | 1,250 | 15 | ALTA | Pendente | Mantém conteúdo |
| /calculadora-lucro-real/ | /ferramentas/calculadora-tributaria | Ferramenta | 850 | 8 | ALTA | Pendente | Refazer ferramenta |
| /sobre-a-osp/ | /sobre | Institucional | 420 | 2 | MÉDIA | Pendente | Novo conteúdo |

**Classificação de Prioridade:**

```
ALTA (Must-Have):
- Páginas com > 500 visitas/mês
- Páginas com conversões
- Landing pages de campanhas ativas
- Páginas que rankeiam Top 3 no Google

MÉDIA (Should-Have):
- Páginas com 100-500 visitas/mês
- Conteúdo institucional importante
- Páginas linkadas de outros sites

BAIXA (Nice-to-Have):
- Páginas com < 100 visitas/mês
- Conteúdo desatualizado
- Posts de blog antigos sem tráfego
```

---

## 🎯 PASSO 5: Identificar "Must-Keep" URLs

**Baseado no seu site, essas páginas provavelmente são críticas:**

### Páginas de Solução (ALTA Prioridade)
```
/contabilidade-para-industrias/
/contabilidade-lucro-real/
/contabilidade-lucro-presumido/
/contabilidade-simples-nacional/
/contabilidade-consultiva/
/gestao-financeira/
/planejamento-tributario/
```

### Ferramentas/Calculadoras (ALTA Prioridade)
```
/calculadora-lucro-real/
/simulador-tributario/
/calculadora-simples-nacional/
```

### Páginas Institucionais (MÉDIA Prioridade)
```
/sobre/
/sobre-nos/
/sobre-a-osp/
/equipe/
/contato/
/resultados/
/cases/
/clientes/
```

### Blog/Conteúdo (Analisar Tráfego)
```
/blog/
/blog/[posts-principais]/
/artigos/
/novidades/
```

### Segmentos/Setores (Se existirem)
```
/industria/
/tecnologia/
/saude/
/comercio/
```

---

## 🔄 PASSO 6: Plano de Redirecionamentos 301

**Criar arquivo de configuração para Firebase Hosting:**

`/osp-contabilidade/firebase.json` já tem a estrutura. Vamos adicionar os redirects:

```json
{
  "hosting": {
    "public": "dist",
    "rewrites": [...],
    "redirects": [
      {
        "source": "/contabilidade-para-industrias",
        "destination": "/solucoes/industrias",
        "type": 301
      },
      {
        "source": "/calculadora-lucro-real",
        "destination": "/ferramentas/calculadora-tributaria",
        "type": 301
      },
      {
        "source": "/sobre-a-osp",
        "destination": "/sobre",
        "type": 301
      },
      {
        "source": "/blog/:slug",
        "destination": "/blog/:slug",
        "type": 301
      }
    ]
  }
}
```

---

## 📊 PASSO 7: Auditoria de Conteúdo

**Para cada página ALTA prioridade, documente:**

### Template de Auditoria:

```markdown
### Página: /contabilidade-para-industrias/

**URL Atual:** https://www.ospcontabilidade.com.br/contabilidade-para-industrias/
**URL Nova:** https://osp.com.br/solucoes/industrias

**Métricas:**
- Visitas/mês: XXX
- Posição Google (palavra-chave principal): #X
- Conversões/mês: XX
- Taxa de conversão: X.X%

**SEO:**
- Title atual: "..."
- Meta Description atual: "..."
- H1 atual: "..."
- Palavras-chave que rankeiam: industria, contabilidade industrial, etc.

**Conteúdo:**
- [x] Texto precisa ser reescrito (usar Guia de Linguagem OSP)
- [ ] Pode ser mantido como está
- [x] CTAs precisam ser atualizados
- [x] Imagens precisam ser otimizadas

**Ações:**
- Reescrever seguindo tom de voz OSP
- Adicionar seção TRIBUTA360/GESTÃO360
- Criar CTA "Fale com Especialista"
- Adicionar cases de indústrias
- Schema.org: Service markup
```

---

## 🛠️ FERRAMENTAS ÚTEIS

### Gratuitas:
- **Google Analytics 4** - Tráfego e comportamento
- **Google Search Console** - Performance orgânica
- **Screaming Frog** (até 500 URLs grátis) - Crawl completo
- **Export All URLs** (WordPress plugin) - Lista de URLs
- **Google Sheets** - Organizar dados

### Pagas (Opcionais):
- **Ahrefs** ou **SEMrush** - Análise de backlinks, keywords
- **Screaming Frog Pago** - Sites maiores (> 500 URLs)

---

## ✅ CHECKLIST DE AÇÕES IMEDIATAS

**Você pode fazer HOJE:**

- [ ] Exportar relatório GA4 "Páginas e telas" (últimos 6 meses)
- [ ] Exportar relatório Search Console "Páginas" (últimos 6 meses)
- [ ] Instalar plugin "Export All URLs" no WordPress
- [ ] Exportar lista completa de URLs
- [ ] Criar planilha Google Sheets com template acima
- [ ] Identificar top 10 páginas por tráfego
- [ ] Listar URLs de campanhas ativas (Google Ads/Meta)
- [ ] Verificar se há backlinks importantes (ferramentas gratuitas: Google Search Console → Links)

---

## 📥 OUTPUTS ESPERADOS (Para Próxima Sessão)

**Me envie ou compartilhe:**

1. **CSV/Sheet:** Páginas do GA4 (Top 50 por tráfego)
2. **CSV/Sheet:** Páginas do Search Console (Top 50 por cliques)
3. **CSV/Sheet:** Lista completa de URLs do WordPress
4. **Planilha Master** iniciada com classificação de prioridades
5. **Lista de campanhas ativas** (URLs de destino)

**Com esses dados, eu crio:**
- Plano completo de 301 redirects
- Mapa de migração página por página
- Checklist de conteúdo a preservar/reescrever
- Configuração Firebase pronta para go-live

---

## 🎯 PRÓXIMO PASSO

**Depois deste inventário completo, vamos para:**
- **ENTREGA 2:** Implementar GA4 + UTMs + Pixel no site novo
- **ENTREGA 3:** WhatsApp com pré-captação + Forms

**Mas primeiro, precisamos garantir que não vamos perder tráfego orgânico na migração!** 🛡️

---

**Quer que eu crie um script automatizado para ajudar a extrair essas informações?** Posso fazer um script que:
- Crawla o site WordPress atual
- Extrai títulos, meta descriptions, H1s
- Gera a planilha master automaticamente
- Sugere os redirecionamentos 301

**Só me avisar e eu faço!** 🚀
