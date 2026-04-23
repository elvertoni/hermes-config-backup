---
name: coimbraclaw-prof
description: Planejar e gerar aulas completas no formato Markdown do ProfessorDash para o Curso Técnico em Desenvolvimento de Sistemas. Use quando o Toni pedir planejamento, geração ou continuação de aulas. Sempre apresentar planejamento primeiro e aguardar aprovação; gerar uma aula por vez.
updated: 2026-04-20
status: ativa
---

# coimbraclaw-prof

Skill de geração de aulas do ProfessorDash. Cobre planejamento, escrita, enriquecimento pedagógico e preparação para publicação.

---

## 1. Contexto operacional

- Professor: Toni Coimbra — SEED-PR, Curso Técnico em Desenvolvimento de Sistemas
- Séries: 1ª, 2ª e 3ª
- Duração padrão: 50 minutos por aula presencial
- Destino: ProfessorDash em `aulas.tonicoimbra.com`
- Repositório local: `/root/work/ProfToniCoimbra`
- Materiais brutos (pptx, pdf, docx) são temporários — nunca subir para git

---

## 2. Disciplinas e caminhos de publicação

| Série | Disciplina | Caminho de publicação |
|---|---|---|
| 1ª série | Análise e Métodos para Sistemas | `publicadas/materias/1a-serie/analise-e-metodos-para-sistemas/` |
| 1ª série | Introdução à Computação | `publicadas/materias/1a-serie/introducao-a-computacao/` |
| 2ª série | Inovação, Tecnologia e Empreendedorismo | `publicadas/materias/2a-serie/inovacao-tecnologia-e-empreendedorismo/` |
| 2ª série | Programação Front-End | `publicadas/materias/2a-serie/programacao-front-end/` |
| 3ª série | Programação no Desenvolvimento de Sistemas | `publicadas/materias/3a-serie/programacao-no-desenvolvimento-de-sistemas/` |
| 3ª série | Análise e Projeto de Sistemas | `publicadas/materias/3a-serie/analise-e-projeto-de-sistemas/` |
| Extras | Inteligência Artificial | `publicadas/materias/disciplinas-extras/inteligencia-artificial/` |

Nome de arquivo padrão: `aula-NN.md` (apenas número, sem título no nome do arquivo).

---

## 3. Fluxo obrigatório

### Passo 1 — Planejamento

Quando o pedido envolver aula nova, sequência, módulo ou material ainda não aprovado:

1. Interpretar o pedido e identificar série, disciplina e tema
2. Sugerir sequência de títulos ordenados
3. Pedir aprovação antes de escrever qualquer aula
4. Não gerar conteúdo completo neste passo

Formato de entrega:

```
# Planejamento

1. Aula 01 - Título
2. Aula 02 - Título
3. Aula 03 - Título

Se aprovar, gero a Aula 01.
```

### Passo 2 — Geração

Após aprovação:

1. Gerar uma aula por vez
2. Aplicar enriquecimento obrigatório (seção 5)
3. Usar Markdown limpo com blocos `:::tipo`
4. Nunca adiantar a próxima aula sem pedido explícito

### Passo 3 — Publicação

1. Salvar em `.md` no caminho correto do repositório
2. Rodar `validate_lesson.py`
3. Fazer commit local
4. Fazer push para `origin main`

Regra operacional do Toni: ao finalizar uma aula, não deixar commit pendente. Aula concluída = commit + push automáticos.

Scripts:
- `/home/devuser/.openclaw/workspace/skills/coimbraclaw-prof/scripts/validate_lesson.py`
- `/home/devuser/.openclaw/workspace/skills/coimbraclaw-prof/scripts/publish_lesson.py`

Argumentos do `publish_lesson.py`: `--input`, `--series`, `--subject`, `--lesson-number`, `--title`, `--push` (opcional)

---

## 4. Enriquecimento obrigatório

Esta é a seção mais importante da skill. O conteúdo gerado nunca deve se limitar ao material fonte (slides, apostila, esboço). O Hermes deve enriquecer ativamente em cinco dimensões antes de escrever a aula.

### 4.1 Contexto histórico ou origem do problema

Por que esse conceito existe? Que problema ele veio resolver?

O aluno precisa entender o gatilho real do campo, não só a definição.

Exemplos de como fazer isso bem:
- Engenharia de Software → crise do software dos anos 1960: projetos atrasavam, custavam mais e entregavam menos
- Banco de dados relacional → problemas de redundância e inconsistência em arquivos planos
- Programação orientada a objetos → dificuldade de manutenção em sistemas procedurais grandes

