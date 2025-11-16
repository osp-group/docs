# MARKETING — Growth, Conteúdo e Campanhas

**Data:** 16 de novembro de 2025
**Versão:** 0.1
**Status:** Em estruturação (Opção A)

---

## Objetivo
Criar um hub único para estratégia de growth, planejamento editorial, campanhas pagas, ativos criativos e resultados. Este diretório deve substituir a fragmentação atual entre `docs/campaigns/`, `docs/strategy/` e planilhas espalhadas.

## Subpastas Prioritárias
- `estrategia/`: posicionamento, narrativas, calendário de temas e OKRs de marketing.
- `conteudo/`: planos editoriais, briefs de blog, roteiros de vídeo e guidelines de copy.
- `campanhas/`: registros de Google Ads, Meta, ABM, nurture e respectivas retros.
- `ativos/`: bibliotecas de peças (PDF, slides, thumbnails) com metadados e owners.
- `performance/`: dashboards resumidos com highlights e links para `DADOS_INTELIGENCIA/`.

## Migração Imediata
1. Trazer `docs/campaigns/` (Google Ads, CTA audits) para `MARKETING/campanhas/`.
2. Copiar `EDITORIAL_PLAN_BLOG_ARTICLES_NOV2025.md` para `MARKETING/conteudo/`.
3. Linkar `SEO_ANALYTICS_DASHBOARD_NOV2025.md` como referência cruzada com dados.
4. Criar checklist de aprovação alinhado com `docs/design-system/` para garantir consistência visual.

## Dependências e Próximos Passos
- Atualizar `INDEX_GERAL.md` e `NAVIGATION.md` com a nova rota de marketing.
- Criar dossiê de campanhas vivas contendo métricas mínimas (CTR, CPL, ROAS).
- Conectar tasks de growth com automações em `scripts/maintenance/` quando necessário.
