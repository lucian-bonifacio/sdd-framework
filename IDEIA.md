
# SDD FRAMEWORK
## Documento Mestre de Concepção, Requisitos e Decisões

**Status:** Planejamento inicial  
**Data:** 05/11/2026  
**Versão:** 0.1  
**Natureza:** Framework de inicialização, planejamento e preparação de projetos de software.

---

# 1. VISÃO GERAL

## 1.1. O que é o SDD Framework?

O SDD Framework é uma ferramenta reutilizável destinada a padronizar a criação, o planejamento e a preparação de projetos de software desenvolvidos com agentes de inteligência artificial.

Seu propósito é permitir que diferentes projetos sejam iniciados utilizando o mesmo processo, a mesma organização documental e os mesmos critérios de qualidade.

O framework deverá ser simples, reutilizável, versionado, atualizável e independente do agente de IA utilizado.

## 1.2. Problema que queremos resolver

Atualmente, diferentes projetos de software acabam utilizando:

- Estruturas documentais diferentes.
- Fluxos de planejamento diferentes.
- Formatos diferentes para PRDs, especificações e tarefas.
- Instruções diferentes para agentes de IA.
- Critérios inconsistentes para iniciar a implementação.
- Procedimentos pouco padronizados para revisar decisões.

Essa inconsistência dificulta a manutenção, a reutilização de conhecimentos e a evolução dos processos.

## 1.3. Objetivo

Criar uma ferramenta capaz de transformar uma ideia inicial em um projeto de software devidamente planejado, documentado e preparado para implementação.

O resultado deverá ser um projeto independente, com sua própria documentação, suas próprias regras e suas próprias tarefas.

## 1.4. Princípio fundamental

O framework prepara o projeto.

O agente de IA executa o projeto.

O framework não será uma dependência obrigatória durante a implementação.

---

# 2. PRINCÍPIOS DO FRAMEWORK

## P-001 — Simplicidade

Adotar sempre a solução mais simples que atenda às necessidades.

Evitar abstrações, automações e estruturas desnecessárias.

## P-002 — Padronização

Todos os projetos deverão seguir um processo comum de planejamento e documentação.

## P-003 — Documentação orientada a decisões

Documentos existem para materializar, preservar e comunicar decisões.

Não devem existir apenas por obrigação metodológica.

## P-004 — Desenvolvimento incremental

O planejamento poderá evoluir conforme novas funcionalidades e necessidades surgirem.

Não será necessário detalhar integralmente todo o software antes de iniciar seu desenvolvimento.

## P-005 — Independência operacional

Após o planejamento, o projeto deverá possuir informações suficientes para que um agente de IA execute as tarefas sem depender do SDD Framework.

## P-006 — Independência de agentes

O framework deverá buscar compatibilidade com diferentes agentes, especialmente:

- OpenAI Codex.
- Claude Code.

Particularidades de instalação e integração poderão variar entre os agentes.

## P-007 — Reutilização

O framework deverá ser utilizado em vários projetos sem exigir a criação de um processo diferente para cada um.

## P-008 — Evolução controlada

O framework terá versionamento próprio e poderá ser atualizado independentemente dos projetos que o utilizam.

## P-009 — Aplicação proporcional

O nível de detalhamento deve acompanhar a complexidade do projeto ou da funcionalidade.

Alterações pequenas não deverão exigir documentação desproporcional.

## P-010 — Revisão humana

As decisões relevantes serão submetidas à avaliação do usuário.

O agente poderá propor soluções, mas não deverá presumir a aprovação de decisões importantes.

---

# 3. ESCOPO

## 3.1. Responsabilidades do framework

O framework será responsável por:

1. Inicializar sua integração em novos projetos.
2. Conduzir a concepção do produto.
3. Levantar e organizar requisitos.
4. Orientar definições arquiteturais.
5. Organizar o planejamento geral.
6. Produzir especificações de funcionalidades.
7. Orientar decisões de design técnico.
8. Decompor funcionalidades em tarefas.
9. Criar e atualizar documentos de governança.
10. Preparar o AGENTS.md próprio do projeto.
11. Verificar a consistência dos artefatos produzidos.
12. Preparar a transferência para a implementação.
13. Permitir revisões futuras do planejamento.
14. Manter um processo padronizado entre projetos.

