# Guia de funcionamento do SDD Framework

Este manual descreve a implementação atual da versão 0.1.0: o que cada comando
faz, quais arquivos são criados e quem mantém cada informação. Pertence à
documentação do **framework**; não é um documento governado obrigatório dos
consumidores nem é copiado para eles pelo init.

## 1. Primeiro, diferencie os dois projetos

| Projeto | Conteúdo |
|---|---|
| Repositório `sdd-framework` | Código, templates e regras que desenvolvemos para distribuir |
| Projeto consumidor | Seu produto, com documentos preenchidos, instruções e ferramentas locais |

Por exemplo: `src/sdd_framework/assets/templates/PRD.md` é o modelo distribuído;
o `docs/PRD.md` do consumidor descreve o produto dele. O `docs/PRD.md` deste
repositório descreve o próprio SDD Framework.

## 2. Exemplo de primeira utilização

No terminal, antes de abrir o agente no consumidor:

```bash
python3 /home/lucian/projects/sdd-framework/sdd.py init /tmp/teste-sdd
```

Nesse exemplo, o programa vem da cópia local do framework e o destino é
`/tmp/teste-sdd`. Se o destino não existir, ele é criado. O padrão é preparar
Codex e Claude Code (`--agent both`). `--agent` não abre ou executa esses agentes.

Depois, abra o consumidor no agente e peça: **“Inicie. Quero planejar meu projeto.”**
O programa já preparou as instruções; a conversa com o agente é que levanta
informações e preenche os documentos. Init sozinho não inventa o produto.

## 3. O que acontece durante o init

| Passo | Comportamento |
|---|---|
| 1 | Determina o caminho de destino e cria sua raiz, se necessário |
| 2 | Cria `.sdd/lock` para evitar operações CLI concorrentes |
| 3 | Se já houver configuração válida, informa que o projeto está inicializado e não muda arquivos |
| 4 | Identifica o modo inicial: novo ou existente; permite informar `--mode new` ou `--mode existing` |
| 5 | Lê e valida a distribuição: versão, política, templates, skill, configuração nativa e script |
| 6 | Prepara o conjunto de arquivos e verifica conflitos, caminhos e permissões antes de escrever recursos |
| 7 | Instala o snapshot, as integrações selecionadas, o script local e o plano de adequação |
| 8 | Salva configuração e manifesto, informa os arquivos alterados e remove o lock |

A detecção de modo é uma heurística de presença de arquivos. Init não interpreta
o código existente. README, código ou documentação já presentes podem indicar
`existing`; o inventário de conteúdo é responsabilidade do agente depois.

Se um conflito for detectado, o conteúdo existente é preservado. A pasta `.sdd/`
pode ter sido criada para o lock antes desse diagnóstico. Em falhas ordinárias
durante a escrita, a implementação tenta restaurar os arquivos já alterados;
isso não é garantia transacional contra interrupção do sistema.

## 4. Pastas e arquivos criados imediatamente

Estrutura padrão de um consumidor vazio após init com `--agent both`:

```text
projeto/
├── AGENTS.md
├── CLAUDE.md
├── .codex/
│   └── config.toml
├── .agents/
│   └── skills/sdd/
│       ├── SKILL.md
│       └── references/
│           ├── WORKFLOW.md
│           └── ARTIFACTS.md
├── .claude/
│   └── skills/sdd/
│       ├── SKILL.md
│       └── references/
│           ├── WORKFLOW.md
│           └── ARTIFACTS.md
├── scripts/
│   └── atualizar_roadmap.py
├── docs/
│   ├── inbox/
│   └── decisions/
├── specs/
└── .sdd/
    ├── config.json
    ├── manifest.json
    ├── adoption/
    │   ├── TASKS.md
    │   └── tasks/
    │       ├── T-001.md
    │       ├── T-002.md
    │       ├── T-003.md
    │       ├── T-004.md
    │       ├── T-005.md
    │       └── T-006.md
    └── framework/
        ├── bundle.json
        ├── policy.json
        ├── integrations/codex/config.toml
        ├── scripts/atualizar_roadmap.py
        ├── skill/
        │   ├── SKILL.md
        │   └── references/
        │       ├── WORKFLOW.md
        │       └── ARTIFACTS.md
        └── templates/
            ├── README.md
            ├── AGENTS.md
            ├── PRD.md
            ├── ARCHITECTURE.md
            ├── ROADMAP.md
            ├── SPEC.md
            ├── DESIGN.md
            ├── TASKS.md
            ├── TASK.md
            ├── CHECKPOINT.md
            ├── INBOX.md
            ├── ADR.md
            └── VALIDATION.md
```

