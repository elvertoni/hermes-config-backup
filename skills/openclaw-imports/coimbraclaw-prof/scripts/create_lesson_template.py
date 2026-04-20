#!/usr/bin/env python3
import argparse
from pathlib import Path


def build_template(title: str, description: str, order: int, with_frontmatter: bool = True) -> str:
    parts = []
    if with_frontmatter:
        parts.append("---")
        parts.append(f"title: {title}")
        parts.append(f"description: {description}")
        parts.append(f"order: {order}")
        parts.append("published: true")
        parts.append("---")
        parts.append("")

    parts.extend(
        [
            f"# {title}",
            "",
            f"Nesta aula, vamos estudar {title.lower()} de forma objetiva, relacionando o conceito ao contexto técnico e à prática dos estudantes.",
            "",
            "## Abertura",
            "",
            ":::objetivo",
            "Definir o objetivo principal da aula e o que o estudante deve conseguir fazer ao final.",
            ":::",
            "",
            ":::dica",
            "Antecipar uma estratégia de observação, comparação ou estudo para facilitar a compreensão.",
            ":::",
            "",
            ":::curiosidade",
            "Registrar um fato curto, histórico ou contextual que aumente o interesse pela aula.",
            ":::",
            "",
            "## Desenvolvimento",
            "",
            ":::conceito",
            "Escrever aqui a definição central do conteúdo.",
            ":::",
            "",
            "Desenvolver primeiro a ideia central em Markdown simples, com explicação clara e progressiva.",
            "",
            "Se a aula for fundacional, definir explicitamente os subtipos, partes ou categorias principais antes de começar a cobrar distinções.",
            "",
            ":::exemplo",
            "Adicionar um exemplo concreto que conecte teoria e prática.",
            ":::",
            "",
            "Conectar o exemplo ao conceito com mais uma explicação curta antes da primeira questão.",
            "",
            ":::questao Um estudante da SEED-PR aplicou esse conceito em uma situação real. Qual cenário mostra o uso mais adequado?",
            "a) Alternativa A *",
            "b) Alternativa B",
            "c) Alternativa C",
            "d) Alternativa D",
            "> Explicar por que a alternativa correta representa um cenário aplicado.",
            ":::",
            "",
            ":::importante",
            "Destacar um ponto conceitual que não pode ser confundido.",
            ":::",
            "",
            "Explicar uma limitação, dependência, compatibilidade ou consequência prática do conteúdo.",
            "",
            ":::atencao",
            "Corrigir um erro comum ou uma interpretação incorreta, incluindo risco ou limitação.",
            ":::",
            "",
            ":::questao Ao revisar a solução abaixo, qual erro ou problema precisa ser identificado primeiro?",
            "a) Alternativa A",
            "b) Alternativa B *",
            "c) Alternativa C",
            "d) Alternativa D",
            "> Explicar por que a alternativa correta aponta o principal erro ou problema.",
            ":::",
            "",
            ":::roteiro",
            "Registrar a fala do professor, perguntas disparadoras ou transições de condução da aula.",
            ":::",
            "",
            "## Questões de fixação",
            "",
            ":::questao Qual alternativa resume melhor o conceito central desta aula?",
            "a) Alternativa A",
            "b) Alternativa B *",
            "c) Alternativa C",
            "d) Alternativa D",
            "> Explicar por que a alternativa correta resume melhor o conceito.",
            ":::",
            "",
            ":::questao Em uma situação prática, o que tende a acontecer se esse conceito for aplicado sem validação adequada?",
            "a) Alternativa A",
            "b) Alternativa B",
            "c) Alternativa C *",
            "d) Alternativa D",
            "> Explicar por que a alternativa correta representa a consequência mais provável.",
            ":::",
            "",
            ":::questao Sobre as afirmações abaixo, qual NÃO é verdadeira?",
            "a) Alternativa A",
            "b) Alternativa B",
            "c) Alternativa C *",
            "d) Alternativa D",
            "> Explicar por que a alternativa correta é a única incorreta.",
            ":::",
            "",
            "## Atividade prática",
            "",
            ":::exercicio",
            "Descrever uma atividade curta, individual ou em grupo, conectada ao objetivo da aula.",
            ":::",
            "",
            "## Fechamento",
            "",
            ":::resumo",
            "- Retomar a ideia principal",
            "- Reforçar o conceito central",
            "- Relacionar o conteúdo ao cotidiano ou à próxima aula",
            ":::",
            "",
        ]
    )
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Gera um template de aula no formato novo do ProfessorDash.")
    parser.add_argument("--title", required=True, help="Título da aula")
    parser.add_argument("--description", default="Descrição curta da aula", help="Descrição curta")
    parser.add_argument("--order", type=int, default=1, help="Ordem da aula")
    parser.add_argument("--output", required=True, help="Arquivo .md de saída")
    parser.add_argument("--no-frontmatter", action="store_true", help="Omitir frontmatter YAML")
    args = parser.parse_args()

    content = build_template(
        title=args.title,
        description=args.description,
        order=args.order,
        with_frontmatter=not args.no_frontmatter,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