## 3.2. Fora do escopo

O framework não será responsável por:

- Implementar o código do software.
- Executar continuamente as tarefas de desenvolvimento.
- Substituir o agente programador.
- Gerenciar obrigatoriamente o ciclo de testes da implementação.
- Realizar deploys.
- Manter um sistema de agentes executores.
- Impor dependências de execução aos projetos.

Essas responsabilidades pertencerão ao próprio projeto e aos agentes de IA utilizados durante seu desenvolvimento.

---

# 4. CICLO DE VIDA DO SOFTWARE

Foi aprovada a separação do ciclo de vida em dois níveis:

1. Projeto.
2. Funcionalidade.

O framework atuará nas fases anteriores à implementação, preparando os artefatos necessários.

As fases posteriores serão executadas independentemente.

## 4.1. Nível Projeto

Fases:

1. Concepção.
2. Requisitos.
3. Arquitetura.
4. Planejamento.

Essas fases estabelecem as decisões gerais do software.

## 4.2. Nível Funcionalidade

Fases:

1. Especificação.
2. Design.
3. Tarefas.
4. Implementação.
5. Validação.
6. Entrega.

As três primeiras fases serão orientadas pelo SDD Framework.

As três últimas serão realizadas independentemente, utilizando os artefatos produzidos.

## 4.3. Fluxo geral

IDEIA
  |
  v
[SDD FRAMEWORK]
  |
  +-- CONCEPÇÃO
  |     Visão do produto
  |
  +-- REQUISITOS
  |     PRD
  |
  +-- ARQUITETURA
  |     Decisões técnicas gerais
  |
  +-- PLANEJAMENTO
  |     Roadmap
  |
  +-- ESPECIFICAÇÃO
  |     Requisitos detalhados da funcionalidade
  |
  +-- DESIGN
  |     Solução técnica da funcionalidade
  |
  +-- TAREFAS
  |     Trabalho executável
  |
  +-- PREPARAÇÃO FINAL
        Documentos e AGENTS.md consistentes
  |
  v
[PROJETO INDEPENDENTE]
  |
  +-- IMPLEMENTAÇÃO
  |
  +-- VALIDAÇÃO
  |
  +-- ENTREGA
  |
  v
SOFTWARE ENTREGUE

O ciclo de planejamento poderá ser reutilizado para novas funcionalidades e revisões futuras.

---

# 5. DEFINIÇÃO DAS FASES

## 5.1. Concepção

**Objetivo:** compreender a ideia do software.

**Entrada:** ideia inicial.

**Atividades:**

- Identificar o problema.
- Identificar o público.
- Identificar o resultado esperado.

**Saída:** visão inicial do produto, incorporada ao PRD.

**Critério de conclusão:**

Problema, público e resultado esperado estão suficientemente claros.

**Status:** aprovado.

## 5.2. Requisitos

**Objetivo:** definir o que o software precisa fazer.

**Entrada:** visão do produto.

**Atividades propostas:**

- Identificar funcionalidades principais.
- Definir requisitos não funcionais.
- Definir o escopo inicial.
- Identificar restrições.
- Identificar regras de negócio relevantes.

**Saída proposta:** PRD consolidado.

**Critério de conclusão proposto:**

Requisitos gerais suficientemente claros para orientar a arquitetura.

**Observação:**

Não é necessário detalhar completamente cada funcionalidade nesta fase.

**Status:** proposta discutida; aprovação formal pendente.

## 5.3. Arquitetura

**Objetivo:** definir a estrutura técnica geral do software.

**Entrada:** requisitos gerais.

**Atividades:**

- Selecionar tecnologias.
- Definir componentes principais.
- Estabelecer organização do sistema.
- Identificar decisões de segurança.
- Definir estratégias de integração.
- Registrar restrições arquiteturais.

**Saída proposta:** ARCHITECTURE.md.

**Critério de conclusão:**

A estrutura técnica oferece orientação suficiente para o desenvolvimento.

