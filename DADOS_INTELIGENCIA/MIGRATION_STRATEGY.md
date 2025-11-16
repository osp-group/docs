# Estratégia de Migração Notion → DADOS_INTELIGENCIA

**Data:** 16 de novembro de 2025
**Total de arquivos:** ~1536 arquivos MD
**Status:** Em planejamento

---

## 1. Visão Geral

A migração do Notion para a estrutura de `DADOS_INTELIGENCIA` segue o mapeamento definido em `mapping.md`. Cada seção do Notion será distribuída conforme abaixo:

### 1.1 Estrutura de Origem (Notion)
- **COMERCIAL/96aa58a095a8468ab98ab9ea3654fded/**: FAQ, Processos, Forecast, Propostas, Home (ICP, Playbook)
- **MARKETING/b31eb47e27ca408fb1cb2da50c82ba9d/ + fab8cf0a2103417a9dca6e145ed3a43c/**: Campanhas, Social Media, Ativos, Calendário
- **INTELIGÊNCIA/14a311d0c553812d8c7300427da1c85f/**: Base de Dados, Galeria de Processos, Gestão
- **GESTÃO/2e17fad0ff084611b7fd75160e9375ae/**: Relatórios, Equipe, Reuniões
- **HOME/db8ec75569f7421699c76c201767ae4b/**: Onboarding, Produtos
- **REPOSICIONAMENTO/21d311d0c5538150aa0f0042be5729f2/**: Branding, Site

### 1.2 Estrutura de Destino (DADOS_INTELIGENCIA)
```
DADOS_INTELIGENCIA/
├── CONHECIMENTO/
│   ├── learning/         ← HOME/Onboarding + Treinamentos
│   ├── solucoes/         ← HOME/Produtos + Reposicionamento
│   ├── personas/         ← COMERCIAL/ICP + CONHECIMENTO de clientes
│   ├── casos/            ← INTELIGÊNCIA/Galeria de Processos
│   └── segmentos/        ← COMERCIAL/Base de Clientes
├── MARKETING/
│   ├── ativos/           ← MARKETING/Ativos de marca, Apresentações
│   ├── campanhas/        ← MARKETING/Campanhas, Briefing, Calendário
│   ├── conteudo/         ← MARKETING/Social Media, Painel Semântico
│   ├── estrategia/       ← REPOSICIONAMENTO + MARKETING estratégico
│   └── performance/      ← Relatórios de performance
├── OPERACOES/
│   ├── governanca/       ← GESTÃO/Políticas + DADOS_INTELIGENCIA/governanca
│   ├── processos/        ← COMERCIAL/Processos + GESTÃO/Rotinas
│   └── workflows/        ← Cadências e workflows
├── VENDAS/
│   ├── processos/        ← COMERCIAL/Processos de venda
│   ├── forecast/         ← COMERCIAL/Forecast
│   ├── opportunities/    ← COMERCIAL/Propostas
│   └── personas/         ← COMERCIAL/ICP (cópia de referência)
└── DADOS_INTELIGENCIA/
    ├── fontes/           ← Arquivos CSV/JSON brutos
    ├── analises/         ← Sínteses e insights
    ├── dashboards/       ← Descrição de painéis
    ├── governanca/       ← Políticas e compliance
    ├── modelos/          ← Forecasting, LTV, CAC
    └── Notion/           ← Backup/Referência do Notion
```

---

## 2. Plano de Migração por Categoria

### 2.1 COMERCIAL → VENDAS, CONHECIMENTO, DADOS_INTELIGENCIA

**Subpastas:** FAQ, Processos, Forecast, Propostas, Home (ICP, Playbook)

| Origem | Destino | Ação |
|--------|---------|------|
| COMERCIAL/Home/ICP* | CONHECIMENTO/personas/ + VENDAS/personas/ | **Copiar** - sintetizar em MD com links |
| COMERCIAL/Home/Playbook | VENDAS/processos/ | **Copiar** - versão consolidada |
| COMERCIAL/FAQ | CONHECIMENTO/learning/ | **Copiar** - criar índice temático |
| COMERCIAL/Processos/* | VENDAS/processos/ + OPERACOES/workflows/ | **Copiar** - Cadência de e-mails → workflows |
| COMERCIAL/Forecast* | VENDAS/forecast/ + DADOS_INTELIGENCIA/modelos/ | **Copiar** - se houver dados, mover para fontes/ |
| COMERCIAL/Propostas | VENDAS/opportunities/ | **Copiar** - templates e histórico |

### 2.2 MARKETING → MARKETING (centralizado)

**Subpastas:** Endomarketing, Social Media, Ativos, Briefing, Calendário, Apresentação, Painel Semântico

| Origem | Destino | Ação |
|--------|---------|------|
| MARKETING/Ativos de marca | MARKETING/ativos/ | **Copiar** - logos, guidelines |
| MARKETING/Social Media | MARKETING/conteudo/ + MARKETING/campanhas/ | **Copiar** - agrupar por tipo |
| MARKETING/Briefing de campanha | MARKETING/campanhas/ | **Copiar** - criar índice |
| MARKETING/Calendário de conteúdo | MARKETING/performance/ | **Copiar** - referência de planos |
| MARKETING/Painel semântico | MARKETING/conteudo/ | **Copiar** - pilares e palavras-chave |
| MARKETING/Apresentação | MARKETING/ativos/ | **Copiar** - deck template |
| MARKETING/Endomarketing | OPERACOES/processos/ | **Copiar** - comunicação interna |

### 2.3 INTELIGÊNCIA → DADOS_INTELIGENCIA, CONHECIMENTO

**Subpastas:** Base de Dados, Galeria de Processos, Gestão

| Origem | Destino | Ação |
|--------|---------|------|
| INTELIGÊNCIA/Base de Dados/* | DADOS_INTELIGENCIA/fontes/ | **Copiar** - CSV/JSON brutos |
| INTELIGÊNCIA/Base de Dados (análises) | DADOS_INTELIGENCIA/analises/ | **Copiar** - insights e métricas |
| INTELIGÊNCIA/Galeria de Processos | CONHECIMENTO/casos/ | **Copiar** - jornadas de clientes |
| INTELIGÊNCIA/Gestão | DADOS_INTELIGENCIA/governanca/ | **Copiar** - políticas de dados |

### 2.4 GESTÃO → OPERACOES, DADOS_INTELIGENCIA

**Subpastas:** Relatórios, Equipe, Reuniões

| Origem | Destino | Ação |
|--------|---------|------|
| GESTÃO/Relatórios | DADOS_INTELIGENCIA/dashboards/ | **Copiar** - metadados (título, owner, atualização) |
| GESTÃO/Equipe | OPERACOES/processos/ | **Copiar** - organogramas, contatos |
| GESTÃO/Reuniões | OPERACOES/processos/ | **Copiar** - atas e agendas |

### 2.5 HOME → CONHECIMENTO

**Subpastas:** Onboarding, Produtos

| Origem | Destino | Ação |
|--------|---------|------|
| HOME/Onboarding | CONHECIMENTO/learning/ | **Copiar** - trilhas e guias |
| HOME/Produtos/* | CONHECIMENTO/solucoes/ | **Copiar** - descrição de ofertas |

### 2.6 REPOSICIONAMENTO → MARKETING, CONHECIMENTO

**Subpastas:** Branding, Site

| Origem | Destino | Ação |
|--------|---------|------|
| REPOSICIONAMENTO/Branding* | MARKETING/estrategia/ + MARKETING/ativos/ | **Copiar** - guidelines novos |
| REPOSICIONAMENTO/Site | MARKETING/estrategia/ | **Copiar** - briefing e roadmap |

---

## 3. Abordagem Técnica

### 3.1 Fase 1: Auditoria e Catalogação (Manual)
1. Listar todos os arquivos por categoria
2. Identificar tipos: Markdown, CSV, JSON, imagens, links externos
3. Criar mapa de referências cruzadas
4. Documentar links de Google Drive (Issue #2)

### 3.2 Fase 2: Migração Estruturada
**Opcão A (Recomendada): Cópia seletiva com síntese**
- Copiar estrutura de diretórios
- Sintetizar arquivos em Markdown consolidado
- Criar índices temáticos
- Manter referências ao Notion original

**Opção B: Migração literal**
- Copiar todos os 1536 arquivos as-is
- Criar apenas índices e README
- Conservar estrutura de hash do Notion

### 3.3 Fase 3: Validação e Limpeza
1. Criar README em cada pasta destino
2. Registrar todas as migrações em log
3. Testar referências cruzadas
4. Remover ou arquivar conteúdo obsoleto

---

## 4. Priorização Imediata

**P1 (Essa semana):**
- [ ] COMERCIAL/FAQ → CONHECIMENTO/learning/
- [ ] COMERCIAL/ICP → CONHECIMENTO/personas/
- [ ] HOME/Produtos → CONHECIMENTO/solucoes/

**P2 (Próxima semana):**
- [ ] INTELIGÊNCIA/Base de Dados → DADOS_INTELIGENCIA/fontes/
- [ ] MARKETING/* → MARKETING/ativos/, campanhas/
- [ ] GESTÃO/Relatórios → DADOS_INTELIGENCIA/dashboards/

**P3 (Backlog):**
- [ ] Arquivos menores e menos críticos
- [ ] Consolidação final e limpeza

---

## 5. Referências Externas

- Links de Google Drive: Serão catalogados em `DRIVE_REFERENCES.md`
- Issue #2: Compliance e rastreabilidade
- `mapping.md`: Detalhes de mapeamento

---

## 6. Próximos Passos

1. **Validar com o time**: Confirmar prioridades e abordagem
2. **Executar Fase 1**: Auditoria completa
3. **Criar scripts**: Automação de cópia/consolidação se necessário
4. **Documentar**: Cada movimento registrado

**Responsável:** Data Ops / Documentação
**Status:** Aguardando aprovação
