---
name: classroom-activity-publish
description: Publicar atividades no Google Classroom seguindo o padrão do Toni, especialmente quando a entrega usa Google Forms com nota, tópico próprio e naming `Atividade NNN - Xº TRI`. Use quando o pedido for postar, agendar, replicar, padronizar ou documentar atividades no Classroom, inclusive extraindo questões de materiais de aula e aplicando o fluxo real observado no vídeo de referência.
---

# classroom-activity-publish

## Regras fundamentais (não negociáveis)

### Fonte dos materiais
- TODOS os conteúdos de aula (ppt, docx, pdf, vídeos etc) estão no Google Drive da conta **coimbrabot.ai@gmail.com**
- A pasta raiz pode variar. IDs antigos documentados (`1kX5kZg0IWa8DcHKhTMZ4ssZnmhpJP1tG`, `1iJaC3_cIpWsxQd8RiWH5m8dEJWSsONGw`) já retornaram 404 — **não hardcode IDs de pasta**
- Estrutura observada na prática (2026-04-22): pasta `ITE` (ID `1Un7Ca2IaCMWlVmwOpI-BCOk5o_8Eh2lS`) com subpastas `AULA_01` a `AULA_23`, cada uma contendo `.docx`, `.pptx` e arquivos de prática
- Para localizar: fazer busca genérica no Drive (`name contains 'ITE'`, `name contains 'Atividade'`) ou listar pastas raiz, em vez de assumir IDs fixos
- Para ler/analizar qualquer material de aula, usar a API do Drive com o token de coimbrabot.ai (google_token.json)

### Conta do Classroom
- TODAS as atividades no Classroom são publicadas na conta **Elvertoni.coimbra@escola.pr.gov.br**
- NUNCA usar a conta coimbrabot.ai para Classroom
- O token para essa conta fica em google_token_escola.json

### Risco real: revogação do token do coimbrabot.ai
- O refresh_token do coimbrabot.ai já foi revogado várias vezes (`invalid_grant`). Não assumir que ele está sempre válido
- Se o refresh falhar com `invalid_grant`, o único caminho é gerar um novo link de autorização OAuth, pedir ao usuário que abra no navegador logado na conta coimbrabot.ai, copie o `code=` da URL de redirect (localhost:8085), e troque aqui pelo token novo
- Client ID do coimbrabot.ai: `298622568101-7fb6a0dvp1g45bc5t8bc6to87occs047.apps.googleusercontent.com`
- Redirect URI usada: `http://localhost:8085`
- Salvar o novo token em `google_token.json` imediatamente

### Fallback quando a Forms API está desabilitada no projeto do bot
- Se criar Form com o token do coimbrabot.ai retornar `SERVICE_DISABLED` (Forms API não ativada no projeto Google Cloud do bot), **usar o token da conta escola** (`google_token_escola.json`) para criar e configurar o Form
- A conta escola possui escopo `forms.body` e funciona perfeitamente para criar Forms, batchUpdate, quiz, etc.
- Isso não impede de usar o coimbrabot.ai para leitura de materiais no Drive — apenas separa: Drive = bot, Forms/Classroom = escola

### Padrão de publicação
- título no formato `Atividade NNN - Xº TRI`
- tópico com o mesmo nome da atividade
- nota máxima `100`
- Google Forms quando a atividade for objetiva
- descrição curta e direta

## Overview

Use esta skill para publicar atividades no Google Classroom no padrão do Toni.

Priorize consistência operacional:
- título no formato `Atividade NNN - Xº TRI`
- tópico com o mesmo nome da atividade
- nota máxima `100`
- Google Forms quando a atividade for objetiva
- descrição curta e direta

## Workflow

### Fontes para extração de atividades (workflow simplificado)

