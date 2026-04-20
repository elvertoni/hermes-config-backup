# Fallback por gog para Classroom + Forms

Use este fallback quando não houver browser/automação visual disponível.

## O que funciona neste host

Já foi confirmado que funcionam, ao menos em parte:
- `gog classroom topics create`
- `gog classroom coursework create`
- `gog classroom coursework list/get`
- `gog forms create`
- `gog forms update`
- `gog forms add-question`

## Limitação importante já encontrada

No ambiente atual, o fluxo por `gog` não expôs claramente a anexação nativa do Google Form dentro da atividade do Classroom, no mesmo padrão do fluxo UI do Toni.

Ou seja:
- a atividade pode ser criada
- o formulário pode ser criado
- mas o anexo nativo do Form à atividade pode não ficar disponível via CLI atual

## Fallback aceitável

Quando precisar entregar algo funcional mesmo sem anexo nativo:

1. criar o tópico com o mesmo título da atividade
2. criar o Google Form com o mesmo título
3. adicionar as perguntas
4. publicar a atividade com:
   - título correto
   - tópico correto
   - `100` pontos
   - link público do Form na descrição

## Exemplo real já executado

Curso:
- `793556557371`

Publicação feita:
- tópico `Atividade 009 - 1º TRI`
- assignment `Atividade 009 - 1º TRI`
- form criado e linkado na descrição

## Modelo de descrição curta

```text
Aula 08 — Priorização e Validação de Requisitos

Responda o formulário da atividade no link abaixo:
<LINK_DO_FORM>
```

Se fizer sentido, encerrar com uma linha direta como:
- `Marque a alternativa correta.`
- `Leia com atenção e responda ao formulário.`

## Regra de honestidade operacional

Ao usar fallback:
- dizer explicitamente que ficou com link do Form na descrição
- não afirmar que o Form ficou anexado nativamente se isso não ocorreu
