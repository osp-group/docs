# 📊 MAPEAMENTO COMPLETO DE RELATÓRIOS - STATUS E GAPS

**Data: 27 de outubro de 2025 | Período: Últimos 3 meses (27 Jul - 27 Out)**

---

## 🎯 RESUMO EXECUTIVO

| Status | Total | Completos | Incompletos | Faltando |
|--------|-------|-----------|------------|----------|
| **Relatórios** | 8 | 3 ✅ | 3 ⚠️ | 2 ❌ |
| **Dados GSC** | 100% | 75% | 25% | - |
| **Dados GA4** | 100% | 80% | 20% | - |
| **Período** | 92 dias | Alguns | Alguns | - |

**Status Geral: 76% COMPLETO | Faltam: 24% (fáceis de gerar)**

---

## 📋 RELATÓRIOS QUE VOCÊ TEM (✅ COMPLETOS)

### 1️⃣ **gsc-pages-consolidado.csv** ✅ COMPLETO
```
Status: ✅ Pronto
Período: 92 dias (27 jul - 27 out) ✅
Colunas: URL, Cliques, Impressões, CTR, Posição_Media, Categoria, Prioridade, Acao_Sugerida
Linhas: 22 URLs top (filtradas)
Dados: GSC apenas
Falta: Posição média em ALGUMAS URLs (nem todas têm)
```

**Análise:**
- ✅ Cliques: 4.225 distribuídos
- ✅ Impressões: 247.753 distribuídos
- ✅ CTR: Calculado por URL
- ⚠️ Posição média: TEM (7.31, 8.09, 23.94, etc) - **MAS NEM TODAS URLs TÊMMM**

### 2️⃣ **MATRIZ_CONSOLIDADA_GSC_GA4_SEMRUSH.csv** ✅ COMPLETO
```
Status: ✅ Pronto
Período: 92 dias (27 jul - 27 out) ✅
Colunas: 18 colunas (GSC + GA4 + Semrush)
Linhas: 30 URLs top (consolidadas)
Dados: Multiplas fontes consolidadas
```

**Análise:**
- ✅ GSC data: Cliques, Posição, Impressões, CTR
- ✅ GA4 data: Sessões, Usuários, Conversões, Taxa
- ✅ Semrush data: Visibilidade, Ranking
- ✅ Período: Alinhado 92 dias
- ✅ Top conversor: /contabilidade-lucro-real-gads/ com 549 conversões

### 3️⃣ **osp-url-inventory-2025-10-16.csv** ⚠️ INCOMPLETO
```
Status: ⚠️ Estrutura ok, dados vazios
Período: 2025-10-16 (data do arquivo)
Colunas: URL Antiga, Caminho, Tipo, URL Nova, Tráfego, Conversões, Prioridade, Status 301
Linhas: APENAS HEADER (corpo vazio!)
Dados: Nenhum
```

**Problema:**
- ❌ Arquivo template sem dados preenchidos
- ❌ Período: Data do arquivo não significa que coleta é de 27-out
- ❌ Faltam: Todos os dados (tráfego, conversões, prioridade)

**Ação:** ❌ PRECISA SER REGENERADO

---

## ⚠️ RELATÓRIOS COM PERÍODO INCOMPLETO (⚠️ PARCIAIS)

### 4️⃣ **GSC - Performance por Página (COM POSIÇÃO)** ⚠️ FALTA
```
Status: ⚠️ FALTA - CRÍTICO!
Período: ??? (não exportado com período específico)
Colunas esperadas: URL, Cliques, Impressões, CTR, Avg Position
Linhas esperadas: 145+ URLs (todas do site)
Dados: Nenhum (não coletado ainda)
```

**Por quê falta:**
- Você tem dados GSC aggregados mas NÃO por página individual completo
- `gsc-pages-consolidado.csv` tem apenas TOP 20 URLs
- Faltam: 125+ URLs menores que não foram exportadas