`docs/inbox/`, `docs/decisions/` e `specs/` começam vazias. Init não cria PRD,
arquitetura, roadmap, README de produto, SPECs ou CHECKPOINT vazios na raiz.

### 4.1 Instruções e integrações na raiz

| Caminho | Finalidade e tratamento |
|---|---|
| `AGENTS.md` | Instruções do projeto. Init acrescenta o bloco `SDD:START/END`; conteúdo externo é preservado. O agente enriquece o restante com contexto, comandos e restrições do consumidor |
| `CLAUDE.md` | Ponte para o Claude ler o AGENTS.md. Criada para `claude` ou `both`, preservando conteúdo externo ao bloco SDD |
| `.codex/config.toml` | Configuração Codex local. O modelo é neutro, com comentários e sem fixar modelo/permissões. Criado para `codex` ou `both`, somente se ausente |
| `.agents/skills/sdd/SKILL.md` | Entrada da skill para Codex: instrui o agente a conduzir o planejamento e manter o processo |
| `.claude/skills/sdd/SKILL.md` | A mesma skill, instalada no diretório reconhecido pelo Claude |
| `references/WORKFLOW.md` em cada skill | Etapas, critérios de avanço, execução de tarefas, pausas, trabalho humano e revisão |
| `references/ARTIFACTS.md` em cada skill | Caminhos, modelos, metadados, estados e responsabilidades dos documentos |

Com `--agent codex`, somente a integração Codex é preparada; com `claude`, somente
Claude; com `none`, nenhuma integração nativa é criada. AGENTS.md, script,
snapshot e plano de adequação continuam sendo preparados.

Pastas como `.codex/` e `.agents/` podem estar protegidas durante uma sessão
Codex. Criar config.toml não remove essa proteção. Por isso, prepare o consumidor
no terminal com acesso de escrita antes de abrir a sessão do agente.

### 4.2 Configuração e inventário em .sdd/

| Arquivo | Finalidade |
|---|---|
| `config.json` | Configuração desta instalação: versão, agente, etapa e adaptações de caminhos |
| `manifest.json` | Versão e hashes dos recursos e blocos administrados; ajuda a detectar alterações e conflitos |
| `lock` | Arquivo temporário de exclusão entre operações CLI; normalmente removido ao terminar |

Campos de `config.json`:

| Campo | Conteúdo |
|---|---|
| `schema_version` | Versão do formato da configuração, atualmente 1 |
| `framework_version` | Versão dos recursos aplicados ao consumidor |
| `mode` | `new` ou `existing` |
| `agent` | `codex`, `claude`, `both` ou `none` |
| `phase` | Etapa atual; começa em `discovery` |
| `document_paths` | Equivalências entre caminhos canônicos e documentação já existente |
| `interface` | `null` enquanto desconhecido; depois `true` ou `false` |
| `design_system` | Referência e versão do Design System existente, ou `null` |
| `update_source` | Fonte Git e ref explicitamente configuradas para atualização, ou `null` |

Configuração é dado local, não uma aprovação de requisitos. Manifesto não é
assinatura de segurança nem evidência de que os testes do produto passaram.

