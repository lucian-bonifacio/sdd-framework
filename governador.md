<!-- SDD:GOVERNADOR:START -->
# Governador SDD

Versão do procedimento: 0.4.2. Instruções para a IA que trabalha no projeto,
escritas para leitura, revisão e contestação humanas.

Execute somente por acionamento explícito do usuário ou da skill SDD. Instalação,
update, leitura do arquivo e abertura de sessão não são acionamento. O controle
de execução fica em .sdd/execucao.json; decisões e trabalho do projeto ficam nos
documentos governados pertinentes, sem seção de aplicação neste arquivo.
Use os [contratos](docs/padroes/CONTRATOS.md) em todos os escopos. Os templates,
contratos e a skill do SDD Framework são as únicas referências de padrão e método
para esta execução; não consulte templates ou skills de outros frameworks.

### Execução e reexecução
O critério de pronto de cada item é o ponto de partida. Se alguma condição não
estiver atendida, o item não está concluído: execute somente o que falta e preserve
o que já estiver pronto. Se todas estiverem atendidas, o item está concluído.
Não há estados intermediários.

Depois de concluído, consulte .sdd/execucao.json no próximo acionamento. Se o
framework mudou, trate somente as operações alteradas e seus impactos diretos,
conferindo os critérios afetados. Se não mudou, preserve o documento. A skill SDD
explica como manter esse controle; o update identifica mudanças, sem executar a
organização ou declarar critérios cumpridos.

<!-- SDD:USES:["docs/padroes/CONTRATOS.md#", "docs/padroes/CONTRATOS.md#escrita-e-fontes", "docs/padroes/CONTRATOS.md#metadados-e-identificacao", "docs/padroes/CONTRATOS.md#execucao-dos-tickets-e-manutencao", "docs/padroes/CONTRATOS.md#estados-dos-escopos-do-governador", "docs/padroes/CONTRATOS.md#reconstrucao-e-referencias", ".agents/skills/sdd/SKILL.md", ".claude/skills/sdd/SKILL.md", ".agents/skills/sdd/agents/openai.yaml"] -->

<!-- SDD:ITEM:prd:START -->
<!-- SDD:USES:["docs/padroes/PRD.md", "docs/padroes/CONTRATOS.md#prd"] -->
## 1. PRD

### Objetivo
Definir o contrato do produto: problema, público, resultado esperado, escopo,
requisitos e restrições. PRD é o documento de requisitos do produto.

### Objeto de saída
docs/PRD.md, construído pelo template PRD do SDD Framework. Este é o documento
vigente de requisitos do produto; fontes de mesma função fornecem conteúdo,
não um padrão alternativo.

### Requisitos e insumos
Use a descrição do produto, informações de negócio, decisões do usuário e fontes
pertinentes. Identifique o que é conhecido e o que falta; pergunte somente
informações indispensáveis que não estejam disponíveis.