**Impacto:**
- ⭐⭐⭐ CRÍTICO: Sem isto não sabe posição média de 125+ URLs
- Não consegue priorizar redirects corretamente
- Pode perder páginas bem ranqueadas

**Como gerar:** 5 minutos
```
GSC → Performance → Group by Page → Adicionar coluna "Avg position" → Exportar CSV
```

---

### 5️⃣ **GA4 - Páginas com Conversões Completo** ⚠️ FALTA
```
Status: ⚠️ FALTA - Precisa confirmação
Período: 27 jul - 27 out (precisa confirmar)
Colunas esperadas: Page, Sessions, Users, Conversions, Conversion Rate
Linhas esperadas: 100+ URLs
Dados: MATRIZ tem apenas 30 URLs top
```

**Por quê falta:**
- MATRIZ_CONSOLIDADA tem 30 URLs top do GA4
- Mas faltam: 70+ URLs menores com tráfego < 100 sessões
- Não exportou TODAS as páginas do GA4, apenas as principais

**Impacto:**
- 🟡 IMPORTANTE: Sem completo, não sabe páginas pequenas com potencial
- Pode ignorar páginas niche com alta taxa conversão

**Como gerar:** 10 minutos
```
GA4 → Páginas e Telas → Adicionar métrica "Conversões" → Exportar CSV COMPLETO (não apenas top 30)
```

---

### 6️⃣ **GA4 - Validação de 3 URLs com Conversão=0** ⚠️ FALTA CONFIRMAÇÃO
```
Status: ⚠️ FALTA - Precisa investigação
URLs: /calculadora-lucro-real/, /filmes-sobre-contabilidade/, /quando-vale-a-pena-migrar/
Período: 27 jul - 27 out
Problema: 3 URLs têm tráfego (487, 899, 315 sessões) MAS conversão = 0 na MATRIZ
Pergunta: DEVERIA ter conversão? SIM/NÃO?
```

**Por quê falta:**
- Não foi investigado ainda se é tracking problem ou comportamento esperado
- MATRIZ mostra 0 conversões mas pode ser desatualizado

**Impacto:**
- 🟡 IMPORTANTE: Se DEVERIAM converter, é bug GA4 que precisa fix antes migração
- Se NÃO deveriam, está tudo certo

**Como gerar:** 5 minutos
```
GA4 → Páginas e Telas → Procurar pelas 3 URLs → Ver coluna de conversões → Registrar se = 0 ou > 0
```

---

## ❌ RELATÓRIOS QUE FALTAM COMPLETAMENTE (❌ INEXISTENTES)

### 7️⃣ **GSC - Coverage (Cobertura Completa de URLs)** ❌ INEXISTENTE
```
Status: ❌ NÃO EXPORTADO
Período: ???
Colunas esperadas: URL, Status (coberta/não coberta), Data da última verificação
Linhas esperadas: 145+ URLs
Dados: ZERO
```

**Por quê falta:**
- Este relatório nunca foi exportado
- Você tem dados de performance mas não de cobertura

**Impacto:**
- 🟢 NICE-TO-HAVE: Útil para confirmar que todas URLs estão indexadas
- Não é crítico para migração (tem performance já)

**Como gerar:** 3 minutos
```
GSC → Cobertura → Selecionar "Cobertas" → Exportar CSV
```

---

### 8️⃣ **GSC - Erros e Avisos** ❌ INEXISTENTE
```
Status: ❌ NÃO EXPORTADO
Período: ???
Colunas esperadas: URL, Tipo de erro (404, servidor, crawl), Quantidade
Linhas esperadas: Deveria ser ZERO ou poucos
Dados: ZERO
```

**Por quê falta:**
- Este relatório nunca foi verificado
- Não sabe se tem 404s ou problemas de crawling

**Impacto:**
- 🟡 IMPORTANTE: Se tiver 404s, precisa corrigir antes migração
- URLs com erro podem estar perdendo ranking

**Como gerar:** 3 minutos
```
GSC → Cobertura → Filtrar por "Erro" → Exportar lista de URLs problemáticas
```

---

