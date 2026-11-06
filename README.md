# SDD Framework

Framework de planejamento e governança documental para projetos conduzidos com
agentes de IA. Versão inicial funcional: **0.1.0**. Python **3.11+**, sem
dependências de execução externas, APIs de IA ou serviços obrigatórios.

## Objetivo
Transformar ideias e projetos existentes em trabalho organizado: requisitos,
arquitetura, roadmap, especificações, tickets, decisões e passagem de contexto.
O framework instala a skill SDD, templates e instruções; o agente do consumidor
preenche os documentos e implementa as tarefas autorizadas.

Três entradas: **Inicie**, **Update** e **Conferência**. O comando init cria um
plano progressivo de adequação, não documentos de produto vazios nem requisitos
inventados. Dizer "Inicie" ao agente funciona quando a skill está instalada;
na primeira utilização, execute a CLI para torná-la disponível no projeto.

## Como este repositório está organizado

Este repositório constrói o SDD Framework e também utiliza seu próprio padrão.
Por isso, contém tanto os modelos distribuídos quanto documentos preenchidos
sobre o desenvolvimento do framework:

| Local | Responsabilidade |
|---|---|
| `src/sdd_framework/` | Código que implementa a CLI e suas verificações |
| `src/sdd_framework/assets/` | Fontes dos templates, da skill e das regras distribuídas aos consumidores |
| `docs/` e `specs/` | Requisitos, arquitetura, decisões e tarefas para construir o próprio SDD Framework |
| `AGENTS.md` e `CHECKPOINT.md` da raiz | Instruções e passagem de contexto deste projeto |
| `.sdd/` | Instalação local do framework neste repositório, criada pelo init |

Por exemplo, `src/sdd_framework/assets/templates/PRD.md` é o **modelo**;
`docs/PRD.md` contém os **requisitos do SDD Framework**. Cada consumidor terá
seu próprio PRD, preenchido com os requisitos daquele produto.

As tarefas em `specs/*/tasks/` constroem funcionalidades do framework. As tarefas
em `.sdd/adoption/tasks/` registram a adequação deste repositório ao padrão SDD.

Para mudar o que será distribuído, edite `src/sdd_framework/assets/` e atualize
o snapshot local com `python3 sdd.py update .`. Para mudar requisitos ou decisões
deste projeto, edite seus documentos em `docs/` ou `specs/`. A cópia em
`.sdd/framework/` é administrada pela CLI e não deve ser editada diretamente.

Esta explicação e as instruções específicas do AGENTS.md da raiz pertencem ao
desenvolvimento do framework; não são copiadas para os projetos consumidores.

## Como começar
Para obter o projeto pelo GitHub e executar sem instalação global:

```bash
git clone https://github.com/lucian-bonifacio/sdd-framework.git
cd sdd-framework
python3 sdd.py init /caminho/do/projeto
```

Sem instalação, a partir deste checkout:

```bash
python3 sdd.py init /caminho/do/projeto
python3 sdd.py check /caminho/do/projeto
```

Instalação central em ambiente com pip:

```bash
python3 -m pip install /caminho/para/sdd-framework
sdd init /caminho/do/projeto
```

Ou construa um executável portátil, sem pip:

```bash
python3 tools/build_release.py
python3 dist/sdd.pyz init /caminho/do/projeto
python3 dist/sdd.pyz check /caminho/do/projeto
```

O `.pyz` contém CLI, skill, fluxo e templates. Pode ser copiado para outra máquina
com Python 3.11+. O pacote ainda não foi publicado em registro público; use uma
distribuição local ou uma fonte Git explicitamente revisada.

Após init, abra Codex ou Claude Code no consumidor e peça **"Inicie"**.
O agente seguirá AGENTS.md e `.sdd/adoption/TASKS.md`, levantará informações e
executará o trabalho pronto. As decisões relevantes de produto continuam humanas.

### Diretórios nativos dos agentes

Execute init no terminal **antes de abrir o agente**. Com `--agent both` (padrão),
a instalação prepara `.codex/config.toml`, `.agents/skills/sdd/` para Codex e
`.claude/skills/sdd/` para Claude. A seleção de um agente prepara somente sua
integração; `--agent none` não cria diretórios nativos.

O config.toml inicial é um modelo TOML neutro, com orientação em comentários:
mantém as preferências das demais camadas sem fixar modelo ou permissões. O
arquivo passa a pertencer ao consumidor: init/update preservam configurações
existentes, e check aponta ausência ou TOML inválido. Update prepara o modelo
se o arquivo ainda não existir numa instalação anterior.

