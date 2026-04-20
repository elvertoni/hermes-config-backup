---
name: coimbraclaw-prof
description: Skill para geração de aulas completas no formato Markdown do ProfessorDash, com blocos :::tipo, questões interativas e publicação via scripts. Use quando o Toni pedir planejamento, geração, revisão, validação ou publicação de aulas do ProfessorDash. Pipeline alinhado ao renderer e ao validador em Markdown-fonte.
updated: 2026-04-05
status: ativa
---

# skillprof / coimbraclaw-prof

## 1. Identidade e propósito

A skill `coimbraclaw-prof` — apelido editorial `skillprof` — é a skill definitiva do OpenClaw para planejar, escrever, revisar e preparar aulas no formato Markdown do ProfessorDash.

O foco desta skill é gerar aulas com sintaxe compatível com o renderer real do projeto, isto é, com blocos `:::tipo`, seções em Markdown puro e questões interativas no padrão aceito por `validate_lesson.py` e pelo renderer do ProfessorDash.

O contexto operacional desta skill é o seguinte:

- o ProfessorDash renderiza o campo de aula com Markdown
- os blocos `:::tipo` viram componentes ricos no renderer
- o template da aula define o visual final desses componentes
- os scripts em `/home/devuser/.openclaw/workspace/skills/coimbraclaw-prof/scripts/` compõem o pipeline de validação e publicação

Esta skill existe para impedir erros recorrentes:

- gerar aula em formato diferente do que o ProfessorDash realmente renderiza
- usar HTML bruto em vez de blocos `:::tipo`
- publicar aula em série ou disciplina errada
- confiar em documentação antiga ou inconsistente com o código atual
- manter materiais brutos do Drive no git ou no workspace por tempo demais

Escopo desta skill:

- planejamento de aulas
- geração de uma aula por vez
- uso correto dos blocos especiais
- escrita de questões interativas
- preparação para validação
- documentação do fluxo de publicação

Fonte de verdade desta skill:

- `skills/coimbraclaw-prof/SKILL.md`
- `skills/coimbraclaw-prof/_meta.json`
- `skills/coimbraclaw-prof/references/repo-layout.md`
- `skills/coimbraclaw-prof/references/lesson-template.md`
- `skills/coimbraclaw-prof/scripts/create_lesson_template.py`
- `skills/coimbraclaw-prof/scripts/validate_lesson.py`
- `skills/coimbraclaw-prof/scripts/publish_lesson.py`

Observação operacional importante:

Quando houver conflito entre documentação textual e código, o código lido no repositório prevalece.

## 2. Disciplinas e séries disponíveis

Tabela extraída de `references/repo-layout.md`.

| Série | Disciplina | Slug da série | Slug da disciplina | Caminho relativo de publicação |
|---|---|---|---|---|
| 1ª série | Análise e Métodos para Sistemas | `1a-serie` | `analise-e-metodos-para-sistemas` | `publicadas/materias/1a-serie/analise-e-metodos-para-sistemas/` |
| 1ª série | Introdução à Computação | `1a-serie` | `introducao-a-computacao` | `publicadas/materias/1a-serie/introducao-a-computacao/` |
| 2ª série | Inovação, Tecnologia e Empreendedorismo | `2a-serie` | `inovacao-tecnologia-e-empreendedorismo` | `publicadas/materias/2a-serie/inovacao-tecnologia-e-empreendedorismo/` |
| 2ª série | Programação Front-End | `2a-serie` | `programacao-front-end` | `publicadas/materias/2a-serie/programacao-front-end/` |
| 3ª série | Programação no Desenvolvimento de Sistemas | `3a-serie` | `programacao-no-desenvolvimento-de-sistemas` | `publicadas/materias/3a-serie/programacao-no-desenvolvimento-de-sistemas/` |
| 3ª série | Análise e Projeto de Sistemas | `3a-serie` | `analise-e-projeto-de-sistemas` | `publicadas/materias/3a-serie/analise-e-projeto-de-sistemas/` |
| Disciplinas extras | Inteligência Artificial | `disciplinas-extras` | `inteligencia-artificial` | `publicadas/materias/disciplinas-extras/inteligencia-artificial/` |

Regras de mapeamento:

