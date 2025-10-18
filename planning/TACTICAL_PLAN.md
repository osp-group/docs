# 🚀 OSP Contabilidade - Plano de Implementação Tático

**Data:** 16 de Outubro de 2025  
**Objetivo:** Lançar novo site preservando SEO/performance + integração CRM + mensuração completa

---

## 📊 FASE 0: Status Atual (Enquanto CRM Deploya)

### ✅ Já Temos:
- Site atual WordPress no ar (osp.com.br)
- Site novo React/Firebase pronto (osp-website-2026.web.app)
- CRM Twenty deployando no Render.com
- Firestore configurado
- Google Workspace (e-mail) funcionando

### ⏳ Em Progresso:
- Deploy do CRM no Render (aguardando build)
- Integração website → CRM via Firebase Functions

---

## 🎯 ENTREGA 1: Inventário SEO + Plano de 301 (URGENTE)

### Páginas Must-Keep (Mapear URLs Atuais)

**Prioridade ALTA** (geram tráfego orgânico):
```
/contabilidade-para-industrias/
/contabilidade-lucro-real/
/calculadora-lucro-real/
/reforma-tributaria-2026/
/blog/ (principais artigos)
```

**Prioridade MÉDIA** (campanhas ativas):
```
/servicos/
/sobre/
/contato/
/resultados/
```

### Ações Imediatas:

1. **Exportar Google Analytics 4** (últimos 6 meses):
   ```
   Top 50 páginas por:
   - Sessões orgânicas
   - Conversões (preenchimento de formulário)
   - Taxa de conversão
   ```

2. **Exportar Search Console**:
   ```
   - URLs com impressões > 1000
   - Queries com cliques > 50
   - Páginas com CTR > 3%
   ```

3. **Criar mapa de redirecionamentos**:
   ```
   WordPress URL → React URL
   /servicos/contabilidade-industria/ → /solucoes/industrias
   /calculadora/ → /ferramentas/calculadora-lucro-real
   ```

### Arquivo para Criar:
`/osp-contabilidade/public/redirects.json`

---

## 🎯 ENTREGA 2: GA4 + UTMs + Pixels/CAPI

### 2.1 Configurar GA4 Completo

**Eventos Prioritários** (criar em todo o site):

```javascript
// client/src/lib/analytics.ts

export const trackEvent = (eventName: string, params?: object) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, params);
  }
};

// Eventos principais:
export const events = {
  // Navegação
  page_view: (page_title: string, page_path: string) => 
    trackEvent('page_view', { page_title, page_path }),
  
  // Interações
  view_solution: (solution_name: string) => 
    trackEvent('view_item', { 
      item_category: 'solucao',
      item_name: solution_name 
    }),
  
  // Conversões
  generate_lead: (form_type: string, solution: string) => 
    trackEvent('generate_lead', { 
      form_type,
      solution,
      value: 1 
    }),
  
  // WhatsApp
  whatsapp_click: (page: string, solution: string) =>
    trackEvent('whatsapp_iniciado', { page, solution }),
  
  // Downloads
  download_material: (material_name: string) =>
    trackEvent('download', { material_name })
};
```

### 2.2 Padrão de UTMs

**Template para todas as campanhas**:
```
https://osp.com.br/[pagina]?
  utm_source=[google|meta|linkedin|email]
  &utm_medium=[cpc|social|email|organic]
  &utm_campaign=[nome-campanha-descritivo]
  &utm_content=[variacao-criativo]
  &utm_term=[palavra-chave] (só Google Ads)
```

**Exemplos práticos**:
```
Meta Ads - Indústrias:
utm_source=meta&utm_medium=cpc&utm_campaign=industrias-q4-2025&utm_content=video-producao

Google Ads - Lucro Real:
utm_source=google&utm_medium=cpc&utm_campaign=lucro-real-generico&utm_term=contador-lucro-real

LinkedIn - GESTÃO360:
utm_source=linkedin&utm_medium=social&utm_campaign=gestao360-lancamento&utm_content=carrossel-dashboard
```

### 2.3 Meta Pixel + CAPI

**Já implementado no site atual?** Se sim, migrar para o novo:

```typescript
// client/src/lib/meta-pixel.ts

export const fbq = (...args: any[]) => {
  if (typeof window !== 'undefined' && window.fbq) {
    window.fbq(...args);
  }
};

// Eventos padronizados
export const metaEvents = {
  pageView: () => fbq('track', 'PageView'),
  
  viewContent: (contentName: string, contentCategory: string) =>
    fbq('track', 'ViewContent', {
      content_name: contentName,
      content_category: contentCategory
    }),
  
  lead: (solution: string, value: number = 100) =>
    fbq('track', 'Lead', {
      content_name: solution,
      value: value,
      currency: 'BRL'
    }),
  
  // IMPORTANTE: Evento customizado para ICP qualificado
  leadQualified: (solution: string, value: number = 500) =>
    fbq('trackCustom', 'LeadQualificado', {
      solution,
      value,
      currency: 'BRL'
    })
};
```

