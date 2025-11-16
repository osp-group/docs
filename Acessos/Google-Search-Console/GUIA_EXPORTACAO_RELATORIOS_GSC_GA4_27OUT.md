# 🚀 GUIA DE EXPORTAÇÃO DE RELATÓRIOS (27 Out 2025)
**Período: Últimos 3 meses (27 de Julho - 27 de Outubro de 2025)**

> ✅ **PERÍODO CONFIRMADO:** 92 dias exatos (últimos 3 meses, sendo o último dia 27 de outubro de 2025)

---

## 📋 RESUMO EXECUTIVO

Você precisa exportar **3 relatórios críticos**:

| # | Relatório | Fonte | Impacto | Status |
|---|-----------|-------|--------|--------|
| 1 | Performance por Página (com Posição) | GSC | ⭐⭐⭐ CRÍTICO | ❌ FALTA |
| 2 | Investigar 3 URLs com Conversão=0 | GA4 | ⭐⭐⭐ CRÍTICO | ⚠️ VERIFICAR |
| 3 | Confirmar Período GA4 | GA4 | ⭐ VALIDAÇÃO | ⚠️ CONFIRMAR |

**Tempo total estimado:** 30 minutos

---

## 🎯 EXPORTAÇÃO #1: GSC - Performance por Página (COM POSIÇÃO MÉDIA)

### ❌ O Que Falta
```
Você tem: Cliques, impressões, CTR
Falta: POSIÇÃO MÉDIA por página (crítico!)
```

### 📍 PASSO-A-PASSO (Google Search Console)

**PASSO 1: Abrir GSC**
```
URL: https://search.google.com/search-console
Conta: ospcontabilidade.com.br (ou seu domínio)
```

**PASSO 2: Ir para Performance**
```
Menu Esquerdo
├─ Clique em "Performance" (ou "Desempenho")
└─ Você verá gráfico com Cliques, Impressões, CTR, Posição
```

**PASSO 3: Configurar Período**
```
Caixa de Data (canto superior direito)
├─ OPÇÃO 1 (mais rápido): Selecionar "Últimos 3 meses"
│  └─ Confirmar que mostra: "Jul 27 - Oct 27, 2025" ou similar
│
├─ OPÇÃO 2 (customizado): Inserir datas manualmente
│  ├─ Data Inicial: 27 de Julho de 2025
│  ├─ Data Final: 27 de Outubro de 2025
│  └─ Clicar "Aplicar" ou "Apply"
│
✅ RESULTADO: Ambas opções resultam no mesmo período (92 dias)
```

**PASSO 4: Agrupar por Página**
```
Procure por "Agrupar por" (ou "Group by") - geralmente em cima da tabela
├─ Clique no dropdown
└─ Selecione "Página" (ou "Page")

Resultado: Você verá tabela com uma linha POR URL
```

**PASSO 5: CRÍTICO - Adicionar Coluna "Avg Position"**
```
Na tabela, procure ícone de "Colunas" (⚙️ engrenagem, geralmente à direita)
├─ Clique nela
├─ Você verá lista de colunas disponíveis
├─ MARCAR (✅) estas colunas:
│  ✅ Cliques
│  ✅ Impressões
│  ✅ CTR
│  ✅ Avg position (⭐⭐⭐ ESTA É A CRÍTICA!)
└─ Clicar "OK" ou "Aplicar"

Resultado: Tabela agora tem coluna "Avg position" para cada URL
```

**PASSO 6: Exportar CSV**
```
No topo à direita, procure ícone de "Exportar" (↓ ou "Export")
├─ Clique nele
├─ Selecione formato: CSV (recomendado)
│  ou Google Sheets (se preferir compartilhar link)
└─ Download ou Compartilhar

Arquivo será nomeado algo como:
"performance_page_YYYYMMDD.csv"
```

**PASSO 7: Renomear Arquivo**
```
Renomear para: gsc-performance-com-posicao-27out.csv

Localizar arquivo em:
/Users/gpagotto/osp-website/contabilidade/
```

