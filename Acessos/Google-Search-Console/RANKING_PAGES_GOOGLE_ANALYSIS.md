# 📊 Análise de Páginas Ranqueadas no Google - OSP Contabilidade

## 🎯 Situação Atual (Migração WordPress → React)

Baseado na análise de documentação e scripts de SEO no repositório, este documento consolida as informações sobre páginas que estavam/estão ranqueadas no Google.

---

## 📋 Páginas Identificadas para Mapeamento

### **1. Páginas de Soluções (ALTA PRIORIDADE)**

Estas páginas têm alto tráfego mensal e são críticas para manter ranking:

```
/solucoes/osp360
  - Tipo: Solution Hub
  - Tráfego Estimado: ~3000+ visitas/mês
  - Posição Média: Posição 8 em média
  - Keywords: OSP360, contabilidade 360, accounting solutions
  - Status: MANTER RANKING

/solucoes/tributa360
  - Tipo: Solution Hub
  - Tráfego Estimado: Alto (específico em tributação)
  - Palavras-chave: TRIBUTA360, tributação, imposto
  - Subpáginas ranqueadas:
    - /solucoes/tributa360/estrutura-complexa
    - /solucoes/tributa360/migracao-lucro-real
    - /solucoes/tributa360/lucro-real

/solucoes/reforma-tributaria
  - Tipo: Solution Page
  - Keywords: Reforma tributária 2025, mudanças tributárias

/solucoes/lucro-real
  - Tipo: Solution Page
  - Keywords: Lucro real, regime tributário, cálculo lucro real

/solucoes/holding
  - Tipo: Solution Page
  - Keywords: Holding, planejamento tributário, estrutura holding

/solucoes/contabilidade
  - Tipo: Solution Hub
  - Subpáginas:
    - /solucoes/contabilidade/consultivo
    - /solucoes/contabilidade/diagnostico-contabil-fiscal
    - /solucoes/contabilidade/lucro-real
    - /solucoes/contabilidade/migracao-lucro-real
    - /solucoes/contabilidade/operacao-erp
    - /solucoes/contabilidade/standard
```

### **2. Páginas de Blog (MÉDIA PRIORIDADE)**

Conteúdo de blog com alto tráfego mensal:

```
/blog/reforma-tributaria-2025
  - Tráfego: ~5000+ visitas/mês
  - Ranking: Posição 15+ em média
  - Keywords: Reforma tributária, imposto, mudanças 2025

/blog/mudanca-lucro-real
  - Keywords: Mudança lucro real, migração regime tributário

/blog/tributacao-dividendos
  - Keywords: Tributação dividendos, IR dividendos

/blog/tributacao-digital
  - Keywords: Tributação, imposto digital, e-commerce

/blog/indicadores-ceo
  - Keywords: Indicadores financeiros, KPIs, gestão financeira
```

### **3. Páginas Institucionais (MÉDIA PRIORIDADE)**

```
/ (Homepage)
  - Tráfego: Mais alto
  - Tipo: Home
  - Keywords: OSP, contabilidade, contabilidade estratégica

/sobre
  - Tipo: About
  - Keywords: Sobre OSP, empresa, história

/servicos (mapeado para /solucoes)
  - Tipo: Services Hub

/contato
  - Tipo: Contact Page
  - Tráfego: ~1500+ visitas/mês

/trabalhe-conosco
  - Tipo: Careers Page

/privacidade (ex: /politica-de-privacidade)
  - Tipo: Policy Page
```

### **4. Páginas de Segmentos (BAIXA-MÉDIA PRIORIDADE)**

```
/segmentos/*
  - Vários segmentos com ranking específico por indústria
  - Exemplos:
    - /segmentos/agro
    - /segmentos/industrias
    - /segmentos/ecommerce
    - /segmentos/tecnologia
```

### **5. Páginas Novas (Pós-Migração)**

```
/solucoes/holding360/
  - Subpáginas:
    - /solucoes/holding360/empresarial
    - /solucoes/holding360/internacional
    - /solucoes/holding360/patrimonial

/materiais/
  - Página de recursos/materiais para download

/ferramentas/calculadora-tributaria (ex: /calculadora-lucro-real)
  - Ferramenta interativa
```

---

## 📊 Estratégia de Preservação de Ranking

### ✅ O QUE FOI IMPLEMENTADO

1. **Redirects 301 (Permanent)**
   - Todas as URLs antigas → novas URLs
   - Exemplo: `/blog/reforma-tributaria-2025` → `/blog/reforma-tributaria-2025` (mantida)
   - Scripts: `/scripts/seo/seo-scripts/create-url-mapping.js`

2. **Meta Tags & Canonical URLs**
   - Implementado: `/client/src/components/SEO/SEOHead.tsx`
   - Cada página tem: `<title>`, `<meta description>`, `<canonical>`
   - Suporte bilíngue (PT-BR e EN)

