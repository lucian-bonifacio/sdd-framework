# Contratos dos artefatos — versão 1

## Organização
Projeto: README.md, AGENTS.md, docs/PRD.md, docs/ARCHITECTURE.md,
docs/ROADMAP.md, docs/inbox/, docs/decisions/ e CHECKPOINT.md quando houver pausa.
Funcionalidade: specs/NNN-nome/SPEC.md, TASKS.md, tasks/T-NNN.md e DESIGN.md
quando `design: separate`. Não criar README por SPEC.
Configuração e recursos: `.sdd/config.json`, `.sdd/manifest.json`,
`.sdd/framework/` e `.sdd/adoption/` (tickets da adoção inicial).
Integração Codex: `.codex/config.toml` e `.agents/skills/sdd/`. Integração Claude:
`.claude/skills/sdd/` e ponte CLAUDE.md. Init/update preparam configuração Codex
neutra somente se ausente; uma configuração existente pertence ao consumidor e
é preservada. A conferência verifica presença e sintaxe TOML, sem impor valores.
Execute init/update no terminal com permissão antes da sessão se `.codex` ou
`.agents` forem protegidas. O config não remove a proteção nem concede confiança.
Cada arquivo tem uma fonte de verdade. TASKS.md contém links, sem duplicar
status. O ROADMAP é a visão geral: o agente usa o script local
`scripts/atualizar_roadmap.py` para manter tarefas e ações humanas, conforme AGENTS.md. Atualizar
estados nos tickets e refletir o resultado nessa seção, preservando o planejamento.
Não exigir CLI ou framework instalado para fazer isso. `sdd check --roadmap` é
um auxiliar opcional de conferência explícita. Não criar STATUS.md ou relatório
global de validação. Resultado e evidência resumida ficam no ticket; evidência
extensa, quando útil, em `specs/NNN-nome/validation/`, vinculada ao ticket.

## Metadados
Documentos governados e tickets usam frontmatter YAML **restrito** entre `---`:
uma chave por linha, valor escalar em uma linha ou lista em sintaxe JSON.
Não usar YAML aninhado, aliases ou strings multilinha nos metadados. O corpo é
Markdown livre. Listas: `dependencies: ["specs/001-base/tasks/T-001.md"]`.
Strings com dois-pontos ou `#` devem usar aspas JSON. Campos adicionais escalares
ou listas são preservados. Templates documentam o contrato; remover marcadores
`[PREENCHER: ...]` e `{{...}}` ao preencher.

## Documentos gerais
PRD, ARCHITECTURE e ROADMAP: `status: draft|accepted|superseded`.
Conteúdo mínimo: as seções dos templates, inclusive README e AGENTS. O bloco de
instruções SDD deve ser preservado ao enriquecer AGENTS. PRD define IDs RF-NNN e
RNF-NNN. Requisitos detalhados da SPEC usam RF-NNN/RNF-NNN (escopo local).
Requisitos gerais devem ser referenciados no texto da SPEC, sem copiar contratos.

## SPEC e DESIGN
SPEC: `id: NNN-nome`, `status`, `design: inline|separate`.
No modo inline, preencher Design técnico; no separado, apontar para DESIGN.md,
que possui `status`. Pendências impeditivas não permitem declarar `accepted`.
SPEC inclui comportamento, fronteiras e CA-NNN verificáveis. DESIGN explica
como satisfazer a SPEC, sem substituir o contrato. Design System é referência
externa quando fornecido; registrar localização e versão no projeto.

## Tickets
ID T-NNN é único dentro da entrega; identidade completa é o caminho relativo ao
projeto. Dependências usam caminhos relativos à raiz, incluindo outra entrega.
Nunca reciclar ou renumerar IDs já usados.

Campos: `id`, `status`, `executor`, `authorization`, `dependencies`,
`requirements`, `verification`. Requisitos são IDs definidos na SPEC da entrega.
Tickets de adoção em `.sdd/adoption/tasks/` dispensam IDs de SPEC porque governam
a própria adequação, não requisitos do produto.