### ✅ Checklist Antes de Enviar
```
[ ] Período correto? (27 Jul - 27 Out 2025)
[ ] Agrupado por Página? (não por Query)
[ ] Tem coluna "Avg position"?
[ ] Tem coluna "Cliques"?
[ ] Tem coluna "Impressões"?
[ ] Tem coluna "CTR"?
[ ] Arquivo salvo em .csv?
[ ] Nome: gsc-performance-com-posicao-27out.csv?
```

### 💾 Salvar em Local Conheco
```
Salvar arquivo aqui:
/Users/gpagotto/osp-website/contabilidade/gsc-performance-com-posicao-27out.csv
```

---

## 🎯 EXPORTAÇÃO #2: GA4 - Investigar 3 URLs com Conversão=0

### ❌ O Problema

3 páginas com TRÁFEGO mas ZERO conversões rastreadas:

| URL | Sessões | Conversões | Taxa |
|-----|---------|-----------|------|
| /calculadora-lucro-real/ | 487 | 0 | 0% |
| /filmes-sobre-contabilidade-10-filmes-para-se-inspirar/ | 899 | 0 | 0% |
| /quando-vale-a-pena-migrar-para-o-lucro-real/ | 315 | 0 | 0% |

### 🔍 Investigação

**OPÇÃO 1: Verificar em GA4 se essas URLs têm conversões**

```
URL: https://analytics.google.com
Conta: OSP Contabilidade
Propriedade: ospcontabilidade.com.br
```

**PASSO 1: Ir para Relatórios**
```
Menu Esquerdo
├─ "Relatórios" (ou "Reports")
```

**PASSO 2: Abrir Relatório de Engajamento**
```
Submenu:
├─ "Engajamento" (ou "Engagement")
│  └─ "Páginas e telas" (ou "Pages and Screens")
```

**PASSO 3: Configurar Período**
```
Caixa de Data (canto superior direito)
├─ OPÇÃO 1 (mais rápido): Selecionar "Últimos 3 meses"
│  └─ Confirmar que mostra: "27 de jul. - 27 de out. de 2025" ou similar
│
├─ OPÇÃO 2 (customizado): Inserir datas manualmente
│  ├─ Data Inicial: 27 de Julho de 2025
│  ├─ Data Final: 27 de Outubro de 2025
│  └─ Clicar "Aplicar" ou "Apply"
│
✅ RESULTADO: Ambas opções resultam no mesmo período (92 dias)
```

**PASSO 4: Adicionar Métrica de Conversão**
```
Procure por "Adicionar métrica" (+ sign) na tabela
├─ Clique nela
├─ Busque por "lead" (minúsculas)
├─ Procure por:
│  - "lead_lucro_real"
│  - "conversões"
│  - "goals"
│  - qualquer métrica que represente conversão
└─ Selecione e clique "OK"

Resultado: Nova coluna com conversões aparece
```

**PASSO 5: Procurar pelas 3 URLs**
```
Na tabela, procure pelas 3 URLs usando CTRL+F (ou CMD+F no Mac):
1. /calculadora-lucro-real/
2. /filmes-sobre-contabilidade-10-filmes-para-se-inspirar/
3. /quando-vale-a-pena-migrar-para-o-lucro-real/

Verificar:
├─ Essa URL aparece na tabela?
├─ Se SIM: Qual o número na coluna de conversões?
│  - Se ZERO → Tracking problem OU página não converte
│  - Se NÚMERO > 0 → Ótimo! Dados eram desatualizados
├─ Se NÃO → URL não tem dados em GA4 (possível 404 ou URL diferente)
```

**PASSO 6: Exportar para Verificação**
```
Se quiser exportar a tabela completa para análise:
├─ Botão "Exportar" (↓) no topo direito
├─ Formato: CSV
├─ Arquivo: ga4-pages-conversions-27out.csv
```

### ❓ Descobertas Possíveis