- a série e a disciplina devem ser sempre escolhidas dentro desta tabela
- o slug informado aos scripts deve bater exatamente com a tabela
- o arquivo final segue o padrão `aula-XX-titulo-slug.md`
- a publicação final vai sempre para `publicadas/materias/...`

## 3. Fluxo obrigatório

### 1. Planejamento

Nesta etapa, o agente não gera a aula completa.

O agente:

- interpreta o pedido
- identifica série, disciplina e tema
- sugere a sequência de tópicos ou títulos de aulas
- pede aprovação antes de escrever a Aula 1

Entrega esperada:

- lista curta e ordenada
- sem corpo completo de aula
- sem publicação

### 2. Aprovação

Nesta etapa, o professor confirma o plano ou ajusta o escopo.

O agente:

- confirma o recorte temático aprovado
- fixa a série e disciplina corretas
- confirma a aula que será gerada agora

Entrega esperada:

- confirmação objetiva do que foi aprovado
- ausência de conteúdo completo antes da aprovação

### 3. Geração

Nesta etapa, o agente escreve a aula.

O agente:

- gera uma aula por vez
- usa Markdown limpo
- estrutura o conteúdo com `:::tipo`
- cria questões interativas no padrão do renderer
- evita HTML bruto
- usa `scripts/create_lesson_template.py` como gerador-base quando precisar começar uma aula nova no formato canônico
- trata aulas fundacionais como aulas de base: **explica antes de cobrar**
- define explicitamente o conceito principal antes de pedir distinções ou classificação
- quando a aula apresenta uma categoria ampla (ex.: software, hardware, redes), explica os subtipos principais com exemplos reais antes das perguntas
- usa questões inline apenas como verificação de compreensão, não como substitutas da explicação

Entrega esperada:

- aula completa
- título claro
- introdução
- seções pedagógicas coerentes
- fechamento

### 4. Validação

Nesta etapa, o agente confronta a aula com o contrato real do projeto.

O agente:

- revisa a sintaxe Markdown
- revisa a presença dos blocos necessários
- confere se a aula respeita o contrato do renderer
- confronta a aula com o comportamento real de `validate_lesson.py`
- detecta inconsistências entre renderer e validador antes de tentar publicar

Entrega esperada:

- aula revisada
- nota explícita sobre qualquer incompatibilidade do pipeline

### 5. Publicação

Nesta etapa, o agente usa os scripts do projeto.

O agente:

- salva o conteúdo em arquivo `.md`
- chama o script de publicação com os argumentos corretos
- informa o caminho publicado
- informa o status da validação
- informa o status de commit e push

Entrega esperada:

- confirmação do arquivo publicado
- caminho final
- resumo do resultado operacional

## 4. Contrato Markdown do ProfessorDash

### 4.1 Regra central

O contrato real do ProfessorDash é definido principalmente por:

- `skills/coimbraclaw-prof/scripts/validate_lesson.py`
- `skills/coimbraclaw-prof/scripts/publish_lesson.py`
- o renderer do ProfessorDash, que usa blocos `:::tipo`

### 4.2 Regra sobre frontmatter YAML

Estado operacional desta skill:

- frontmatter YAML é **opcional**
- se presente, o validador remove o bloco antes de validar o conteúdo da aula

Conclusão operacional definitiva:

- o arquivo pode incluir ou omitir o bloco YAML
- ambos os formatos são válidos
- se o fluxo do professor exigir metadados formais, manter frontmatter YAML é a forma recomendada

### 4.3 Estrutura por blocos `:::tipo`

Os blocos `:::tipo` são a forma nativa de estruturar conteúdo especial no ProfessorDash.

Consequência:

- `:::tipo` é a forma certa de escrever componentes especiais
- o HTML resultante deve ser produzido pelo renderer, não manualmente pelo autor da aula

### 4.4 HTML direto no Markdown

Regra recomendada por esta skill:

- nunca usar HTML direto no Markdown da aula

Conclusão:

- para consistência editorial e para preservar o contrato do ProfessorDash, não escrever HTML manual
- usar apenas Markdown comum e blocos `:::tipo`

### 4.5 Título e abertura

`validate_lesson.py` exige:

- a primeira linha útil do arquivo deve ser um título H1 no formato `# Título`
- a primeira linha de conteúdo depois do H1 deve ser um parágrafo simples

Isso significa:

- não começar a aula com bloco `:::`
- não começar com lista
- não começar com tabela
- não começar com citação

### 4.6 Seções mínimas

`validate_lesson.py` procura obrigatoriamente:

- `## Questões de fixação`
- `## Atividade prática`
- `## Fechamento`

Observação:

- o script emite warning se houver menos de 4 seções H2
- a primeira linha útil precisa ser H1
- a primeira linha de conteúdo após o título precisa ser um parágrafo simples

### 4.7 Questões

No formato autoral:

- `:::questao` é a sintaxe de autoria
- a validação ocorre diretamente sobre o Markdown fonte
- o validador atual exige **exatamente 2 blocos** `:::questao` por aula
- cada bloco deve ter exatamente **1 alternativa** terminando com ` *`
- o conteúdo continua devendo ensinar antes de cobrar, mesmo com só 2 questões no contrato atual

Conclusão operacional:

- o contrato do renderer é `:::questao`
- o contrato do validador atual é `:::questao` com **2 blocos exatos**
- a documentação antiga que falava em 5 a 6 questões está desatualizada para este ambiente
- o sistema deve **ensinar antes de avaliar**, especialmente em aulas fundacionais

### 4.8 Limites de tamanho recomendados

Recomendação editorial definitiva desta skill:

- título: até 80 caracteres
- descrição curta: até 160 caracteres quando usada em metadados auxiliares
- introdução: 1 a 2 parágrafos curtos
- cada bloco `:::tipo`: 3 a 10 linhas úteis
- cada seção H2: 1 objetivo pedagógico claro
- aula completa: preferencialmente entre 700 e 1800 palavras
- questões: enunciado curto, alternativas objetivas, gabarito conciso

## 5. Blocos disponíveis

### 5.1 `:::objetivo`

Sintaxe exata:

```markdown
:::objetivo
Ao final da aula, o estudante será capaz de identificar os elementos centrais do tema.
:::
```

### 5.2 `:::importante`

Sintaxe exata:

```markdown
:::importante
Nem todo sistema automatizado usa inteligência artificial.
:::
```

### 5.3 `:::dica`

Sintaxe exata:

```markdown
:::dica
Peça aos alunos que comparem um chatbot simples com um assistente que aprende com dados.
:::
```

### 5.4 `:::exemplo`

Sintaxe exata:

```markdown
:::exemplo
Um aplicativo de streaming que recomenda filmes com base no histórico do usuário usa técnicas de IA para prever preferências.
:::
```

### 5.5 `:::atencao`

Sintaxe exata:

```markdown
:::atencao
Evite dizer que toda decisão automática é inteligente. Muitas vezes ela apenas segue regras programadas.
:::
```

### 5.6 `:::conceito`

Sintaxe exata:

```markdown
:::conceito
Inteligência artificial é a área da computação dedicada a construir sistemas capazes de executar tarefas que exigem análise, decisão ou previsão.
:::
```

### 5.7 `:::exercicio`

Sintaxe exata:

```markdown
:::exercicio
Observe três aplicações do seu dia a dia e classifique quais usam dados para prever, recomendar ou reconhecer padrões.
:::
```

### 5.8 `:::curiosidade`

Sintaxe exata:

```markdown
:::curiosidade
O termo inteligência artificial foi consolidado em 1956, em um encontro de pesquisadores em Dartmouth.
:::
```

### 5.9 `:::roteiro`

Sintaxe exata:

```markdown
:::roteiro
Pergunte aos alunos quais aplicativos do celular parecem “pensar”.
Anote no quadro as respostas antes de apresentar a definição formal.
:::
```

Correção importante:

- `:::roteiro` deve ser tratado como apoio de fala do professor
- não afirmar ocultação automática em modo aluno sem evidência de código

### 5.10 `:::resumo`

Sintaxe exata:

```markdown
:::resumo
- IA usa dados para reconhecer padrões
- nem toda automação é IA
- exemplos cotidianos ajudam a identificar aplicações reais
:::
```

### 5.11 `:::questao`

Sintaxe exata:

```markdown
:::questao O que caracteriza uma aplicação de inteligência artificial?
a) Executar sempre a mesma regra sem analisar dados
b) Usar dados para reconhecer padrões e apoiar decisões *
c) Exibir uma tela colorida para o usuário
d) Ser executada apenas na internet
> A alternativa correta é a letra B porque IA depende do uso de dados e modelos para estimar, classificar ou recomendar algo.
:::
```

