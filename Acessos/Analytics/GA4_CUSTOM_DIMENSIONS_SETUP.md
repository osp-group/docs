# GA4 Custom Dimensions Setup Guide

**Created:** November 9, 2025
**Issue:** #342 - Finalizar integração GA4
**Priority:** 🔴 CRITICAL - Dados sendo perdidos sem essa configuração

---

## 🚨 Por que isso é CRÍTICO?

O código do site já envia Custom Dimensions para o GA4, mas **se não forem configuradas no Admin do GA4, os dados são PERDIDOS**.

**Impacto:**
- ❌ Sem segmentação de leads (hot/warm/cold)
- ❌ Sem análise de journey stage (awareness/consideration/decision)
- ❌ Sem identificação de CTAs mais efetivos
- ❌ Sem dados de onde as conversões acontecem

**Resultado:** Decisões de marketing baseadas em dados incompletos = campanhas menos eficientes.

---

## 📊 Custom Dimensions a Configurar

São 4 dimensions que o código usa mas que NÃO existem no GA4:

| Dimension | Parameter Name | Scope | Descrição | Valores Possíveis |
|-----------|---------------|-------|-----------|-------------------|
| **User Journey Stage** | `user_journey_stage` | Event | Estágio do usuário no funil | `awareness`, `consideration`, `decision` |
| **CTA Location** | `cta_location` | Event | Localização do CTA na página | `hero`, `inline`, `footer`, `sticky`, `card`, `modal` |
| **Page Type** | `page_type` | Event | Tipo de página onde ocorreu o evento | `homepage`, `solution`, `segment`, `institutional`, `materiais`, `ads` |
| **Lead Quality** | `lead_quality` | Event | Qualidade do lead | `hot`, `warm`, `cold` |

---

## 🛠️ Passo a Passo - Configuração Manual (Interface em Português)

### 1. Acessar Administrador do GA4

1. Abra: https://analytics.google.com/
2. Selecione a propriedade: **OSP Contabilidade** (ID: G-9S0DCFZQKX)
3. Clique em **Administrador** (ícone de engrenagem no canto inferior esquerdo)

### 2. Navegar até Definições Personalizadas

1. Na coluna da **Propriedade** (meio da tela), procure a seção **Exibição de dados**
2. Clique em **Definições personalizadas**
3. Você verá uma tela com abas: **Dimensões personalizadas** e **Métricas personalizadas**
4. Certifique-se de estar na aba **Dimensões personalizadas**

### 3. Criar Dimensão #1: User Journey Stage

1. Clique no botão **Criar dimensão personalizada** (canto superior direito)
2. Preencha os campos:
   - **Nome da dimensão:** `User Journey Stage`
   - **Escopo:** `Evento`
   - **Descrição:** `Estágio do usuário no funil de conversão (awareness, consideration, decision)`
   - **Parâmetro do evento:** `user_journey_stage`
3. Clique em **Salvar**

### 4. Criar Dimensão #2: CTA Location

1. Clique em **Criar dimensão personalizada** novamente
2. Preencha:
   - **Nome da dimensão:** `CTA Location`
   - **Escopo:** `Evento`
   - **Descrição:** `Localização do CTA na página (hero, inline, footer, sticky, card, modal)`
   - **Parâmetro do evento:** `cta_location`
3. Clique em **Salvar**

### 5. Criar Dimensão #3: Page Type

1. Clique em **Criar dimensão personalizada**
2. Preencha:
   - **Nome da dimensão:** `Page Type`
   - **Escopo:** `Evento`
   - **Descrição:** `Tipo de página (homepage, solution, segment, institutional, materiais, ads)`
   - **Parâmetro do evento:** `page_type`
3. Clique em **Salvar**

### 6. Criar Dimensão #4: Lead Quality

1. Clique em **Criar dimensão personalizada**
2. Preencha:
   - **Nome da dimensão:** `Lead Quality`
   - **Escopo:** `Evento`
   - **Descrição:** `Qualidade do lead (hot, warm, cold)`
   - **Parâmetro do evento:** `lead_quality`
3. Clique em **Salvar**

---

## 🧪 Validação

### Teste 1: Verificar na Interface

1. **Administrador** → **Definições personalizadas** → **Dimensões personalizadas**
2. Você deve ver 4 dimensões listadas:
   - ✅ User Journey Stage (evento)
   - ✅ CTA Location (evento)
   - ✅ Page Type (evento)
   - ✅ Lead Quality (evento)

### Teste 2: DebugView (Imediato)

1. Acesse: **Relatórios** → **Tempo real** → **DebugView**
2. Ative o modo de depuração:
   ```bash
   # No navegador, abra o Console (F12) e execute:
   gtag('config', 'G-9S0DCFZQKX', { debug_mode: true });
   ```
