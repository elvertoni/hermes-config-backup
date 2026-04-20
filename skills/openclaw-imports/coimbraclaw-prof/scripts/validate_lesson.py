#!/usr/bin/env python3
import argparse
import json
import re
import unicodedata
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n?", re.DOTALL)
ALT_CORRECT_RE = re.compile(r"^[a-zA-Z]\)\s*.+?\s\*\s*$")
QUESTION_OPEN_RE = re.compile(r"^:::questao\s+(.+)$")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
BLOCK_START_RE = re.compile(r"^:::(\w+)(?:\s+.*)?$")
SCENARIO_HINTS = [
    "cenario",
    "situacao",
    "contexto",
    "caso",
    "na pratica",
    "um agente",
    "uma equipe",
    "um sistema",
    "um desenvolvedor",
    "um estudante",
    "um usuario",
    "uma empresa",
    "um professor",
    "um cliente",
]
ERROR_HINTS = [
    "erro",
    "problema",
    "falha",
    "bug",
    "incorreto",
    "inadequado",
    "errado",
    "risco",
    "riscos",
    "limitacao",
    "vulnerabilidade",
]
NOT_TRUE_HINTS = [
    "nao e verdadeira",
    "nao e verdadeiro",
    "nao corresponde",
]


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def normalize_for_match(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.lower()).strip()


def first_nonempty_line(lines):
    for idx, line in enumerate(lines):
        if line.strip():
            return idx, line
    return None, None


def next_content_line(lines, start_index):
    for idx in range(start_index, len(lines)):
        line = lines[idx]
        if line.strip():
            return idx, line
    return None, None


def is_plain_paragraph_line(line):
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith(("<", "#", "-", "*", ">", "|", ":::")):
        return False
    if re.match(r"^\d+\.\s", stripped):
        return False
    return True


def extract_question_blocks(text: str):
    blocks = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        open_match = QUESTION_OPEN_RE.match(line.strip())
        if open_match:
            prompt = open_match.group(1).strip()
            block_lines = [line]
            start_line = i + 1
            i += 1
            while i < len(lines):
                block_lines.append(lines[i])
                if lines[i].strip() == ":::":
                    break
                i += 1
            blocks.append(
                {
                    "prompt": prompt,
                    "text": "\n".join(block_lines),
                    "start_line": start_line,
                }
            )
        i += 1
    return blocks


def validate_question_block(block):
    errors = []
    lines = [line.rstrip() for line in block["text"].splitlines()]
    correct_count = 0
    for line in lines[1:]:
        stripped = line.strip()
        if ALT_CORRECT_RE.match(stripped):
            correct_count += 1
    if correct_count != 1:
        errors.append(
            f"A questão iniciada na linha {block['start_line']} precisa ter exatamente uma alternativa terminando com ' *'."
        )
    return errors


def classify_question(prompt: str):
    normalized = normalize_for_match(prompt)
    is_scenario = any(hint in normalized for hint in SCENARIO_HINTS)
    is_error = any(hint in normalized for hint in ERROR_HINTS)
    is_not_true = any(hint in normalized for hint in NOT_TRUE_HINTS)
    return {
        "scenario": is_scenario,
        "error": is_error,
        "not_true": is_not_true,
    }


def find_heading_lines(lines):
    result = {}
    for idx, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line.strip())
        if match:
            result.setdefault(match.group(1), idx)
    return result


def find_block_lines(lines):
    positions = {}
    for idx, line in enumerate(lines, start=1):
        match = BLOCK_START_RE.match(line.strip())
        if match:
            positions.setdefault(match.group(1), []).append(idx)
    return positions


def count_plain_paragraphs_before_line(lines, line_no):
    count = 0
    in_block = False
    for idx, raw in enumerate(lines, start=1):
        if idx >= line_no:
            break
        line = raw.strip()
        if line.startswith(":::"):
            in_block = not in_block if line == ":::" else True
            continue
        if in_block:
            continue
        if is_plain_paragraph_line(raw):
            count += 1
    return count


