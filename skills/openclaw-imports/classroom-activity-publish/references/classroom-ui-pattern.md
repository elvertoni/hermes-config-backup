# Fluxo UI do Toni para publicar atividade no Google Classroom

Fonte desta referência:
- vídeo: `Gravação de Tela 2026-03-15 182048.mp4`
- Drive fileId: `1aN8AOqx0Ru-y3C00ogLl5eXcMjD7nSZw`
- analisado em 2026-04-08

## Objetivo do fluxo

Publicar uma atividade no Google Classroom com Google Forms integrado, seguindo o padrão visual e operacional que o Toni usa de fato.

## Padrão observado

- atividade criada dentro da turma desejada
- título no formato `Atividade 003 - 2º TRI` (generalizar para `Atividade NNN - Xº TRI`)
- tópico com o mesmo nome da atividade
- pontuação: `100`
- formulário Google Forms anexado à atividade
- `Importação de notas` ativada
- sem data de entrega, salvo necessidade
- publicação pelo botão `Atribuir`

## Sequência observada no vídeo

### 1. Entrar na turma certa

No mural da turma, abrir a turma correta antes de iniciar a postagem.

### 2. Criar a atividade

Abrir a criação de atividade no Classroom.

Campos observados:
- `Título*`
- `Instruções (opcional)`
- área de anexos (`Drive`, `YouTube`, `Criar`, `Fazer upload`, `Link`, etc.)
- painel lateral com turma, estudantes, pontos, data, tema e rubrica

### 3. Preencher o título

Usar o padrão:
- `Atividade NNN - Xº TRI`

No vídeo:
- primeiro houve digitação parcial/incorreta
- depois o título foi corrigido para `Atividade 003 - 2º TRI`

## 4. Anexar um Google Forms

No vídeo, a atividade ficou com um anexo do tipo Google Forms identificado como `Blank Quiz`.

Interpretação operacional:
- o fluxo preferido é anexar/criar um Google Forms diretamente a partir da atividade
- isso mantém o formulário ligado ao Classroom no padrão nativo

## 5. Configurar a atividade

Configurações claramente visíveis:
- turma: a turma selecionada
- atribuição: `Todos os estudantes`
- pontos: `100`
- data de entrega: `Sem data de entrega`
- tema/tópico: mesmo nome da atividade
- `Importação de notas`: ativada
- `Modo bloqueado em Chromebooks`: desativado no caso observado
- originalidade/plágio: não era o foco do fluxo

## 5.1 Configurações obrigatórias do Google Forms

Além da atividade no Classroom, o formulário deve seguir este padrão:
- `Criar teste`: ativado
- `Coletar e-mail verificado`: ativado
- `Limitar a 1 resposta`: ativado
- `50` pontos por questão objetiva

Se uma automação não conseguir aplicar uma dessas opções, não considerar o trabalho realmente fechado sem avisar.

## 6. Editar o formulário

O vídeo mostra ida ao Google Forms para editar o formulário anexado.

Elementos visíveis:
- título do formulário igual ao da atividade
- aba `Perguntas`
- questão de múltipla escolha / seleção
- alternativas preenchidas
- resposta correta marcada
- pontuação configurada

Também foi visível a cópia de um texto-base para servir como enunciado/contexto da questão.

## 7. Voltar ao Classroom e revisar

De volta à atividade do Classroom, conferir:
- título final correto
- formulário anexado
- tópico correto
- pontuação 100
- descrição/instrução curta

Texto de instrução curto visto no fluxo analisado:
- algo no padrão `Marque a alternativa correta.`

## 8. Publicar

Usar o botão azul `Atribuir`.

Menu visível no vídeo:
- `Atribuir`
- `Agendar`
- `Salvar rascunho`
- `Descartar rascunho`

Default: `Atribuir`, salvo pedido explícito para agendar.

## Checklist final

Antes de considerar pronto:
- [ ] turma correta
- [ ] título no padrão
- [ ] tópico igual ao título
- [ ] pontuação 100
- [ ] formulário anexado nativamente
- [ ] importação de notas ativa
- [ ] `Criar teste` ativado no Form
- [ ] `Coletar e-mail verificado` ativado
- [ ] `Limitar a 1 resposta` ativado
- [ ] `50` pontos por questão objetiva
- [ ] instrução curta e clara
- [ ] atividade atribuída/publicada

## Observação importante

Este fluxo é o padrão humano observado no vídeo.

### Mapeamento para API pública (descoberto em 2026-04-08)

A API pública do Classroom não permite enviar `materials.form` diretamente na criação.

O caminho que funciona é:
- criar a atividade com `materials.link`
- usar como URL o **edit URL** do Google Form
- o Classroom converte automaticamente esse link em `materials.form`

Exemplo conceitual:

```json
{
  "title": "Atividade 009 - 1º TRI",
  "workType": "ASSIGNMENT",
  "state": "PUBLISHED",
  "maxPoints": 100,
  "materials": [
    {
      "link": {
        "url": "https://docs.google.com/forms/d/<FORM_ID>/edit",
        "title": "Atividade 009 - 1º TRI"
      }
    }
  ]
}
```

Na resposta, o material passa a aparecer como `form`, com `formUrl`, `title` e `thumbnailUrl`.

Se a atividade já foi criada sem esse material nativo, `PATCH` em `materials` não funciona. Nesse caso, recriar a atividade é o caminho mais limpo.
