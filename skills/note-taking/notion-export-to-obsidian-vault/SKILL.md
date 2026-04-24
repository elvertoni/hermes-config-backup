---
name: notion-export-to-obsidian-vault
description: Importar exports ZIP do Notion para o vault operacional do Hermes/Obsidian com preservação do bruto em raw/, curadoria seletiva em wiki/ e commit+push final.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# notion-export-to-obsidian-vault

Use quando o Toni enviar um ou mais exports do Notion em ZIP e quiser migrar para o Obsidian/vault.

## Objetivo

Fazer migração em duas camadas:
1. preservar o bruto em `raw/`
2. promover só o que presta para `wiki/`

Sem jogar export cru direto no wiki.

## Contexto do ambiente do Toni

- Vault operacional: `/root/hermes-vault`
- Vault Git/espelho: `/root/hermes-wiki`
- Ambos devem receber o bruto importado quando a tarefa envolver preservação operacional + publicação Git
- Sempre finalizar com commit+push no GitHub quando houver mudança persistente no vault versionado

## Fluxo padrão

### 0. Quando vierem LINKS públicos (sem ZIP)

Se o Toni enviar links públicos do Notion (em vez de export ZIP), use o fallback por API pública de páginas:

- endpoint: `POST https://www.notion.so/api/v3/loadPageChunk`
- payload mínimo:
  - `pageId` (UUID com hífens)
  - `limit: 100`
  - `cursor: {"stack": []}`
  - `chunkNumber: 0`
  - `verticalColumns: false`
- repetir chamadas enquanto `cursor.stack` vier preenchido; parar quando voltar vazio
- extrair blocos de `recordMap.block` e converter para Markdown
- varrer links internos/subpáginas e repetir o processo para cobrir páginas referenciadas

Observações:
- IDs de URL do Notion costumam vir com 32 hex sem hífen. Converter para UUID antes da chamada.
- Esse método funciona bem para conteúdo textual público.
- Anexos/arquivos privados podem não vir completos sem export autenticado.

Depois seguir os mesmos passos de inventário, classificação em `raw/`, curadoria em `wiki/` e commit+push.

### 1. Descompactar tudo

Exports do Notion podem vir com um ZIP externo que contém um ZIP interno `Part-1.zip`.

Procedimento:
- extrair o ZIP recebido para diretório temporário
- procurar ZIPs internos extraídos
- extrair também esses ZIPs internos
- só depois inventariar o conteúdo real

Nunca assumir que o primeiro ZIP já contém os `.md` finais.

### 2. Inventariar

Levantar pelo menos:
- total de arquivos
- quantos `.md`
- quantos `.csv`
- quantos anexos (`.pdf`, imagens, `.docx`, etc.)
- exemplos de caminhos e nomes relevantes

Gerar um inventário em:
- `outputs/notion-import-AAAA-MM-DD-inventario.md`

## 3. Classificar por destino

Categorias operacionais padrão do Toni:
- `professor`
- `dev`
- `pessoal`
- `referencias`

Regra prática:
- `professor` → aula, SEED, Classroom, planejamento, conteúdo didático
- `dev` → setup, ferramentas, infra, IA, automação, programação, runbooks técnicos
- `pessoal` → páginas de pessoas e notas pessoais identificáveis
- `referencias` → links, material solto, utilitários, itens sem encaixe técnico/pedagógico forte

Quando houver dúvida, preferir `referencias` em vez de contaminar `professor` ou `wiki/`.

## 4. Importar bruto para raw/

Salvar o import bruto preservando nomes e subpastas sob um prefixo de lote:

- `raw/professor/notion-import-AAAA-MM-DD/`
- `raw/dev/notion-import-AAAA-MM-DD/`
- `raw/pessoal/notion-import-AAAA-MM-DD/`
- `raw/referencias/notion-import-AAAA-MM-DD/`

Preservar anexos junto com os `.md` relacionados sempre que possível.

## 5. Curadoria seletiva para wiki/

Não promover tudo.

Promover apenas notas com valor durável, por exemplo:
- runbooks úteis
- regras operacionais
- setup técnico reaproveitável
- referências que afetam o trabalho do Toni

Criar uma página-síntese do lote em:
- `wiki/HERMES/importacao-de-exports-do-notion-AAAA-MM-DD.md`

Essa página deve conter:
- resumo do lote
- contagem por categoria
- critério de classificação usado
- conexões para notas promovidas
- fontes no `raw/` e no inventário

## 6. Atenção a conteúdo desatualizado

Se uma nota técnica importada trouxer orientação que conflita com regras atuais do Toni, não descartar automaticamente.

Faça assim:
- preserve o bruto em `raw/`
- na nota curada do `wiki/`, marque explicitamente a parte desatualizada
- exemplo real: notas recomendando Sonnet como modelo padrão devem ser sinalizadas porque a regra atual do Toni é priorizar Codex via OAuth/OpenAI