**Observação:**

Decisões específicas de funcionalidades poderão ser realizadas posteriormente.

**Status:** processo aprovado; detalhamento documental pendente.

## 5.4. Planejamento

**Objetivo:** organizar o desenvolvimento do software.

**Entrada:** requisitos e arquitetura geral.

**Atividades propostas:**

- Identificar entregas.
- Organizar prioridades.
- Definir marcos.
- Estabelecer sequência de desenvolvimento.
- Identificar dependências relevantes.

**Saída proposta:** ROADMAP.md.

**Critério de conclusão proposto:**

Existe uma sequência de desenvolvimento suficientemente clara.

**Status:** detalhamento pendente.

## 5.5. Especificação

**Objetivo:** detalhar uma funcionalidade.

**Entrada:** requisitos gerais e funcionalidade selecionada.

**Atividades propostas:**

- Definir comportamento esperado.
- Detalhar regras de negócio.
- Identificar entradas e saídas.
- Descrever cenários relevantes.
- Definir critérios de aceitação.

**Saída proposta:** SPEC da funcionalidade.

**Critério de conclusão proposto:**

A funcionalidade está suficientemente definida para orientar seu design.

**Status:** detalhamento pendente.

## 5.6. Design

**Objetivo:** definir como implementar tecnicamente a funcionalidade.

**Entrada:** especificação aprovada e arquitetura existente.

**Atividades propostas:**

- Definir componentes necessários.
- Identificar alterações nos dados.
- Estabelecer contratos e interfaces.
- Identificar integrações.
- Verificar aderência à arquitetura.

**Saída proposta:** design técnico da funcionalidade, preferencialmente incorporado à SPEC quando suficiente.

**Critério de conclusão proposto:**

A solução técnica está suficientemente definida para decomposição em tarefas.

**Status:** detalhamento pendente.

## 5.7. Tarefas

**Objetivo:** transformar especificações em unidades executáveis.

**Entrada:** especificação e design.

**Atividades propostas:**

- Decompor o trabalho.
- Identificar dependências.
- Estabelecer sequência de execução.
- Definir resultados verificáveis.
- Associar tarefas às especificações.

**Saída proposta:** arquivos ou listas padronizadas de tarefas.

**Critério de conclusão proposto:**

Um agente consegue compreender o trabalho necessário e seus critérios de conclusão.

**Status:** detalhamento pendente.

## 5.8. Implementação, Validação e Entrega

Essas fases pertencem ao ciclo de vida do software, mas não ao escopo operacional do SDD Framework.

Serão conduzidas pelos agentes de execução e pelas instruções próprias do projeto.

**Status:** separação aprovada.

---

# 6. DOCUMENTAÇÃO E GOVERNANÇA

## 6.1. Princípio documental

Todo documento deverá ter uma finalidade clara.

Sua existência deve ser justificada pela necessidade de registrar ou comunicar informações relevantes.

## 6.2. Artefatos previstos

| Artefato | Finalidade |
|---|---|
| PRD.md | Visão do produto e requisitos gerais |
| ARCHITECTURE.md | Arquitetura e decisões técnicas gerais |
| ROADMAP.md | Organização das entregas |
| SPEC | Especificação de uma funcionalidade |
| Design técnico | Definição da solução de uma funcionalidade |
| TASKS | Unidades de trabalho executáveis |
| AGENTS.md | Regras e instruções para agentes de IA |

Os nomes e os caminhos definitivos ainda serão padronizados.

## 6.3. Criação progressiva

O framework não deverá gerar todos os documentos vazios durante a inicialização.

Os documentos deverão surgir conforme as fases forem realizadas.

## 6.4. Atualização documental

Os documentos poderão evoluir durante o ciclo de vida do software.

Alterações relevantes deverão preservar a coerência entre requisitos, arquitetura, especificações e tarefas.

## 6.5. Documentos próprios dos projetos

Os documentos gerados pertencerão exclusivamente ao projeto.

Não dependerão do framework para serem lidos, utilizados ou modificados manualmente.

---

# 7. HARNESS E AGENTES DE IA