Antes de publicar, localizar o material-base:
1. **No Drive (coimbrabot.ai)** — pasta AULAS_RCO, subpasta da disciplina, buscar arquivos como `AULA_XX_*ATIVIDADE*.docx` ou similar
2. **Ler o DOCX** — extrair enunciados, alternativas e gabarito (resposta comentada em vermelho)
3. **Copiar para o Form** — transferir questões pro Google Forms, marcar resposta correta
4. **Publicar no Classroom (elvertoni.coimbra)** — criar atividade com Form anexado

O arquivo .docx da atividade geralmente contém:
- título/formato (ex: "EPT PARANÁ — Curso Técnico — DESENVOLVIMENTO DE SISTEMAS")
- questões com texto-base + alternativas a/b/c/d
- **resposta comentada** logo abaixo (em vermelho/destaque) indicando qual alternativa é correta e por quê

Extrair: título interno, enunciado curto, perguntas, alternativas, gabarito.

### 2. Aplicar o padrão do Toni

Usar estes defaults, salvo instrução diferente do Toni:
- título: `Atividade NNN - Xº TRI`
- tópico: mesmo texto do título
- pontos: `100`
- sem data de entrega, a menos que o Toni peça data
- turma: usar a disciplina/turma informada pelo link ou courseId
- descrição curta, sem enrolação

Quando a atividade for de múltipla escolha em formulário, usar descrição curta como:
- `Marque a alternativa correta.`
- ou uma variante igualmente direta e adequada ao conteúdo

### 3. Escolher a rota de publicação

#### Rota A — Fluxo ideal observado no vídeo (UI / Classroom + Forms nativo)

Quando o objetivo for reproduzir o padrão real do Toni no Classroom com formulário integrado, seguir `references/classroom-ui-pattern.md`.

Esse é o padrão preferido porque:
- o Form fica anexado nativamente à atividade
- a importação de notas fica integrada
- o fluxo corresponde ao processo humano real usado pelo Toni

#### Rota B — Automação por API/CLI (funciona)

Usar `gog classroom` + `gog forms` e, quando necessário, chamada REST direta do Classroom API.

**Descoberta importante em 2026-04-08:**
- A API REST do Google Classroom **não aceita** `materials.form` na criação (`Unsupported material type: FORM`)
- `PATCH` também **não aceita** atualizar `materials`
- **Mas** criar a atividade com `materials.link` apontando para o **edit URL** do Google Form faz o Classroom **converter automaticamente** o material para `form` no objeto retornado

### Método correto para anexo nativo do Form

Para obter o cartão nativo do Google Forms dentro da atividade:
1. criar/editar o Form normalmente
2. usar o **edit URL** do Form (`https://docs.google.com/forms/d/<FORM_ID>/edit`)
3. criar a atividade no Classroom com:
   - `workType: ASSIGNMENT`
   - `materials: [{"link": {"url": <FORM_EDIT_URL>, "title": <TITULO>}}]`
4. o Classroom faz o upgrade automático e retorna `materials.form`

### Observação crítica

- `materials.form` é **read-only** na API pública
- o caminho suportado para chegar ao resultado nativo é **`link -> auto-upgrade para form`**
- isso permite reproduzir o padrão visual do Toni **sem browser**, desde que a atividade seja criada desse jeito desde o início
- se a atividade já existir sem material nativo, o caminho prático é **recriar** a atividade; `PATCH` em `materials` não funciona
- se houver um rascunho anterior com o mesmo título, mas com material errado (ex.: DOCX anexado em vez de Form), o procedimento correto é **apagar o rascunho errado e recriar**. Tentar “consertar” o mesmo `courseWork` não resolve o material nativo.

Fallback aceitável quando necessário:
- criar o Form
- publicar a atividade no Classroom
- colocar o link público do Form na descrição
- **esta abordagem NÃO é equivalente ao padrão nativo**
- registrar claramente que ficou em modo fallback

### 4. Montar o Google Form

Para formulários objetivos:
- criar o formulário com o mesmo título da atividade
- adicionar descrição curta com disciplina + aula
- adicionar `Nome completo` como primeira pergunta obrigatória, se fizer sentido para a rotina do Toni
- adicionar as questões da atividade
- usar múltipla escolha quando houver alternativas fechadas
- marcar resposta correta quando o fluxo suportar quiz/gabarito