## 6. Regras para questões interativas

### 6.1 Sintaxe completa linha a linha

Linha 1:

```markdown
:::questao Enunciado da pergunta?
```

Linha 2 em diante:

```markdown
a) Alternativa A
b) Alternativa B
c) Alternativa C *
d) Alternativa D
```

Linha de explicação:

```markdown
> Explicação do gabarito
```

Fechamento:

```markdown
:::
```

### 6.2 Como escrever alternativas

Escreva sempre no padrão:

- `a) Texto`
- `b) Texto`
- `c) Texto`
- `d) Texto`

### 6.3 Como marcar a alternativa correta

A alternativa correta é marcada com um asterisco no final da linha:

```markdown
c) Alternativa correta *
```

### 6.4 Como adicionar gabarito e explicação

Use uma linha iniciada por `>`:

```markdown
> A resposta correta é a letra C porque...
```

### 6.5 Compatibilidade com o validador atual

O validador atual valida diretamente o Markdown fonte:

- detecta blocos `:::questao`
- aceita entre **5 e 6 blocos** por aula
- exige exatamente uma alternativa terminando com ` *` em cada bloco
- exige pelo menos 1 questão de cenário real aplicado
- exige pelo menos 1 questão de erro, problema, falha ou risco
- limita a no máximo 2 questões no padrão “não é verdadeira”

Portanto:

- a sintaxe autoral correta `:::questao` é compatível com o validador
- não é necessário gerar HTML manual para passar na validação

## 7. Estrutura padrão de uma aula

### 7.1 Template solicitado com frontmatter

O template canônico completo fica em `references/lesson-template.md`.

Princípio pedagógico obrigatório do template atual:

- primeiro construir o conceito
- depois mostrar exemplo concreto
- só então inserir questão inline
- em aulas fundacionais, nomear e explicar explicitamente os subtipos principais antes das perguntas

Estrutura resumida do contrato atual:

```markdown
---
title: Título da aula
description: Descrição curta da aula
order: 1
published: true
---

# Título da aula

Parágrafo introdutório simples apresentando o tema, a relevância e o recorte da aula.

## Abertura

:::objetivo
Objetivo de aprendizagem.
:::

:::dica
Estratégia de observação ou estudo.
:::

:::curiosidade
Fato curto de contexto.
:::

## Desenvolvimento

:::conceito
Definição central.
:::

:::exemplo
Caso concreto de aplicação.
:::

:::questao Um estudante da SEED-PR aplicou esse conceito em um cenário real. Qual situação representa melhor esse uso?
a) Alternativa A *
b) Alternativa B
c) Alternativa C
d) Alternativa D
> Explique por que a alternativa correta representa um cenário aplicado.
:::

:::importante
Ponto crítico.
:::

:::atencao
Erro comum, risco ou limitação.
:::

:::questao Ao revisar a solução abaixo, qual erro ou problema precisa ser identificado primeiro?
a) Alternativa A
b) Alternativa B *
c) Alternativa C
d) Alternativa D
> Explique por que a alternativa correta aponta o principal problema.
:::

:::roteiro
Notas do professor.
:::

## Questões de fixação

:::questao Questão de consolidação do conceito.
a) Alternativa A
b) Alternativa B *
c) Alternativa C
d) Alternativa D
> Explique a resposta correta.
:::

:::questao Questão de aplicação prática.
a) Alternativa A
b) Alternativa B
c) Alternativa C *
d) Alternativa D
> Explique a consequência mais provável.
:::

:::questao Sobre as afirmações abaixo, qual NÃO é verdadeira?
a) Alternativa A
b) Alternativa B
c) Alternativa C *
d) Alternativa D
> Explique por que a alternativa correta é a única incorreta.
:::

## Atividade prática

:::exercicio
Atividade conectada ao objetivo da aula.
:::

## Fechamento

:::resumo
- Síntese 1
- Síntese 2
- Síntese 3
:::
```

## 8. Publicação

### 8.1 Caminho exato dos scripts no workspace atual

