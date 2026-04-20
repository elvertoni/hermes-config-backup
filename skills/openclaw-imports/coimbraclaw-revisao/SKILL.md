---
name: coimbraclaw-revisao
description: Revisar aulas do ProfessorDash — sintaxe, blocos, questões e profundidade pedagógica. Use quando o Toni pedir revisão, feedback, checagem ou melhoria de uma aula antes de publicar ou após publicada.
updated: 2026-04-20
status: ativa
---

# coimbraclaw-revisao

Skill de revisão de aulas do ProfessorDash. Cobre dois eixos: revisão técnica (sintaxe, contrato do renderer, validador) e revisão pedagógica (profundidade, enriquecimento, qualidade do conteúdo).

---

## 1. Quando usar esta skill

- Toni pede "revisa essa aula"
- Toni pede "está boa assim?" após geração
- Toni quer melhorar uma aula já publicada no repo
- Aula foi gerada mas ainda não passou pelo validador
- Aula parece rasa, genérica ou muito próxima do slide original

---

## 2. Fluxo de revisão

### Passo 1 — Leitura completa

Ler a aula inteira antes de emitir qualquer opinião. Não interromper com perguntas.

### Passo 2 — Revisão técnica (checklist)

Verificar cada item abaixo e registrar: ✅ ok / ⚠️ atenção / ❌ erro

**Abertura**
- [ ] Primeira linha é H1 (`# Título`)
- [ ] Segunda linha é parágrafo simples, sem HTML, sem bloco `:::`, sem lista

**Seções obrigatórias**
- [ ] `## Questões de fixação` presente
- [ ] `## Atividade prática` presente
- [ ] `## Fechamento` presente
- [ ] Mínimo de 4 seções H2

**Questões**
- [ ] Entre 5 e 6 blocos `:::questao`
- [ ] Cada questão tem exatamente 1 alternativa marcada com ` *`
- [ ] Cada questão tem gabarito com `>` e mínimo 2 linhas
- [ ] Pelo menos 1 questão de cenário real aplicado
- [ ] Pelo menos 1 questão de erro, problema, falha ou risco
- [ ] No máximo 2 questões inline antes de `## Questões de fixação`
- [ ] No máximo 2 questões no formato "NÃO é verdadeira"
- [ ] Nenhuma questão aparece antes de `:::conceito` + explicação + `:::exemplo`

**Blocos**
- [ ] Nenhum HTML bruto no corpo da aula
- [ ] `:::roteiro` usado como apoio de fala, sem conteúdo essencial escondido
- [ ] `:::resumo` no fechamento com 3 a 5 itens

### Passo 3 — Revisão pedagógica (checklist)

Verificar cada dimensão de enriquecimento:

**Contexto histórico ou origem do problema**
- [ ] A aula explica por que o conceito existe, não só o que é
- [ ] Tem gatilho histórico, problema original ou motivação real

**Caso real**
- [ ] Há pelo menos um caso concreto e documentado (empresa, projeto, falha, sistema)
- [ ] O caso não é inventado nem genérico demais ("imagine uma empresa que...")
- [ ] O caso está conectado diretamente ao conceito da aula

**Conexão com o aluno técnico**
- [ ] A aula responde implicitamente "onde vou usar isso nos próximos 2 anos?"
- [ ] Há referência ao contexto do estágio, projeto do curso ou início de carreira

**Tensão ou contraponto**
- [ ] `:::atencao` traz erro real, limitação ou mal-uso — não repetição do conceito em negativo
- [ ] Há pelo menos um ponto de tensão intelectual ("parece simples, mas...")

**Curiosidade**
- [ ] `:::curiosidade` traz algo que o aluno não esperava
- [ ] Não repete o que já foi dito na aula

**Densidade geral**
- [ ] A aula vai além do slide/apostila fonte
- [ ] Um aluno que só lesse o slide teria aprendido mais alguma coisa nova aqui
- [ ] A linguagem é adequada ao ensino técnico (nem acadêmica demais, nem vaga demais)

### Passo 4 — Entrega do diagnóstico

Formato de saída obrigatório:

```
## Revisão técnica

✅ / ⚠️ / ❌  [item]: [observação objetiva se houver problema]

## Revisão pedagógica

✅ / ⚠️ / ❌  [dimensão]: [observação objetiva se houver problema]

## Resumo

[2 a 4 linhas: o que está bem, o que precisa melhorar, prioridade de correção]

## Próximo passo

[Uma ação clara: "posso corrigir agora" / "precisa de mais contexto do tema" / "pronta para publicar"]
```

### Passo 5 — Correção (se solicitada)

Se Toni pedir para corrigir após o diagnóstico:

1. Corrigir apenas os itens marcados como ⚠️ ou ❌
2. Não reescrever o que está funcionando
3. Entregar a aula corrigida completa no final
4. Não misturar diagnóstico e correção na mesma resposta

---

## 3. Critérios de qualidade pedagógica

### O que torna uma aula boa neste contexto

Uma aula boa para o Técnico em Desenvolvimento de Sistemas:

- Ensina o conceito com clareza antes de cobrar
- Mostra um caso real que o aluno pode imaginar vivendo
- Explica por que o conceito existe, não só o que é
- Tem pelo menos um ponto de tensão ou surpresa
- A atividade prática cabe em 15 a 20 minutos reais de sala
- O aluno sai sabendo algo que não sabia ao entrar

### O que torna uma aula fraca

- Reproduz os bullets do slide sem acrescentar nada
- Define o conceito sem explicar por que ele existe
- Usa exemplos genéricos ("imagine uma empresa de TI...")
- `:::curiosidade` repete o que o `:::conceito` já disse
- `:::atencao` é só o conceito escrito em negativo
- Atividade prática não tem conexão clara com o conteúdo da aula
- Questões testam memorização de definição, não compreensão aplicada

---

## 4. Regras absolutas

- NUNCA emitir diagnóstico sem ter lido a aula inteira
- NUNCA misturar diagnóstico e reescrita na mesma resposta
- NUNCA reescrever o que está correto — corrigir só o que está errado
- NUNCA aprovar uma aula com menos de 5 questões ou sem os 3 blocos obrigatórios
- NUNCA aprovar questão sem gabarito explicativo de no mínimo 2 linhas
- NUNCA aprovar `:::curiosidade` que repete o conceito já explicado
- SEMPRE usar o checklist completo das seções 2 e 3
- SEMPRE entregar o diagnóstico antes da correção
- SEMPRE indicar claramente se a aula está pronta para publicar ou não
