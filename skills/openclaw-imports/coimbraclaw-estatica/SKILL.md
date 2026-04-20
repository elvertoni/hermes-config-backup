---
name: coimbraclaw-estatica
description: Gerar aulas estáticas em HTML/CSS para o ProfessorDash no padrão visual blueprint/apostila. Use quando o Toni pedir aula estática, padrão blueprint, HTML/CSS puro, apostila visual ou material imprimível.
updated: 2026-04-20
status: ativa
---

# coimbraclaw-estatica

Skill de geração de aulas estáticas em HTML com CSS embutido. Não depende do validador Markdown nem do renderer do ProfessorDash. Serve para apostilas, materiais impressos, aulas visuais standalone e distribuição fora do site.

---

## 1. Quando usar esta skill

Sinais claros de que é esta skill, não `coimbraclaw-prof`:

- "aula estática"
- "padrão blueprint"
- "HTML/CSS puro"
- "apostila visual"
- "quero imprimir" / "salvar em PDF"
- "usar fora do site"
- "igual àquela sobre blueprint"
- referência ao arquivo `blueprint-de-software-para-tcc.html`

Se o pedido for aula normal do ProfessorDash renderizada em Markdown → usar `coimbraclaw-prof`.

---

## 2. Fonte de verdade visual

Arquivo de referência no repositório:
`/root/work/ProfToniCoimbra/publicadas/materias/3a-serie/analise-e-projeto-de-sistemas/blueprint-de-software-para-tcc.html`

Antes de gerar qualquer aula estática, ler esse arquivo para alinhar:
- tokens de cor
- tipografia
- estrutura de seções
- estilo dos callouts
- blocos de código

---

## 3. Padrão visual

### Paleta principal (dark theme)

```css
:root {
  --bg-base:      #000000;
  --bg-surface:   #0d0d0d;
  --bg-elevated:  #1a1a1a;
  --text-primary: #e5e2e1;
  --text-muted:   #a0a0a0;
  --accent-green:  #10b981;
  --accent-violet: #8b5cf6;
  --accent-cyan:   #06b6d4;
  --accent-coral:  #f87171;
  --border:        rgba(255,255,255,0.08);
}
```

### Tipografia

- Títulos e corpo: `Geist` (Google Fonts)
- Código: `Geist Mono` ou `JetBrains Mono`
- Tamanho base: 16px
- Line-height: 1.7

### Estrutura de página

- `<!DOCTYPE html>` completo
- `<style>` embutido — sem dependência de CSS externo
- Google Fonts via `@import` no `<style>`
- Capa inicial com título, subtítulo, série, disciplina e data
- Seções como cards com borda sutil
- Callouts coloridos por tipo
- Blocos de código com fundo escuro e syntax highlight manual
- Rodapé: `Material produzido pelo Prof. Toni Coimbra.`

---

## 4. Modo apostila imprimível

Quando o pedido mencionar "apostila", "imprimir", "PDF", "HTML estático" ou "usar onde quiser":

- Implementar dois temas via CSS custom properties: `[data-theme="dark"]` e `[data-theme="light"]`
- Adicionar botão de alternância de tema com persistência em `localStorage`
- Adicionar botão `window.print()`
- Incluir `@media print` com:
  - limpeza de botões e UI de navegação
  - fundo branco, texto preto
  - contraste adequado para papel e PDF
  - quebras de página controladas

---

## 5. Estrutura pedagógica

A estrutura de conteúdo segue o mesmo princípio da `coimbraclaw-prof`: ensinar antes de cobrar.

Ordem recomendada:

1. Capa (título, subtítulo, metadados)
2. Introdução — contexto e motivação
3. Conceito central — definição clara
4. Contexto histórico ou origem do problema
5. Caso real de mercado (não genérico)
6. Subtipos, categorias ou componentes (se aplicável)
7. Exemplos práticos
8. Pontos de atenção e erros comuns
9. Atividade prática (se solicitada)
10. Fechamento e resumo

### Enriquecimento obrigatório

Mesmo nas aulas estáticas, aplicar as cinco dimensões de enriquecimento:

- **Contexto histórico**: por que o conceito existe, qual problema ele resolve
- **Caso real**: empresa, projeto, falha ou sistema documentado
- **Conexão profissional**: onde o aluno técnico vai usar isso
- **Tensão**: o que falha, o que confunde, o que não é óbvio
- **Curiosidade**: algo que o aluno não esperava

---

## 6. Callouts visuais

Usar `<div class="callout callout-[tipo]">` com ícone e texto.

Tipos e cores:

| Tipo | Cor de borda | Ícone sugerido |
|---|---|---|
| `conceito` | `--accent-cyan` | 📖 |
| `exemplo` | `--accent-violet` | 📝 |
| `importante` | `--accent-coral` | ⚠️ |
| `atencao` | `--accent-coral` | 🚨 |
| `dica` | `--accent-green` | 💡 |
| `curiosidade` | `--accent-cyan` | 🔍 |
| `exercicio` | `--accent-violet` | ✍️ |
| `resumo` | `--accent-green` | 📋 |

Estrutura HTML do callout:

```html
<div class="callout callout-conceito">
  <div class="callout-icon">📖</div>
  <div class="callout-body">
    <p class="callout-title">Conceito</p>
    <p class="callout-text">Definição central aqui.</p>
  </div>
</div>
```

---

## 7. Blocos de código

```html
<div class="code-block">
  <div class="code-header">
    <span class="code-lang">python</span>
  </div>
  <pre><code>
# código aqui
  </code></pre>
</div>
```

CSS do bloco de código:

```css
.code-block {
  background: #0d0d0d;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  margin: 1.5rem 0;
}
.code-header {
  background: #1a1a1a;
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
}
pre {
  margin: 0;
  padding: 1.25rem;
  overflow-x: auto;
}
code {
  font-family: 'Geist Mono', 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  color: var(--text-primary);
  line-height: 1.6;
}
```

---

## 8. Publicação

Salvar em `.html` no caminho correto do repositório:

```
/root/work/ProfToniCoimbra/publicadas/materias/[serie]/[disciplina]/aula-XX-titulo-slug.html
```

Após salvar:

```bash
git status
git add [arquivo]
git commit -m "aula: [título]"
git push origin main
```

---

## 9. Resposta final esperada

Ao concluir, informar:

```
Arquivo criado: aula-XX-titulo-slug.html
Caminho: publicadas/materias/[serie]/[disciplina]/
Commit: [SHA]
Push: ok / pendente
Tema: dark + light com alternância
Impressão: @media print configurado
```

---

## 10. Regras absolutas

- NUNCA usar esta skill quando o pedido for aula normal do ProfessorDash em Markdown
- NUNCA entregar HTML sem CSS embutido — o arquivo deve ser standalone
- NUNCA usar paleta clara como padrão se o site estiver em dark theme, salvo pedido explícito de apostila imprimível
- NUNCA inventar casos de mercado — usar apenas casos documentados
- NUNCA misturar os dois formatos: pedido de blueprint → `.html`; aula normal → `.md`
- SEMPRE ler o arquivo de referência antes de gerar visual novo
- SEMPRE incluir `@media print` quando o pedido mencionar impressão ou PDF
- SEMPRE aplicar enriquecimento pedagógico (seção 5) mesmo em aulas estáticas
- SEMPRE usar `Material produzido pelo Prof. Toni Coimbra.` no rodapé de apostilas independentes
- SEMPRE informar commit SHA e status do push ao concluir