Padrões: [template PRD](docs/padroes/PRD.md),
[método PRD](docs/padroes/CONTRATOS.md#prd) e
[skill SDD](.agents/skills/sdd/SKILL.md).
Consulte uma fonte quando ela fornecer informação necessária ao PRD, não por
fazer parte de uma rotina administrativa.

### Execução
Os passos abaixo explicam como produzir o PRD. Execute apenas o necessário para
atender aos critérios ainda não cumpridos; não refaça os pontos prontos. Na
reexecução após conclusão, limite os ajustes às alterações do framework e seus
impactos diretos, conforme a regra geral.

1. Localize documentos que definem o produto ou cumprem a função de PRD. Se existirem, identifique conteúdo a aproveitar e contradições reais; se não existirem, obtenha as informações necessárias com o usuário.
2. Esclareça problema, público, objetivos, resultado esperado, escopo e exclusões. Código pertinente pode servir de evidência, sem virar requisito aceito automaticamente.
3. Para construir o PRD, use o template padrão, existam ou não documentos anteriores. Incorpore conteúdo útil, regras, justificativas, decisões, IDs e evidências válidas; não preserve o formato antigo por equivalência.
4. Confira origem e destino; substitua o documento vigente e retire concorrentes somente após preservação e autorização aplicável.
5. Confira o critério de pronto. Não invente produto, métricas, requisitos ou aprovação para completar o documento.

O procedimento é o mesmo para qualquer projeto. A existência de documentos
determina quais informações aproveitar, não se o padrão será aplicado.
Não execute a aplicação nem altere o negócio por mera organização documental.

### Critério de pronto
A tarefa está resolvida quando:
- o PRD existe no template próprio, com conteúdo real e sem campos por preencher;
- problema, público, objetivos, resultado esperado, escopo e exclusões estão claros;
- requisitos funcionais e de qualidade têm IDs estáveis e condições verificáveis;
- restrições, regras e conteúdo essencial aproveitado estão preservados;
- decisões necessárias estão aceitas, referências são válidas e não há contradição impeditiva.

Se uma condição aplicável não estiver atendida, existe uma pendência: informe
qual condição falta e a ação necessária. Se estiverem atendidas, indique a
evidência no PRD. A conclusão é determinada por esses critérios, não por uma
classificação separada de situações ou pelo simples status do documento.
<!-- SDD:ITEM:prd:END -->

<!-- SDD:ITEM:specs:START -->
<!-- SDD:USES:["docs/padroes/SPEC.md", "docs/padroes/CONTRATOS.md#spec"] -->
## 2. SPECs

**Objetivo e saída.** Especificar a entrega em specs/NNN-nome/SPEC.md, vinculada ao
PRD: comportamento, limites, RF-NNN locais e CA-NNN com condições observáveis.

**Estado.** Mantenha evidências por SPEC no controle de execução. O item não está concluído quando faltar
decisão ou design necessário; descreva o impedimento e trate o escopo correspondente.
Não declare accepted só porque o texto foi preenchido.

**Templates e skill.** Abra [SPEC](docs/padroes/SPEC.md) e use a
[skill SDD](.agents/skills/sdd/SKILL.md) no escopo SPEC.
Use o template SPEC do SDD Framework para cenários verificáveis, IDs e formato.

**Execução.** Leia o PRD e delimite a entrega, comportamento, exclusões, falhas e
aceitação. Localize especificações ou documentos de mesma função. Havendo conteúdo,
aproveite obrigações, decisões, IDs e evidências; sem conteúdo suficiente, obtenha
as informações necessárias. Construa a SPEC pelo template próprio em ambos os casos,
sem copiar o PRD ou inventar funcionalidades futuras. Defina design inline ou a
necessidade de DESIGN.md no escopo técnico. Código atual não é requisito aceito.

**Conclua quando.** Comportamento, aceitação e design aplicável estiverem coerentes
e sem pendência impeditiva. Se o design ainda depender do escopo 3, registre essa
dependência e volte para concluir a SPEC depois de resolvê-la.
<!-- SDD:ITEM:specs:END -->

<!-- SDD:ITEM:arquitetura:START -->
<!-- SDD:USES:["docs/padroes/ARCHITECTURE.md", "docs/padroes/DESIGN.md", "docs/padroes/ADR.md", "docs/padroes/CONTRATOS.md#arquitetura-e-design"] -->
## 3. Arquitetura e design

**Objetivo e saída.** Definir docs/ARCHITECTURE.md e o design da SPEC com componentes,
contratos, tecnologias, invariantes e forma de verificação proporcionais ao projeto.

**Estado.** Registre arquitetura e design separadamente quando houver trabalho
distinto. Design inline concluído dispensa DESIGN.md; justifique essa escolha,
sem criar um arquivo vazio.

**Templates e skill.** Abra [ARCHITECTURE](docs/padroes/ARCHITECTURE.md),
[DESIGN](docs/padroes/DESIGN.md) e, para decisões transversais, [ADR](docs/padroes/ADR.md).
Use a [skill SDD](.agents/skills/sdd/SKILL.md) no escopo técnico.
Os templates técnicos do SDD Framework definem os padrões deste escopo.

**Execução.** Leia PRD/SPEC e localize documentos técnicos, restrições e decisões.
Aproveite invariantes, justificativas e soluções existentes, quando houver; obtenha
as informações faltantes e construa os documentos pelo padrão próprio. Não escolha
stack por rotina. Identifique se há interface; quando houver, registre Design System
existente e sua versão, sem criá-lo implicitamente. Apresente contradições reais ao
usuário e relacione requisitos à solução, sem inventar migração ou compatibilidade.

**Conclua quando.** Houver orientação técnica suficiente e design coerente com a
SPEC, decisões impeditivas resolvidas e verificação planejada. Atualize o estado da SPEC.
<!-- SDD:ITEM:arquitetura:END -->

<!-- SDD:ITEM:tasks:START -->
<!-- SDD:USES:["docs/padroes/TASK.md", "docs/padroes/CONTRATOS.md#tasks-e-roadmap"] -->
## 4. Tasks

**Objetivo e saída.** Preparar tickets executáveis em specs/NNN-nome/tasks/T-NNN.md,
cobrindo as obrigações da SPEC. Cada ticket define objetivo, escopo, dependências,
executor, autorização, aceitação, verificação e resultado.

**Estado.** Mantenha Tasks como concluído quando os tickets estiverem preparados
e coerentes. Isso não significa que a implementação desses tickets terminou.
O estado de cada tarefa permanece no próprio ticket.

**Templates e skill.** Abra [TASK](docs/padroes/TASK.md) e use a
[skill SDD](.agents/skills/sdd/SKILL.md) no escopo Tasks.
Use o template TASK do SDD Framework para ações concretas e verificáveis.

**Execução.** Leia SPEC/design e localize tarefas já existentes. Decomponha as
obrigações em ações concretas com caminhos, dependências e evidência prevista.
Construa os tickets no padrão, aproveitando IDs, estados, aceites e evidências
válidos quando existirem. Crie obrigações novas somente onde faltar cobertura;
não reabra trabalho concluído para reformatar. Preparar tickets não autoriza
implementar o produto.

**Conclua quando.** A SPEC estiver coberta, os tickets forem claros e houver
tarefas prontas identificadas. Produto pode continuar com tickets pendentes.
<!-- SDD:ITEM:tasks:END -->

<!-- SDD:ITEM:roadmap:START -->
<!-- SDD:USES:["docs/padroes/ROADMAP.md", "docs/padroes/CONTRATOS.md#tasks-e-roadmap"] -->
## 5. ROADMAP

**Objetivo e saída.** Consolidar entregas, prioridades, dependências e acompanhamento
em docs/ROADMAP.md, com links para SPECs e tickets reais.

**Estado.** Registre o estado do ROADMAP no controle de execução; estados das tarefas continuam
nos tickets. Não exija TASKS.md, STATUS.md ou memória paralela como outro controle.

**Templates e skill.** Abra [ROADMAP](docs/padroes/ROADMAP.md) e use a
[skill SDD](.agents/skills/sdd/SKILL.md) no escopo de acompanhamento.
Use os requisitos e as unidades verificáveis da SPEC como referências de organização.
O template ROADMAP do SDD Framework define a organização deste documento.

**Execução.** Localize arquivos de prioridades/entregas e leia SPECs/tickets.
Construa o ROADMAP pelo template, aproveitando prioridades, dependências e
adiamentos reais quando existirem. Sem informação anterior, defina a primeira
entrega com o usuário. Migre conteúdo útil e retire concorrentes no escopo
autorizado. Não invente planejamento distante ou uma fila rígida entre trabalhos
independentes, nem mantenha processo divergente por costume.

**Conclua quando.** Entregas, prioridades e dependências estiverem compreensíveis,
os links forem válidos e ações humanas necessárias estiverem visíveis.
<!-- SDD:ITEM:roadmap:END -->

<!-- SDD:ITEM:agents:START -->
<!-- SDD:USES:["docs/padroes/AGENTS.md", "docs/padroes/README.md", "docs/padroes/CONTRATOS.md#agents-e-readme"] -->
## 6. AGENTS e README

**Objetivo e saída.** Manter AGENTS.md como instrução local do agente e README.md
como explicação do produto e de seu uso. CLAUDE.md referencia AGENTS e o acionamento
explícito; não mantém outro procedimento.

**Estado.** Registre AGENTS e README separadamente quando necessário; concluído
exige instruções coerentes e comandos reais, não apenas seções presentes.

**Templates e skill.** Abra [AGENTS](docs/padroes/AGENTS.md),
[README](docs/padroes/README.md) e use a
[skill SDD](.agents/skills/sdd/SKILL.md) no escopo de instruções.
Use os templates e a skill SDD instalados; mantenha as regras locais de
acionamento explícito e os comandos próprios do projeto.

**Execução.** Localize instruções e explicações de uso existentes, quando houver,
e os comandos reais do projeto. Construa a parte própria de AGENTS/README pelos
templates, incorporando contexto, comandos, pré-requisitos, decisões e restrições
compatíveis. Preserve blocos administrados. Processo divergente só continua por
decisão específica em ADR aceita; atualize referências depois de
retirar documentos concorrentes.

**Conclua quando.** O agente puder executar tarefas locais pelas instruções do
projeto e o usuário puder entender como usar o produto, sem depender do framework.
<!-- SDD:ITEM:agents:END -->

<!-- SDD:ITEM:encerramento:START -->
<!-- SDD:USES:["docs/padroes/CHECKPOINT.md", "docs/padroes/ADR.md", "docs/padroes/INBOX.md", "docs/padroes/VALIDATION.md", "docs/padroes/CONTRATOS.md#encerramento"] -->
## 7. Encerramento e continuidade

**Objetivo e saída.** Encerrar o escopo documental solicitado, registrar evidências
no controle de execução e produzir CHECKPOINT.md para execução independente do projeto.

**Estado.** Registre concluído somente com critérios cumpridos e sem decisão
obrigatória pendente. Um pedido restrito a um artefato conclui esse escopo; não
declare organização integral se outros documentos necessários ainda faltarem.

**Templates e skill.** Abra [CHECKPOINT](docs/padroes/CHECKPOINT.md). Use
[ADR](docs/padroes/ADR.md), [INBOX](docs/padroes/INBOX.md) e
[VALIDATION](docs/padroes/VALIDATION.md) somente para decisões, propostas e evidências
reais. Use a [skill SDD](.agents/skills/sdd/SKILL.md) no escopo de encerramento.
Siga o método de encerramento dos contratos do SDD Framework para evidências
proporcionais e passagem de contexto.

**Execução.** Confira os objetos produzidos, conteúdo aproveitado, critérios,
contradições decididas, referências e remoções autorizadas. Havendo execução
anterior, preserve resultados e evidências válidos. Produza o CHECKPOINT de passagem;
justifique documentos condicionais não aplicáveis, sem inventar ADRs, propostas,
relatórios ou design separado. Presença de arquivo ou instalação bem-sucedida não
prova qualidade documental.

**Conclua quando.** O conjunto solicitado estiver coerente e verificável, as pendências
obrigatórias resolvidas e a próxima ação clara. Não exija produto implementado para
encerrar organização. Depois, execute tarefas locais e mantenha documentos afetados
sem reiniciar o governador; nova organização exige novo acionamento explícito.
<!-- SDD:ITEM:encerramento:END -->

<!-- SDD:GOVERNADOR:END -->