## 📊 TABELA RESUMO: O QUE VOCÊ TEM vs O QUE FALTA

| # | Relatório | Tem? | Período OK? | Completo? | Ação |
|---|-----------|------|-----------|----------|------|
| 1 | GSC Pages (Top 20) | ✅ | ✅ | ⚠️ Parcial | Usar como está |
| 2 | MATRIZ GSC+GA4+Semrush | ✅ | ✅ | ✅ | Usar como está |
| 3 | URL Inventory | ✅ | ❌ | ❌ Vazio | ❌ REGENERAR |
| 4 | **GSC Performance COMPLETO** | ❌ | - | - | ✅ GERAR (5 min) |
| 5 | **GA4 Páginas COMPLETO** | ❌ | - | - | ✅ GERAR (10 min) |
| 6 | **GA4 Validar 3 URLs** | ⚠️ | ✅ | ⚠️ | ⏳ INVESTIGAR (5 min) |
| 7 | GSC Coverage | ❌ | - | - | ⏳ GERAR (3 min) |
| 8 | GSC Erros/Avisos | ❌ | - | - | ⏳ GERAR (3 min) |

---

## 🎯 PRIORIDADE: O QUE GERAR PRIMEIRO

### 🔴 CRÍTICO (Deve gerar HOJE):
```
RELATÓRIO #4: GSC Performance COMPLETO com Posição Média
├─ Por quê: Sem isto, não consegue mapear 125+ URLs menores
├─ Impacto: Perder páginas bem ranqueadas na migração
├─ Tempo: 5 minutos
└─ Status: ❌ INEXISTENTE → Precisa gerar
```

### 🟡 IMPORTANTE (Deve gerar HOJE):
```
RELATÓRIO #5: GA4 Páginas COMPLETO
├─ Por quê: MATRIZ tem apenas 30 URLs top, faltam 70+
├─ Impacto: Ignorar potencial em páginas niche
├─ Tempo: 10 minutos
└─ Status: ⚠️ PARCIAL → Precisa completar

RELATÓRIO #6: Investigar 3 URLs com Conversão=0
├─ Por quê: Descobrir se é tracking bug ou esperado
├─ Impacto: Se bug, corrigir antes da migração
├─ Tempo: 5 minutos (investigação rápida)
└─ Status: ⚠️ DUVIDOSO → Precisa confirmar
```

### 🟢 LEGAL-TO-HAVE (Pode gerar depois):
```
RELATÓRIO #7: GSC Coverage
├─ Por quê: Confirmar que todas URLs estão cobertas
├─ Impacto: Nice-to-have, não crítico
├─ Tempo: 3 minutos
└─ Status: ❌ Não exportado

RELATÓRIO #8: GSC Erros/Avisos
├─ Por quê: Ver se tem 404s ou erros
├─ Impacto: Se tiver, precisa corrigir
├─ Tempo: 3 minutos
└─ Status: ❌ Não verificado
```

---

## 🚀 PLANO DE AÇÃO: PRÓXIMAS 30 MINUTOS

### Passo 1: Gerar GSC Performance COMPLETO (5 min)
```
1. GSC → Performance
2. Data: "Últimos 3 meses" ou 27/07 até 27/10
3. Group by: "Página"
4. Adicionar coluna: "Avg position" (⚙️)
5. Exportar: CSV
6. Nomear: gsc-performance-completo-27out.csv
7. Salvar em: /Users/gpagotto/osp-website/contabilidade/
```

**Validação:** Arquivo deve ter 145+ linhas (uma por URL)

---

### Passo 2: Gerar GA4 Páginas COMPLETO (10 min)
```
1. GA4 → Relatórios → Engajamento → Páginas e Telas
2. Data: "Últimos 3 meses" ou 27/07 até 27/10
3. Adicionar métrica: "Conversões"
4. Exportar: CSV COMPLETO (não apenas top 30!)
5. Nomear: ga4-pages-conversions-completo-27out.csv
6. Salvar em: /Users/gpagotto/osp-website/contabilidade/
```