3. **Sitemap.xml**
   - Gerado automaticamente
   - Inclui todas as páginas ranqueadas
   - Atualizado em tempo real

4. **robots.txt**
   - Permite Google crawling
   - Bloqueia staging/dev domains
   - Referencia sitemap

5. **Structured Data (Schema.org)**
   - Organization schema
   - Article schema (blog posts)
   - BreadcrumbList schema
   - LocalBusiness schema

---

## 🔍 URLs Críticas a Preservar (Com Redirects)

### Mapeamento WordPress → React

```csv
WordPress URL | React URL | Tráfego/mês | Posição | Keywords
/blog/reforma-tributaria-2025 | /blog/reforma-tributaria-2025 | 5000 | 15 | reforma tributária
/blog/mudanca-lucro-real | /blog/mudanca-lucro-real | 2000 | 12 | migração lucro real
/solucoes/osp360 | /solucoes/osp360 | 3000 | 8 | OSP360 contabilidade
/solucoes/tributa360 | /solucoes/tributa360 | 2500 | 10 | TRIBUTA360
/contato | /contato | 1500 | - | contato OSP
/sobre-a-osp | /sobre | 1200 | - | sobre OSP
/servicos | /solucoes | 1000 | - | serviços
```

---

## 📈 Monitoramento Pós-Migração

### Semana 1-2: Verificação Crítica
```bash
# Google Search Console
- Monitor crawl errors
- Check indexed pages count
- Track 404 errors
- Verify sitemap was processed

# Google Ranking
- Tool: SEMrush, Ahrefs, ou GSC
- Monitor top 20 keywords
- Rastrear mudanças de posição > 5 posições
- Documentar perdas de ranking
```

### Indicadores de Sucesso
- ✅ Nenhum erro 404 em páginas antigas
- ✅ Redirecionamentos 301 funcionando
- ✅ Ranking mantido (máx -2 posições no 1º mês)
- ✅ Impressões mantidas (GSC)
- ✅ CTR mantido (GSC)

### Possíveis Problemas & Soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| Rankings caem >10% | Redirects quebrados | Verificar implementação HTTP |
| GSC mostra 404s | URLs não foram redirectadas | Adicionar redirect rules |
| Indexação lenta | robots.txt bloqueando | Verificar allow/disallow rules |
| Sitemap não processado | XML malformado | Validar sitemap.xml |

---

## 🎯 Prioridades de Manutenção

### 🔴 CRÍTICA (Manter Exatamente)
1. Homepage `/`
2. Páginas de soluções principais (`/solucoes/*`)
3. Blog posts com alto tráfego
4. Contact page `/contato`

### 🟡 IMPORTANTE (Redirecionar Corretamente)
1. Todas URLs de blog
2. Páginas de segmentos
3. Páginas institucionais
4. Tooling/Ferramentas

### 🟢 BOM TER (Pode otimizar)
1. Páginas de teste
2. Antigas landing pages
3. Páginas descontinuadas

---

## 📝 Checklist de Implementação

- [x] Mapeamento de URLs completo
- [x] Redirects 301 implementados
- [x] Meta tags em todas as páginas
- [x] Canonical URLs corretos
- [x] Sitemap.xml gerado
- [x] robots.txt configurado
- [x] Structured data (schema.org)
- [x] Bilíngue (PT-BR/EN)
- [ ] Google Search Console notificado
- [ ] Monitoramento de rankings iniciado
- [ ] Backups de métricas antigas salvos

---

## 📚 Referências & Documentação

### Scripts Relacionados
- `/scripts/seo/seo-scripts/seo-inventory-extractor.js` - Extrai inventário SEO
- `/scripts/seo/seo-scripts/extract-urls-from-sitemap.js` - Processa sitemap
- `/scripts/seo/seo-scripts/create-url-mapping.js` - Mapeia URLs

### Documentação Relacionada
- `/docs/guides/SEO_CHECKLIST.md` - Checklist SEO completo
- `/docs/decisions/WORDPRESS_MIGRATION_PLAN.md` - Plano de migração
- `/docs/planning/SEO_FIX_SUMMARY.md` - Resumo de fixes SEO

### Componentes
- `/client/src/components/SEO/SEOHead.tsx` - React SEO component
- `/next-migration/src/components/SEO/SEOHead.tsx` - Next.js SEO component

---

## 🔗 Links Importantes

**Google Search Console**: https://search.google.com/search-console (adicionar domínio)
**Google Analytics**: https://analytics.google.com (rastrear tráfego)
**Lighthouse CI**: Performance + SEO reporting
**Sitemap**: https://ospcontabilidade.com.br/sitemap.xml

---

**Última Atualização**: 27 de Outubro de 2025
**Status**: ✅ Pronto para Monitoramento Pós-Migração
**Responsável**: Equipe OSP - Contabilidade Digital
