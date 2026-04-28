---
name: google-forms-quiz
description: Criar avaliação Google Forms com modo quiz e gabarito
---

# Google Forms Quiz — Criar avaliação com gabarito

## Trigger
Criar avaliação no Google Forms com modo quiz e gabarito para o Classroom.

## Pré-requisitos
- Token OAuth2 da conta escola (`/root/.hermes/google_token_escola.json`)
- Form já criado com `POST https://forms.googleapis.com/v1/forms`
- Modo quiz ativado com `updateSettings` antes de adicionar grading

## Estrutura correta de uma questão (createItem)

```python
item = {
    "title": "Texto completo da pergunta aqui?",  # title no NÍVEL do item
    "questionItem": {
        "question": {
            "questionId": "1",
            "required": True,
            "choiceQuestion": {
                "type": "RADIO",
                "options": [
                    {"value": "(A) Alternativa A", "isOther": False},
                    {"value": "(B) Alternativa B", "isOther": False},  # gabarito
                    {"value": "(C) Alternativa C", "isOther": False},
                    {"value": "(D) Alternativa D", "isOther": False},
                ],
                "shuffle": False
            },
            "grading": {
                "correctAnswers": {
                    "answers": [
                        {"location": {"index": 1}, "score": "1.0"}  # índice 1 = alternativa B
                    ]
                }
            }
        }
    }
}
```

## Armadilhas
- **NÃO** colocar `text` dentro de `question` — não existe esse campo
- O texto da pergunta vai em **`item.title`**, não em `item.questionItem.question`
- Gabarito = `index` da alternativa correta em `correctAnswers.answers[].location.index`
- Quiz mode deve ser ativado **antes** de adicionar grading
- `updateMask` para grading: `"questionItem.question.grading"`
- `requiredRevisionId` muda após cada `batchUpdate`

## Ordem de operações
1. Criar form (`POST`)
2. Adicionar descrição (`updateSettings` com `description`)
3. Ativar quiz mode (`updateSettings` com `quizSettings.isQuiz: true`)
4. Criar questões com `createItem` (cada uma = 1 `batchUpdate`)
5. Publicar no Classroom (`courseWork.create` com `materials.form`)

## Scripts de referência
- `/tmp/create_aps_form_v2.py` — estrutura errada (text em question)
- `/tmp/build_blueprint_form.py` — estrutura antiga incorreta
