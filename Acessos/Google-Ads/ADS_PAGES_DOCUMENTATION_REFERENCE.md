# 📚 ADS PAGES DOCUMENTATION - REFERENCE GUIDE

**Data:** 13 de novembro de 2025
**Version:** 1.0
**Última atualização:** Após validação final de todas as 4 páginas

---

## 📖 ÍNDICE

1. [Overview Geral](#overview-geral)
2. [Estrutura de Pastas](#estrutura-de-pastas)
3. [Componentes Utilizados](#componentes-utilizados)
4. [Padrões de Implementação](#padrões-de-implementação)
5. [Metadata & SEO](#metadata--seo)
6. [Analytics & Tracking](#analytics--tracking)
7. [Design & Styling](#design--styling)
8. [Como Criar Nova Página](#como-criar-nova-página)
9. [Checklist de Validação](#checklist-de-validação)

---

## Overview Geral

### O que são Ads Pages?

Ads Pages são landing pages otimizadas para anúncios pagos (Google Ads, Facebook Ads, etc). Diferem das páginas normais por terem:
- ✅ Metadata com `robots: index: false` (não indexar no Google)
- ✅ Foco 100% em conversão (form ou WhatsApp)
- ✅ Sem navegação principal (hero direto)
- ✅ Tracking analítico detalhado em cada CTA
- ✅ Copy agressivo com numbers e urgency

### Estratégia de 2 Variantes

Para cada **solução/segmento**, criamos **2 páginas ads**:

1. **Form Variant** (tradicional)
   - URL: `/ads/solucao-nome`
   - CTA: Formulário embedded
   - Copy: Foco em "Proposta Personalizada"
   - Ideal para: Lead quality, email capture

2. **WhatsApp Variant** (mobile-first)
   - URL: `/ads/solucao-nome-wa`
   - CTA: Botões WhatsApp + Floating button
   - Copy: Foco em "48h via WhatsApp"
   - Ideal para: Engagement, speed, mobile

### Exemplo Real: Lucro Real

| Aspecto | Form Variant | WhatsApp Variant |
|---------|--------------|------------------|
| URL | `/ads/contabilidade-lucro-real` | `/ads/contabilidade-lucro-real-wa` |
| Hero | AdsHeroSection + FormExpanded | Custom hero + WhatsAppDirectCTA |
| CTA Principal | Form inline (embedded) | WhatsApp buttons |
| Floating Button | Sticky form button | WhatsAppSticky (premium) |
| Copy | "Proposta personalizada em 48h" | "Resposta em 5 min via WhatsApp" |
| Best For | Desktop users, form lovers | Mobile users, mobile-first |

---

## Estrutura de Pastas

### Layout Padrão

```
next-migration/src/app/ads/
├── layout.tsx                              # Layout compartilhado
├── page.tsx                                # Página raiz (/ads)
│
├── contabilidade-lucro-real/
│   └── page.tsx                            # Form variant (545 linhas)
│
├── contabilidade-lucro-real-wa/
│   └── page.tsx                            # WhatsApp variant (438 linhas)
│
├── contabilidade-industria/
│   └── page.tsx                            # Form variant (440 linhas)
│
├── contabilidade-industria-wa/
│   └── page.tsx                            # WhatsApp variant (435 linhas)
│
└── [outras paginas...]
```

### Convenção de Nomenclatura

**URL Pattern:** `/ads/[categoria]-[solucao]` ou `/ads/[categoria]-[solucao]-wa`

Exemplos:
- ✅ `/ads/contabilidade-lucro-real` (Form)
- ✅ `/ads/contabilidade-lucro-real-wa` (WhatsApp)
- ✅ `/ads/contabilidade-industria` (Form)
- ✅ `/ads/contabilidade-industria-wa` (WhatsApp)

**Naming Convention:**
- Use **kebab-case** (hífens, sem underscore)
- Prefixo: `contabilidade-` (para manter consistência)
- Sufixo: `-wa` (only para WhatsApp variants)
- Sem números, sem underscores, sem uppercase

---

## Componentes Utilizados

### Form Variant (Componentes Principais)

```tsx
import {
  AdsHeroSection,           // Hero com form side-by-side
  BenefitsSection,          // Grid de 6 benefícios
  ProcessSection,           // 4-step process
  TeamSection,              // 3 team members
  IntegrationsSection,      // ERP integrations
  InlineCTA,                // Inline CTA cards
  UrgencySection,           // Urgency + final CTA
  ScrollToFormButton,       // Sticky form button
} from "@/components/ads";

import { FormExpanded } from "@/components/ads/FormExpanded"; // Form fields
```

### WhatsApp Variant (Componentes Principais)

```tsx
import { WhatsAppDirectCTA } from "@/components/ads/WhatsAppDirectCTA";  // Hero + CTA buttons
import { WhatsAppSticky } from "@/components/ads/WhatsAppSticky";        // Floating button
import {
  BenefitsSection,          // Grid de 6 benefícios
  ProcessSection,           // 4-step process
  TeamSection,              // 3 team members
  IntegrationsSection,      // ERP integrations
  InlineCTA,                // Inline CTA cards
  UrgencySection,           // Urgency + final CTA
} from "@/components/ads";
```

### Componentes Compartilhados

Ambas variantes usam:
- `BenefitsSection` - Lista de 6 benefícios com ícones
- `ProcessSection` - 4-step methodology
- `TeamSection` - Team members profile
- `IntegrationsSection` - ERP logos
- `TestimonialsGridSection` - 3 success cases
- `FAQSectionWrapper` - 8-10 FAQs
- `UrgencySection` - Final urgency + CTA

---

## Padrões de Implementação

### Pattern 1: Metadata Setup

```tsx
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Contabilidade Consultiva para Lucro Real | Proposta | OSP",  // 60 chars max
  description:
    "Desde 1977: +600 empresas, +100 migrações. R$ 120mi economia. Proposta em 48h...", // 160 chars max
  robots: {
    index: false,    // ⚠️ IMPORTANTE: Não indexar em buscadores
    follow: true,
  },
  alternates: {
    canonical: "https://ospcontabilidade.com.br/contabilidade/lucro-real",
  },
};
```

### Pattern 2: Page Component Structure

**Form Variant:**
```tsx
export default function LucroRealAdsPage() {
  return (
    <>
      {/* 1. Hero */}
      <AdsHeroSection
        badge="✓ Especialistas Desde 1977 | Proposta Em 48h"
        title="Lucro Real: Especialistas Entregam Até 37% Em Otimização"
        subtitle="..."
        trustSignals={[...]}
        campaign="contabilidade-lucro-real-search"
      />

      {/* 2. Success Cases */}
      <section>...</section>

      {/* 3. Benefits */}
      <BenefitsSection
        title="Por Que Escolhem a OSP"
        ctaText="Solicitar Proposta"
        ctaHref="#form"
        benefits={[...]}
      />

      {/* 4. Process */}
      <ProcessSection
        title="Como Funciona"
        steps={[...]}
      />

      {/* 5. Team */}
      <TeamSection
        title="Especialistas"
        members={[...]}
      />

      {/* 6. Integrations */}
      <IntegrationsSection
        title="Integrações"
        systems={[...]}
      />

      {/* 7. Testimonials */}
      <TestimonialsGridSection
        title="Cases de Sucesso"
        testimonials={[...]}
      />

      {/* 8. FAQ */}
      <FAQSectionWrapper faqs={[...]} />

      {/* 9. Urgency */}
      <UrgencySection
        title="Seu Contador é Especialista?"
        ctaText="Solicitar Proposta Agora"
        reasons={[...]}
      />
    </>
  );
}
```

**WhatsApp Variant:**
```tsx
export default function LucroRealWAPage() {
  return (
    <>
      {/* 1. Custom Hero (sem form) */}
      <section>
        {/* WhatsAppDirectCTA + trust signals */}
      </section>

      {/* 2-8. Same as Form variant (without FormExpanded) */}
      <BenefitsSection ... />
      <ProcessSection ... />
      <TeamSection ... />
      <IntegrationsSection ... />
      <TestimonialsGridSection ... />
      <FAQSectionWrapper ... />

      {/* 9. Urgency */}
      <UrgencySection ... />

      {/* 10. Floating Button */}
      <WhatsAppSticky />
    </>
  );
}
```

### Pattern 3: CTA Strategy

**Form Variant (5+ CTAs):**
- Hero: "Solicitar Proposta" (scroll to form)
- After Cases: InlineCTA card
- Benefits header: "Solicitar Proposta"
- After Benefits: InlineCTA card
- After Testimonials: InlineCTA card
- Sticky: ScrollToFormButton (mobile)
- Urgency: "Solicitar Proposta Agora"

**WhatsApp Variant (4 CTAs - streamlined):**
- Hero: WhatsAppDirectCTA (lg)
- Benefits header: "Solicitar Proposta" link
- Final section: WhatsAppDirectCTA (md, id="cta-whatsapp")
- Urgency: "Solicitar Proposta Agora"
- Floating: WhatsAppSticky (premium, appears after 3s)

### Pattern 4: Copy Structure

**Title Formula:**
```
"[Solução]: [Benefit] Em [Métrica]"

Exemplos:
- "Lucro Real: Especialistas Entregam Até 37% Em Otimização Tributária"
- "A Contabilidade Estratégica que Sua Indústria Merece"
```

**Subtitle Formula:**
```
"[Trust signal]. [Promise]. [Outcome]."

Exemplo:
"Seu braço contábil estratégico. +600 empresas confiam em nós.
Você tem especialistas que otimizam IRPJ/CSLL. Proposta em 48h."
```

**Urgency Title Formula:**
```
"Seu [Role] é Especialista em [Topic]?"

Exemplos:
- "Seu Contador é Especialista no Lucro Real?"
- "Seu Contador Domina Precificação Industrial?"
```

**Urgency Reasons (3-4 bullets com números):**
```
- "[Problema] = [Impacto financeiro]"
- "[Causa] = [Risco]"
- "[Deficiência] = [Custo percentual]"
```

---

## Metadata & SEO

### Title Tags

**Formato:** `[Solução] | [Benefit] | [Brand]`
**Comprimento:** 55-61 caracteres

Exemplos:
- ✅ "Contabilidade Consultiva para Lucro Real | Proposta | OSP" (59)
- ✅ "Especialistas em Contabilidade Industrial | 48 Anos | OSP" (57)

### Meta Descriptions

**Formato:** `[Promise]. [Social proof]. [CTA]`
**Comprimento:** 155-160 caracteres

Exemplos:
- ✅ "Desde 1977: +600 empresas, +100 migrações Lucro Real, R$ 120mi em economia. Proposta em 48h." (95)
- ✅ "A referência em contabilidade industrial há 48 anos. Estruturação tributária, compliance EFD, planejamento fiscal avançado." (125)

### Robots Meta

**IMPORTANTE:** Todas as ads pages devem ter:
```tsx
robots: {
  index: false,    // Não indexar em buscadores (é página de ads)
  follow: true,    // Mas rastrear links internos
}
```

### Canonical URLs

Apontam para página "principal" da solução:
```tsx
alternates: {
  canonical: "https://ospcontabilidade.com.br/contabilidade/lucro-real",
}
```

---

## Analytics & Tracking

### Implementação Padrão

**Em Componentes de CTA:**

```tsx
import { useAnalytics } from '@/hooks/useAnalytics';
import { trackCTAClick } from '@/lib/gtm-tracking';

export function MyComponent() {
  const { trackCTA } = useAnalytics();

  const handleClick = () => {
    // Track com useAnalytics
    trackCTA({
      event_label: "MyComponent CTA Click",
      cta_type: "form",  // ou "whatsapp"
      cta_location: "my_component",
    });

    // Track com dataLayer (GTM)
    if (typeof window !== 'undefined' && (window as any).dataLayer) {
      (window as any).dataLayer.push({
        event: 'my_component_click',
        eventCategory: 'engagement',
        eventLabel: 'MyComponent',
        value: 1,
      });
    }
  };
}
```

### Eventos Padrão por Componente

| Componente | Evento | Localização | Tipo |
|-----------|--------|-------------|------|
| AdsHeroSection | `hero_cta_click` | hero | form/whatsapp |
| WhatsAppDirectCTA | `whatsapp_cta_click` | hero/inline | whatsapp |
| WhatsAppSticky | `whatsapp_sticky_click` | sticky | whatsapp |
| FormExpanded | `form_submit` | hero | form |
| InlineCTA | `inline_cta_click` | section | form/whatsapp |
| UrgencySection | `urgency_cta_click` | footer | form/whatsapp |

### Campaign Parameter

Form variant recebe campaign para rastrear origem:

```tsx
<AdsHeroSection
  ...
  campaign="contabilidade-lucro-real-search"  // Google Ads source
/>
```

Nomenclatura:
- `[solucao]-search` → Google Search Ads
- `[solucao]-display` → Google Display/Remarketing
- `[solucao]-facebook` → Facebook Ads
- `[solucao]-tiktok` → TikTok Ads

---

## Design & Styling

### Paleta de Cores

**Primary (Empresa):**
- Color: HSL(210 100% 40%) = Azul
- Used for: Buttons, links, icons, CTA primary
- Variants: primary/90 (hover), primary/80 (active)

**Secondary (WhatsApp):**
- Color: HSL(142 71% 45%) = Green (WhatsApp)
- Used: Only WhatsApp buttons + floating button
- Variants: green-600 (base), green-700 (hover)

**Neutros:**
- Gray-900 (headings)
- Gray-700 (body text)
- Gray-50 (backgrounds)
- White (cards)

### Componentes de Design

**Buttons:**
```tsx
// Primary CTA Button
<button className="bg-primary hover:bg-primary/90 text-white px-6 py-3 rounded-lg">
  Solicitar Proposta
</button>

// Secondary Button
<button className="bg-gray-100 hover:bg-gray-200 text-gray-900">
  Learn More
</button>

// WhatsApp Button
<button className="bg-green-600 hover:bg-green-700 text-white">
  Iniciar Conversa
</button>
```

**Cards:**
```tsx
<div className="bg-white rounded-xl border-2 border-primary/20 p-8 shadow-sm hover:shadow-md">
  {/* Content */}
</div>
```

**Badges:**
```tsx
<Badge variant="destructive" className="text-sm font-semibold animate-pulse">
  ✓ Especialistas Desde 1977 | Proposta Em 48h
</Badge>
```

### Animações

**Scroll Reveal (entrada dos elementos):**
```tsx
<ScrollReveal animation="fadeInUp">
  <div>Content</div>
</ScrollReveal>
```

**Floating Button:**
- `animate-in fade-in slide-in-from-bottom-2` (entrada)
- `animate-bounce` (badge pulsando)
- `animate-pulse` (background glow)
- `hover:scale-105` (scale no hover)

**CTA Buttons:**
- `hover:shadow-xl` (sombra no hover)
- `active:scale-95` (feedback no clique)
- `transition-all duration-300` (suavidade)

---

## Como Criar Nova Página

### Step 1: Preparar Dados de Conteúdo

Antes de codificar, prepare em documento separado:

```markdown
# Dados para Nova Página: [Solução]

## Headline
- Title: "..."
- Subtitle: "..."

## Trust Signals
- +XX empresas
- +YY migrações
- R$ ZZmi economia

## Success Cases (2x)
- Case 1: Industry, numbers
- Case 2: Industry, numbers

## Benefits (6x)
- [Benefit 1]: [Description]
- [Benefit 2]: [Description]

## Process (4 steps)
- Step 1: [Title] [Description]
- Step 2: ...

## Team
- [3 team members]

## FAQs (8-10x)
- Q1: A1
- Q2: A2

## Urgency
- Title: "..."
- Reasons (3-4x)
```

### Step 2: Criar Pastas

```bash
cd next-migration/src/app/ads/

# Para Form variant
mkdir -p solucao-nome
touch solucao-nome/page.tsx

# Para WhatsApp variant
mkdir -p solucao-nome-wa
touch solucao-nome-wa/page.tsx
```

### Step 3: Copiar Template Form Variant

```bash
# Copiar de exemplo existente
cp contabilidade-lucro-real/page.tsx solucao-nome/page.tsx
```

Depois editar:
- Metadata (title, description, canonical)
- AdsHeroSection (badge, title, subtitle, campaign)
- Todos os textos (success cases, benefits, process, team, faqs, urgency)
- Ícones (adaptar conforme solução)

### Step 4: Copiar Template WhatsApp Variant

```bash
cp contabilidade-lucro-real-wa/page.tsx solucao-nome-wa/page.tsx
```

Depois editar:
- Metadata
- Hero section (sem form, com WhatsAppDirectCTA)
- Mesmos conteúdos (success cases, benefits, etc)
- Urgency section

### Step 5: Validação

```bash
# Type check
npm run type-check

# Build
npm run build

# Dev server
npm run dev

# Test URLs
# http://localhost:3000/ads/solucao-nome
# http://localhost:3000/ads/solucao-nome-wa
```

### Step 6: Deployment

```bash
git add next-migration/src/app/ads/solucao-nome*
git commit -m "feat(ads): add solucao-nome pages (form + wa variants)"
git push origin main
```

---

## Checklist de Validação

### Antes de Deploy

**Copy & Messaging** ✓
- [ ] Title é impactante (até 60 chars)
- [ ] Subtitle contém números específicos
- [ ] Urgency section tem gatilho emocional claro
- [ ] CTAs dizem "Solicitar Proposta" (consistente)
- [ ] Nenhuma promessa vaga ou genérica

**Design** ✓
- [ ] Cores corretas (primary blue, green WhatsApp)
- [ ] Responsive (testar 320px, 768px, 1024px)
- [ ] Botões 44px+ altura (mobile accessible)
- [ ] Floating button apenas em WA variants
- [ ] Animações não são distrativas

**Técnico** ✓
- [ ] `npm run type-check` → 0 errors
- [ ] Metadata completa (title, description, robots, canonical)
- [ ] `robots: index: false` configurado
- [ ] Imagens otimizadas
- [ ] Nenhum console error no dev server

**Analytics** ✓
- [ ] useAnalytics hook importado
- [ ] trackCTA em todos os CTAs principais
- [ ] dataLayer.push em eventos críticos
- [ ] Campaign parameter em Form variant
- [ ] Floating button (WA variant) com tracking

**SEO** ✓
- [ ] Meta title: 55-61 chars
- [ ] Meta description: 155-160 chars
- [ ] Canonical URL correto
- [ ] Headings estruturados (H1, H2, H3)
- [ ] Alt text em imagens

**Conteúdo** ✓
- [ ] 2 success cases com números reais
- [ ] 6 benefits com ícones e descrições
- [ ] 4-step process documentado
- [ ] 8-10 FAQs respondidas
- [ ] Team members com fotos

### Após Deploy

**Monitoring** ⚠️
- [ ] GA4 tracking funcionando em production
- [ ] Form submissions chegando em CRM
- [ ] WhatsApp links abrindo corretamente
- [ ] Bounce rate < 60% (esperado)
- [ ] Session duration > 2 minutos

**A/B Testing** 📈
- [ ] Comparar Form vs WhatsApp variant
- [ ] Testar copy variations (title, subtitle)
- [ ] Otimizar CTA placement se necessário
- [ ] Refinar urgency messaging

---

## Perguntas Frequentes

### P: Por que `robots: index: false` em ads pages?

**R:** Ads pages são otimizadas para conversão via anúncios pagos, não para SEO orgânico. Indexá-las criaria:
- Conteúdo duplicado (conflita com página principal)
- Atração de tráfego orgânico qualidade inferior
- Confusão em métricas de analytics

### P: Quando usar Form vs WhatsApp variant?

**R:**
- **Form:** Quando você quer email + informações detalhadas (lead quality)
- **WhatsApp:** Quando você quer engajamento rápido e mobile-first

Recomendação: Sempre criar AMBAS, depois A/B testar.

### P: Posso usar componentes customizados fora de /components/ads?

**R:** Sim, mas preferência é:
1. Usar componentes de `/components/ads` (já otimizados)
2. Reutilizar de `/components/sections` (genéricos)
3. Criar novos em `/components/ads` se específico para ads

### P: Como adaptar para outro idioma?

**R:** Use variáveis de i18n:
```tsx
import pt from "@/locales/pt-BR/translation.json";
import en from "@/locales/en/translation.json";

const locale = params.locale || 'pt'; // URL param
const t = locale === 'pt' ? pt : en;

// Depois use t.ads.[page].[section]
```

### P: Qual é o tempo de carregamento esperado?

**R:** Esperado: < 2 segundos (dev) / < 1 segundo (prod)
Se > 3 segundos, otimizar:
- Imagens (use next/image)
- Código splitting
- Cache headers

---

## Referências Rápidas

### Commits Relevantes

- `bb7810e` - Final readiness review (todas 4 páginas validadas)
- `a691983` - Route rename (industria → contabilidade-industria)
- `910c1fd` - Premium floating button upgrade
- `a30e93f` - Green WhatsApp theme harmonization

### Arquivos Chave

- `/next-migration/src/app/ads/` - Todas as ads pages
- `/next-migration/src/components/ads/` - Componentes reutilizáveis
- `/docs/ADS_PAGES_FINAL_READINESS_NOV13.md` - Validação final
- `/docs/ADS_LAUNCH_CHECKLIST_SUMMARY.md` - Quick reference

### Componentes Importados

```tsx
// Do @/components/ads
AdsHeroSection
BenefitsSection
ProcessSection
TeamSection
IntegrationsSection
InlineCTA
UrgencySection
ScrollToFormButton
WhatsAppDirectCTA
WhatsAppSticky
FormExpanded

// De outros lugares
TestimonialsGridSection (@/components/sections)
FAQSectionWrapper (@/components)
ScrollReveal (@/components)
Badge (@/components/ui/badge)
```

---

## Conclusão

Esta documentação é seu **mapa de referência** para criar novas ads pages. As 4 páginas atuais (Lucro Real, Indústria, versões form e WA) são o **padrão ouro** que você deve replicar.

**Para próximas páginas:**
1. Copiar estrutura exata das páginas existentes
2. Substituir conteúdo (copy, imagens, números)
3. Rodar checklist completo
4. Deploy e monitor

**Não inovar sem aprovação** - o padrão foi validado em produção com sucesso.

---

**Documento criado:** 13 de novembro de 2025
**Versão:** 1.0
**Mantido por:** [Team Name]
**Última validação:** Commit bb7810e
