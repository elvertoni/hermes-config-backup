---
name: profdash-static-lesson
description: Criar aulas estáticas em HTML/CSS para o repositório ProfToniCoimbra quando o Toni pedir o padrão visual tipo blueprint/apostila, em vez do formato Markdown validado do ProfessorDash.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# profdash-static-lesson

Use esta skill quando o Toni pedir explicitamente:
- “aula estática”
- “padrão blueprint”
- HTML/CSS puro
- apostila visual/editorial
- ou quando ele rejeitar o formato Markdown do ProfessorDash por esperar um `.html` estilizado

## Quando usar

Esta skill existe porque há dois fluxos diferentes no ecossistema do Toni:

1. `coimbraclaw-prof`
- gera aula em Markdown
- segue o validador `validate_lesson.py`
- publica em `.md`
- serve para o renderer do ProfessorDash

2. `profdash-static-lesson`
- gera aula estática em HTML com CSS embutido
- não depende do validador Markdown
- serve para materiais no estilo apostila/blueprint visual
- publica em `.html`

Se o Toni mencionar o arquivo `blueprint-de-software-para-tcc.html` ou disser que quer “no padrão da aula estática”, **não usar o pipeline Markdown**.

## Fonte de verdade

Arquivo de referência confirmado no repositório:
- `/root/work/ProfToniCoimbra/publicadas/materias/3a-serie/analise-e-projeto-de-sistemas/blueprint-de-software-para-tcc.html`

Esse arquivo mostra o padrão visual esperado:
- HTML completo
- CSS embutido no `<style>`
- capa editorial
- cards/seções
- callouts visuais
- aparência de apostila premium

## Procedimento

### 1. Confirmar o formato esperado

Antes de escrever, verificar se o pedido é:
- aula dinâmica/renderizada em Markdown
ou
- aula estática `.html`

Sinais de aula estática:
- “quero em HTML/CSS apenas”
- “padrão blueprint”
- “aula estática”
- “igual àquela sobre blueprint”

### 2. Inspecionar a referência

Ler o arquivo de blueprint para reaproveitar a linguagem visual:
- capa com destaque editorial
- variáveis CSS em `:root`
- seções como cards
- callouts coloridos
- blocos de código com fundo escuro

### 3. Estruturar a aula

A estrutura recomendada é:
- `<!DOCTYPE html>`
- `<head>` com `<style>` embutido
- capa inicial com título, subtítulo e metadados
- seções com `h2`
- callouts explicativos
- exemplos de código
- exemplos visuais quando fizer sentido
- atividade prática ao final
- fechamento/resumo

### 4. Padrão pedagógico

Quando o Toni pedir algo como “explicação top” + “apenas um exercício ao final”:
- ensinar bem antes de cobrar
- evitar quiz intermediário se isso conflitar com o pedido
- deixar uma única atividade prática no final
- usar exemplos concretos e próximos da realidade dos alunos

### 5. Publicação

Salvar em `.html` dentro do repositório `ProfToniCoimbra`, no caminho da disciplina correspondente.

Exemplo:
- `publicadas/materias/2a-serie/programacao-front-end/aula-01-criacao-de-tabelas-com-html-e-css.html`

### 6. Git

Depois de salvar:
- revisar `git status`
- revisar diff se necessário
- `git add`
- `git commit`
- `git push origin main`

## Achados importantes

### O caminho do repo pode divergir da documentação

A documentação antiga pode apontar para:
- `/home/devuser/projects/ProfToniCoimbra`

Mas no ambiente real o clone pode estar em:
- `/root/work/ProfToniCoimbra`

Se scripts exigirem o caminho antigo, um symlink funcional resolve:
- `/home/devuser/projects/ProfToniCoimbra -> /root/work/ProfToniCoimbra`

### Não misturar os dois formatos

Se o usuário pediu aula estática e você publicar só `.md`, o resultado pode ficar tecnicamente correto para o ProfessorDash, mas errado para a expectativa do Toni.

A regra é:
- pedido de blueprint/estático → publicar `.html`
- pedido de aula normal do ProfessorDash → publicar `.md`

## Resposta final esperada

Ao concluir, informar de forma objetiva:
- arquivo criado
- caminho publicado
- commit SHA
- status do push
- se a versão anterior em `.md` foi mantida ou removida