## 7.1. Conceito

O harness corresponde ao conjunto de instruções, skills, integrações e mecanismos que orientam o comportamento dos agentes.

O SDD Framework utilizará esse conjunto para conduzir o planejamento.

## 7.2. Estratégia aprovada

O framework começará com uma única skill principal:

SDD

Essa skill será responsável por orientar todo o processo de planejamento anterior à implementação.

Não serão criadas skills individuais para cada fase sem necessidade concreta.

## 7.3. Responsabilidades da skill SDD

- Identificar a fase atual.
- Consultar as informações disponíveis.
- Conduzir o levantamento de informações.
- Identificar lacunas e inconsistências.
- Propor decisões quando necessário.
- Registrar decisões aprovadas.
- Produzir e atualizar documentos.
- Verificar critérios de conclusão.
- Orientar a transição entre fases.
- Preparar o projeto para execução independente.

## 7.4. Skills adicionais

A criação de skills adicionais não será obrigatória.

Durante a implementação, cada projeto poderá possuir suas próprias skills especializadas.

Essas skills não dependerão do SDD Framework.

## 7.5. Independência dos agentes

O framework deverá buscar compatibilidade com Codex e Claude Code.

A implementação específica das integrações ainda será definida.

---

# 8. AGENTS.MD

## 8.1. Dois contextos diferentes

Existem dois arquivos conceitualmente distintos.

### AGENTS.md do SDD Framework

Pertence ao repositório do framework.

Orienta agentes que trabalham no desenvolvimento e na manutenção do próprio framework.

Não será copiado obrigatoriamente para projetos consumidores.

### AGENTS.md do projeto

Pertence ao software que está sendo construído.

Orienta os agentes responsáveis por desenvolver e manter esse software.

## 8.2. Inicialização

Ao executar o comando de inicialização, o framework poderá criar um AGENTS.md mínimo no novo projeto.

Esse documento incluirá inicialmente:

- Orientações para utilizar a skill SDD.
- Regras gerais de planejamento.
- Instruções provisórias relevantes.

## 8.3. Evolução

Conforme os requisitos e a arquitetura forem definidos, o AGENTS.md do projeto será enriquecido.

Poderá conter:

- Visão resumida do projeto.
- Tecnologias adotadas.
- Referências à documentação.
- Convenções de desenvolvimento.
- Comandos de testes.
- Regras de segurança.
- Restrições operacionais.
- Instruções para agentes executores.

## 8.4. Prevenção de conflitos

O framework não deverá competir com as instruções próprias do projeto.

O projeto terá um AGENTS.md principal na raiz.

O SDD não deverá sobrescrever instruções existentes indiscriminadamente.

Ao concluir o planejamento, o AGENTS.md deverá permitir a execução independente.

## 8.5. Conclusão do planejamento

A conclusão não exige remover o AGENTS.md nem desinstalar o framework.

O projeto poderá manter uma referência opcional ao SDD para futuras revisões.

Nenhuma instrução essencial à implementação deverá depender da disponibilidade da skill SDD.

---

# 9. DISTRIBUIÇÃO E INSTALAÇÃO

## 9.1. Modelo geral

O SDD Framework será um projeto independente, mantido em repositório Git próprio.

Seu conteúdo será reutilizável em diferentes projetos.

## 9.2. Componentes previstos

O conjunto poderá conter:

1. Framework metodológico.
2. Skill SDD.
3. Templates documentais.
4. Ferramenta CLI.
5. Mecanismo de atualização.
6. Integrações com agentes.

A implementação exata será definida posteriormente.

## 9.3. CLI

A proposta é oferecer uma interface de linha de comando.

Comandos conceituais:

sdd init

Inicializa a integração do framework em um projeto.

sdd update

Atualiza os componentes do framework utilizados pela instalação.

sdd detach

Opcionalmente desvincula o framework de um projeto.

**Importante:** esses comandos são propostas; ainda não foram implementados.

## 9.4. Instalação centralizada

Preferência por uma instalação central reutilizável.

Os projetos não deverão exigir cópias independentes de toda a skill SDD.

Isso permitirá manter uma fonte principal das instruções.

