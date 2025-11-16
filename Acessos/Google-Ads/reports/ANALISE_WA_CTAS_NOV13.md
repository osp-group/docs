# Análise de CTAs - Páginas WA

**Data:** 13 de novembro de 2025
**Páginas Analisadas:**
- `/ads/contabilidade-lucro-real-wa`
- `/ads/industria-wa`

---

## 📊 Estado Atual das CTAs

### **LUCRO REAL WA**

| Posição | Atual | Descrição |
|---------|-------|-----------|
| CTA 1 (After Cases) | "Fale com Especialista" | "Quer Conversar Sobre Sua Empresa?" |
| CTA 2 (After Benefits - header) | "Quero Esses Benefícios" | BenefitsSection ctaText |
| CTA 3 (After Benefits - inline) | "Fale com Especialista" | "Pronto Para Ter Compliance?" |
| CTA 4 (After Testimonials) | "Fale com Especialista" | "Junte-se a Empresas..." |
| CTA 5 (Final) | "Fale com Especialista" | UrgencySection |

### **INDÚSTRIA WA**

| Posição | Atual | Descrição |
|---------|-------|-----------|
| CTA 1 (After Cases) | "Fale com Especialista" | "Quer Conversar Sobre Sua Indústria?" |
| CTA 2 (After Benefits - header) | "Quero Esses Benefícios" | BenefitsSection ctaText |
| CTA 3 (After Benefits - inline) | "Fale com Especialista" | "Vamos Conversar?" |
| CTA 4 (After Testimonials) | "Fale com Especialista" | "Junte-se a Indústrias..." |
| CTA 5 (Final) | "Fale com Especialista" | UrgencySection |

---

## 🎯 Problema Identificado

**Foco atual:** Conversação genérica ("Fale com Especialista")
**Foco desejado:** Solicitar proposta específica

---

## 💡 Sugestões de Mudança

### **Proposta 1: Variação por Posição (RECOMENDADO)**

Manter a jornada natural do user mas com Copy mais focado:

#### **CTA 1 - After Cases** (Top of page - Awareness)
```
Atual:  "Fale com Especialista"
Novo:   "Solicitar Proposta"
Title:  "Quer Conversar Sobre Sua Empresa?" → "Pronto Para Sua Proposta?"
Desc:   "Proposta personalizada via WhatsApp em 48h..."
```

#### **CTA 2 - Benefits Header** (Mid page - Consideration)
```
Atual:  "Quero Esses Benefícios"
Novo:   "Solicitar Proposta" (mantém direção ao WhatsApp)
Context: Depois de ver os 6 benefícios, user já quer agir
```

#### **CTA 3 - After Benefits** (Engagement point)
```
Atual:  "Fale com Especialista"
Novo:   "Solicitar Proposta Agora"
Title:  "Pronto Para Ter Compliance?" → "Pronto Para Sua Proposta?"
```

#### **CTA 4 - After Testimonials** (Trust point)
```
Atual:  "Fale com Especialista"
Novo:   "Solicitar Proposta" (forte conversion point - já viu prova social)
Title:  "Junte-se a..." → "Peça Sua Proposta Agora"
```

#### **CTA 5 - Urgency** (Bottom - Last chance)
```
Atual:  "Fale com Especialista"
Novo:   "Solicitar Proposta Agora"
Title:  Urgency title (já bom)
```

---

### **Proposta 2: Alternativa - Duas Variações Paralelas**

Se quiser testar dois approaches:

**A - "Solicitar Proposta"** (Direct)
- Simples, objetivo, clara intenção
- Melhor para: Leads que já decidiram
- Risco: Pode assustar indeciso

**B - "Fale com Especialista"** (Consultivo)
- Mais suave, consultivo, sem compromisso
- Melhor para: Leads em early awareness
- Benefício: Menos fricção inicial

---

## 📝 Copy Recomendado (por posição)

### **LUCRO REAL WA**

```tsx
// CTA 1: After Cases
<InlineCTA
  title="Sua Estrutura Tributária Está Otimizada?"
  description="Proposta personalizada via WhatsApp em 48h. Sem custo. Sem compromisso."
  ctaText="Solicitar Proposta"
  variant="primary"
  ctaScrollTo="cta-whatsapp"
/>

// CTA 2: Benefits Section ctaText
ctaText="Solicitar Proposta"

// CTA 3: After Benefits
<InlineCTA
  title="Pronto Para Sua Proposta Tributária?"
  description="Proposta personalizada via WhatsApp em 48h. Sem custo. Sem compromisso."
  ctaText="Solicitar Proposta"
  variant="secondary"
  ctaScrollTo="cta-whatsapp"
/>

// CTA 4: After Testimonials
<InlineCTA
  title="Peça Sua Proposta Agora"
  description="Proposta personalizada via WhatsApp em 48h. Comece sua otimização tributária hoje."
  ctaText="Solicitar Proposta"
  variant="primary"
  ctaScrollTo="cta-whatsapp"
/>

// CTA 5: Urgency
ctaText="Solicitar Proposta Agora"
```

### **INDÚSTRIA WA**

```tsx
// CTA 1: After Cases
<InlineCTA
  title="Pronto Para Sua Proposta de Precificação?"
  description="Proposta personalizada via WhatsApp em 48h. Sem custo. Sem compromisso."
  ctaText="Solicitar Proposta"
  variant="primary"
  ctaScrollTo="cta-whatsapp"
/>

// CTA 2: Benefits Section ctaText
ctaText="Solicitar Proposta"

// CTA 3: After Benefits
<InlineCTA
  title="Pronto Para Sua Proposta Industrial?"
  description="Proposta personalizada via WhatsApp em 48h. Sem custo. Sem pressão."
  ctaText="Solicitar Proposta"
  variant="secondary"
  ctaScrollTo="cta-whatsapp"
/>

// CTA 4: After Testimonials
<InlineCTA
  title="Peça Sua Proposta Agora"
  description="Proposta personalizada via WhatsApp em 48h. Comece sua transformação tributária hoje."
  ctaText="Solicitar Proposta"
  variant="primary"
  ctaScrollTo="cta-whatsapp"
/>

// CTA 5: Urgency
ctaText="Solicitar Proposta Agora"
```

---

## ✅ Recomendação Final

**Implementar Proposta 1 (Variação por Posição):**

1. **Muda TODOS os `ctaText`** de "Fale com Especialista" para **"Solicitar Proposta"**
2. **Muda alguns títulos** para focar em "proposta personalizada" vs "conversa"
3. **Mantém descrições** (já mencionam WhatsApp + 48h)
4. **Benefício:** User entende que a ação = gera uma proposta formal (não só uma conversa)

**Impacto Esperado:**
- ↑ CTR (mais claro o valor final)
- ↑ Lead quality (leads sabem que vão receber proposta)
- ↓ Bounce rate (menos "clicking just to chat")
- ↑ Conversion rate (mentalidade de "vou receber uma proposta" vs "vou conversar")

---

## 🚀 Implementação

Quando pronto, aplicar em ambas as páginas:
1. `/ads/contabilidade-lucro-real-wa/page.tsx`
2. `/ads/industria-wa/page.tsx`

Commit: `refactor(ads-wa): focus CTAs on 'Solicitar Proposta' instead of conversation`

