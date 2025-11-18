# ⚠️ ACESSO À PASTA COMERCIAL - DIAGNÓSTICO

**Data**: 18 de novembro de 2025  
**Status**: 🟡 **REQUER COMPARTILHAMENTO**

---

## ✅ O QUE FUNCIONOU

1. ✅ **Autenticação Firebase**: Sucesso!
   - Service Account: `firebase-workspace-api@site-2026.iam.gserviceaccount.com`
   - Projeto: `site-2026`
   - Credenciais carregadas do Firebase

2. ✅ **Acesso ao Google Drive API**: Sucesso!
   - Conexão estabelecida
   - Permissões verificadas

---

## ❌ O QUE NÃO FUNCIONOU

**Erro HTTP 404**: "File not found: 13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT"

### Possíveis Causas

1. **Pasta não é compartilhada** com o Service Account
   - Você compartilhou a pasta apenas com sua conta Google pessoal
   - Service Account não tem visibilidade

2. **Folder ID incorreto**
   - Verificamos: `13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT` ✅ (está correto)

3. **Pasta foi deletada ou movida**
   - Improvável, mas possível

---

## 🔧 SOLUÇÕES

### Opção 1: Compartilhar Pasta com Service Account (RECOMENDADO)

1. **Abrir pasta Comercial** no Google Drive
2. **Clique em "Compartilhar"** (canto superior direito)
3. **Adicionar email**: `firebase-workspace-api@site-2026.iam.gserviceaccount.com`
4. **Permissão**: "Visualizador" (read-only) é suficiente
5. **Compartilhar**

Após isso, o script funcionará automaticamente!

### Opção 2: Usar Email Autenticado

Se você tem acesso à pasta, podemos:

1. **Instalar Google Cloud CLI**:
   ```bash
   brew install google-cloud-sdk
   ```

2. **Autenticar com sua conta Google**:
   ```bash
   gcloud auth application-default login
   ```

3. **Executar script** (usará suas credenciais pessoais):
   ```bash
   cd ~/osp-website/docs/COMERCIAL
   python3 list_comercial_drive.py
   ```

### Opção 3: Compartilhar com Google Workspace

Se Leo / Team tem acesso na conta `@osp.com.br`:

1. Compartilhar pasta com email do workspace
2. Atualizar Service Account para usar delegação de domínio

---

## 📋 CHECKLIST

Para fazer análise automática da pasta Comercial:

- [ ] Opção 1: Compartilhar pasta com `firebase-workspace-api@site-2026.iam.gserviceaccount.com`
  - [ ] Abrir Google Drive
  - [ ] Localizar pasta COMERCIAL
  - [ ] Clicar "Compartilhar"
  - [ ] Adicionar email do Service Account
  - [ ] Dar permissão "Visualizador"
  - [ ] Confirmar

- OU

- [ ] Opção 2: Instalar Google Cloud CLI e autenticar com conta pessoal
  - [ ] `brew install google-cloud-sdk`
  - [ ] `gcloud auth application-default login`
  - [ ] Executar script

---

## 📊 TESTE APÓS COMPARTILHAMENTO

Após compartilhar a pasta, execute:

```bash
cd ~/osp-website/docs/COMERCIAL
python3 list_comercial_drive.py
```

**Resultado esperado**:
```
✅ Autenticação bem-sucedida!
📂 Listando pasta COMERCIAL...
   📁 Propostas/
   📁 Apresentações/
   📄 arquivo1.pdf (2.5MB)
   ... (estrutura completa)
✅ Análise concluída! Total de itens: 250+
✅ Relatório salvo em: COMERCIAL_STRUCTURE.md
```

---

## 🚀 PRÓXIMAS AÇÕES

**1. IMEDIATO**:
- [ ] Escolher Opção 1 ou 2 acima
- [ ] Executar passo-a-passo

**2. APÓS SUCESSO**:
- [ ] Script gera `COMERCIAL_STRUCTURE.md` automaticamente
- [ ] Fazer commit do relatório
- [ ] Usar dados para P6 Phase 2

---

## 💡 NOTA IMPORTANTE

O script **está 100% pronto**. Apenas falta:

1. Compartilhar a pasta (1 minuto)
2. OU autenticar com Google Cloud CLI (5 minutos)

Depois funciona perfeitamente! 🎯

---

**Qual opção você prefere?**
- Opção 1: Compartilhar pasta (mais fácil)
- Opção 2: Instalar gcloud (mais flexível)