**Validação:** Arquivo deve ter 100+ linhas (uma por página)

---

### Passo 3: Investigar 3 URLs em GA4 (5 min)
```
1. GA4 → Páginas e Telas (período: 27/07 até 27/10)
2. Procurar: CTRL+F (ou CMD+F)
   - /calculadora-lucro-real/
   - /filmes-sobre-contabilidade-10-filmes-para-se-inspirar/
   - /quando-vale-a-pena-migrar-para-o-lucro-real/
3. Verificar coluna de conversões para cada uma
4. Registrar: conversões = 0 ou > 0?
5. Criar arquivo: ga4-investigacao-3-urls-27out.txt
   Conteúdo:
   /calculadora-lucro-real/: conversões = ?
   /filmes-sobre-contabilidade/: conversões = ?
   /quando-vale-a-pena-migrar/: conversões = ?
6. Salvar em: /Users/gpagotto/osp-website/contabilidade/
```

**Validação:** Cada URL deve ter um resultado (zero ou número > 0)

---

### Passo 4: BÔNUS - Gerar Coverage + Erros (6 min - opcional)
```
A. Coverage (3 min):
   GSC → Cobertura → Filtrar "Cobertas" → Exportar → gsc-coverage-27out.csv

B. Erros (3 min):
   GSC → Cobertura → Filtrar "Erro" → Exportar → gsc-erros-27out.csv
   (Esperado: 0 erros ou muito poucos)
```

---

## 📝 CHECKLIST FINAL

**HOJE (próxima 1 hora):**
```
[ ] Gerar GSC Performance COMPLETO (5 min)
    └─ Arquivo: gsc-performance-completo-27out.csv

[ ] Gerar GA4 Páginas COMPLETO (10 min)
    └─ Arquivo: ga4-pages-conversions-completo-27out.csv

[ ] Investigar 3 URLs em GA4 (5 min)
    └─ Arquivo: ga4-investigacao-3-urls-27out.txt

[ ] (Opcional) Coverage + Erros (6 min)
    └─ Arquivos: gsc-coverage-27out.csv, gsc-erros-27out.csv

[ ] Validar período em TODOS os arquivos (27/07 até 27/10)

[ ] Salvar tudo em: /Users/gpagotto/osp-website/contabilidade/
```

**DEPOIS (próximas 2 horas):**
```
[ ] Consolidar todos em uma única MATRIZ atualizada
[ ] Validar que 145+ URLs mapeadas
[ ] Verificar que 584+ conversões rastreadas
[ ] Preparar para León validar
```

---

## 📊 RESULTADO ESPERADO

Depois que você gerar tudo:

```
Total de Relatórios: 8/8 ✅
├─ Completos: 5 ✅
├─ Parciais: 1 ⚠️
└─ Nice-to-have: 2 🟢

Dados Consolidados:
├─ GSC: 145+ URLs com posição, cliques, impressões, CTR ✅
├─ GA4: 100+ páginas com sessões, usuários, conversões ✅
├─ Semrush: 30+ keywords, 50 competitors, visibility ✅
└─ Validação: 3 URLs investigadas, gap identificado ✅

Período: 27 julho - 27 outubro 2025 (92 dias)
Status: 100% PRONTO PARA MIGRAÇÃO ✅
```

---

## 🎯 RESUMO: O QUE FAZER AGORA

```
Você tem:
✅ GSC pages top 20
✅ MATRIZ consolidada 30 URLs
✅ Dados Semrush
⚠️ Investigações que precisam ser confirmadas

Falta:
❌ GSC performance COMPLETO (145+ URLs)
❌ GA4 páginas COMPLETO (100+ URLs)
⚠️ Validação de 3 URLs suspeitas

AÇÃO IMEDIATA:
→ Gerar 3 relatórios (20 minutos total)
→ Consolidar tudo em 1 MATRIZ final
→ PRONTO para León!
```

---

**Status: 76% PRONTO | Faltam: 24% (fáceis de gerar em 30 minutos max)**

**Pronto para começar a gerar?**