## 9.5. Git e versionamento

O framework terá seu próprio histórico Git.

Novas versões poderão:

- Corrigir problemas.
- Melhorar templates.
- Alterar o fluxo de planejamento.
- Adicionar integrações.
- Refinar instruções da skill.

A atualização do framework não deverá modificar automaticamente documentos já aprovados dos projetos.

## 9.6. Atualizações controladas

A evolução do framework deve preservar a estabilidade dos projetos existentes.

Projetos poderão continuar utilizando documentos produzidos por versões anteriores.

A estratégia exata de compatibilidade e fixação de versões ainda será definida.

---

# 10. FUNCIONAMENTO PRÁTICO

## 10.1. Exemplo: criação de um projeto

O usuário abre um terminal:

mkdir new-projeto
cd new-projeto
code .

Em seguida:

sdd init

O comando prepara o ambiente para utilizar o framework.

## 10.2. Estrutura inicial ilustrativa

new-projeto/
├── AGENTS.md
└── .sdd/
    └── config.yaml

A estrutura definitiva ainda será definida.

## 10.3. Planejamento

O usuário inicia um agente:

codex

E solicita:

"Quero desenvolver um sistema de gestão financeira.
Vamos planejar utilizando o SDD."

O agente identifica a skill SDD e inicia a Concepção.

O processo avança progressivamente, produzindo os documentos necessários.

## 10.4. Estrutura após o planejamento

Exemplo ilustrativo:

new-projeto/
├── AGENTS.md
├── .sdd/
│   └── config.yaml
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   └── ROADMAP.md
├── specs/
│   └── gestao-financeira.md
└── tasks/
    ├── TASK-001.md
    └── TASK-002.md

Essa estrutura não está definitivamente aprovada.

## 10.5. Encerramento do SDD

Ao concluir o planejamento:

1. O agente verifica a consistência documental.
2. Confirma que as tarefas estão preparadas.
3. Confirma que o AGENTS.md contém instruções suficientes.
4. Identifica pendências relevantes.
5. Encerra a atuação da skill SDD.

O projeto passa a ser implementado independentemente.

## 10.6. Implementação

O usuário poderá solicitar:

"Implemente a TASK-001."

O agente utilizará:

- AGENTS.md do projeto.
- Arquitetura documentada.
- Especificações relevantes.
- Tarefas aprovadas.
- Skills próprias de execução, quando existirem.

A skill SDD não será necessária.

## 10.7. Reutilização futura

Se o usuário desejar uma nova funcionalidade:

"Quero adicionar conciliação bancária ao sistema.
Vamos planejar essa funcionalidade com o SDD."

A skill poderá ser novamente utilizada.

A execução anterior continuará independente.

---

# 11. CONCLUSÃO DO FRAMEWORK

## 11.1. O framework possui um ponto de encerramento?

Sim.

Cada ciclo de planejamento possui início e conclusão.

## 11.2. O framework será removido automaticamente?

Não.

A auto-remoção foi rejeitada.

O framework poderá ser útil para:

- Novas funcionalidades.
- Revisões de requisitos.
- Mudanças arquiteturais.
- Atualização de especificações.
- Replanejamento.

## 11.3. Dependência após o planejamento

A implementação não deverá depender do framework.

O projeto deverá possuir todos os documentos e instruções necessários para continuar autonomamente.

## 11.4. Desvinculação

Uma eventual funcionalidade de desvinculação será opcional.

Sua execução não deverá apagar documentos ou código do projeto.

---

# 12. REFERÊNCIAS E INSPIRAÇÕES

## 12.1. Akita — AI Lair

https://ailair.akitaonrails.com/pt-br/workflow/

Referência para:

- Organização de workflows.
- Instruções para agentes.
- Skills reutilizáveis.
- Execução orientada por tarefas.
- Melhoria contínua.
- Redução de procedimentos desnecessários.

Não será copiado integralmente.

## 12.2. GitHub Spec Kit

https://github.com/github/spec-kit

Referência para:

- Spec-Driven Development.
- Inicialização de projetos.
- CLI.
- Templates.
- Especificações.
- Planejamento.
- Tarefas.
- Integração com agentes de IA.

