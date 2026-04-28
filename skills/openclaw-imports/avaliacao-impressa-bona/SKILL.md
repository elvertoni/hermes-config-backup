---
name: avaliacao-impressa-bona
description: Gerar avaliações impressas no padrão do Colégio Estadual Theodoro de Bona. Use quando o Toni pedir prova, avaliação, teste ou recuperação para qualquer disciplina.
---

# avaliacao-impressa-bona

Skill para gerar avaliações impressas no padrão oficial do Colégio Estadual Theodoro de Bona — EFMP. Cabeçalho institucional preservado, formatação padronizada e upload automático para Google Docs (Drive coimbrabot).

---

## 1. Padrão visual

### Cabeçalho
O template DOCX (`Avaliacao_Bona_Template.docx`) contém o cabeçalho oficial da escola com:
- Brasão/logotipo circular à esquerda ("COLÉGIO ESTADUAL THEODORO DE BONA")
- Brasão à direita
- Nome da escola, endereço, telefone, e-mail
- Campos: Série/Ano, Turma, Trimestre, Data, Nota, Valor, Disciplina, Professor, Aluno(a)

**NUNCA adicionar título redundante no corpo** (ex: "AVALIAÇÃO DE..."). Os dados da disciplina já estão no cabeçalho.

### Corpo da prova
- **Enunciados:** negrito, tamanho 11pt, alinhamento à esquerda
- **Alternativas:** regular, tamanho 10.5pt, recuo de 1.2cm, alinhamento à esquerda
- **Instruções:** "Leia atentamente... Cada questão vale 0,6 pontos."
- **Fonte:** Times New Roman (padrão do template)
- **Margens:** 2cm top/bottom, 2.5cm left/right
- **Rodapé:** "BOA PROVA!" centralizado, negrito, 12pt
- **Valor padrão:** 0,6 pontos por questão (total = questões × 0,6)

### Distribuição de alternativas
- Equilibrar entre A, B, C, D (ex: A=3, B=2, C=3, D=2 para 10 questões)
- NUNCA concentrar a resposta correta em uma única letra
- Após embaralhar, verificar distribuição e ajustar manualmente se necessário

---

## 2. Fluxo de geração

### Passo 1 — Ler as aulas
Ler os arquivos `.md` das aulas no repositório:
```
/root/work/ProfToniCoimbra/publicadas/materias/{serie}/{disciplina}/
```

### Passo 2 — Criar questões
- 10 questões de múltipla escolha com 4 alternativas cada
- Distribuir entre as aulas do intervalo solicitado
- Evitar decoreba — focar em compreensão e aplicação
- Incluir pelo menos 1 questão com caso real
- Incluir pelo menos 1 questão que exige raciocínio de diagnóstico

### Passo 3 — Embaralhar alternativas
- A correta NUNCA deve ficar na mesma posição em todas as questões
- Distribuir balanceado entre A/B/C/D (diferença máxima de 1 entre letras)
- Fazer manualmente para garantir equilíbrio

### Passo 4 — Gerar DOCX
Usar o script `scripts/generate.py`:
```bash
python3 ~/.hermes/skills/openclaw-imports/avaliacao-impressa-bona/scripts/generate.py /tmp/questions.json Avaliacao_Disciplina
```
O script:
- Usa o template Theodoro de Bona com cabeçalho preservado
- Aplica margens 2cm/2.5cm
- Adiciona **letras** (a, b, c, d) antes de cada alternativa
- Enunciados em negrito 11pt, alternativas regular 10.5pt com recuo 1.2cm
- "BOA PROVA!" centralizado ao final

O template está em: `~/.hermes/cache/documents/doc_81bd7d337c3d_Avaliacao_Bona_Template.docx`

### Passo 5 — Upload para Google Docs
```bash
python3 /root/.hermes/scripts/refresh_google_token.py
# Upload multipart DOCX -> Google Doc via Drive API
# Exemplo em /tmp/mp_final.txt
```
O token do coimbrabot (`~/.hermes/google_token.json`) já tem escopos `drive` e `documents`. O refresh é automático via script.

---

## 3. Template de questões

```python
questions = [
    ("1. Enunciado em negrito...",
     ["a) Alternativa A",
      "b) Alternativa B (correta)",
      "c) Alternativa C",
      "d) Alternativa D"],
     "B"),  # gabarito
    ...
]
```

---

## 4. Estrutura de diretórios relevante

| Caminho | Conteúdo |
|---------|----------|
| `~/.hermes/cache/documents/doc_81bd7d337c3d_Avaliacao_Bona_Template.docx` | Template com cabeçalho oficial |
| `~/.hermes/scripts/refresh_google_token.py` | Renovação automática de token OAuth |
| `~/.hermes/google_token.json` | Token OAuth coimbrabot (drive + documents) |
| `/root/work/ProfToniCoimbra/publicadas/materias/` | Aulas publicadas por série/disciplina |

---

## 5. Disciplinas atendidas

| Série | Disciplina | Caminho |
|-------|-----------|---------|
| 1ª | Análise e Métodos para Sistemas | `publicadas/materias/1a-serie/analise-e-metodos-para-sistemas/` |
| 1ª | Introdução à Computação | `publicadas/materias/1a-serie/introducao-a-computacao/` |
| 2ª | Inovação, Tecnologia e Empreendedorismo | `publicadas/materias/2a-serie/inovacao-tecnologia-e-empreendedorismo/` |
| 2ª | Programação Front-End | `publicadas/materias/2a-serie/programacao-front-end/` |
| 3ª | Programação no Desenvolvimento de Sistemas | `publicadas/materias/3a-serie/programacao-no-desenvolvimento-de-sistemas/` |
| 3ª | Análise e Projeto de Sistemas | `publicadas/materias/3a-serie/analise-e-projeto-de-sistemas/` |

---

## 6. Pitfalls

- NUNCA adicionar título no corpo (dados já estão no cabeçalho)
- NUNCA deixar todas as respostas corretas na mesma letra
- NUNCA esquecer de adicionar as letras (a, b, c, d) antes de cada alternativa
- NUNCA esquecer de renovar o token antes do upload
- NUNCA usar `execute_code` para manipular tokens (a censura corrompe o valor)
- SEMPRE usar o template com cabeçalho — nunca criar documento do zero
- SEMPRE verificar distribuição do gabarito antes de gerar o DOCX
- SEMPRE entregar o link do Google Docs + gabarito

---

## 7. Exemplo de uso

```
Usuário: "faça uma avaliação de introducao a computacao no mesmo padrao, da aula 01 até 09"
```

Resposta esperada:
1. Ler aulas 01 a 09
2. Criar 10 questões com distribuição balanceada A/B/C/D
3. Gerar DOCX com template Bona
4. Upload para Google Docs
5. Entregar link + gabarito