- `/home/devuser/.openclaw/workspace/skills/coimbraclaw-prof/scripts/create_lesson_template.py`
- `/home/devuser/.openclaw/workspace/skills/coimbraclaw-prof/scripts/validate_lesson.py`
- `/home/devuser/.openclaw/workspace/skills/coimbraclaw-prof/scripts/publish_lesson.py`

### 8.2 Caminho interno do repositório usado pelo script de publicação

No código de `publish_lesson.py`, a constante é:

```python
REPO_PATH = Path("/home/devuser/projects/ProfToniCoimbra")
```

### 8.2 Geração de rascunho no formato novo

Use o gerador para iniciar uma aula no formato canônico:

```bash
python3 /home/devuser/.openclaw/workspace/skills/coimbraclaw-prof/scripts/create_lesson_template.py \
  --title "Título da aula" \
  --description "Descrição curta da aula" \
  --order 1 \
  --output /tmp/aula.md
```

O script gera um rascunho já compatível com o formato novo, com:

- H1
- parágrafo introdutório simples
- blocos `:::tipo`
- 5 blocos `:::questao`
- pelo menos 1 questão de cenário real aplicado
- pelo menos 1 questão de erro ou problema
- `## Questões de fixação`
- `## Atividade prática`
- `## Fechamento`

### 8.3 Argumentos necessários do `publish_lesson.py`

O script exige:

- `--input`
- `--series`
- `--subject`
- `--lesson-number`
- `--title`

Argumento opcional:

- `--push`

### 8.4 Materiais brutos do Drive

Materiais-fonte baixados do Drive (pptx, pdf, mp4, docx e similares) são temporários:

- baixar para `materiais-seed/<disciplina>/<aula>/raw/`
- esta pasta está no `.gitignore` e nunca deve ser commitada
- após extrair texto e gerar a aula, apagar os arquivos brutos o quanto antes
- manter apenas `text/` e `sintese.md` do corpus
- nunca fazer push de vídeo, pptx, pdf ou material bruto para nenhum repositório

## 9. Resposta ao professor

### 9.1 Durante o planejamento

Formato esperado:

```markdown
# Planejamento da sequência

1. Aula 1 - Introdução ao tema
2. Aula 2 - Conceitos centrais
3. Aula 3 - Aplicações práticas
4. Aula 4 - Revisão e atividade

Se aprovar, eu gero a Aula 1 no formato do ProfessorDash.
```

### 9.2 Após a publicação

Formato esperado:

```markdown
Publicação concluída.

Arquivo: aula-01-introducao-a-inteligencia-artificial.md
Título: Introdução à Inteligência Artificial
Blocos criados: 9
Questões criadas: 2
Validação: ok
Caminho publicado: publicadas/materias/disciplinas-extras/inteligencia-artificial/aula-01-introducao-a-inteligencia-artificial.md
```

## 9.3 Aulas estáticas em HTML (modo blueprint / site real)

Quando o pedido for uma aula estática em HTML, não basta converter o conteúdo para um arquivo solto. O visual deve conversar com o ecossistema real do ProfessorDash.

Padrão visual preferencial:
- dark theme
- fonte `Geist` para títulos e corpo
- fonte `Geist Mono` ou equivalente para código
- superfícies escuras (`#000000`, `#0d0d0d`, `#1a1a1a`)
- texto claro (`#e5e2e1`)
- paleta de apoio compatível com o site:
  - verde `#10b981`
  - violeta `#8b5cf6`
  - ciano `#06b6d4`
  - coral `#f87171`
- bordas suaves com branco translúcido
- aparência clean, técnica e premium

Fonte de verdade para esse visual:
- `templates/base.html`
- `templates/aulas/aula_detalhe.html`
- layouts experimentais em `layout/aula/code.html`

Conduta correta:
- antes de criar/refatorar uma aula estática, ler os tokens reais do projeto
- alinhar cores, tipografia, contraste e espaçamento ao site atual
- evitar visual de apostila clara se o site real estiver em dark theme, salvo quando o professor pedir explicitamente formato de apostila imprimível
- manter o conteúdo pedagógico, mas adaptar UI/UX ao sistema existente

### Modo apostila estática reutilizável

Quando o professor quiser um HTML estático “tipo apostila” que possa:
- imprimir em A4 / salvar em PDF
- abrir fora do site
- manter identidade visual próxima do ProfessorDash