Diferença fundamental:

O Spec Kit também orienta a implementação.

Nosso framework será limitado ao planejamento e à preparação.

## 12.3. OpenSpec

https://github.com/Fission-AI/OpenSpec

Referência para:

- Planejamento incremental.
- Especificações de mudanças.
- Organização de documentos.
- Evolução de requisitos.
- Simplicidade operacional.
- Integração com agentes.

## 12.4. BMAD Method

https://github.com/bmad-code-org/BMAD-METHOD

Referência para:

- Levantamento de requisitos.
- Estruturação de PRDs.
- Planejamento arquitetural.
- Separação de responsabilidades.

Não pretendemos reproduzir sua complexidade de agentes especializados.

## 12.5. Get Shit Done (GSD)

https://github.com/gsd-build/get-shit-done

Referência para:

- Planejamento orientado a entregas.
- Organização de contexto.
- Decomposição do trabalho.
- Ciclos de validação.

## 12.6. Akita — AI Memory

https://github.com/akitaonrails/ai-memory

Referência conceitual para:

- Distribuição reutilizável.
- Instalação em projetos.
- Integração com ferramentas de IA.
- Versionamento e manutenção centralizada.

O SDD Framework não pretende reproduzir suas funcionalidades de memória.

---

# 13. REGISTRO DE DECISÕES

## DEC-001 — Estrutura do ciclo de vida

**APROVADA**

Dois níveis:

Projeto:
- Concepção.
- Requisitos.
- Arquitetura.
- Planejamento.

Funcionalidade:
- Especificação.
- Design.
- Tarefas.
- Implementação.
- Validação.
- Entrega.

## DEC-002 — Princípios gerais

**APROVADA**

- Simplicidade.
- Funcionalidade.
- Documentação orientada a decisões.
- Desenvolvimento incremental.
- Aplicação proporcional.
- Independência de agentes.

## DEC-003 — Concepção

**APROVADA**

A Concepção responderá:

- Qual problema resolver?
- Para quem?
- Qual resultado esperado?

As respostas serão incorporadas ao PRD.

## DEC-004 — Requisitos

**PENDENTE DE APROVAÇÃO FORMAL**

Proposta:

Definir funcionalidades principais, requisitos não funcionais, escopo e restrições.

Resultado: PRD consolidado.

## DEC-004A — Estratégia de skills

**ALINHAMENTO ESTABELECIDO**

Uma skill principal SDD para todo o processo pré-implementação.

Skills adicionais somente quando justificadas.

## DEC-004B — Repositório central

**APROVADA**

Criar um projeto independente chamado provisoriamente:

sdd-framework

Esse projeto será reutilizado na inicialização de outros softwares.

## DEC-004C — Instalação e versionamento

**ALINHAMENTO ESTABELECIDO**

- Repositório Git independente.
- Instalação centralizada preferencial.
- Atualizações controladas.
- Reutilização entre projetos.
- CLI proposta.

Os mecanismos específicos ainda serão definidos.

## DEC-004D — Persistência e AGENTS.md

**APROVADA**

- Framework disponível para revisões futuras.
- Sem auto-remoção.
- Cada projeto possui AGENTS.md próprio.
- O AGENTS.md do framework governa apenas o próprio framework.
- A skill SDD conduz o planejamento.
- As instruções de implementação pertencem ao projeto.

## DEC-004E — Limite de responsabilidade

**APROVADA**

O SDD Framework termina sua atuação operacional ao entregar um projeto planejado e preparado.

A implementação, validação e entrega serão independentes.

---

# 14. PENDÊNCIAS

## 14.1. Processo

- Aprovar formalmente a fase de Requisitos.
- Detalhar a fase de Planejamento.
- Detalhar Especificação.
- Detalhar Design.
- Detalhar Tarefas.
- Definir o critério final de prontidão para implementação.
- Definir como tratar revisões e mudanças de escopo.

## 14.2. Documentação

