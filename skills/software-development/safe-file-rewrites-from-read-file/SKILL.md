---
name: safe-file-rewrites-from-read-file
description: Evita corromper arquivos ao regravar conteúdo lido com a ferramenta read_file, que retorna linhas prefixadas com numeração no formato LINE|CONTENT.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Safe file rewrites from `read_file`

Use esta skill quando precisar transformar conteúdo de arquivos e regravar o resultado usando `execute_code`, `write_file` ou outro fluxo que passe pelo output de `read_file`.

## Problema real

A ferramenta `read_file` retorna o conteúdo com prefixo de linha no formato:

```text
123|conteudo da linha
```

Se esse texto for regravado diretamente no arquivo, o arquivo fica corrompido com os prefixos `N|` embutidos.

## Regra prática

- **Nunca** use a saída crua de `read_file` como conteúdo para `write_file`.
- Para regravação completa, prefira:
  1. ler o arquivo com `execute_code` via Python `open(...).read()`, ou
  2. remover explicitamente os prefixos `^\s*\d+\|` antes de escrever.
- Para mudanças pontuais, prefira `patch` em vez de rewrite completo.

## Fluxo seguro

### Opção 1 — melhor para rewrite completo

Dentro de `execute_code`, leia o arquivo com Python nativo:

```python
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()
# transforme text
with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
```

### Opção 2 — se você já recebeu texto vindo de `read_file`

Remova o prefixo antes de escrever:

```python
import re
clean = re.sub(r'^\s*\d+\|', '', raw_text, flags=re.M)
```

## Verificação obrigatória

Depois de qualquer rewrite feito a partir de conteúdo lido antes:

1. Reabra o início do arquivo com `read_file`
2. Verifique se as linhas **não** começam com `1|texto real do arquivo` duplicado no conteúdo
3. Se houver corrupção, remova os prefixos com regex e regrave

## Sinais de erro

Se o arquivo começar assim:

```text
1|#!/usr/bin/env python3
2|import os
```

isso é normal no output do `read_file`.

Se o conteúdo real do arquivo começar assim:

```text
     1|#!/usr/bin/env python3
```

ou pior:

```text
1|1|#!/usr/bin/env python3
```

então o arquivo foi corrompido por rewrite incorreto.

## Regra final

- `read_file` é seguro para inspeção
- `patch` é melhor para edições localizadas
- `open(...).read()` é melhor para rewrite completo dentro de `execute_code`