### 4.3 Plano de adequação em .sdd/adoption/

`TASKS.md` é o índice dos seis tickets iniciais:

| Ticket | Trabalho |
|---|---|
| `T-001.md` | Inventariar e integrar o projeto |
| `T-002.md` | Consolidar README e PRD |
| `T-003.md` | Definir arquitetura e instruções do projeto |
| `T-004.md` | Organizar roadmap |
| `T-005.md` | Especificar a primeira entrega |
| `T-006.md` | Preparar tickets e transferência para execução independente |

O primeiro começa em `ready`; os seguintes em `pending`, encadeados por
dependências. A autorização desses tickets cobre a organização solicitada;
não aprova silenciosamente decisões importantes de produto ou implementação.
Eles não ficam concluídos apenas porque init terminou: o agente precisa fazer
o trabalho, verificar e registrar os resultados.

### 4.4 Snapshot em .sdd/framework/

É a cópia versionada dos recursos que o framework disponibiliza para consulta.

| Caminho | Finalidade |
|---|---|
| `bundle.json` | Identificação da versão e compatibilidade da distribuição |
| `policy.json` | Etapas, seções exigidas e valores aceitos pelo verificador estrutural |
| `skill/` | Fonte local das instruções genéricas, também copiada para os agentes selecionados |
| `integrations/codex/config.toml` | Modelo original da configuração nativa, não a configuração editável do consumidor |
| `scripts/atualizar_roadmap.py` | Modelo original da ferramenta local, não a cópia editável em scripts/ da raiz |
| `templates/` | Modelos de preenchimento; não são os documentos reais do produto |

Os treze templates:

| Template | Artefato que orienta |
|---|---|
| `README.md` | Apresentação e primeiros passos |
| `AGENTS.md` | Contexto, comandos e convenções para agentes |
| `PRD.md` | Problema, público, objetivos, requisitos e restrições |
| `ARCHITECTURE.md` | Estrutura técnica, contratos e verificação |
| `ROADMAP.md` | Entregas, prioridades e acompanhamento das tarefas |
| `SPEC.md` | Comportamento e aceitação de uma funcionalidade |
| `DESIGN.md` | Solução técnica, quando precisar de documento separado |
| `TASKS.md` | Índice e organização das tarefas de uma entrega |
| `TASK.md` | Ticket individual, com estado, obrigações e resultado |
| `CHECKPOINT.md` | Passagem de contexto e orientação de retomada |
| `INBOX.md` | Pesquisa ou proposta ainda em avaliação |
| `ADR.md` | Decisão arquitetural relevante |
| `VALIDATION.md` | Evidência extensa opcional, vinculada a um ticket; não um relatório global obrigatório |

Não editar diretamente o snapshot. Para personalizações do produto, editar os
documentos e ferramentas do próprio consumidor. Para evoluir o framework,
alterar as fontes no repositório do framework e aplicar uma atualização revisada.

### 4.5 Script do consumidor em scripts/

`scripts/atualizar_roadmap.py` é criado quando ausente e passa a pertencer ao
consumidor. Updates preservam um arquivo local existente, inclusive customizado.

O AGENTS.md e a skill orientam o agente a executá-lo após alterações nos tickets:

```bash
python3 scripts/atualizar_roadmap.py
```

O script:

1. Lê tickets em `specs/*/tasks/` e os de `.sdd/adoption/tasks/`, quando presentes.
2. Obtém estados, executores, verificações e ações humanas registradas.
3. Agrupa tarefas por entrega e calcula os totais.
4. Atualiza somente o bloco `SDD:PROGRESS:START/END` do roadmap.
5. Preserva planejamento e conteúdo externo ao bloco; em erro de leitura ou
   marcadores, não declara sucesso nem substitui o roadmap por um resumo parcial.