### Restrição real da API do Forms (confirmada em 2026-04-15)

Na criação inicial do formulário, a API aceita **apenas** `info.title`.

Se tentar criar já com descrição, retorna erro no padrão:
- `Only info.title can be set when creating a form.`

Caminho correto:
1. `forms.create` com apenas o título
2. `forms.batchUpdate` para:
   - preencher `info.description`
   - ativar `quizSettings.isQuiz`
   - ativar `emailCollectionType=VERIFIED`
   - criar os itens/perguntas

Ou seja: descrição e configurações do quiz entram **depois** da criação, nunca no payload inicial.

#### Configurações obrigatórias do formulário (padrão do Toni)

Em **Configurações**, usar este padrão por default, salvo instrução diferente do Toni:
- **Criar teste**: marcado
- **Coletar e-mail verificado**: marcado
- **Limitar a 1 resposta**: marcado
- **Pontuação por questão**: `50` pontos por questão objetiva

Observações:
- não assumir `100` pontos totais no Form; o padrão é `50` por questão
- a atividade no Classroom pode continuar com `100` pontos quando fizer sentido para a rotina da turma
- se o fluxo/API não conseguir aplicar uma dessas configurações, relatar isso explicitamente

Se houver texto-base grande, resumir o suficiente para caber bem no enunciado. Não despejar blocos longos sem necessidade.

### 5. Publicar e conferir

Após criar:
- confirmar título
- confirmar tópico
- confirmar nota 100
- confirmar se o Form está anexado nativamente ou apenas linkado
- confirmar no Form: `Criar teste`, `coletar e-mail verificado`, `limitar a 1 resposta`
- confirmar `50` pontos por questão objetiva
- guardar links finais do Classroom e do Form
- relatar qualquer limitação técnica real, sem inventar desculpa

## Achados operacionais importantes (2026-04-15)

### Escopo OAuth obrigatório para tópicos do Classroom

Se a automação precisa:
- listar tópicos
- criar tópico
- atribuir `topicId` à atividade

então o token OAuth da conta escolar precisa incluir explicitamente:
- `https://www.googleapis.com/auth/classroom.topics`

Sintoma quando falta esse escopo:
- criar atividade funciona
- criar/listar tópico falha com `ACCESS_TOKEN_SCOPE_INSUFFICIENT`
- a atividade pode ser publicada sem `topicId`

Correção:
- reautorizar a conta escolar com `classroom.topics`
- depois criar o tópico e fazer `PATCH` do `courseWork` com `updateMask=topicId`

### Limitação real da API do Google Forms na criação

Na criação inicial do formulário, a API aceita apenas:
- `info.title`

Se tentar criar já com `info.description`, a API responde erro 400 no padrão:
- `Only info.title can be set when creating a form. To add items and change settings, use batchUpdate.`

Fluxo correto:
1. `forms.create()` apenas com `info.title`
2. `forms.batchUpdate()` para:
   - `updateFormInfo` com `description`
   - `updateSettings` (`quizSettings.isQuiz`, `emailCollectionType`)
   - `createItem` para perguntas
3. só depois publicar/anexar no Classroom

### Analisar vídeos de referência do Drive

Quando Toni manda um link de vídeo do Google Drive para entender o processo:

1. **Download via Google Drive API** — gdown falha com arquivos privados ("Cannot retrieve the public link"). Usar `google-api-python-client` com o token OAuth do coimbrabot.ai:
   ```python
   from google.oauth2.credentials import Credentials
   from googleapiclient.discovery import build
   from googleapiclient.http import MediaIoBaseDownload
   # Usar google_token.json (coimbrabot.ai) ou google_token_escola.json
   ```
2. **Extrair frames** — ffmpeg a cada 10s para cobrir o vídeo:
   ```bash
   ffmpeg -i video.mp4 -vf "fps=1/10,scale=960:-1" /tmp/frames/frame_%03d.jpg
   ```