usar este compromisso de implementação:
- arquivo HTML único, sem dependência do Django
- incluir Google Fonts (`Geist` + `Geist Mono`)
- definir tokens via CSS custom properties para **dois temas**:
  - `[data-theme="dark"]`
  - `[data-theme="light"]`
- adicionar botão simples de alternância de tema com persistência em `localStorage`
- adicionar botão `window.print()`
- incluir `@media print` com limpeza da UI e contraste adequado para papel/PDF
- manter estrutura de apostila (hero + seções + callouts + blocos de código + tabela demo), não layout de dashboard
- no modo tela, preservar a paleta do ecossistema:
  - verde `#10b981`
  - violeta `#8b5cf6`
  - ciano `#06b6d4`
  - coral `#f87171`
- no rodapé, preferir texto autoral do professor em vez de branding do sistema quando o material for distribuído como apostila independente
  - padrão seguro: `Material produzido pelo Prof. Toni Coimbra.`

Heurística prática:
- se o pedido mencionar “apostila”, “imprimir”, “PDF”, “usar onde quiser” ou “HTML estático”, não entregar visual de painel/app; entregar visual editorial limpo com tema claro/escuro e impressão tratada.

## 10. Regras absolutas

- NUNCA gerar aula completa antes da aprovação do planejamento quando o pedido ainda estiver em fase de definição.
- NUNCA publicar em série ou disciplina fora da tabela de `repo-layout.md`.
- NUNCA usar HTML bruto como forma principal de autoria da aula.
- NUNCA começar a aula com bloco especial, lista, tabela ou citação; a primeira linha útil deve ser H1 e a linha seguinte deve ser um parágrafo simples.
- NUNCA omitir as seções `## Questões de fixação`, `## Atividade prática` e `## Fechamento` quando o objetivo for seguir o validador atual.
- NUNCA usar menos de 5 nem mais de 6 blocos `:::questao` por aula no contrato atual.
- NUNCA colocar a primeira questão antes de o conceito ter sido explicado e exemplificado.
- NUNCA usar questões para substituir explicação fundacional.
- NUNCA usar mais de 2 questões inline antes de `## Questões de fixação`.
- NUNCA marcar mais de uma alternativa correta em um mesmo bloco `:::questao`.
- NUNCA deixar a aula sem pelo menos 1 questão de cenário real aplicado.
- NUNCA deixar a aula sem pelo menos 1 questão de erro, problema, falha ou risco.
- NUNCA usar mais de 2 questões no formato “qual NÃO é verdadeira”.
- NUNCA esconder incompatibilidades do pipeline para forçar publicação.
- NUNCA gerar HTML manual para satisfazer o validador.
- NUNCA subir materiais brutos do Drive para git.
- SEMPRE incluir frontmatter YAML se o professor solicitar metadados; o validador aceita frontmatter opcional.
- SEMPRE usar Markdown limpo com blocos `:::tipo` para autoria de componentes especiais.
- SEMPRE conferir `validate_lesson.py` antes de prometer publicação automática.
- SEMPRE gerar uma aula por vez após a aprovação.
- SEMPRE usar nomes de arquivo no padrão `aula-XX-titulo-slug.md`.
- SEMPRE tratar o código do repositório como fonte de verdade acima de documentação antiga, notas resumidas ou memória operacional.

## Apêndice A. Mapa resumido dos callouts

| Bloco | Ícone | Classe CSS |
|---|---|---|
| `objetivo` | `🎯` | `c-green` |
| `importante` | `⚠️` | `c-amber` |
| `dica` | `💡` | `c-blue` |
| `exemplo` | `📝` | `c-violet` |
| `atencao` | `🚨` | `c-coral` |
| `conceito` | `📖` | `c-blue` |
| `exercicio` | `✍️` | `c-violet` |
| `curiosidade` | `🔍` | `c-blue` |

## Apêndice B. Resumo das correções incorporadas

- frontmatter YAML agora é tratado como opcional na validação
- `:::questao` é o formato autoral correto e validado diretamente no Markdown fonte
- `:::roteiro` é tratado como apoio de fala, sem afirmar ocultação automática indevida
- o pipeline foi documentado como alinhado ao formato autoral do ProfessorDash
- materiais brutos do Drive foram formalmente marcados como temporários e proibidos no git