## 7. Atualizar índice e log

No vault Git (`/root/hermes-wiki`):
- atualizar `wiki/index.md`
- adicionar entrada no topo de `wiki/log.md`

A entrada de log deve registrar:
- que os ZIPs foram descompactados, incluindo `Part-1.zip` internos se houver
- que o bruto foi classificado em `raw/`
- quais páginas de wiki foram criadas
- se houve conteúdo desatualizado sinalizado

## 8. Commit e push

Ao terminar:
- `git add` dos arquivos importados e curados
- `git commit`
- `git push origin main`
- verificar que o repositório ficou limpo após o push

## Resultado esperado

Entregar ao Toni:
- quantos arquivos foram importados
- distribuição por categoria
- páginas do wiki criadas
- caminho do inventário
- commit SHA
- status do push

## Limpeza de nomes do Notion (obrigatória)

Exports do Notion vêm com hashes de 32 caracteres hex no final dos nomes:
- `Github 31466fbdbb9080c5bf65caddbd7bfe19.md` → `Github.md`
- `Antigravity 2f866fbdbb9080a3a657e41ea89c96a2.md` → `Antigravity.md`
- Subpastas também: `PYCODEBR 31966fbdbb90808184d8dc7ca16b6a21/` → `PYCODEBR/`

**Regex correto para limpar nomes de arquivo:**
```python
import re
import os

def clean_name(name):
    """Remove hash do Notion do final do nome antes da extensão"""
    base, ext = os.path.splitext(name)
    base = re.sub(r'\s+[a-f0-9]{32}$', '', base)
    return base + ext
```

**Para limpar caminhos completos (arquivos + diretórios):**
```python
def clean_path(rel_path):
    """Limpa hashes de todas as partes de um caminho relativo"""
    parts = rel_path.split(os.sep)
    clean_parts = []
    for p in parts:
        if '.' in p:
            # é arquivo
            clean_parts.append(clean_name(p))
        else:
            # é diretório
            clean_parts.append(re.sub(r'\s+[a-f0-9]{32}$', '', p))
    return os.sep.join(clean_parts)
```

**Aplicar em:**
1. Nomes de arquivos `.md`
2. Nomes de diretórios (subpastas do export)
3. Nomes de anexos quando possível

**Cuidado com a construção do caminho destino:**
- O backup do Notion pode ter estrutura: `backup/dev/notion-import-YYYY-MM-DD/Aula X .../arquivo.md`
- Ao reconstruir em `raw/dev/notion-import-YYYY-MM-DD/`, remover o prefixo `notion-import-YYYY-MM-DD/` do caminho relativo antes de aplicar `clean_path`
- Verificar com `find` que não há double-nesting (`raw/dev/notion-import-.../notion-import-.../`)

**NÃO deixar os hashes originais** — o usuário espera nomes limpos e legíveis.

## Verificação antes de entregar

Antes de considerar a tarefa pronta, confirmar:
- `find raw/ -name '*[a-f0-9]*' | grep -E '[a-f0-9]{32}'` retorna vazio
- Todos os arquivos têm nomes legíveis sem hash
- Subpastas também estão limpas
- Não há double-nesting de diretórios

## Curadoria: menos é mais

O usuário prefere **curadoria seletiva e minimalista**. Erros comuns a evitar:

- **NÃO promover tudo que parece técnico** para `wiki/`. Uma nota com apenas um link solto ou uma dica de 2 linhas não precisa de página wiki própria.
- **LER o conteúdo real** antes de classificar. Um arquivo chamado `Linux AWS.md` pode ser apenas 3 linhas de anotações soltas (vai para `referencias`), não um runbook completo (vai para `dev`).
- **Preservar em raw/ é suficiente** para a maioria do material. Só promover para `wiki/` quando houver valor duradouro, passo a passo reutilizável ou decisão técnica documentada.
- **Evitar duplicatas**: o Notion exporta às vezes a mesma página com IDs diferentes (ex: `Toni Coimbra d2d4...md` e `Toni Coimbra d2d6...md`). Manter apenas uma cópia em `raw/`, descartar duplicatas.

Quando em dúvida, pergunte ao usuário: "Posso promover X para wiki/ ou prefere deixar só em raw/?"

## Pitfalls

- Não esquecer do ZIP interno `Part-1.zip`
- Não promover export cru em massa para o `wiki/` — ser seletivo
- Não perder anexos relacionados na cópia para `raw/`
- Não tratar conteúdo antigo como regra vigente sem sinalização
- **NÃO preservar hashes do Notion nos nomes de arquivo/pasta**
- **CUIDADO com path construction** — evitar double-nesting e truncamento acidental de nomes de diretório
- Não esquecer commit+push no final
