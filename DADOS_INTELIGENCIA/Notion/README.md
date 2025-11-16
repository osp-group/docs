# Notion — Base de Conhecimento Centralizada

Este diretório replica o workspace do Notion e serve como ponto de partida para distribuir conhecimento em `CONHECIMENTO/`, `MARKETING/`, `OPERACOES/`, `VENDAS/` e `DADOS_INTELIGENCIA`.

## Estrutura da transferência

- `Notion/HOME`: contém `Onboarding` e `Produtos` — materiais de treinamento e apresentação que alimentam `CONHECIMENTO/learning/` e `CONHECIMENTO/solucoes/`.
- `Notion/COMERCIAL`: reúne `Base de Clientes`, `Processos`, `Forecast de Vendas`, `Propostas` e `FAQ`. Deve ser refletido diretamente em `VENDAS/processos/`, `VENDAS/forecast/` (criar se necessário) e `CONHECIMENTO/personas/` quando houver insights de ICP.
- `Notion/MARKETING`: campanhas, estratégia, ativos e performance com links para drives compartilhados. Os guias de Social Media (ex.: `Social Media 1b3311d0c55380379aaecaf0de73ddbe.md`) apontam para pastas do Google Drive em `https://drive.google.com/drive/folders/1Gkp-vc_olXnBsMFl2V0XmaXh-Rh7o47q` e `https://drive.google.com/drive/folders/19XDA5aBWD468md_sQMhjluvRlNMNJQTq`. Esses ativos devem alimentar `MARKETING/ativos/`, `MARKETING/campanhas/` e `DADOS_INTELIGENCIA/dashboards/` (metadados de performance).
- `Notion/GESTÃO`: políticas, rotinas e relatórios — base para `OPERACOES/governanca/` e `DADOS_INTELIGENCIA/governanca/`. Em especial, a pasta `Relatórios` traz listas extensas de campanhas com links para vídeos no Google Drive (ex.: `https://drive.google.com/file/d/1cPdCIkD...`), importantes para o histórico de performance.
- `Notion/INTELIGÊNCIA`: contém `Base de Dados`, `Galeria de Processos` e sub-estruturas de equipe. Use como referência para `DADOS_INTELIGENCIA/analises/`, `DADOS_INTELIGENCIA/fontes/` e `CONHECIMENTO/cases/`.
- `Notion/REPOSICIONAMENTO`: material estratégico para reposicionamento da marca, ideal para `MARKETING/estrategia/` e `CONHECIMENTO/solucoes/`.

## Google Drive & Issue 2

Todos os links do Notion com `drive.google.com` são fonte de arquivos atualizados (vídeos, apresentações, templates). Ao migrar conteúdo para os subdiretórios de dados, mantenha as URLs originais em notas de referência e verifique se a Issue #2 já documenta atualizações específicas de Drive — caso contrário, crie um resumo nela.

## Próximos passos sugeridos

1. Para cada subpasta listada acima, crie sub-README com orientação de conteúdos do Notion que devem ser copiados ou sumarizados.
2. Automatize um log de atualização (ex.: `DADOS_INTELIGENCIA/updates.md`) para registrar quando um link do Drive ou página do Notion for movida ou reformatada.
3. Confirme com a equipe se há relatórios críticos na pasta `Notion/INTELIGÊNCIA/14a311.../Base de Dados` que precisam virar arquivos CSV/MD em `DADOS_INTELIGENCIA/fontes/`.