**CAPI (Conversions API)** - Implementar via Firebase Function:
```
Fluxo: CRM status change → Firebase Function → Meta CAPI
Eventos: Desqualificado, ICP, Proposta, Ganho (VITAL!)
```

---

## 🎯 ENTREGA 3: Forms Fase 1 (Manter ActiveCampaign) + WhatsApp

### 3.1 Manter Formulários Atuais (Transição Segura)

**Estratégia**:
1. Manter embeds do ActiveCampaign nas páginas principais
2. Make.com continua integrando AC → CRM atual
3. **Novo**: Adicionar webhook para Firebase → CRM Twenty (paralelo)

### 3.2 WhatsApp com Pré-Captação ⭐ INOVAÇÃO

**Implementação inteligente**:

```typescript
// client/src/components/WhatsAppButton.tsx

interface WhatsAppLead {
  name?: string;
  phone?: string;
  solution: string;
  segment?: string;
  revenue?: string;
}

export const WhatsAppButton = ({ solution, pageName }: Props) => {
  const handleWhatsAppClick = async () => {
    // 1. Capturar informações básicas
    const lead: WhatsAppLead = {
      solution,
      segment: detectSegmentFromPage(pageName)
    };
    
    // 2. Salvar no CRM antes de abrir WhatsApp
    await saveToCRM(lead);
    
    // 3. Trackear evento
    trackEvent('whatsapp_click', {
      solution,
      page: pageName
    });
    
    // 4. Mensagem pré-formatada
    const message = createWhatsAppMessage(solution);
    
    // 5. Abrir WhatsApp
    window.open(
      `https://wa.me/5511999999999?text=${encodeURIComponent(message)}`,
      '_blank'
    );
  };
  
  return <button onClick={handleWhatsAppClick}>...</button>;
};

// Mensagem contextual por solução
const createWhatsAppMessage = (solution: string) => {
  const messages = {
    'TRIBUTA360': 'Olá! Estou interessado no TRIBUTA360 para otimizar a carga tributária da minha empresa.',
    'GESTÃO360': 'Olá! Quero conhecer o GESTÃO360 para ter dados financeiros em tempo real.',
    'HOLDING360': 'Olá! Gostaria de entender como uma holding pode proteger meu patrimônio.'
  };
  
  return messages[solution] || 'Olá! Vim pelo site da OSP e gostaria de mais informações.';
};
```

**Vantagens**:
- ✅ Lead já está no CRM antes mesmo de responder
- ✅ Contexto da página/solução registrado
- ✅ Mensagem personalizada = melhor UX
- ✅ SDR já sabe de onde veio e o que interessa

### 3.3 Roteiro de Qualificação SDR

**Perguntas-chave por telefone/WhatsApp**:

```
1. SEGMENTO
   "Qual o segmento principal da sua empresa?"
   → Indústria, Comércio, Serviços, Tecnologia, Saúde, etc.

2. FATURAMENTO ANUAL
   "Faturamento aproximado por ano?"
   → < R$ 500k, R$ 500k-2M, R$ 2M-10M, > R$ 10M
   
3. REGIME TRIBUTÁRIO ATUAL
   "Hoje vocês são Simples, Lucro Presumido ou Real?"
   
4. DOR PRINCIPAL (adaptar ao Guia de Linguagem)
   "O que te trouxe até a OSP? Está pagando muito imposto, precisa de mais controle ou quer crescer com segurança?"
   → Tributário, Gestão, Expansão/Holding

5. URGÊNCIA
   "Quando precisa de uma solução rodando?"
   → Imediato (< 30 dias), Curto prazo (1-3 meses), Planejamento (> 3 meses)
```

**ICP Score Automático** (implementar no CRM):
```
Pontuação:
- Faturamento > R$ 2M: +3 pontos
- Indústria/Tecnologia/Saúde: +2 pontos  
- Lucro Real ou quer migrar: +2 pontos
- Dor = Tributário/Gestão: +2 pontos
- Urgência < 3 meses: +1 ponto