**CENÁRIO 1: URLs têm 0 conversões em GA4**
```
Significado: Ou não tem CTAs (esperado) ou tracking não está funcionando
Ação: Você confirma se DEVERIAM ter conversões
     Se SIM → Bug GA4, precisa fix antes da migração
     Se NÃO → OK, páginas são informativas mesmo
```

**CENÁRIO 2: URLs têm conversões > 0 em GA4**
```
Significado: Dados da matriz anterior estavam desatualizados
Ação: Atualizar matriz consolidada com números novos
```

**CENÁRIO 3: URLs não aparecem em GA4**
```
Significado: Possível URL diferente ou redirect anterior
Ação: Procurar URL similar ou verificar se há redirecionamento
```

### ✅ Checklist
```
[ ] Abrir GA4 em período correto (27 Jul - 27 Out)?
[ ] Adicionar métrica de conversão?
[ ] Procurar pelas 3 URLs?
[ ] Registrar: tem conversão? SIM/NÃO/DESCONHECIDO?
[ ] Se ZERO: essa URL DEVERIA converter? SIM/NÃO/DESCONHECIDO?
[ ] Exportar para arquivo (opcional)
```

---

## 🎯 EXPORTAÇÃO #3: GA4 - Confirmar Período

### ✅ Validação Rápida

**PASSO 1: Abrir GA4**
```
URL: https://analytics.google.com
Conta: OSP Contabilidade
Propriedade: ospcontabilidade.com.br
```

**PASSO 2: Ir para Relatórios**
```
Menu Esquerdo
├─ "Relatórios"
│  └─ "Engajamento"
│     └─ "Páginas e telas"
```

**PASSO 3: Verificar Data Selecionada**
```
Caixa de Data (canto superior direito)
├─ Qual período está selecionado agora?
├─ É "27 de Julho - 27 de Outubro"?
├─ Ou é "últimos 3 meses"?
├─ Ou é algo diferente?
```

**PASSO 4: Ajustar se Necessário**
```
Se NÃO está no período correto:
├─ Clique na caixa de data
├─ Selecione período customizado:
│  Data Início: 27 de Julho de 2025
│  Data Fim: 27 de Outubro de 2025
└─ Clicar "Aplicar"
```

**PASSO 5: Confirmar**
```
Após aplicar, verificar:
├─ Cabeçalho agora mostra: "27 de jul. - 27 de out. de 2025" ou similar
└─ Total de Sessões muda para ~11.220 (aproximadamente)
```

### ✅ Checklist
```
[ ] GA4 está aberto?
[ ] Período é 27 Jul - 27 Out 2025?
[ ] Total de Sessões é ~11.220?
[ ] Total de Usuários é ~9.687?
```

---

## 📊 RESUMO: O Que Você Vai Exportar

### Exportação #1: GSC Performance com Posição
```
Arquivo: gsc-performance-com-posicao-27out.csv
Colunas esperadas:
├─ URL (ou "Página")
├─ Cliques
├─ Impressões
├─ CTR (%)
├─ Avg position ⭐
Exemplo de linha:
/contabilidade-lucro-real/,168,N/A,N/A,15.5
/calculadora-lucro-real/,623,4682,13.31,7.31
```

### Exportação #2: GA4 - Verificação de 3 URLs
```
Arquivo: ga4-pages-conversions-27out.csv (opcional)
Informações a registrar:
├─ /calculadora-lucro-real/ → Conversões: ?
├─ /filmes-sobre-contabilidade/ → Conversões: ?
├─ /quando-vale-a-pena-migrar/ → Conversões: ?

Resultado esperado:
├─ Se 0: Confirmar se DEVERIA ter conversão
├─ Se > 0: Atualizar matriz
```

### Exportação #3: GA4 - Validação de Período
```
Confirmação:
├─ Período GA4: 27 Jul - 27 Out 2025 ✅
├─ Alinhado com GSC ✅
└─ Pronto para análise consolidada ✅
```

---