3. **Análise com vision** — chamar `vision_analyze` em cada frame pedindo descrição completa da tela

Fallback se python-docx não instalado: extrair DOCX como ZIP → ler `word/document.xml` → extrair nós `w:t`.

## Operational Notes

- Conta preferencial para Classroom/Forms da escola: `elvertoni.coimbra@escola.pr.gov.br`
- Se a API/escopo falhar nessa conta, dizer o motivo real
- Para Drive, o ambiente atual pode ter diferenças entre contas OAuth; não assumir que ambas têm o mesmo acesso
- Se houver vídeo/referência visual nova do Toni, atualizar a referência desta skill em vez de improvisar na próxima vez

### Falha total do token do Drive (coimbrabot.ai) — caso real de 2026-04-23

Durante uma tentativa de publicação, o token de `google_token.json` (coimbrabot.ai@gmail.com) retornou:
- `invalid_grant` no refresh (não recuperável)
- `401 UNAUTHENTICATED` em qualquer chamada ao Drive

Isso significa que o refresh token foi **revogado ou expirou permanentemente**, não apenas que o access token precisava de refresh.

**Conduta correta quando isso acontece:**
1. Verificar se `google_token_escola.json` consegue acessar o Drive — **não consegue**, pois AULAS_RCO está na conta coimbrabot.ai
2. Informar o Toni imediatamente que o token do Drive está quebrado
3. Oferecer duas saídas:
   - **Reautorizar o OAuth do coimbrabot.ai** (gerar novo auth code e trocar por token)
   - **Receber o arquivo da atividade direto no Telegram** — extrair do anexo e seguir o fluxo normal de criação do Form + Classroom
4. Não ficar tentando o mesmo token revogado

### IDs de cursos confirmados (escola — 2026-04-23)

Lista obtida via `classroom.googleapis.com/v1/courses` com escopo de professor:

| ID | Nome | Escola |
|---|---|---|
| `842738572792` | Inovacao Tec E Empreend - 2º Ano A Manha | THEODORO DE BONA |
| `793583873515` | Programacao Front-End - 2º Ano A Manha | THEODORO DE BONA |
| `842739696988` | Analise E Metodo Para Sistemas - 1º Ano A Manha | THEODORO DE BONA |
| `842739634878` | Programacao No Des De Sistemas - 3º Ano A Manha | THEODORO DE BONA |
| `842739184622` | Analise E Projeto De Sistemas - 3º Ano A Manha | THEODORO DE BONA |
| `842736656239` | Introd A Computacao - 1º Ano A Manha | THEODORO DE BONA |
| `842489098476` | Programacao No Des De Sistemas - 3º Ano C Noite | PEDRO PIEKAS |
| `842490128694` | Introd A Computacao - 1º Ano C Noite | PEDRO PIEKAS |
| `842489183984` | **Inovacao Tec E Empreend - 2º Ano C Noite** | PEDRO PIEKAS |
| `793556557371` | **Analise E Projeto De Sistemas - 3º Ano C Noite** | PEDRO PIEKAS |

**Favoritos:**
- **APS NOITE** = `793556557371`
- **ITE NOITE** = `842489183984`

### Escopo insuficiente para tópicos (caso real de 2026-04-15)

Foi confirmado um caso em que o token da conta da escola permitia:
- ler/criar `courseWork`
- criar Google Forms
- anexar o Form nativamente via `materials.link -> auto-upgrade para form`

Mas **não** permitia listar/criar tópicos (`courses.topics`) por escopo insuficiente.

Sintoma típico:
- erro `ACCESS_TOKEN_SCOPE_INSUFFICIENT` ao chamar tópicos do Classroom

Conduta correta:
- não travar a publicação inteira por causa do tópico
- publicar a atividade mesmo sem `topicId`, se o resto estiver funcional
- relatar explicitamente que ficou sem tópico por limitação real de OAuth
- se o Toni quiser o fluxo 100% igual ao manual, reautenticar depois com escopo adequado