≥ 7 pontos = ICP FORTE (prioridade SDR)
4-6 pontos = ICP MÉDIO (cadência padrão)
< 4 pontos = DESQUALIFICAR ou nutrir
```

---

## 🎯 ENTREGA 4: Dashboard CAC/LTV (BI de Marketing)

### Métricas Prioritárias

**Painel Principal** (atualização semanal):

```
┌─────────────────────────────────────────────┐
│ FUNIL DE MARKETING                          │
├─────────────────────────────────────────────┤
│ Investimento Mídia: R$ X,XXX               │
│ Impressões: XXX,XXX                         │
│ Cliques: X,XXX (CTR: X.XX%)                │
│ CPCmédio: R$ X.XX                          │
│                                             │
│ Leads Gerados: XXX (CPL: R$ XXX)           │
│ └─ ICP: XX% (CPL ICP: R$ XXX) ⭐          │
│                                             │
│ Reuniões Agendadas: XX (XX%)               │
│ Propostas Enviadas: XX (XX%)               │
│ Ganhos: XX (Win Rate: XX%)                 │
│                                             │
│ CAC Total: R$ X,XXX                        │
│ LTV Médio: R$ XX,XXX                       │
│ LTV/CAC: X.Xx (meta: > 3.0)               │
└─────────────────────────────────────────────┘
```

**Quebras Importantes**:
- Por solução (TRIBUTA360, GESTÃO360, etc.)
- Por segmento (Indústria, Tecnologia, Saúde...)
- Por origem (Google Ads, Meta, Orgânico, LinkedIn)
- Por criativo/campanha

### Fontes de Dados

```
Marketing:
- Google Ads API → Investimento, Impressões, Cliques, Conversões
- Meta Ads API → Investimento, Impressões, Cliques, Leads
- GA4 → Sessões, Eventos, Conversões por origem

CRM (quando pronto):
- Leads criados por origem/UTM
- Status: Desqualificado, ICP, Reunião, Proposta, Ganho
- Valor do contrato (LTV)
- Data de fechamento (Payback)
```

### Implementação Rápida

**Opção 1: Google Sheets + Looker Studio** (grátis, rápido)
- Conectores nativos para Ads/GA4
- CRM exporta CSV semanal via script
- Atualização manual do LTV por contrato

**Opção 2: Metabase + PostgreSQL** (profissional)
- CRM já está no PostgreSQL
- Importar dados de Ads via scripts
- Dashboards em tempo real

---

## 🎯 ENTREGA 5: MVP CRM (4 Módulos Core)

### Já Está Deployando! 

**O Twenty CRM que estamos subindo tem:**

✅ **1. Leads** (People + Companies)
✅ **2. Pipeline** (Opportunities com stages personalizáveis)
✅ **3. Agenda & Reuniões** (Tasks + Calendar integration)
✅ **4. API GraphQL** (para eventos de conversão)

### Personalização Necessária (Pós-Deploy)

**1. Customizar Stages do Pipeline**:
```
Inbound:
- Novo Lead
- Qualificação (SDR)
- Reunião Agendada
- Proposta Enviada
- Negociação
- Ganho 🎉 / Perdido ❌

Outbound:
- Prospecção
- Contato Inicial
- Qualificado
- Demonstração
- Proposta
- Ganho 🎉 / Perdido ❌
```

**2. Campos Personalizados**:
```
Person (Lead):
- Segmento (dropdown)
- Faturamento Anual (dropdown)
- Regime Tributário (dropdown)
- ICP Score (número 0-10)
- UTM Source, Medium, Campaign (texto)

Company:
- CNPJ
- Setor
- Número de funcionários
- Faturamento anual

Opportunity:
- Solução (TRIBUTA360, GESTÃO360, etc.)
- Valor Estimado (R$)
- Data de Fechamento Prevista
- Probabilidade (%)
```

**3. Automações** (Workflows do Twenty):
```
Quando Lead criado com ICP Score ≥ 7:
→ Atribuir para SDR automaticamente
→ Criar tarefa "Ligação de qualificação" (SLA: 2h)
→ Enviar notificação Slack

Quando Reunião marcada:
→ Enviar evento para Meta CAPI (Lead Qualificado)
→ Criar task de follow-up automático

Quando Ganho:
→ Enviar evento para Google Ads (Conversion)
→ Enviar para Meta CAPI com valor real do contrato
→ Criar onboarding automático (V1 futura)
```

---

## 🎯 ENTREGA 6: SEO Orientado a Receita

### Páginas-Matriz por Solução

**Estrutura SEO Otimizada**:

```
/solucoes/tributa360/
- H1: TRIBUTA360 - Planejamento Tributário Estratégico
- Meta Description com CTA
- Seções: O que é, Como funciona, Benefícios, Casos, CTA
- Schema.org: Service + Organization
- Internal links para segmentos relacionados

