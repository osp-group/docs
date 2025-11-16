# 📋 TEMPLATE - Coletar GA4 (Conversões por Página)

**Este arquivo te guia passo-a-passo para coletar dados GA4**

---

## 📍 O Que Você Precisa Coletar

### Dados Necessários do GA4:
```
URL da página | Sessões | Usuários | Eventos (Lead) | Taxa Conversão
/calculadora-lucro-real/ | 1200 | 800 | 150 | 12.5%
/blog/reforma-tributaria/ | 500 | 400 | 50 | 10%
```

---

## 🔧 Passo-a-Passo (GA4 Portuguese UI)

### PASSO 1: Abrir Google Analytics 4
```
URL: https://analytics.google.com
Login: seu_email@gmail.com
```

### PASSO 2: Selecionar Propriedade
```
Conta: OSP Contabilidade (ou o nome exato da sua conta)
Propriedade: ospcontabilidade.com.br (ou URL do seu site)
```

### PASSO 3: Ir em Relatórios
```
Menu Esquerdo:
├─ "Relatórios" (ou "Reports" se em inglês)
```

### PASSO 4: Abrir Relatório de Engajamento
```
Relatórios
├─ "Engajamento" (ou "Engagement")
│  └─ "Páginas e telas" (ou "Pages and Screens")
```

### PASSO 5: Configurar Período
```
Data: 27 de Julho - 27 de Outubro de 2025 (mesmo período do GSC)

Confirmar que o período está correto na caixa de data
```

### PASSO 6: Adicionar Métrica de Conversão
```
Procure em cima da tabela por:
├─ "Adicionar métrica" (+ sign) → Buscar "Conversões"
├─ Ou "Adicionar métrica" → "Lead Events"

Selecione a coluna que corresponde a LEADS (conversões)

PROCURE POR NOMES COMO:
- "lead"
- "lead_lucro_real"
- "formulario"
- "request_demo"
- "contact"
```

### PASSO 7: Visualizar Dados Completos
```
Sua tabela agora deve ter:

Coluna 1: Caminho da página (URL)
Coluna 2: Sessões (Visualizações totais)
Coluna 3: Usuários
Coluna 4: [Sua métrica de conversão]
Coluna 5: Taxa de eventos (%)

EXEMPLO:
/calculadora-lucro-real/ | 1200 | 800 | 150 leads | 12.5%
```

### PASSO 8: Exportar Dados
```
Botão em cima à direita: "Exportar" ou "Export"
├─ CSV
├─ Google Sheets
└─ Outro formato

RECOMENDADO: CSV (mais fácil de trabalhar)
```

### PASSO 9: Salvar Arquivo
```
Nome: ga4-pages-conversions.csv

Guardar em local seguro (vai precisar depois)
```

### PASSO 10: (OPCIONAL) Google Sheets
```
Se preferir compartilhar via Google Sheets:
1. Copiar dados no GA4
2. Colar em novo Google Sheet
3. Compartilhar link comigo
```

---

## 📝 Formato Esperado do CSV

```
Page,Sessions,Users,Events,Event Conversion Rate
/calculadora-lucro-real/,1245,832,156,12.53%
/blog/reforma-tributaria-2025/,587,421,59,10.05%
/segmentos/contabilidade-especializada-em-transportadora/,312,215,31,9.94%
/,4105,2890,380,9.26%
/filmes-sobre-contabilidade/,801,580,72,8.99%
```

---

## 🔍 Possíveis Problemas e Soluções

### Problema 1: Não vejo métrica de conversões
**Solução:**
- Conversões podem estar com nome diferente
- Procure por "Events" ao invés de "Conversions"
- Se ainda não achar, converse comigo

### Problema 2: Período não há dados
**Solução:**
- Verificar se período (27 Jul - 27 Out) está correto
- Se não, expandir período para "Últimos 3 meses"

### Problema 3: Muitas linhas (500+)
**Solução:**
- Normal! Significa que tem muitas páginas
- Exportar tudo mesmo, é valioso

### Problema 4: Conversão aparece como 0 em todas páginas
**Solução:**
- Significa que conversões não estão rastreadas no GA4
- Trocar para métrica de "Events" genéricos
- Se nenhuma métrica funcionar, coletar manualmente

---

## ✅ Checklist Antes de Enviar

- [ ] Período correto (27 Jul - 27 Out 2025)?
- [ ] Arquivo em CSV ou Google Sheet?
- [ ] Contém pelo menos 50+ linhas (páginas)?
- [ ] Tem coluna de "Conversões" ou "Events"?
- [ ] Arquivo salvo com nome descritivo?

---

## 📤 Como Enviar

Depois de coletar, você pode:

1. **Compartilhar CSV:** Enviar arquivo direto
2. **Google Sheets:** Compartilhar link
3. **Screenshot:** Se tiver problema, tirar print da tela
4. **Upload:** Colocar arquivo em repositório

**Escreva no chat quando tiver pronto!**

---

## ⏱️ Tempo Estimado

- Coletar no GA4: 10-15 minutos
- Exportar CSV: 2-3 minutos
- **Total: ~20 minutos**

---

## 🎯 Próximo Passo Após Coletar

Depois que você enviar GA4 + GSC (que já temos):

1. Consolidar ambos em 1 arquivo final
2. Mapear Old URL → New URL (você decide)
3. Criar estratégia de redirects
4. Implementar em React site
5. Monitorar migração

**Leon vai validar tudo antes de implementar!**