### Forms API desabilitada no projeto do bot (2026-04-22)

Ao tentar criar um Form com o token do coimbrabot.ai, a API retornou:
- `PERMISSION_DENIED` — `SERVICE_DISABLED`
- Motivo: Google Forms API não estava ativada no projeto Cloud `298622568101`

Solução aplicada: usar o token da conta escolar (`google_token_escola.json`) para toda a criação e edição do Form. Funcionou sem necessidade de ativar APIs no projeto do bot.

Implicação: o workflow padrão agora é:
1. **Drive/leitura de materiais** → token do coimbrabot.ai
2. **Criação de Form + Classroom** → token da conta escolar (mais confiável e já tem todos os escopos)

### Estrutura real do Drive para ITE (2026-04-22)

Em vez da pasta `AULAS_RCO` com subpastas por disciplina, o material de ITE estava organizado como:
- Pasta raiz `ITE` (ID `1Un7Ca2IaCMWlVmwOpI-BCOk5o_8Eh2lS`)
- Subpastas numeradas: `AULA_01` até `AULA_23`
- Dentro de cada aula: `AULA_XX_ATIVIDADE_...docx`, `AULA_XX_...pptx`, `AULA_XX_PRÁTICA_...docx`

Conduta correta: não hardcode IDs de pasta. Sempre listar ou buscar pelo nome.

### Forms API desabilitada no projeto do coimbrabot.ai (confirmado em 2026-04-22)

O projeto Google Cloud vinculado à conta **coimbrabot.ai@gmail.com** (client_id `298622568101-...`) **não tem a Google Forms API ativada**. Sintoma:
- `POST https://forms.googleapis.com/v1/forms` retorna `403 PERMISSION_DENIED` com `reason: SERVICE_DISABLED`

**Conduta correta:**
- **Sempre usar o token da conta escolar** (`google_token_escola.json` / `elvertoni.coimbra@escola.pr.gov.br`) para criar/editar formulários via API.
- O token do coimbrabot.ai continua válido apenas para operações do Drive (ler/baixar materiais de aula).

### Código de autorização OAuth é single-use

O `code` retornado pelo Google na URL de callback (`http://localhost:8085?code=4/0Ab...`) **só pode ser trocado por token uma vez**.

Sintoma de reutilização:
- `invalid_grant` no endpoint `https://oauth2.googleapis.com/token`

Conduta correta:
- se o exchange falhar por qualquer razão (erro de script, timeout, etc.), **gerar novo link de autorização** e obter novo `code`.
- nunca reenviar o mesmo `code` duas vezes.

### Extração de DOCX quando `python-docx` não estiver instalado

Se o host não tiver o módulo `docx`, não parar por isso.

Fallback confiável:
- abrir o `.docx` como ZIP
- ler `word/document.xml`
- extrair os nós `w:t`
- reconstruir os parágrafos manualmente

Esse fallback foi suficiente para extrair enunciados, alternativas e gabarito de atividade real da AULA 09 sem instalar dependências extras.

### Arquivos vindos do Telegram / cache do Hermes

Quando o arquivo vier anexado na conversa do Telegram, o nome local pode chegar com prefixo técnico do cache, por exemplo:
- `doc_<hash>_AULA_13_...docx`

Se esse arquivo for enviado direto ao Drive/Classroom sem tratamento, o material anexado aparece com esse nome feio dentro da atividade.

Conduta correta:
- normalizar o nome antes de anexar ao Classroom
- ou fazer upload e renomear o arquivo no Drive imediatamente depois
- conferir no `courseWork.get()` se `materials[].driveFile.driveFile.title` ficou limpo

Isso evita poluir a atividade com nomes internos do cache do Hermes.

## Resources

- `references/classroom-ui-pattern.md` — fluxo real observado no vídeo de referência
- `references/gog-fallback.md` — fallback por CLI, comandos úteis e limitações atuais