/solucoes/gestao360/
/solucoes/precifica360/
/solucoes/holding360/
...etc
```

**Implementar no React**:
```typescript
// client/src/pages/solucoes/[solution].tsx

export async function generateMetadata({ params }) {
  const solution = getSolutionData(params.solution);
  
  return {
    title: `${solution.name} - ${solution.tagline} | OSP Contabilidade`,
    description: solution.metaDescription,
    openGraph: {
      title: solution.name,
      description: solution.ogDescription,
      images: [solution.ogImage]
    },
    alternates: {
      canonical: `https://osp.com.br/solucoes/${params.solution}`
    }
  };
}
```

### Ferramentas/Calculadoras

**Prioridade** (geram leads qualificados):

1. **Calculadora Lucro Real vs Presumido**
   - URL: `/ferramentas/calculadora-tributaria`
   - Coleta: Faturamento, Despesas, Segmento
   - Resultado: Economia potencial + CTA "Fale com Especialista"

2. **Estimador de Impacto da Reforma 2026**
   - URL: `/reforma-tributaria-2026/simulador`
   - Coleta: Regime atual, Faturamento, Estado
   - Resultado: Cenários 2026/2027 + oferta TRIBUTA360

3. **ROI de Contabilidade Consultiva**
   - URL: `/ferramentas/roi-contabilidade-consultiva`
   - Coleta: Tamanho da empresa, Frequência de decisões
   - Resultado: Valor potencial + oferta GESTÃO360

---

## 📅 CRONOGRAMA SUGERIDO (Próximas 4 Semanas)

### Semana 1 (Atual)
- [x] Deploy CRM no Render (em andamento)
- [ ] Inventário SEO completo (URLs prioritárias)
- [ ] Implementar GA4 + eventos no site novo
- [ ] Configurar Meta Pixel + eventos personalizados

### Semana 2
- [ ] Criar plano de 301 redirects
- [ ] Implementar WhatsApp com pré-captação
- [ ] Integração site → CRM via Firebase Function
- [ ] Configurar campos personalizados no CRM

### Semana 3
- [ ] Testes de integração completa
- [ ] Configurar Meta CAPI (offline conversions)
- [ ] Dashboard BI inicial (Sheets/Looker Studio)
- [ ] Treinamento SDR com novo roteiro

### Semana 4
- [ ] Go-live site novo no domínio principal
- [ ] Monitoramento intensivo (SEO, conversões, CRM)
- [ ] Ajustes finos baseados em dados reais
- [ ] Planejamento V1 do CRM (onboarding)

---

## 💰 Impacto Esperado (Hipóteses)

### Melhorias Estimadas:

```
Taxa de Conversão (Visitante → Lead):
Atual: ~2%
Meta: 3-4% (melhores CTAs, WhatsApp, UX)
= +50% leads com mesmo tráfego

Qualificação ICP:
Atual: ~30% leads viram ICP
Meta: 45-50% (roteiro estruturado, scoring)
= Mais eficiência SDR, menos tempo perdido

Win Rate:
Atual: ~15-20% (estimativa)
Meta: 25-30% (leads mais qualificados, follow-up melhor)
= Mais receita por lead

CAC/LTV:
Atual: Não mensurado
Meta: LTV/CAC > 3.0 (sustentável para escalar mídia)
```

---

## 🎯 Próximos Passos IMEDIATOS (Enquanto CRM Deploya)

### Você pode fazer AGORA:

1. **Exportar dados GA4** (últimos 6 meses)
   - Comportamento > Páginas e telas
   - Aquisição > Tráfego > Fontes/mídias
   - Eventos > Conversões

2. **Listar URLs do WordPress**
   - Instalar plugin "Export All URLs" ou similar
   - Exportar lista completa
   - Destacar páginas com > 100 visitas/mês

3. **Revisar campanhas atuais**
   - Google Ads: grupos de anúncios ativos
   - Meta Ads: conjuntos de anúncios ativos
   - Listar URLs de destino e UTMs usados

4. **Documentar formulários atuais**
   - Quantos formulários existem?
   - Onde estão? (páginas)
   - Para onde enviam? (ActiveCampaign?)
   - Taxa de conversão conhecida?

---

**Quer que eu crie arquivos específicos para alguma dessas entregas?** 

Por exemplo:
- Template de eventos GA4 completo
- Planilha de UTMs padronizada
- Código do WhatsAppButton com pré-captação
- Dashboard CAC/LTV no Looker Studio
- Campos personalizados para o CRM

**Só me avisar e eu gero o código pronto para usar!** 🚀