def validate_markdown(text):
    errors = []
    warnings = []

    stripped = strip_frontmatter(text)

    if re.search(r"<\s*aside\b", stripped, re.IGNORECASE):
        errors.append("Nao pode usar a tag aside.")

    lines = stripped.splitlines()
    title_idx, title_line = first_nonempty_line(lines)
    if title_line is None:
        errors.append("Arquivo vazio.")
        return {"ok": False, "errors": errors, "warnings": warnings}

    if not re.match(r"^#\s+\S+", title_line.strip()):
        errors.append("A primeira linha util precisa ser um titulo H1.")

    intro_idx, intro_line = next_content_line(lines, (title_idx or 0) + 1)
    if intro_line is None:
        errors.append("Falta paragrafo introdutorio apos o titulo.")
    elif not is_plain_paragraph_line(intro_line):
        errors.append("O primeiro bloco apos o titulo precisa ser um paragrafo simples.")

    h2_headings = re.findall(r"^##\s+(.+?)\s*$", stripped, flags=re.MULTILINE)
    if not any(h == "Questões de fixação" for h in h2_headings) and not any(
        h == "Questoes de fixacao" for h in h2_headings
    ):
        errors.append("Falta a secao ## Questoes de fixacao.")
    if not any(h == "Atividade prática" for h in h2_headings) and not any(
        h == "Atividade pratica" for h in h2_headings
    ):
        errors.append("Falta a secao ## Atividade pratica.")
    if "Fechamento" not in h2_headings:
        errors.append("Falta a secao ## Fechamento.")

    heading_lines = find_heading_lines(lines)
    block_lines = find_block_lines(lines)

    conceito_lines = block_lines.get("conceito", [])
    exemplo_lines = block_lines.get("exemplo", [])
    if not conceito_lines:
        errors.append("A aula precisa ter pelo menos 1 bloco :::conceito.")
    if not exemplo_lines:
        errors.append("A aula precisa ter pelo menos 1 bloco :::exemplo.")

    question_blocks = extract_question_blocks(stripped)
    if not (5 <= len(question_blocks) <= 6):
        errors.append("A aula precisa ter entre 5 e 6 blocos :::questao.")
    else:
        scenario_count = 0
        error_count = 0
        not_true_count = 0
        questoes_fixacao_line = heading_lines.get("Questões de fixação") or heading_lines.get("Questoes de fixacao")
        inline_count = 0
        fixacao_count = 0

        first_question_line = question_blocks[0]["start_line"]
        if conceito_lines and first_question_line <= conceito_lines[0]:
            errors.append("A primeira questão não pode aparecer antes do bloco :::conceito.")
        if exemplo_lines and first_question_line <= exemplo_lines[0]:
            errors.append("A primeira questão não pode aparecer antes do bloco :::exemplo.")
        if count_plain_paragraphs_before_line(lines, first_question_line) < 2:
            errors.append("A aula precisa construir minimamente o conceito antes da primeira questão (faltam explicações antes da cobrança).")

        for block in question_blocks:
            errors.extend(validate_question_block(block))
            classification = classify_question(block["prompt"])
            scenario_count += 1 if classification["scenario"] else 0
            error_count += 1 if classification["error"] else 0
            not_true_count += 1 if classification["not_true"] else 0

            if questoes_fixacao_line and block["start_line"] > questoes_fixacao_line:
                fixacao_count += 1
            else:
                inline_count += 1

        if scenario_count < 1:
            errors.append("A aula precisa ter pelo menos 1 questão de cenário real aplicado.")
        if error_count < 1:
            errors.append("A aula precisa ter pelo menos 1 questão que peça identificar erro, problema, falha ou risco.")
        if not_true_count > 2:
            errors.append("A aula pode ter no máximo 2 questões no formato 'qual NÃO é verdadeira'.")
        if inline_count > 2:
            errors.append("A aula pode ter no máximo 2 questões inline antes de ## Questões de fixação.")
        if fixacao_count < 3:
            errors.append("A aula precisa ter pelo menos 3 questões dentro da seção ## Questões de fixação.")

    if len(h2_headings) < 4:
        warnings.append("Poucas secoes H2; revisar estrutura da aula.")

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Arquivo Markdown da aula")
    args = parser.parse_args()

    path = Path(args.path)
    result = validate_markdown(path.read_text(encoding="utf-8"))
    result["path"] = str(path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
