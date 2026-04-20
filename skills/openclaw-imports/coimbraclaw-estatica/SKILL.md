---
name: coimbraclaw-estatica
description: Gerar aulas estáticas em HTML para o ProfessorDash no padrão visual apostila. Use quando o Toni pedir aula estática, padrão blueprint, HTML puro, apostila visual ou material imprimível.
updated: 2026-04-20
status: ativa
---

# coimbraclaw-estatica

Skill de geração de aulas estáticas em HTML. Usa o design system do repositório
ProfToniCoimbra como fonte de verdade visual. Não depende do validador Markdown
nem do renderer do ProfessorDash.

---

## 1. Quando usar esta skill

Sinais claros de que é esta skill, não coimbraclaw-prof:

- "aula estática"
- "padrão blueprint"
- "HTML puro"
- "apostila visual"
- "quero imprimir" / "salvar em PDF"
- "usar fora do site"
- "igual àquela sobre blueprint"
- referência ao arquivo blueprint-de-software-para-tcc.html

Se o pedido for aula normal do ProfessorDash renderizada em Markdown → usar coimbraclaw-prof.

---

## 2. Fonte de verdade visual

Design system no repositório:

```
/root/work/ProfToniCoimbra/_design-system/apostila/
  apostila-template.html   ← template base a duplicar
  apostila.css             ← CSS externo referenciado pelo HTML
  apostila.js              ← JS externo referenciado pelo HTML
  favicon.svg              ← ícone
  modelos/aula_modelo.md   ← modelo de conteúdo em Markdown
```

Antes de gerar qualquer aula estática, ler o apostila-template.html para
alinhar estrutura, classes CSS e blocos disponíveis.

---

## 3. Como gerar uma aula estática

### 3.1 Duplicar o template

```bash
cp /root/work/ProfToniCoimbra/_design-system/apostila/apostila-template.html \
   /root/work/ProfToniCoimbra/publicadas/materias/[serie]/[disciplina]/aula-XX-titulo-slug.html
```

### 3.2 Referenciar CSS e JS com caminho relativo correto

O HTML publicado fica em `publicadas/materias/[serie]/[disciplina]/`.
O design system fica em `_design-system/apostila/`.

Caminho relativo do HTML publicado até o design system:

```
../../../../_design-system/apostila/apostila.css
../../../../_design-system/apostila/apostila.js
../../../../_design-system/apostila/favicon.svg
```

Usar sempre caminhos relativos — nunca absolutos.

### 3.3 Preencher os blocos [EDIT]

O template usa comentários `<!-- [EDIT] -->` para marcar os pontos de edição:

- `<!-- [EDIT] disciplina -->` → nome da disciplina
- `<!-- [EDIT] tema curto -->` → tema da aula (ex: "Aula 01 · Engenharia de Software")
- `<!-- [EDIT] Título da <span class="accent">apostila</span> -->` → título com destaque
- `<!-- [EDIT] Parágrafo de abertura -->` → introdução da aula
- `<!-- [EDIT] -->` nos meta-cards → disciplina, ano letivo, duração, entrega
- Seções, callouts e fechamento conforme conteúdo

### 3.4 Blocos disponíveis no template

Copiar e reutilizar dentro de `<section class="section">`:

```html
<!-- Callout variants: c-primary, c-secondary, c-tertiary, c-warning, c-error -->
<aside class="callout c-primary">
  <div class="callout-mark" aria-hidden="true">✓</div>
  <div class="callout-body">
    <p class="callout-title">Título</p>
    <p class="callout-text">Texto.</p>
  </div>
</aside>

<!-- Bloco de código -->
<div class="code-shell">
  <header class="code-top">
    <span class="dot dot-red"></span>
    <span class="dot dot-yellow"></span>
    <span class="dot dot-green"></span>
    <span class="code-lang">python</span>
  </header>
  <pre><code>código aqui</code></pre>
</div>

<!-- Demonstração visual -->
<div class="demo-wrap">
  <div class="demo-label">Demonstração</div>
  <div class="demo-body">HTML renderizado</div>
</div>

<!-- Roteiro do professor -->
<aside class="roteiro">
  <header class="roteiro-head">
    <span class="roteiro-chip">Roteiro do professor</span>
  </header>
  <p>Fala guiada.</p>
</aside>

<!-- Checklist de fechamento -->
<ul class="checklist">
  <li>Item aprendido</li>
</ul>

<!-- Tags de conteúdo -->
<ul class="tags">
  <li>tag-1</li><li>tag-2</li>
</ul>
```

---

## 4. Enriquecimento pedagógico obrigatório

Mesmo nas aulas estáticas, aplicar as cinco dimensões:

- **Contexto histórico**: por que o conceito existe, qual problema ele resolve
- **Caso real**: empresa, projeto, falha ou sistema documentado — nunca genérico
- **Conexão profissional**: onde o aluno técnico vai usar isso nos próximos 2 anos
- **Tensão**: o que falha, o que confunde, o que não é óbvio
- **Curiosidade**: algo que o aluno não esperava — dado histórico, estatística, origem de termo

---

## 5. Publicação

Caminho final:
```
/root/work/ProfToniCoimbra/publicadas/materias/[serie]/[disciplina]/aula-XX-titulo-slug.html
```

Após salvar:

```bash
cd /root/work/ProfToniCoimbra
git add publicadas/materias/[serie]/[disciplina]/aula-XX-titulo-slug.html
git commit -m "aula: [título da aula]"
git push origin main
```

---

## 6. Resposta final esperada

```
Arquivo: aula-XX-titulo-slug.html
Caminho: publicadas/materias/[serie]/[disciplina]/
CSS/JS: referenciados via caminho relativo ../../../../_design-system/apostila/
Commit: [SHA]
Push: ok / pendente
```

---

## 7. Regras absolutas

- NUNCA usar esta skill para aulas normais do ProfessorDash em Markdown
- NUNCA embutir CSS ou JS inline — sempre referenciar os arquivos do design system
- NUNCA usar caminhos absolutos para CSS/JS — sempre relativos
- NUNCA inventar casos de mercado — usar apenas casos documentados
- NUNCA misturar os dois formatos: pedido de apostila → .html; aula normal → .md
- SEMPRE ler apostila-template.html antes de gerar conteúdo novo
- SEMPRE aplicar enriquecimento pedagógico (seção 4)
- SEMPRE usar Material produzido pelo Prof. Toni Coimbra. no rodapé
- SEMPRE informar commit SHA e status do push ao concluir