- Definir nomes definitivos.
- Definir estrutura de diretórios.
- Criar templates.
- Definir relações entre documentos.
- Definir critérios de consistência.
- Decidir quando separar ou combinar SPEC e design.
- Definir padrão de identificação das tarefas.
- Definir estrutura final do AGENTS.md.

## 14.3. Harness

- Definir estrutura da skill SDD.
- Definir instruções e referências internas.
- Definir integração com Codex.
- Definir integração com Claude Code.
- Definir como o agente identifica a fase atual.
- Definir como o agente registra aprovações.
- Definir como o projeto opera após o encerramento do SDD.

## 14.4. Distribuição

- Decidir a tecnologia da CLI, se necessária.
- Definir o comando de instalação.
- Definir o funcionamento do sdd init.
- Definir o funcionamento do sdd update.
- Avaliar necessidade de sdd detach.
- Definir estratégia de versões.
- Definir mecanismo de integração centralizada.
- Definir regras de atualização sem sobrescrita indevida.

## 14.5. Qualidade

- Definir verificações documentais.
- Definir testes do próprio framework.
- Validar inicialização em projeto vazio.
- Validar instalação em projeto existente.
- Validar preservação de AGENTS.md existente.
- Validar execução independente.
- Validar reutilização futura da skill.
- Validar atualização do framework.

---

# 15. ORDEM RECOMENDADA DE CONSTRUÇÃO

## Etapa 1 — Concluir a definição do processo

Finalizar as fases, suas entradas, atividades, saídas e critérios de conclusão.

## Etapa 2 — Padronizar a documentação

Definir estrutura, nomes e templates.

## Etapa 3 — Construir a skill SDD

Transformar o processo em instruções operacionais para agentes de IA.

## Etapa 4 — Integrar com agentes

Priorizar Codex e, depois, Claude Code.

## Etapa 5 — Testar manualmente

Utilizar a skill em um projeto vazio.

Verificar se os documentos e instruções produzidos permitem uma implementação independente.

## Etapa 6 — Criar a instalação simplificada

Desenvolver a CLI mínima, se continuar sendo a melhor opção.

Priorizar o comando:

sdd init

## Etapa 7 — Versionar e distribuir

Publicar no Git e estabelecer o mecanismo de atualização.

## Etapa 8 — Evoluir conforme necessidades reais

Não adicionar recursos antecipadamente.

---

# 16. DEFINIÇÃO DE SUCESSO

O SDD Framework será considerado funcional quando:

1. Um usuário conseguir iniciar um novo projeto com um procedimento simples.
2. Um agente conseguir conduzir o planejamento utilizando a skill SDD.
3. Os documentos forem produzidos seguindo padrões consistentes.
4. As decisões relevantes forem preservadas.
5. O AGENTS.md do projeto estiver preparado para orientar agentes executores.
6. As tarefas estiverem suficientemente detalhadas para implementação.
7. O desenvolvimento puder continuar sem utilizar o SDD Framework.
8. O framework puder ser reutilizado em outro projeto.
9. As instruções centrais puderem ser atualizadas sem reescrever manualmente todos os projetos.
10. O processo continuar simples o suficiente para ser utilizado rotineiramente.

---

# 17. DIRETRIZ FINAL

O objetivo não é construir o framework de desenvolvimento mais completo do mercado.

O objetivo é construir o menor framework capaz de:

- Transformar ideias em planos executáveis.
- Padronizar documentos.
- Preservar decisões.
- Orientar agentes de IA.
- Preparar projetos independentes.
- Ser reutilizado e aprimorado continuamente.

O framework deverá reduzir trabalho, não criar trabalho.

**Regra principal:**

Se uma etapa, documento, comando ou abstração não demonstrar utilidade concreta, não deverá ser adicionada.

---

# 18. PRÓXIMO PASSO

Retomar a discussão da DEC-004 (Requisitos), ainda pendente de aprovação formal.

Depois, continuar detalhando as demais fases, sempre utilizando o procedimento:

DISCUTIR → DECIDIR → REGISTRAR → AVANÇAR

Uma decisão por vez.

Não iniciar a implementação do framework antes de concluir as definições mínimas necessárias.

---

FIM DO DOCUMENTO