## 🚀 PRÓXIMOS PASSOS

### DEPOIS QUE VOCÊ EXPORTAR:

**1. Enviar arquivo GSC:**
```
gsc-performance-com-posicao-27out.csv
Salvar em: /Users/gpagotto/osp-website/contabilidade/
```

**2. Registrar descobertas GA4:**
```
Criar arquivo: ga4-investigacao-3-urls-27out.txt
Conteúdo:
/calculadora-lucro-real/: conversões = ?
/filmes-sobre-contabilidade/: conversões = ?
/quando-vale-a-pena-migrar/: conversões = ?

DEVERIA ter conversão? SIM/NÃO para cada uma
```

**3. Confirmar período:**
```
"GA4 confirmado no período 27 Jul - 27 Out ✅"
```

### DEPOIS EU:
```
1. Consolidar GSC novo com GA4
2. Atualizar MATRIZ_CONSOLIDADA_GSC_GA4_SEMRUSH.csv
3. Validar com você os 3 URLs suspeitos
4. Preparar para León validar
```

---

## ⏱️ TIMELINE

```
AGORA (próximos 30 min):
├─ 10 min: Exportar GSC com posição (EXPORTAÇÃO #1)
├─ 10 min: Investigar 3 URLs em GA4 (EXPORTAÇÃO #2)
├─ 3 min: Confirmar período GA4 (EXPORTAÇÃO #3)
└─ 7 min: Salvar e registrar

DEPOIS (próximas 2 horas):
├─ Consolidar dados
├─ Atualizar matriz
└─ Preparar para León
```

---

## ❓ DÚVIDAS DURANTE EXPORTAÇÃO?

Se ficar preso em algum passo:

```
1. Qual ícone não acha?
   → Descrição: (procure ícone que parece uma engrenagem/⚙️)

2. Qual coluna não aparece?
   → Nome em inglês vs português pode variar
   → Procure alternativas

3. Período diferente?
   → Use "Últimos 3 meses" como fallback
   → Depois confirmamos datas exatas

4. Arquivo não exporta?
   → Tente Google Sheets ao invés de CSV
   → Compartilha link comigo
```

---

## ✅ CHECKLIST FINAL

```
ANTES DE COMEÇAR:
[ ] Tenho acesso a GSC (ospcontabilidade.com.br)?
[ ] Tenho acesso a GA4 (ospcontabilidade.com.br)?
[ ] Período: 27 Jul - 27 Out 2025?
[ ] Vou salvar em: /Users/gpagotto/osp-website/contabilidade/?

EXPORTAÇÃO #1 (GSC):
[ ] Abri GSC em Performance?
[ ] Agrupei por Página?
[ ] Adicionei coluna "Avg position"?
[ ] Período correto (27 Jul - 27 Out)?
[ ] Exportei como CSV?
[ ] Renomei para gsc-performance-com-posicao-27out.csv?

EXPORTAÇÃO #2 (GA4 - 3 URLs):
[ ] Abri GA4 em Páginas e Telas?
[ ] Adicionei métrica de conversão?
[ ] Procurei pelas 3 URLs?
[ ] Registrei: conversões = 0 ou > 0?
[ ] Registrei: DEVERIA converter? SIM/NÃO?
[ ] Exportei (opcional)?

EXPORTAÇÃO #3 (GA4 - Período):
[ ] Período GA4 é 27 Jul - 27 Out?
[ ] Alinhado com GSC?
[ ] Sessões totais ~11.220?

PRONTO PARA ENVIAR:
[ ] Arquivo GSC salvo?
[ ] Descobertas GA4 anotadas?
[ ] Período confirmado?
```

---

## 🎯 COMANDO: Pronto? Vamos Começar!

**Me confirma quando estiver pronto:**

```
"Estou pronto para exportar"

Ou se tiver dúvida:
"Onde fica [ícone/coluna/botão] em GSC/GA4?"
```

---

**Você consegue! Todos esses passos levam ~30 minutos no máximo! 🚀**
