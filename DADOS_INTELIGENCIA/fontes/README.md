# Fontes — Dados Brutos e Originais

**Data:** 16 de novembro de 2025
**Versão:** 0.2
**Status:** P2 Em andamento ⏳

---

## 🎯 Objetivo

Centralizar todos os **dados brutos** (dumps, exports, relatórios) de diferentes fontes internas e externas.

---

## 📁 Estrutura Atual (P2)

### vendas/ — Dados de Pipeline e Histórico
- **2024/** — 72 arquivos (sendo migrado do Notion)
- **2025/** — 60 arquivos (sendo migrado do Notion)
- Status: ⏳ Migração em progresso

### depoimentos/ — Histórias de Clientes
- **4 arquivos** (sendo migrado do Notion)
- Status: ⏳ Migração em progresso

---

## 🚀 Planejamento P2

**Migrando agora:**
- ✅ Estrutura de diretórios criada
- ⏳ Dados de Vendas 2024/2025 → `vendas/`
- ⏳ Depoimentos de Clientes → `depoimentos/`
- ⏳ Criar VENDAS_INDEX.md e DEPOIMENTOS_INDEX.md

**Próximas fontes (P3+):**
- GA4 (Analytics)
- GSC (Search Console)
- CRM (Exact Sales / HubSpot)
- Semrush
- RD Station

---

## 📊 Metadados por Fonte

Cada pasta terá INDEX.md com:
- Origem dos dados
- Tipo de conteúdo
- Frequência de atualização
- Responsável
- Última atualização
- Próxima atualização

---

## 🔗 Dependências

- `DADOS_INTELIGENCIA/analises/` — Interpretações
- `DADOS_INTELIGENCIA/dashboards/` — Visualizações
- `DADOS_INTELIGENCIA/modelosv` — Forecasts

---

**Responsável:** Data Ops
**Última Atualização:** 16 de novembro de 2025