3. Navegue no site e clique em um CTA
4. No DebugView, procure o evento `cta_click`
5. Expanda o evento e procure por:
   - ✅ `user_journey_stage: "consideration"`
   - ✅ `cta_location: "hero"`
   - ✅ `page_type: "homepage"`
   - ✅ `lead_quality: "warm"`

Se aparecerem, **está funcionando!**

### Teste 3: Relatórios (24-48h depois)

**⚠️ IMPORTANTE:** Dados de dimensões personalizadas demoram 24-48h para aparecer em relatórios.

1. Após 24h, acesse: **Relatórios** → **Engajamento** → **Eventos**
2. Clique em qualquer evento (ex: `cta_click`)
3. Clique no ícone **"+"** para adicionar dimensão
4. Procure por "User Journey Stage", "CTA Location", etc.
5. Se aparecerem na lista, **dados sendo capturados!**

---

## 📈 Como Usar os Dados

### Análise de Conversão por Journey Stage

**Relatórios → Engajamento → Conversões**
- Adicionar dimensão: `User Journey Stage`
- Ver quantas conversões em cada estágio

**Insights esperados:**
- Se muitas conversões em "awareness" → CTAs estão educando bem
- Se muitas em "decision" → Público já chega pronto para converter

### Análise de CTAs Mais Efetivos

**Relatórios → Engajamento → Eventos → cta_click**
- Adicionar dimensões: `CTA Location` + `Lead Quality`
- Ver quais posições geram leads mais qualificados

**Insights esperados:**
- Hero CTAs → geralmente leads "warm"
- Footer CTAs → geralmente leads "cold" (menos engajados)

### Análise de Páginas de Alta Conversão

**Relatórios → Engajamento → Eventos → form_submit**
- Adicionar dimensão: `Page Type`
- Ver quais tipos de página convertem mais

**Insights esperados:**
- Solution pages → conversões "hot"
- Homepage → conversões "warm"

---

## 🔗 Onde os Dados São Enviados no Código

### FormInline.tsx
```tsx
trackForm({
  lead_quality: 'warm',
  // ...
});

window.gtag('event', 'form_metadata', {
  user_journey_stage: 'decision',
  cta_location: 'inline',
  page_type: 'ads',
  // ...
});
```

### MaterialDownloadDialog.tsx
```tsx
trackCustomEvent('material_download', {
  user_journey_stage: 'consideration',
  cta_location: 'modal',
  page_type: 'materiais',
  lead_quality: 'warm',
  // ...
});
```

### useAnalytics hook
```tsx
trackCTA({
  cta_location: 'hero',
  // Automaticamente adiciona page_path
});
```

---

## ✅ Checklist de Implementação

**Antes da Migração DNS (#344):**
- [ ] 4 Custom Dimensions criadas no GA4 Admin
- [ ] Testes em DebugView confirmam envio
- [ ] Aguardar 24-48h
- [ ] Verificar dados em Reports

**Após 48h:**
- [ ] Reports mostram dados de dimensions
- [ ] Criar 2-3 reports customizados usando dimensions
- [ ] Testar segmentação por lead_quality

---

## 📚 Referências

- **GA4 Custom Dimensions:** https://support.google.com/analytics/answer/10075209
- **GA4 DebugView:** https://support.google.com/analytics/answer/7201382
- **Código tracking:** `next-migration/src/hooks/useAnalytics.ts`
- **Issue GitHub:** #342

---

## 🚨 Troubleshooting

### Problema: Dimensions não aparecem no DebugView

**Causa:** Código não está enviando os parâmetros.

**Solução:**
1. Verificar se `useAnalytics` está importado
2. Console do navegador deve mostrar `📊 Analytics: ...` em development
3. Verificar network tab → procurar requests para `google-analytics.com`

### Problema: Dimensions aparecem no DebugView mas NÃO em Reports

**Causa:** Aguardar 24-48h (normal) OU dimensions não configuradas corretamente.

**Solução:**
1. Verificar **Administrador** → **Definições personalizadas** → está criado?
2. O nome do **Parâmetro do evento** está **exatamente** igual ao código?
   - ✅ `user_journey_stage` (correto)
   - ❌ `userJourneyStage` (errado - case sensitive!)

### Problema: Valores estranhos nos dimensions

**Causa:** Código enviando valores não esperados.

**Solução:**
1. Revisar código → procurar `user_journey_stage:`
2. Validar que só usa valores permitidos (awareness, consideration, decision)
3. Adicionar validação:
   ```tsx
   const validStages = ['awareness', 'consideration', 'decision'];
   if (!validStages.includes(stage)) {
     console.error('Invalid journey stage:', stage);
   }
   ```

---

**Status:** 🟡 Aguardando configuração manual no GA4 Admin
**Responsável:** Admin com acesso ao GA4
**Prazo:** Antes da migração DNS (#344)
