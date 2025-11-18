# DADOS_INTELIGENCIA — Inteligência, Conhecimento e Dados

**Data:** 16 de novembro de 2025  
**Versão:** 0.2  
**Status:** P1 Completo ✅ | P2 Planejado

---

## 🎯 Objetivo

Centralizar **toda inteligência, dados e conhecimento** que alimentam decisões estratégicas da OSP:

- **Conhecimento estruturado:** Produtos, clientes, processos, FAQ
- **Dados brutos:** GA4, GSC, CRM, Semrush, receitas
- **Análises interpretadas:** Insights com recomendações acionáveis
- **Dashboards e painéis:** Performance de campanhas, receita, etc.
- **Governança:** Acesso, compliance, políticas de retenção

---

## 🚀 Começar Agora

👉 **Novo usuario?** Abra: [`QUICK_START.md`](./QUICK_START.md)  
👉 **Visão geral?** Abra: [`INDEX.md`](./INDEX.md)  
👉 **Acompanhar migração?** Abra: [`MIGRATION_LOG.md`](./MIGRATION_LOG.md)

---

## 📁 Estrutura (Versão 0.2)

### ✅ CONHECIMENTO — Base Estruturada
- **learning/** — FAQ, trilhas, onboarding
  - `learning/FAQ.md` ← 36 FAQs consolidadas (NOVO)
- **solucoes/** — 18 produtos catalogados
  - `solucoes/INDEX.md` ← Catálogo com preços e links (NOVO)
- **personas/** — 4 ICPs mapeados
  - `personas/ICP.md` ← 4 personas estruturadas (NOVO)
- **casos/** — Histórias de sucesso (P3)
- **segmentos/** — Análise de mercado (P3)

### ✅ MARKETING — Estratégia e Campanhas
- **ativos/** — Branding, logos, templates (P2)
- **campanhas/** — Campanhas ativas, briefing, calendário (P2)
- **conteudo/** — Social media, painel semântico (P2)
- **estrategia/** — Reposicionamento, branding (P2)
- **performance/** — Análise de desempenho (P2)

### ✅ VENDAS — Processos Comerciais
- **processos/** — Workflows, cadências
  - `processos/WORKFLOWS.md` ← Cadências de e-mail (NOVO)
- **playbooks/** — Estratégias de abordagem (P2)
- **templates/** — Modelos de propostas (P2)
- **treinamentos/** — Materiais de venda (P2)
- **objecoes/** — Tratamento de objeções (P2)

### 📊 Dados Estruturados (Estrutural)
- **fontes/** — Dumps brutos GA4, GSC, CRM, etc. (P2)
- **analises/** — Interpretações e insights (P2)
- **dashboards/** — Metadados de painéis (P2)
- **modelos/** — Forecasting, LTV, CAC
- **governanca/** — Acesso, compliance, políticas
- **Notion/** — Backup dos 1536 arquivos (referência)

---

## 📊 Estado da Migração

### P1 ✅ Concluído (16/11/2025)
```
✅ COMERCIAL/FAQ (36)            → CONHECIMENTO/learning/FAQ.md
✅ HOME/Produtos (18)            → CONHECIMENTO/solucoes/INDEX.md
✅ COMERCIAL/ICP (4)             → CONHECIMENTO/personas/ICP.md
✅ COMERCIAL/Processos           → VENDAS/processos/WORKFLOWS.md

Total: ~60 arquivos → 4 índices (89% redução)
```

### P2 ⏳ Próxima Semana
```
⏳ INTELIGÊNCIA/Base de Dados    → DADOS_INTELIGENCIA/fontes/
⏳ MARKETING/*                    → MARKETING/
⏳ GESTÃO/Relatórios             → DADOS_INTELIGENCIA/dashboards/

Total: ~200 arquivos → 15 índices
```

### P3 ⏳ Backlog
```
⏳ HOME/Onboarding               → CONHECIMENTO/learning/
⏳ INTELIGÊNCIA/Galeria          → CONHECIMENTO/casos/
⏳ REPOSICIONAMENTO/*            → MARKETING/estrategia/

Total: ~300 arquivos → 10 índices
```

---

## 🔗 Recursos do Google Drive

### Dashboards & Analytics
- [Dashboard Revenue Recognition](https://lookerstudio.google.com/placeholder)
- [KPI Dashboard Executivo](https://lookerstudio.google.com/placeholder)
- [Análise Cohort & LTV](https://docs.google.com/spreadsheets/d/placeholder)
- [Forecast Receita 2025](https://docs.google.com/spreadsheets/d/placeholder)
- [Relatório GA4 Consolidado](https://docs.google.com/spreadsheets/d/placeholder)

### Governança & Dados
- [Política de Acesso a Dados](https://docs.google.com/document/d/placeholder)
- [Dicionário de Dados](https://docs.google.com/spreadsheets/d/placeholder)
- [Matriz Compliance LGPD](https://docs.google.com/spreadsheets/d/placeholder)

**📌 Ver lista completa:** [`planning/technical/GOOGLE_DRIVE_RESOURCES_P6.md`](../planning/technical/GOOGLE_DRIVE_RESOURCES_P6.md)

---

## 🔍 Como Encontrar Informação

| Você quer... | Abra... |
|-------------|---------|
| Perguntas frequentes | `CONHECIMENTO/learning/FAQ.md` |
| Lista de produtos | `CONHECIMENTO/solucoes/INDEX.md` |
| Perfil de cliente | `CONHECIMENTO/personas/ICP.md` |
| Cadência de e-mail | `VENDAS/processos/WORKFLOWS.md` |
| **Modelos de Proposta** | `../COMERCIAL/recursos/01_MODELOS_PROPOSTA.md` |
| **Apresentações Institucionais** | `../COMERCIAL/recursos/02_APRESENTACOES_INSTITUCIONAIS.md` |
| **Playbook OSP** | `../COMERCIAL/recursos/03_PLAYBOOK_DOCUMENTACAO.md` |
| **Dados de Gestão** | `../COMERCIAL/recursos/04_DADOS_PLANILHAS.md` |
| **Índice de Recursos** | `../COMERCIAL/recursos/INDEX.md` |
| Status geral | `MIGRATION_LOG.md` |
| Guia rápido | `QUICK_START.md` |
| Recursos Google Drive | [`planning/technical/GOOGLE_DRIVE_RESOURCES_P6.md`](../planning/technical/GOOGLE_DRIVE_RESOURCES_P6.md) |

---

## 🎯 Origem dos Dados

Toda base migrada do **Notion** mantendo:
- ✅ Conteúdo original
- ✅ Links para Google Docs
- ✅ Estrutura temática
- ✅ Referências cruzadas

**Notion original:** Preservado em `Notion/` para rastreabilidade

---

## 🔗 Dependências e Referências

- `docs/Acessos/` — Permissões de dados (GA4, Ads, GSC, etc.)
- `docs/functions/N8N_WEBHOOK_SETUP.md` — Integrações de dados
- Site OSP — https://ospcontabilidade.com.br
- Google Drive — Links em Soluções (Issue #2)

---

## 📝 Manutenção

Cada pasta tem **README.md** com:
- Status de conteúdo
- Checklist de próximas ações
- Dependências
- Próxima revisão agendada

---

## 📞 Responsáveis

| Área | Responsável | Contato |
|------|-------------|---------|
| CONHECIMENTO | Data Ops | - |
| MARKETING | Marketing Ops | - |
| VENDAS | Sales Ops | - |
| Estrutural | Data Ops | - |

---

## 🚀 Próximas Ações

1. ✅ P1 Concluído (FAQ, Soluções, ICPs, Workflows)
2. ⏳ **P2 Próxima Semana** — Base de Dados, Marketing, Dashboards
3. ⏳ **P3 Backlog** — Onboarding, Casos, Reposicionamento

---

**Última Atualização:** 16 de novembro de 2025  
**Próxima Revisão:** 23 de novembro de 2025 (após P2)