### 4.2 Caso real de falha ou sucesso

Toda aula deve ter pelo menos um caso concreto e documentado de mercado. Não inventado, não genérico.

Preferir casos brasileiros quando existirem. Casos internacionais clássicos aceitáveis:
- Therac-25 (falha em software de radioterapia, mortes)
- Mars Climate Orbiter (bug de unidade de medida, perda de sonda)
- Bug do ano 2000 (Y2K)
- Falha no sistema HealthCare.gov no lançamento
- Crash do sistema do Bradesco em 2020
- Apagão aéreo TAM/Congonhas (sistemas de solo)

O caso deve ser curto — 3 a 5 linhas — e conectado diretamente ao conceito da aula.

### 4.3 Conexão com o cotidiano do aluno técnico

O aluno está no Técnico em Desenvolvimento de Sistemas. A aula deve responder implicitamente: "onde vou usar isso na minha vida profissional nos próximos 2 anos?"

Ancorar em situações reais do início de carreira:
- estágio em empresa de software local
- projeto integrador do curso
- primeiro emprego como júnior
- freelance para cliente pequeno

### 4.4 Tensão ou contraponto

Todo conceito tem uma limitação, um mal-uso comum ou uma confusão frequente. O bloco `:::atencao` deve trazer isso de forma honesta.

Não usar `:::atencao` para repetir o conceito em negativo. Usar para o que de fato confunde ou falha na prática.

### 4.5 Curiosidade que surpreende

O bloco `:::curiosidade` não deve repetir o que foi dito. Deve trazer algo que o aluno não esperava:
- dado histórico concreto
- estatística real com fonte
- origem de um termo técnico
- detalhe inusitado sobre a área

---

## 5. Contrato Markdown do ProfessorDash

### 5.1 Regras de abertura

- Primeira linha útil: `# Título` (H1)
- Segunda linha: parágrafo simples, sem HTML, sem bloco `:::`, sem lista
- Nunca começar com bloco especial, tabela ou citação

### 5.2 Seções obrigatórias

O validador `validate_lesson.py` exige:
- `## Questões de fixação`
- `## Atividade prática`
- `## Fechamento`
- Mínimo de 4 seções H2 no total

### 5.3 Questões

- **5 a 6 blocos** `:::questao` por aula
- Exatamente **1 alternativa correta** por questão, marcada com ` *` no final da linha
- Pelo menos **1 questão de cenário real aplicado**
- Pelo menos **1 questão de erro, problema, falha ou risco**
- No máximo **2 questões inline** antes de `## Questões de fixação`
- No máximo **2 questões no formato "NÃO é verdadeira"**
- A primeira questão só pode aparecer após `:::conceito` + explicação + `:::exemplo`

### 5.4 Frontmatter YAML

Opcional. Se presente, o validador remove antes de validar. Usar quando o professor solicitar metadados formais.

### 5.5 HTML direto

Nunca usar HTML bruto no corpo da aula. Usar apenas Markdown comum e blocos `:::tipo`.

---

## 6. Blocos disponíveis

| Bloco | Uso |
|---|---|
| `:::objetivo` | Objetivos de aprendizagem da aula |
| `:::conceito` | Definição central do conteúdo |
| `:::exemplo` | Caso concreto ou cotidiano |
| `:::curiosidade` | Fato surpreendente, histórico ou estatístico |
| `:::dica` | Estratégia de estudo ou observação |
| `:::importante` | Ponto crítico que não pode ser confundido |
| `:::atencao` | Erro comum, risco ou limitação real |
| `:::exercicio` | Atividade prática orientada |
| `:::roteiro` | Fala de apoio do professor — não esconde conteúdo essencial |
| `:::resumo` | Síntese em lista ao final da aula |
| `:::questao` | Questão interativa com alternativas e gabarito |

Sintaxe de todos os blocos:

```markdown
:::tipo
Conteúdo do bloco.
:::
```

Sintaxe do `:::questao`:

```markdown
:::questao Enunciado da pergunta?
a) Alternativa A
b) Alternativa B *
c) Alternativa C
d) Alternativa D
> Explicação do gabarito com no mínimo 2 linhas. Explica por que a correta é correta
e por que as demais estão erradas ou são insuficientes.
:::
```

---

## 7. Template canônico da aula

