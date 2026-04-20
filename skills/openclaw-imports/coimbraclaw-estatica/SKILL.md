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

O template usa comentários `<!-- [EDIT] -->` para marcar os pontos de edição.
Preencher pelo menos estes pontos obrigatórios:

- topbar / marca:
  - `<!-- [EDIT] disciplina -->` dentro de `.brand-text small`
- hero:
  - `<!-- [EDIT] tema curto -->` dentro de `.eyebrow`
  - `<!-- [EDIT] Título da <span class="accent">apostila</span> -->` dentro de `.hero-title`
  - `<!-- [EDIT] Parágrafo de abertura: o que o aluno vai aprender e em que contexto. -->` dentro de `.hero-lead`
- meta-grid:
  - `<!-- [EDIT] -->` em `Disciplina`
  - `<!-- [EDIT] -->` em `Ano letivo`
  - `<!-- [EDIT] 45 min -->` em `Duração estimada`
  - `<!-- [EDIT] 1 atividade prática -->` em `Entrega`
- sumário:
  - `<!-- [EDIT] Título da seção -->`
  - demais itens `<!-- [EDIT] -->`
- seção modelo:
  - `<!-- [EDIT] Título -->` no `h2`
  - `<!-- [EDIT] parágrafo de abertura. -->`
  - `<!-- [EDIT] -->` no callout de exemplo
- fechamento:
  - `<!-- [EDIT] -->` no checklist final

### 3.4 Estrutura-base real do template

Estes blocos já existem no `apostila-template.html` e devem ser preservados ao duplicar:

- `html[data-theme]` → controla tema dark/light via JS
- `.apostila-shell` → corpo da página
- `.topbar > .topbar-inner` → barra superior fixa
- `.brand`, `.brand-mark`, `.brand-text` → identidade do material
- `.toolbar` → ações do topo
  - `.pill.pill-ghost` → link para `#sumario`
  - `.btn.btn-secondary#theme-toggle` + `#theme-label` → alternância de tema
  - `.btn.btn-primary` → botão `Salvar PDF`
  - `.ic` → classe dos SVGs de ícone usados nos botões
- `main.shell` → container principal
- `.hero`, `.hero-gradient`, `.hero-inner`, `.eyebrow`, `.eyebrow-line`, `.hero-title`, `.hero-lead` → capa da apostila
- `.meta-grid` com `.meta-card` → metadados da aula
- `nav.sumario#sumario` com `.sumario-title`, `.sumario-list`, `.sumario-num` → navegação interna
- `.section` → bloco principal de conteúdo
- `.section-head`, `.section-index` → cabeçalho da seção
- `.section.section-close` → bloco de fechamento
- `.footer-note` + `.mono` → assinatura textual dentro do fechamento
- `footer.page-foot > .page-foot-inner` + `.dotsep` + `#year` → rodapé final da página

### 3.5 Blocos reutilizáveis documentados

Copiar e reutilizar dentro de `<section class="section">` quando fizer sentido:

```html
<!-- Callout variants suportadas pelo CSS: c-primary, c-secondary, c-tertiary, c-warning, c-error -->
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

<!-- Checklist -->
<ul class="checklist">
  <li>Item aprendido</li>
</ul>

<!-- Tags de conteúdo -->
<ul class="tags">
  <li>tag-1</li><li>tag-2</li>
</ul>
```

### 3.6 Regras de integridade com JS e navegação

- Não remover `id="theme-toggle"`, `id="theme-label"` ou `id="year"`, porque `apostila.js` depende deles.
- Manter `id="sumario"` e os links `href="#sec-X"` sincronizados com os `id` reais das seções.
- Ao duplicar ou criar novas seções, repetir o padrão `section.section` + `header.section-head` + `span.section-index`.
- Se o título principal usar destaque visual, manter `<span class="accent">...</span>` dentro de `.hero-title`.

---

## 4. Enriquecimento pedagógico obrigatório

Mesmo nas aulas estáticas, aplicar as cinco dimensões:

- **Contexto histórico**: por que o conceito existe, qual problema ele resolve
- **Caso real**: empresa, projeto, falha ou sistema documentado — nunca genérico
- **Conexão profissional**: onde o aluno técnico vai usar isso nos próximos 2 anos
- **Tensão**: o que falha, o que confunde, o que não é óbvio
- **Curiosidade**: algo que o aluno não esperava — dado histórico, estatística, origem de termo

---

## 6. Características técnicas do design system

### 6.1 Responsividade e impressão

- **Breakpoint mobile:** 720px — abaixo disso o layout se adapta
- **Impressão otimizada:** `@media print` remove gradientes, oculta toolbar, força backgrounds brancos e textos escuros para economizar tinta
- **Botão "Salvar PDF":** chama `window.print()` via `onclick` inline no template

### 6.2 Sistema de temas

- **Controle:** `html[data-theme="dark|light"]` + localStorage `apostila-theme`
- **JavaScript:** `apostila.js` gerencia alternância automática via `#theme-toggle`
- **CSS:** 28+ regras específicas para tema claro usando `[data-theme="light"]`
- **Padrão:** dark theme por default

### 6.3 Tokens visuais

- **Variáveis CSS:** 24 custom properties (`--shell-primary`, `--font-body`, `--content-gap`, etc.)
- **Fontes:** Geist (corpo) + Geist Mono (código) carregadas do Google Fonts
- **Transições:** sutis em hover states, sem animações pesadas

---

## 7. Publicação

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

## 8. Resposta final esperada

```
Arquivo: aula-XX-titulo-slug.html
Caminho: publicadas/materias/[serie]/[disciplina]/
CSS/JS: referenciados via caminho relativo ../../../../_design-system/apostila/
Commit: [SHA]
Push: ok / pendente
```

---

## 9. Regras absolutas

- NUNCA usar esta skill para aulas normais do ProfessorDash em Markdown
- NUNCA embutir CSS ou JS inline — sempre referenciar os arquivos do design system
- NUNCA usar caminhos absolutos para CSS/JS — sempre relativos
- NUNCA inventar casos de mercado — usar apenas casos documentados
- NUNCA misturar os dois formatos: pedido de apostila → .html; aula normal → .md
- SEMPRE ler apostila-template.html antes de gerar conteúdo novo
- SEMPRE aplicar enriquecimento pedagógico (seção 4)
- SEMPRE usar Material produzido pelo Prof. Toni Coimbra. no rodapé
- SEMPRE informar commit SHA e status do push ao concluir