O Codex pode proteger `.codex/` e `.agents/` durante sessões `workspace-write`.
Criar o config antecipadamente não remove essa proteção nem concede confiança
ao projeto. Init/update devem rodar num terminal com acesso de escrita; falhas
detectadas no preflight informam o caminho e não instalam recursos parcialmente.
Veja [configuração](https://learn.chatgpt.com/docs/config-file/config-basic) e
[pastas protegidas](https://learn.chatgpt.com/docs/agent-approvals-security#protected-paths-in-writable-roots).

## Comandos

| Entrada | Exemplos |
|---|---|
| Inicie | `sdd init .`, `sdd inicie . --agent codex`, `sdd init . --mode existing` |
| Update | `sdd update .`, `sdd update . --source /checkout/da/nova-versao` |
| Conferência | `sdd check .`, `sdd conferencia . --phase implementation --spec 001-login` |

Init instala Codex e Claude por padrão. `--agent claude`, `codex`, `both` ou `none`
escolhe a integração inicial. Init repetido não reinstala, não troca a integração
e não altera documentos; para atualizar recursos use update. Não há comando de
migração de integração nesta versão: escolha os agentes na primeira inicialização.
`--agent none` permite usar somente documentos ou outros agentes que leiam AGENTS.md.

Use `--json` para automação. `sdd check --fix` cria tickets de adequação deduplicados,
sem preencher documentos ou aprovar decisões. Não executa código da aplicação.

### Acompanhar o trabalho

O [ROADMAP](docs/ROADMAP.md) é a porta de entrada para entregas, tarefas, estados
e ações pendentes do usuário. O AGENTS.md e a skill orientam o agente a executar
o script **do próprio consumidor** após alterar tickets:

```bash
python3 scripts/atualizar_roadmap.py
```

Esse arquivo é entregue por init/update e passa a pertencer ao projeto. Usa
somente biblioteca padrão Python e funciona sem pacote, CLI, configuração .sdd
ou checkout do framework. Executado de outra pasta, identifica a raiz pela própria
localização em scripts/. `--roadmap caminho/ROADMAP.md` informa caminho alternativo.
Quando existe configuração local de equivalências, ela também é respeitada.
Update preserva scripts locais existentes; novas versões devem ser reconciliadas
conscientemente pelo consumidor. A fonte distribuída é consumer_roadmap.py.

O agente deve conferir saída/diff e tratar erros. O script altera somente o bloco
de acompanhamento, preservando prioridades e planejamento. Datas indicam quando
a visão foi gerada. Estados e resultados são editados nos tickets.

`sdd check --roadmap` continua disponível como auxiliar opcional numa conferência
expressamente solicitada. Não é dependência da rotina do consumidor. Scripts
locais atendem operações mecânicas repetíveis; julgamento continua com o agente.

Critérios de aceitação, testes e revisões aplicáveis atendidos permitem concluir
uma tarefa sem confirmação manual adicional. Ações do usuário são exigidas
somente quando previstas no ticket; registre sua execução e valide o resultado.
Evidências ficam nos tickets. Relatórios extensos são opcionais, vinculados à
tarefa em `specs/NNN-nome/validation/`, sem relatório global de validação.

Etapas aceitas: `discovery`, `requirements`, `architecture`, `planning`,
`specification`, `design`, `tasks`, `implementation`, `validation`, `delivery`.
`--phase X` verifica pré-requisitos de entrada; sem opção, usa a etapa da configuração.
`--spec NNN-nome` limita as exigências de avanço à entrega selecionada; a conferência
continua apontando documentos presentes malformados nas demais entregas.

Exit codes: **0** sem impedimentos estruturais; **1** pendências de conformidade;
**2** erro operacional/configuração. Zero não significa testes executados, aceite
humano obtido ou contrato de comportamento semanticamente validado.

## Atualizações controladas
`sdd update .` aplica os recursos da CLI instalada ou da fonte remota já configurada.
Para buscar uma versão explicitamente escolhida em repositório Git HTTPS:

```bash
sdd update . --repository https://SEU-HOST/SUA-ORG/sdd-framework --ref v0.1.1
```

Substitua URL e tag por uma distribuição real revisada. Essa forma requer Git e
rede; não existe um repositório de atualização presumido. A fonte e ref ficam na
configuração para o próximo update. Prefira tag estável; branches podem mudar.
O update lê apenas o bundle de dados, sem executar scripts remotos. Verifica
compatibilidade da política, recusa downgrade e conflitos com recursos editados.
Mudança de política exige atualizar a CLI, não apenas copiar templates.

Documentos do consumidor, tickets, decisões, INBOX e CHECKPOINT não são
reescritos. Conteúdo fora dos blocos SDD em AGENTS.md/CLAUDE.md é preservado.
Depois de atualizar, execute conferência; adequações surgem como tickets.

## Organização dos consumidores
```text
AGENTS.md
README.md
.codex/config.toml               # quando Codex é selecionado; propriedade do consumidor
.claude/skills/sdd/              # quando Claude é selecionado
.agents/skills/sdd/              # skill do Codex
scripts/atualizar_roadmap.py      # ferramenta autônoma do consumidor
CHECKPOINT.md                    # quando houver passagem de contexto
docs/
  PRD.md
  ARCHITECTURE.md
  ROADMAP.md
  decisions/ADR-NNN.md           # quando necessário
  inbox/ITEM-NNN.md
specs/001-funcionalidade/
  SPEC.md
  DESIGN.md                     # opcional: design também pode ficar na SPEC
  TASKS.md                      # índice, não segunda fonte de estados
  tasks/T-NNN.md
  validation/                   # evidências extensas, quando necessárias
.sdd/
  config.json
  manifest.json
  adoption/TASKS.md              # tickets obrigatórios da adequação inicial
  framework/                    # snapshot versionado de recursos genéricos
```

O agente cria artefatos quando aplicáveis, seguindo templates e gates. Todo ticket
tem requisitos, dependências, executor, autorização, verificação e resultado.
Tarefas autorizadas continuam até conclusão ou bloqueio real; ações do usuário
são explícitas e não impedem trabalho independente. Não há runtime de agentes.

## Projetos existentes e equivalências
Init inventaria o modo, mas não migra documentos por heurística. O agente revisa
conteúdo e referências. `.sdd/config.json` admite `document_paths`, por exemplo:

```json
{"document_paths": {"docs/PRD.md": "documentation/PRODUCT.md"}}
```

Esse trecho é parte da configuração, não o arquivo completo. A equivalência
preserva o caminho existente, mas exige o conteúdo e os metadados do contrato SDD.
Arquivos fora da raiz ou atravessados por links simbólicos são recusados.
Em conflitos, preserve o original, compare as versões e reconcilie manualmente;
não há `--force` destrutivo. Um lock residual deve ser inspecionado antes de removido.

## CHECKPOINT, INBOX e interface
Peça ao agente "gere um checkpoint para encerrar". CHECKPOINT.md registra estado
real, alterações parciais, verificações, decisões, bloqueios e próximo passo.
Ao retomar, o agente confere se essas informações ainda correspondem aos arquivos.
Informações e propostas ainda não aceitas vão à INBOX; não se tornam requisitos
por aparecerem numa sessão ou ferramenta de memória.

O SDD não cria Design System. Configure `interface` e, quando disponível,
`design_system: {"reference": "caminho-ou-URL", "version": "versão"}` no JSON.
O agente deve aplicar essa referência ao front-end. Ausência fica visível.

## Desenvolvimento e validação
```bash
python3 -m unittest discover -s tests -v
python3 sdd.py check . --phase delivery
python3 tools/build_release.py
```

CI roda testes em Linux, macOS e Windows, Python 3.11 e 3.14. Resultados locais e
limites de validação estão em [ticket de distribuição](specs/006-distribuicao/tasks/T-002.md). O ambiente
original de criação não oferece metadados Git utilizáveis nem pip; por isso o
artefato portátil é validado sem instalação e nenhum commit é presumido.

## Documentação
- [Guia detalhado: comandos, pastas e arquivos](docs/GUIA-DE-FUNCIONAMENTO.md)
- [Requisitos](docs/PRD.md)
- [Arquitetura](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Fluxo e formatos](docs/WORKFLOW.md)
- [Decisões](docs/decisions/ADR-001.md)
- [Referências estudadas](docs/REFERENCES.md)
- [Checkpoint atual](CHECKPOINT.md)

`IDEIA.md` é a inspiração histórica, preservada; PRD e specs refletem as decisões
posteriores da conversa. Não publicar pacote ou escolher licença sem definição
do mantenedor; a entrega local não presume autorização para publicação externa.