Usa biblioteca padrão Python, sem importar SDD. Funciona de outra pasta e sem
`.sdd/`; o caminho padrão é `docs/ROADMAP.md`. Pode usar equivalências da configuração
local quando disponível, ou receber `--roadmap caminho/ROADMAP.md` explicitamente.
Durante a escrita, usa lock temporário junto ao roadmap e substituição atômica.
O agente deve conferir saída e diff. O script não executa testes do produto e
não conclui tickets: ele apresenta o que está registrado neles.

## 5. O que o agente cria progressivamente

| Caminho padrão | Quando e para quê |
|---|---|
| `README.md` | Apresentação inicial do produto e como começar |
| `docs/PRD.md` | Consolidação de problema, público, escopo e requisitos |
| `docs/ARCHITECTURE.md` | Definição técnica geral |
| `docs/ROADMAP.md` | Entregas, prioridades e visão geral de tarefas/ações humanas |
| `specs/NNN-nome/SPEC.md` | Especificação da entrega selecionada |
| `specs/NNN-nome/DESIGN.md` | Solução técnica separada quando a complexidade justificar; caso contrário, seção na SPEC |
| `specs/NNN-nome/TASKS.md` | Índice com links para os tickets da entrega |
| `specs/NNN-nome/tasks/T-NNN.md` | Trabalho executável individual |
| `specs/NNN-nome/validation/` | Evidências extensas opcionais vinculadas aos tickets |
| `docs/decisions/ADR-NNN.md` | Decisões transversais relevantes |
| `docs/inbox/ITEM-NNN.md` | Pesquisas e propostas ainda não incorporadas |
| `CHECKPOINT.md` | Estado real ao pedir pausa ou passagem de contexto |

O agente preenche os modelos com as informações do projeto. Rascunho vazio não
satisfaz a etapa que exige o documento. Projetos existentes podem manter caminhos
equivalentes após revisão e registro em `document_paths`.

`T-001` pode existir em várias entregas; a identidade completa é o caminho do
ticket. `TASKS.md` é índice, o ticket é a fonte de estado, e ROADMAP é a visão
consolidada. Não existe README obrigatório por SPEC nem STATUS.md obrigatório.

Critérios de aceitação, testes e revisões aplicáveis atendidos permitem concluir
sem aceite manual adicional. Se a tarefa depender do usuário, registrar sua ação
e verificar o resultado antes da conclusão. O roadmap mostra essas pendências.

## 6. O que faz update

É manutenção opcional dos componentes do framework, não etapa de cada tarefa.

| Situação | Resultado |
|---|---|
| Sem fonte configurada | Usa a distribuição da CLI instalada; não presume um GitHub nem consulta novas versões online |
| `--source /caminho` | Lê uma distribuição local compatível |
| `--repository URL --ref TAG` | Obtém explicitamente uma fonte Git HTTPS; requer Git e rede |
| Recursos administrados intactos | Atualiza snapshot, cópias da skill, blocos SDD e versão |
| Recurso/bloco administrado editado | Recusa conflito e preserva o conteúdo |
| Configuração Codex ou script local existente | Preserva a versão do consumidor |
| Configuração Codex ou script local ausente | Prepara o arquivo correspondente quando aplicável |
| PRD, SPEC, tickets, decisões e roadmap do produto | Não reescreve automaticamente esses documentos |

Incompatibilidade de política exige outra versão da CLI. Downgrade é recusado.
Update não executa scripts do consumidor nem código baixado; instalar recursos
novos não significa que suas mudanças documentais foram aceitas.

## 7. O que faz conferência

`check` (ou `conferencia`) lê documentos, configurações e tickets e apresenta:

- Arquivos exigidos pela etapa e seções vazias/modelos ainda por preencher.
- Metadados, links locais e referências a requisitos.
- Dependências ausentes, ciclos e cobertura declarada de requisitos por tarefas.
- Todas as tarefas por entrega, seus estados e ações humanas pendentes.
- Integridade dos recursos administrados e sintaxe da configuração Codex.

