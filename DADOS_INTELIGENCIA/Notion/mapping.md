# Mapeamento Notion → DADOS_INTELIGENCIA e Squads

Este arquivo sintetiza onde cada área do Notion (HOME, COMERCIAL, MARKETING, GESTÃO, INTELIGÊNCIA, REPOSICIONAMENTO) deve desembarcar dentro da nova estrutura centralizada.

## CONHECIMENTO
- `Notion/HOME/Onboarding`: transforma-se em guias de boas-vindas e trilhas em `CONHECIMENTO/learning/`.
- `Notion/HOME/Produtos`: base para `CONHECIMENTO/solucoes/` e `CONHECIMENTO/cases/`, especialmente quando há argumentos comerciais (ex.: estudo tributário, LTV, ICP).
- `Notion/COMERCIAL/Base de Clientes` e `FAQ`: insumos para `CONHECIMENTO/personas/` e `CONHECIMENTO/segmentos/`, mantendo notas contextuais com links de Drive sempre que houver templates ou provas sociais.
- `Notion/INTELIGÊNCIA/Galeria de Processos`: transforme em `CONHECIMENTO/cases/` ilustrando jornadas e resultados de clientes.

## MARKETING
- `Notion/MARKETING/*`: cada pasta hash contém campanhas, briefs e ativos. Copie ou resuma em `MARKETING/ativos/`, `MARKETING/campanhas/` e `MARKETING/estrategia/` conforme o tipo (ex.: Social Media, Performance, Brand). Identifique os links internos para `drive.google.com/drive/folders/1Gkp-vc...` e `...19XDA5` e cite-os em notas anexas aos ativos.
- `Notion/REPOSICIONAMENTO`: estratégias de reposicionamento vão para `MARKETING/estrategia/` e referenciam `CONHECIMENTO/solucoes/` sempre que houver reposicionamento de ofertas.
- `Notion/GESTÃO/Relatórios`: use as colunas/links (vídeos `drive.google.com/file/d/...`) para alimentar `DADOS_INTELIGENCIA/dashboards/` com metadados de performance e indicadores associados.

## OPERACOES
- `Notion/GESTÃO/Processos`, `Rotina - Pré-venda`, `Gestão 14a...`: alinhe com `OPERACOES/processos/` e `OPERACOES/workflows/` para documentar ritmos e SLAs.
- `Notion/GESTÃO/Políticas` e `Governança`: mova ou resuma em `OPERACOES/governanca/` e espelhe em `DADOS_INTELIGENCIA/governanca/`, especialmente informações sobre acessos (issue #2) e compliance de dados.

## VENDAS
- `Notion/COMERCIAL/Processos`, `Forecast de Vendas`, `Propostas`: concentre em `VENDAS/processos/`, `VENDAS/forecast/` (criar se necessário) e `VENDAS/opportunities/` com tabelas exportadas ou templates. Mantenha os arquivos `FAQ` e `Base de Clientes` como referência para `VENDAS/personas/` e onboarding.
- `Notion/Home/Base de Dados/Vendas`: armazene os CSV (ex.: `Vendas 2025...csv`) em `DADOS_INTELIGENCIA/fontes/` se forem dados históricos ou em `VENDAS/dados/` se forem métricas de forecast.

## DADOS_INTELIGENCIA
- `Notion/INTELIGÊNCIA/Base de Dados`: mova os arquivos `.md` e `.csv` substanciais para `DADOS_INTELIGENCIA/fontes/` e descreva-os em `DADOS_INTELIGENCIA/analises/` com insights/resultados.
- `Notion/INTELIGÊNCIA/Galeria de Processos` e `Base de Dados`: use como histórico de análises e colecione resumos em `DADOS_INTELIGENCIA/analises/` para alimentar apresentações e dashboards.
- `Notion/GESTÃO/Relatórios`: cada relatório com link de vídeo vira um card em `DADOS_INTELIGENCIA/dashboards/`, incluindo datas de publicação e resultados (link para `drive.google.com/file/d/...`).
- `Notion/Notion`: mantenha esta pasta atualizada e use o novo `DADOS_INTELIGENCIA/Notion/README.md` para guiar a transferência contínua.

## Google Drive & Issue #2
- Sempre que uma nota apontar para `drive.google.com`, registre o link na pasta destino (`*_links.md`, por exemplo). Isso garante que, mesmo que os arquivos permaneçam no Drive, o time possa localizar a referência rapidamente.
- Consulte a Issue #2 antes de remover ou renomear qualquer link externo e registre lá (ou crie um resumo) para rastreabilidade.

## Próximas ações sugeridas
1. Criar `README.md` suplementares em `CONHECIMENTO`, `MARKETING`, `OPERACOES`, `VENDAS` e `DADOS_INTELIGENCIA` destacando quais blocos do Notion já foram aterrados.
2. Priorizar os arquivos definidos acima (ex.: FAQs e Social Media) para serem convertidos em MD ou CSV dentro da pasta destino.
3. Estabelecer um log central (ex.: `DADOS_INTELIGENCIA/updates.md`) para registrar quando novos conteúdos do Notion/Drive são migrados ou versionados.