Estados: `pending`, `ready`, `in_progress`, `awaiting_user`, `blocked`, `done`,
`cancelled`. Autorização: `pending|approved`; execução: `agent|user|joint`.
Verificação: `not_verified|passed|failed|not_applicable`.
`ready` só é executável com autorização e dependências concluídas. Cancelamento
de uma dependência não satisfaz seu resultado: rever a tarefa dependente.
Para `done`, exigir `passed` ou `not_applicable` justificado em Verificação,
Resultado concreto e ausência de ação humana pendente. Evidências extensas ficam
em `validation/` com referência no Resultado. Tickets cancelados mantêm motivo.
Critérios automáticos atendidos, testes e revisões aplicáveis aprovados permitem
concluir sem aceite manual adicional. Quando houver dependência humana explícita,
registrar sua execução no Resultado e executar as verificações aplicáveis antes
de concluir. Autorização para executar e evidência de conclusão são distintas.
Alterar apenas status é insuficiente para comprovar conclusão. A CLI verifica
estrutura e referências; o agente revisa qualidade das evidências e obrigações.

## INBOX
`id: ITEM-NNN`, `status: pending|incorporated|discarded`, `created: AAAA-MM-DD`.
Fonte e data, proposta, impacto e decisão a discutir são obrigatórios. Destino
ou justificativa deve ser atualizado ao encerrar. Um item pendente não bloqueia
automaticamente toda implementação; sua relação com a tarefa determina o impacto.

## CHECKPOINT
`status: active|closed`, `updated: AAAA-MM-DD`, `task: caminho-do-ticket|none`.
Template cobre objetivo, trabalho parcial, tentativas úteis, testes reais,
decisões e propostas, próximo passo e leituras. Não armazenar segredos ou saídas
extensas. Quando o trabalho terminou, `task: none` e próximo passo explícito.
O Git mantém versões anteriores; o arquivo corrente é a passagem de contexto.

## ADR
`id: ADR-NNN`, `status: draft|accepted|superseded`. Contexto, decisão, alternativas
e consequências. Ao substituir, acrescentar link para sucessor, mantendo o original.

## Configuração
Scripts do consumidor ficam em `scripts/`. O atualizador de roadmap é criado
quando ausente e não é sobrescrito por update. Python e biblioteca padrão são
suficientes; não há import do SDD. Configuração .sdd é opcional para esse script.
O agente deve executar após mudanças nos tickets, conferir saída/diff e tratar
erros. Não criar scripts para substituir decisões semânticas; automatizar somente
operações repetíveis com escopo e resultado definidos.

Relatórios separados usam o template VALIDATION.md: `verification`, `revision`,
escopo/revisão, verificações e resultados/limitações. Identificar commit ou estado
local realmente testado. Relatório é condicional; não criar um por sessão vazia.

JSON com `schema_version: 1`, `framework_version`, `mode: new|existing`, `agent:
codex|claude|both|none`, `phase` e `document_paths` (mapa de nomes canônicos para
caminhos locais equivalentes). `interface` é `null` até ser esclarecido, depois
booleano. `design_system` é `null` ou objeto `{ "reference": "...", "version":
"..." }`, aceitando URL ou caminho. Arquivos locais são validados por existência.
`update_source` é nulo ou objeto com `repository` HTTPS e `ref` explícita.

## Limites de automação
A CLI detecta estrutura, modelos por preencher, metadados, dependências cíclicas,
referências locais, cobertura declarada, tarefas prontas e ações humanas pendentes.
Ela não atesta comportamento, segurança, aprovação humana real ou qualidade de
requisitos. `sdd check --fix` gera tickets de adequação; não executa código do
consumidor nem muda seu estado para aceito. Exit 1 significa gate estrutural
pendente; exit 2 significa erro operacional/configuração. Exit 0 continua exigindo
a revisão semântica e as verificações de execução descritas no fluxo.
