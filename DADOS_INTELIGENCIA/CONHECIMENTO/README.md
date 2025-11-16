# CONHECIMENTO — Hub Estratégico

**Data:** 16 de novembro de 2025
**Versão:** 0.1
**Status:** Em estruturação (Opção A)

---

## Objetivo
Centralizar tudo o que explica o produto (soluções, segmentos, ICP, diferenciais, estudos de caso e materiais educacionais) em um único hub fácil de navegar. Este diretório substitui a dispersão atual entre `docs/project/`, `docs/analysis/` e planilhas soltas.

## Subpastas Prioritárias
- `solucoes/`: perfis completos das 26 soluções com hero, desafios, aplicações e CTAs.
- `segmentos/`: perfis dos 26 segmentos/ICP com dores, jornada e argumentos de venda.
- `personas/`: personas narrativas e visuais alinhadas às soluções-chave.
- `learning/`: treinamentos rápidos, glossário e listas "start here" para onboarding.
- `cases/`: estudos de caso (PDF/MD) com métricas, depoimentos e playbooks.

## Migração Imediata
1. Mover `docs/project/content/*` para `CONHECIMENTO/solucoes/` mantendo nomes originais.
2. Mover `docs/project/segments/*` para `CONHECIMENTO/segmentos/` e ajustar links nos índices.
3. Copiar `ANALISE_PROFUNDA_BASE_CONHECIMENTO.md` para servir como índice temporário nesta pasta.
4. Atualizar `INDEX_CONHECIMENTO.md` apontando para as novas rotas.

## 🔗 Recursos do Google Drive

### Segmentos & Análises
- [Análise Mercado Agrícola](https://docs.google.com/document/d/placeholder) — Segmento Agrícola
- [Análise Indústrias 4.0](https://docs.google.com/document/d/placeholder) — Setor Industrial
- [Análise Varejo](https://docs.google.com/document/d/placeholder) — Comércio & Varejo
- [Análise Setor Serviços](https://docs.google.com/document/d/placeholder) — Serviços Especializados
- [Análise Educação](https://docs.google.com/document/d/placeholder) — Setor Educacional

### Soluções Core
- [Proposta Contabilidade Standard](https://docs.google.com/document/d/placeholder)
- [Proposta Contabilidade Consultiva](https://docs.google.com/document/d/placeholder)
- [Modelo Lucro Real](https://docs.google.com/spreadsheets/d/placeholder)
- [Guia Holding Familiar](https://docs.google.com/document/d/placeholder)
- [Deck OSP360](https://docs.google.com/presentation/d/placeholder)

**📌 Ver lista completa:** [`planning/technical/GOOGLE_DRIVE_RESOURCES_P6.md`](../../planning/technical/GOOGLE_DRIVE_RESOURCES_P6.md)

---

## Dependências e Próximos Passos
- **Cross-links:** garantir que NAVIGATION, INDEX_GERAL e QUICK_REFERENCE apontem para `CONHECIMENTO/` até 20/nov.
- **Governança:** definir owners (produto + marketing) no `docs/MAINTENANCE.md`.
- **Template:** reutilizar cabeçalho padrão descrito em `STRUCTURE.md` para cada documento migrado.
- **Recursos Drive:** Links para templates, análises e dashboards estão sendo consolidados em GOOGLE_DRIVE_RESOURCES_P6.md

```
