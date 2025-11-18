# 📋 GUIA PASSO-A-PASSO: Compartilhar Pasta COMERCIAL

**Data**: 18 de novembro de 2025  
**Objetivo**: Dar acesso à pasta COMERCIAL para o Service Account  
**Tempo**: ~1-2 minutos

---

## 🎯 PASSO 1: Abrir Google Drive

1. Ir para: https://drive.google.com/
2. Você deve estar logado com sua conta Google

---

## 🔍 PASSO 2: Localizar Pasta COMERCIAL

**Opção A: Pelo Link Direto**
- Abrir: https://drive.google.com/drive/folders/13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT

**Opção B: Procurar**
- Na barra de pesquisa do Drive, digitar: "COMERCIAL"
- Clicar na pasta que aparecer

---

## 📤 PASSO 3: Compartilhar a Pasta

### 3.1 Clique em "Compartilhar"
- Localizar o botão **"Compartilhar"** no canto superior direito
- Pode estar como um ícone de pessoas ou texto "Compartilhar"

### 3.2 Janela de Compartilhamento Abre
- Deve aparecer uma caixa de diálogo
- Pode mostrar quem já tem acesso

---

## ➕ PASSO 4: Adicionar o Service Account

### 4.1 Campo de Entrada
- Clicar no campo onde diz "Compartilhar com pessoas e grupos" ou similar
- Ou procurar botão para "Adicionar pessoas"

### 4.2 Copiar e Colar o Email

**Email do Service Account**:
```
firebase-workspace-api@site-2026.iam.gserviceaccount.com
```

**Como fazer**:
1. Copiar email acima (Ctrl+C ou Cmd+C)
2. Colar no campo de compartilhamento (Ctrl+V ou Cmd+V)

### 4.3 Pressionar Enter ou Tab
- O email deve aparecer em uma sugestão
- Clicar na sugestão ou pressionar Enter

---

## 🔐 PASSO 5: Definir Permissão

### 5.1 Selecionar Nível de Acesso

Quando o email for adicionado, aparecerá uma opção de permissão:

**Recomendado: "Visualizador"**
```
- Visualizador: Pode visualizar (ler) mas não editar
  ✅ Esto é o que queremos
```

Outras opções (não use):
```
- Comentarista: Pode comentar (não queremos)
- Editor: Pode editar (não queremos, inseguro)
```

### 5.2 Escolher "Visualizador"
- Clique no dropdown e selecione "Visualizador"

---

## ✅ PASSO 6: Confirmar e Compartilhar

### 6.1 Clique em "Compartilhar" ou "Enviar"
- Procurar botão azul com texto "Compartilhar", "Enviar", "Concluído", etc.

### 6.2 Confirmação
- Deve aparecer mensagem: "Compartilhado com sucesso" ou similar
- Janela pode fechar automaticamente

---

## 🎉 PRONTO!

A pasta COMERCIAL agora é acessível pelo Service Account!

### Próximo Passo: Testar o Script

```bash
cd ~/osp-website/docs/COMERCIAL
python3 list_comercial_drive.py
```

**Resultado esperado**:
```
✅ Autenticação bem-sucedida!
   Fonte: Firebase config (contabilidade)
   Service Account: firebase-workspace-api@site-2026.iam.gserviceaccount.com

📂 Listando pasta COMERCIAL...
   📁 Propostas/
   📁 Apresentações/
   📁 Contratos/
   ...
✅ Análise concluída! Total de itens: 250+
✅ Relatório salvo em: COMERCIAL_STRUCTURE.md
```

---

## ⚠️ SE ALGO NÃO FUNCIONOU

### "Email inválido" ou "Email não encontrado"

**Solução**: Verificar que copiou corretamente
```
firebase-workspace-api@site-2026.iam.gserviceaccount.com
```

Sem espaços extras, sem caracteres adicionais.

### "Usuário já tem acesso"

**Solução**: Já foi compartilhado!
- Volte ao terminal
- Execute o script: `python3 list_comercial_drive.py`

### Ainda aparece "Pasta vazia" após rodar script

**Possível causa**: Script precisa de mais tempo para refletir as permissões
- Aguarde 5-10 minutos
- Rode o script novamente

---

## 🔗 RESUMO VISUAL

```
Google Drive
    ↓
Pasta COMERCIAL (13qFDT4ijKPRrnCR2JrK4kWvuDauzx9zT)
    ↓
Botão "Compartilhar" → Adicionar email → Selecionar "Visualizador"
    ↓
firebase-workspace-api@site-2026.iam.gserviceaccount.com
    ↓
✅ Compartilhado!
    ↓
Script Python consegue ler
    ↓
Gera COMERCIAL_STRUCTURE.md automaticamente
```

---

**Próximo**: Após compartilhar, execute o script e vou gerar o relatório completo! 🚀
