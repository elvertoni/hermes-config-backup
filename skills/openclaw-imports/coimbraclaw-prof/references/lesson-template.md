# Template canônico — skillprof / coimbraclaw-prof

Use este template como base autoral do ProfessorDash no contrato novo.

Regras incorporadas:
- 5 a 6 blocos `:::questao`
- pelo menos 1 questão de cenário real aplicado
- pelo menos 1 questão de erro, problema, falha ou risco
- no máximo 2 questões inline antes de `## Questões de fixação`
- pelo menos 3 questões dentro de `## Questões de fixação`
- no máximo 2 questões no formato “não é verdadeira”
- a primeira questão só pode aparecer **depois** de construção conceitual mínima (`:::conceito` + explicação + `:::exemplo`)

Lição operacional tirada da revisão da Aula 07 de IAC:
- **não cobrar antes de ensinar**
- se a aula introduz um conceito fundacional, definir explicitamente o termo central antes de pedir distinções
- se a aula apresenta uma categoria ampla (ex.: software, hardware, redes), explicar os subtipos principais com exemplos concretos antes das perguntas
- pergunta inline serve para verificação de compreensão, não para substituir explicação

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
Defina o que o estudante deve aprender ao final da aula.
:::

:::dica
Antecipe uma estratégia de observação ou estudo.
:::

:::curiosidade
Traga um fato histórico ou contextual curto.
:::

## Desenvolvimento

:::conceito
Apresente a definição central do conteúdo.
:::

Parágrafo de explicação em Markdown comum, sem HTML.

Se a aula for fundacional, explique aqui os subtipos, partes ou categorias principais com exemplos reais antes de qualquer cobrança.

:::exemplo
Mostre um caso concreto de aplicação ou um exemplo do cotidiano do aluno.
:::

Parágrafo curto conectando o exemplo ao conceito.

:::questao Um estudante da SEED-PR encontrou esse conceito em uma situação real. Qual cenário mostra melhor a aplicação prática?
a) Alternativa A *
b) Alternativa B
c) Alternativa C
d) Alternativa D
> Explique por que a alternativa correta representa um cenário aplicado.
:::

:::importante
Reforce um ponto conceitual que não pode ser confundido.
:::

Parágrafo explicando limite, risco, compatibilidade, dependência ou consequência prática.

:::atencao
Corrija um erro comum de interpretação ou destaque um risco importante.
:::

:::questao Ao revisar a solução abaixo, qual erro ou problema precisa ser identificado primeiro?
a) Alternativa A
b) Alternativa B *
c) Alternativa C
d) Alternativa D
> Explique por que a alternativa correta aponta o principal problema.
:::

:::roteiro
Registre perguntas de condução oral, transições ou exemplos que o professor deve puxar em aula.
:::

## Questões de fixação

:::questao Qual alternativa resume melhor o conceito central da aula?
a) Alternativa A
b) Alternativa B *
c) Alternativa C
d) Alternativa D
> Explique por que a alternativa correta resume melhor o conceito.
:::

:::questao Em uma situação prática, o que tende a acontecer se esse conceito for aplicado sem validação adequada?
a) Alternativa A
b) Alternativa B
c) Alternativa C *
d) Alternativa D
> Explique por que a alternativa correta representa a consequência mais provável.
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
Oriente uma atividade curta, individual ou em grupo, conectada ao conteúdo.
:::

## Fechamento

:::resumo
- Retome a ideia principal
- Reforce o conceito central
- Relacione com o cotidiano ou com a próxima aula
:::
```
