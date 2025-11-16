# OPERACOES — Processos e Execução

**Data:** 16 de novembro de 2025
**Versão:** 0.1
**Status:** Em estruturação (Opção A)

---

## Objetivo
Reunir todos os processos operacionais (deploy, suporte, atendimento, finanças internas e compliance) em um backbone único, evitando duplicidade entre `docs/deployment/`, `docs/testing/`, `docs/issues/` e arquivos soltos.

## Subpastas Prioritárias
- `processos/`: runbooks, SOPs e fluxos etapa a etapa.
- `workflows/`: diagramas e checklists de squads multifuncionais.
- `qualidade/`: testes, QA, auditorias e planos de contingência.
- `suporte/`: FAQs internas, macros de atendimento e scripts de crise.
- `governanca/`: políticas, SLAs e indicadores de confiabilidade.

## Migração Imediata
1. Mover checklists de deploy e QA de `docs/deployment/` e `docs/testing/` para `processos/` e `qualidade/`.
2. Importar `MAINTENANCE.md` como referência cruzada para garantir rastreio de donos/rotinas.
3. Criar ligação com `scripts/maintenance/` para tarefas automatizadas de operação.
4. Mapear conteúdo de `docs/issues/` que vira procedimento repetível e trazer para esta pasta.

## Dependências e Próximos Passos
- alinhar com equipe de operações para validar SLAs antes de mover conteúdo crítico.
- Atualizar `INDEX_OPERACIONAL.md` apontando para `OPERACOES/`.
- Documentar responsáveis e cadência de revisão em `QUICK_REFERENCE.md`.
