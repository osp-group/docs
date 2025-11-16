# DADOS_INTELIGENCIA — Insights, Métricas e Fontes

**Data:** 16 de novembro de 2025
**Versão:** 0.1
**Status:** Em estruturação (Opção A)

---

## Objetivo
Concentrar todas as fontes de dados (GA4, GSC, CRM, planilhas de receita, pesquisas) e análises interpretadas que alimentam decisões de produto, marketing e vendas. Este diretório trabalha em parceria com `MARKETING/performance/` e `VENDAS/processos/`.

## Subpastas Prioritárias
- `fontes/`: dumps brutos (CSV/JSON) vindos de GA4, GSC, HubSpot, RD, Semrush etc.
- `dashboards/`: descrições de painéis, owners, filtros críticos e limites de atualização.
- `analises/`: leituras interpretadas (SEO, Ads, Revenue) com recomendações acionáveis.
- `modelos/`: planilhas de forecasting, cohort, LTV e CAC compartilhadas.
- `governanca/`: documentação de acesso, compliance e políticas de retenção.

## Migração Imediata
1. Mover `docs/analytics/`, `docs/performance/` e `docs/reports/` relevantes para subpastas específicas.
2. Conectar `INDICE_DADOS_ANALYTICS_COMPLETO.md` como índice mestre dentro desta pasta.
3. Vincular `docs/Acessos/` (assim que criado) na seção de governança para garantir rastreabilidade.
4. Criar log de atualização automática para cada dashboard crítico.

## Dependências e Próximos Passos
- Validar permissões listadas em `docs/functions/N8N_WEBHOOK_SETUP.md`.
- Mapear owners por fonte (Data Ops, Marketing Ops) e registrar em `MAINTENANCE.md`.
- Automatizar alertas de atualização (cron) adicionando scripts em `scripts/maintenance/` quando necessário.