| Opção | Efeito |
|---|---|
| Sem opções de escrita | Somente leitura e diagnóstico |
| `--phase etapa` | Confere condições documentais para entrar nessa etapa |
| `--spec NNN-nome` | Foca exigências de avanço na entrega selecionada |
| `--json` | Apresenta dados estruturados para ferramentas |
| `--fix` | Cria tickets deduplicados de adequação; não inventa documentos aprovados |
| `--roadmap` | Auxiliar opcional que atualiza o bloco de acompanhamento do roadmap |

A conferência não executa testes da aplicação, não prova a qualidade dos
requisitos e não autoriza trabalho. Código de saída 0 significa ausência de
impedimentos estruturais, 1 indica pendências, e 2 indica erro operacional.

O consumidor não precisa desse comando para continuar: suas instruções, testes,
documentos e scripts locais sustentam o trabalho. O comando é uma ferramenta
adicional quando se pede uma revisão do padrão do framework.

## 8. Quem pode editar o quê

| Categoria | Responsável | Tratamento |
|---|---|---|
| Documentos do produto e tickets | Agente/usuário do consumidor | Evoluem segundo requisitos e decisões aceitas |
| Roadmap, bloco de acompanhamento | Script local acionado pelo agente | Derivado dos tickets; não alterar estados apenas nesse resumo |
| `scripts/atualizar_roadmap.py` e `.codex/config.toml` reais | Consumidor | Podem ser adaptados; updates os preservam |
| Snapshot `.sdd/framework/` e cópias instaladas da skill | Atualização controlada do framework | Alterações locais causam conflito em update |
| Blocos SDD em AGENTS/CLAUDE | Framework | Conteúdo externo é preservado; edição interna exige reconciliação |
| Campos locais de `.sdd/config.json` | Agente/usuário | Registrar etapa e equivalências sem contornar critérios de avanço |
| `.sdd/manifest.json` | CLI | Não alterar hashes para esconder conflito |

## 9. Repetir init e usar projetos existentes

Init repetido com configuração válida não reinstala e não troca a integração.
Por exemplo, executar `init --agent claude` num projeto já inicializado com
`codex` não faz uma migração de agente nesta versão.

Em projeto existente, init preserva os documentos; depois o agente identifica
equivalências e conflitos e planeja sua adequação. Ele não deve apagar decisões
válidas nem declarar conformidade apenas por reconhecer nomes de arquivos.

## 10. Arquivos deste repositório que não vão para o consumidor

| Caminho aqui | Papel |
|---|---|
| `sdd.py` | Entrada de desenvolvimento para executar a CLI deste checkout |
| `src/sdd_framework/cli.py` | Comandos e apresentação da CLI |
| `src/sdd_framework/project.py` | Instalação, integração e atualização |
| `src/sdd_framework/checks.py` | Conferência estrutural e tickets corretivos |
| `src/sdd_framework/storage.py` | Leitura/escrita, caminhos, lock e preservação |
| `src/sdd_framework/markdown.py` | Metadados e seções Markdown |
| `src/sdd_framework/progress.py` | Adaptador opcional da CLI para acompanhamento |
| `src/sdd_framework/consumer_roadmap.py` | Fonte do script autônomo que é copiado ao consumidor com outro caminho |
| `src/sdd_framework/assets/` | Fontes dos recursos distribuídos |
| `tests/` | Testes do framework, com consumidores temporários |
| `tools/build_release.py` | Construtor do executável portátil |
| `dist/sdd.pyz` | Distribuição portátil; pode ser usada para iniciar outro projeto |
| `docs/` e `specs/` deste repositório | Documentação e tarefas para construir o próprio framework |

O consumidor recebe os recursos definidos pela instalação, não uma cópia de
todo este repositório. O núcleo da rotina dele é: **instruções locais → tickets
→ execução e verificações do produto → resultados → roadmap atualizado**.