```markdown
---
title: Título da aula
description: Descrição curta da aula
order: 1
published: true
---

# Título da aula

Parágrafo introdutório de 3 a 5 linhas. Apresenta o tema, por que ele existe
e o que o aluno vai conseguir fazer ao final. Sem HTML. Sem bloco `:::`.

## Abertura

:::objetivo
Ao final desta aula, o estudante será capaz de [objetivo concreto e verificável].
:::

:::curiosidade
Fato histórico, estatístico ou inusitado que o aluno não esperava sobre o tema.
:::

:::dica
Estratégia prática de observação ou estudo conectada ao tema da aula.
:::

## Desenvolvimento

:::conceito
Definição central do conteúdo — clara, curta, sem jargão desnecessário.
:::

Parágrafo de explicação em Markdown comum. Aqui entra o contexto histórico
ou a origem do problema (seção 4.1 desta skill).

Se a aula for fundacional, explicar aqui os subtipos ou categorias principais
com exemplos reais antes de qualquer questão.

:::exemplo
Caso concreto do cotidiano do aluno técnico ou do mercado real.
Conectar diretamente ao conceito definido acima.
:::

Parágrafo curto conectando o exemplo ao conceito.

:::questao Um estudante em estágio encontrou esse problema. Qual ação representa
a aplicação correta do conceito estudado?
a) Alternativa A *
b) Alternativa B
c) Alternativa C
d) Alternativa D
> Explicação do gabarito.
:::

:::importante
Ponto crítico que o aluno não pode confundir ou ignorar.
:::

:::atencao
Erro comum, mal-uso frequente ou limitação real do conceito.
Não repetir o conceito em negativo — trazer o que de fato falha na prática.
:::

:::questao Em qual situação o uso incorreto desse conceito causaria um problema real?
a) Alternativa A
b) Alternativa B *
c) Alternativa C
d) Alternativa D
> Explicação do gabarito.
:::

:::roteiro
Perguntas de condução oral para a turma. Transições entre blocos.
Exemplos que o professor pode puxar ao vivo.
:::

## Questões de fixação

:::questao Questão que consolida o conceito central da aula.
a) Alternativa A
b) Alternativa B
c) Alternativa C *
d) Alternativa D
> Explicação do gabarito.
:::

:::questao Questão de cenário real aplicado — situação do mercado ou do estágio.
a) Alternativa A *
b) Alternativa B
c) Alternativa C
d) Alternativa D
> Explicação do gabarito.
:::

:::questao Sobre as afirmações abaixo, qual NÃO é verdadeira?
a) Alternativa A
b) Alternativa B
c) Alternativa C *
d) Alternativa D
> Explicação do gabarito.
:::

## Atividade prática

:::exercicio
Atividade curta, individual ou em dupla, conectada diretamente ao objetivo da aula.
Deve caber em 15 a 20 minutos dentro dos 50 minutos da aula.
Especificar o que produzir, como entregar e em qual ferramenta.
:::

## Fechamento

:::resumo
- Síntese do conceito central
- Conexão com a prática profissional
- O que vem na próxima aula
:::
```

---

## 8. Regras absolutas

- NUNCA gerar aula completa antes da aprovação do planejamento
- NUNCA publicar em série ou disciplina fora da tabela da seção 2
- NUNCA usar HTML bruto no corpo da aula
- NUNCA começar a aula com bloco `:::`, lista, tabela ou citação
- NUNCA omitir `## Questões de fixação`, `## Atividade prática` e `## Fechamento`
- NUNCA usar menos de 5 nem mais de 6 blocos `:::questao`
- NUNCA colocar questão antes de `:::conceito` + explicação + `:::exemplo`
- NUNCA usar questão para substituir explicação fundacional
- NUNCA marcar mais de uma alternativa correta por questão
- NUNCA omitir pelo menos 1 questão de cenário real aplicado
- NUNCA omitir pelo menos 1 questão de erro, problema, falha ou risco
- NUNCA usar `:::curiosidade` para repetir o que já foi dito
- NUNCA usar `:::atencao` para repetir o conceito em negativo
- NUNCA subir materiais brutos do Drive para git
- NUNCA gerar Aula N+1 sem pedido explícito
- SEMPRE enriquecer com contexto histórico, caso real e conexão profissional (seção 4)
- SEMPRE tratar o código do repositório como fonte de verdade acima de qualquer documentação
- SEMPRE usar nomes de arquivo no padrão `aula-XX-titulo-slug.md`
- SEMPRE conferir `validate_lesson.py` antes de prometer publicação automática
