<!-- SDD:GOVERNADOR:START -->
# Governador SDD

Versão do procedimento: 0.4.2. Instruções para a IA que trabalha no projeto,
escritas para leitura, revisão e contestação humanas. Este procedimento fica em
docs/governador.md. Caminhos textuais e referências SDD:USES partem da raiz do
projeto; links Markdown são relativos a este arquivo.

Execute somente por acionamento explícito do usuário ou da skill SDD. Instalação,
update, leitura do arquivo e abertura de sessão não são acionamento. O controle
de execução fica em .sdd/execucao.json; os destinos das decisões, ações e resultados
estão em [Estados dos escopos do governador](padroes/CONTRATOS.md#estados-dos-escopos-do-governador).
Não acrescente seção de aplicação neste arquivo.
Use os [contratos](padroes/CONTRATOS.md) em todos os escopos. Os templates,
contratos e a skill do SDD Framework são as únicas referências de padrão e método
para esta execução; não consulte templates ou skills de outros frameworks.

### Obrigatoriedade dos itens
No fluxo completo, PRD, SPECs, Arquitetura, Tasks, ROADMAP, AGENTS/README e
Encerramento são obrigatórios. Design é o único item opcional e é recomendado;
sua ausência não impede concluir os itens obrigatórios. ADR, INBOX e VALIDATION
são registros auxiliares produzidos quando houver conteúdo que os justifique,
não outros itens opcionais do fluxo. Um pedido restrito continua limitado ao
escopo autorizado. Acionar o governador sem restringir itens autoriza o fluxo
completo, na ordem numerada abaixo. Conclua o item atual antes de avançar e,
comprovado seu critério de pronto, prossiga automaticamente ao próximo item
abrangido pelo pedido, sem pedir autorização de continuação ou encerrar após uma
entrega parcial. Para Design não adotado, siga a orientação do item 4. Consultar
insumos de outro item não significa executá-lo antecipadamente.

### Execução e reexecução
O critério de pronto de cada item determina o que falta e quando concluir.
Todos os critérios incluem a especificidade do conteúdo: os objetos produzidos
devem identificar ação ou regra, referências e forma de verificação pertinentes
à sua função, com parâmetros reais do projeto, sem marcadores de preenchimento
ou recomendações vagas. Informação indispensável ausente é pendência; não invente
comandos, caminhos, metas, requisitos ou aprovação para completar o padrão.
Aplique estas regras a todos os itens:

1. **Conferir o conteúdo.** Verifique cada exigência do critério de pronto no conteúdo real dos objetos de saída, incluindo todos os componentes da exigência. Quando ela abranger vários requisitos, decisões, referências ou objetos, confira todos; uma amostra não comprova o conjunto.
2. **Executar somente o necessário.** Resolva as exigências do critério de pronto não atendidas e preserve o conteúdo que já satisfaz o critério. Use a Execução de cada item para produzir o que falta, sem reconstruir partes prontas por rotina ou por ausência de registro anterior.
3. **Registrar evidências.** Para cada exigência do critério de pronto atendida, registre em evidence de .sdd/execucao.json a exigência, o caminho do objeto e a seção ou os IDs cujo conteúdo comprova seu cumprimento. A evidência é esse conteúdo, não uma declaração de conclusão. Não acrescente relatórios de aplicação do governador aos objetos produzidos; preserve as seções de verificação e evidências próprias dos templates.
4. **Resolver pendências e justificar dispensas.** Se faltar conteúdo, houver contradição impeditiva ou não for possível verificar uma exigência, registre em remaining do item em .sdd/execucao.json a exigência, a lacuna concreta e a ação necessária. Resolva o que estiver ao seu alcance; se depender de informação ou decisão indispensável do usuário, procure primeiro nas fontes do projeto e, se ausente, faça a pergunta específica, explicando o critério impedido e propondo alternativas fundamentadas quando possível. Aguarde a resposta sem avançar ao próximo item; incorpore a resposta no objeto de saída do item (ou em docs/decisions/ADR-NNN.md para decisão transversal) e retome o critério pendente. Não deixe a pergunta para quando o usuário cobrar a conclusão, não presuma aceite e não invente respostas. Só considere uma exigência não aplicável quando ela for explicitamente condicional e sua hipótese não ocorrer; registre em evidence do mesmo item a justificativa verificável. Falta de informação ou decisão não dispensa exigência obrigatória.
5. **Determinar a conclusão.** O item está concluído somente quando todas as exigências aplicáveis do critério de pronto estiverem comprovadas e não houver pendência. Qualquer exigência não atendida ou não verificada impede conclusão e avanço. Não há estados intermediários; existência do arquivo, status editorial (inclusive draft ou accepted), versão, hash ou declaração não substituem a conferência. A skill explica como registrar completed e applied em .sdd/execucao.json. Se houver impedimento que exija interromper, informe o item e a ação necessária e registre o ponto de retomada em CHECKPOINT.md; essa passagem não conclui o item 8 nem exige novo acionamento para retomar o mesmo pedido autorizado.
6. **Limitar a reexecução.** Após conclusão, no próximo acionamento explícito, consulte .sdd/execucao.json e trate somente alterações do framework e seus impactos diretos nas exigências afetadas do critério de pronto. Preserve conteúdo e evidências válidas das exigências não afetadas; sem alteração pertinente, preserve o objeto. O update identifica mudanças, sem executar o governador ou declarar critérios cumpridos.

<!-- SDD:USES:["docs/padroes/CONTRATOS.md#", "docs/padroes/CONTRATOS.md#escrita-e-fontes", "docs/padroes/CONTRATOS.md#metadados-e-identificacao", "docs/padroes/CONTRATOS.md#execucao-dos-tickets-e-manutencao", "docs/padroes/CONTRATOS.md#estados-dos-escopos-do-governador", "docs/padroes/CONTRATOS.md#reconstrucao-e-referencias", "docs/padroes/CONTRATOS.md#git-e-permissoes", ".codex/rules/sdd-git.rules", ".agents/skills/sdd/SKILL.md", ".claude/skills/sdd/SKILL.md", ".agents/skills/sdd/agents/openai.yaml"] -->

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

Padrões: [template PRD](padroes/PRD.md),
[método PRD](padroes/CONTRATOS.md#prd) e
[skill SDD](../.agents/skills/sdd/SKILL.md).
Consulte uma fonte quando ela fornecer informação necessária ao PRD, não por
fazer parte de uma rotina administrativa.

### Execução
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

<!-- SDD:ITEM:prd:END -->

<!-- SDD:ITEM:specs:START -->
<!-- SDD:USES:["docs/padroes/SPEC.md", "docs/padroes/CONTRATOS.md#spec"] -->
## 2. SPECs

### Objetivo
Especificar cada entrega do escopo solicitado: comportamento, limites e aceitação,
com vínculo aos requisitos do produto e critérios verificáveis para orientar o trabalho.

### Objeto de saída
specs/NNN-nome/SPEC.md para cada entrega, pelo template SPEC do SDD Framework.
O Design opcional do item 4 pode ficar na própria SPEC ou em DESIGN.md; sua
ausência não impede concluir a especificação.

### Requisitos e insumos
Use docs/PRD.md, decisões aceitas e fontes que esclareçam o comportamento da
entrega. Consulte especificações existentes, restrições e evidências pertinentes;
código atual informa a análise, mas não constitui requisito aceito automaticamente.
Consulte os contratos da arquitetura obrigatória do item 3 quando necessários
para esclarecer restrições da entrega, sem inventar decisão de produto.

Padrões: [template SPEC](padroes/SPEC.md),
[método SPEC](padroes/CONTRATOS.md#spec) e
[skill SDD](../.agents/skills/sdd/SKILL.md).

### Execução
1. Localize fontes e especificações da entrega; aproveite comportamento válido, obrigações, decisões, IDs e evidências. Obtenha informações indispensáveis que faltarem.
2. Delimite objetivo, escopo e exclusões a partir do PRD. Defina requisitos locais RF-NNN/RNF-NNN pertinentes, indicando os vínculos com os requisitos do produto, sem copiar o PRD inteiro ou inventar funcionalidades futuras.
3. Escreva critérios CA-NNN que cubram os requisitos locais, com contexto, ação e resultado observável, incluindo falhas e limites relevantes.
4. Construa a SPEC pelo template próprio. Indique design: none quando o Design não for adotado; se adotado no item 4, use design: inline ou design: separate com link para DESIGN.md, sem exigir sua produção para concluir o contrato de comportamento.
5. Confira referências e coerência entre comportamento e aceitação; preserve conteúdo essencial antes de substituir documentos concorrentes no escopo autorizado.

### Critério de pronto
A tarefa está resolvida quando:
- cada entrega do escopo possui SPEC no template próprio, sem campos por preencher;
- objetivo, comportamento, limites e exclusões são claros e coerentes com o PRD;
- requisitos locais têm IDs estáveis, vínculos com o produto e cobertura por critérios CA-NNN verificáveis, incluindo falhas e limites pertinentes;
- o metadado design indica none, inline ou separate conforme a adoção do Design; referências a conteúdo já produzido são válidas, sem exigir solução técnica para concluir a SPEC;
- conteúdo essencial, decisões e evidências estão preservados, referências são válidas e não há decisão ou contradição impeditiva.
<!-- SDD:ITEM:specs:END -->

<!-- SDD:ITEM:arquitetura:START -->
<!-- SDD:USES:["docs/padroes/ARCHITECTURE.md", "docs/padroes/ADR.md", "docs/padroes/CONTRATOS.md#arquitetura"] -->
## 3. Arquitetura

### Objetivo
Definir a orientação técnica obrigatória do projeto: componentes, contratos,
tecnologias, restrições e verificação, com detalhe proporcional aos requisitos.

### Objeto de saída
docs/ARCHITECTURE.md, pelo template ARCHITECTURE do SDD Framework. Decisões
transversais reais que precisarem de registro ficam em docs/decisions/ADR-NNN.md
pelo template ADR; não crie ADR apenas para preencher o mapa.

### Requisitos e insumos
Use PRD, comportamento e aceitação das SPECs, restrições operacionais,
configurações existentes e decisões aceitas. Consulte código, dados e interfaces
quando necessários para fundamentar os contratos técnicos. Se houver interface
visual, use as referências e a versão do Design System existente; não crie um
implicitamente. A arquitetura não depende da adoção do Design do item 4.

Padrões: [ARCHITECTURE](padroes/ARCHITECTURE.md),
[ADR](padroes/ADR.md),
[método Arquitetura](padroes/CONTRATOS.md#arquitetura) e
[skill SDD](../.agents/skills/sdd/SKILL.md).

### Execução
1. Localize fontes técnicas e aproveite soluções, contratos, invariantes, configurações e justificativas válidas. Obtenha restrições faltantes; não escolha stack por rotina nem trate implementação atual como decisão aceita automaticamente.
2. Construa a arquitetura pelo template próprio: contexto, tecnologias justificadas, responsabilidades, dados, integrações, interfaces, restrições e segurança, ligados ao PRD e às SPECs.
3. Explicite decisões, alternativas e riscos pertinentes aos contratos do projeto. Registre em ADR decisões transversais reais e sua aceitação; apresente contradições que exigirem decisão do usuário. Se houver migração arquitetural, defina preservação, compatibilidade e recuperação.
4. Defina como verificar os contratos, com comandos ou procedimentos reais, pré-requisitos e ambientes necessários. Confira os vínculos com PRD, SPECs e ADRs, preservando conhecimento e configurações particulares.

### Critério de pronto
A tarefa está resolvida quando:
- a arquitetura segue o template próprio, sem campos por preencher, e define contexto, componentes, contratos, tecnologias justificadas, restrições e segurança com conteúdo real;
- os contratos são coerentes com PRD e SPECs, e decisões arquiteturais necessárias estão aceitas, com riscos e alternativas pertinentes tratados;
- se houver interface visual, a referência ao Design System existente e sua versão estão explícitas, ou sua ausência está tratada como decisão necessária, sem criação implícita;
- se houver migração arquitetural, preservação, compatibilidade e recuperação em falha estão definidas;
- a verificação planejada tem procedimentos e pré-requisitos claros, sem confundir planejamento com testes já executados;
- conteúdo essencial e configurações particulares estão preservados, referências são válidas e não há contradição ou decisão arquitetural impeditiva. Design opcional ausente não impede concluir a arquitetura.
<!-- SDD:ITEM:arquitetura:END -->

<!-- SDD:ITEM:design:START -->
<!-- SDD:USES:["docs/padroes/DESIGN.md", "docs/padroes/SPEC.md", "docs/padroes/CONTRATOS.md#design"] -->
## 4. Design

### Objetivo
Detalhar a solução técnica de uma entrega para facilitar implementação e
verificação. Este é o único item opcional do fluxo e é recomendado; não substitui
a arquitetura obrigatória nem se torna obrigatório por complexidade ou por rotina.

### Objeto de saída
Quando adotado, design técnico inline na SPEC ou em specs/NNN-nome/DESIGN.md pelo
template DESIGN do SDD Framework. Se não adotado, não há documento de Design a
produzir; a SPEC indica design: none, sem solução fictícia ou arquivo vazio.

### Requisitos e insumos
Use a SPEC, a arquitetura, decisões aceitas e fontes técnicas pertinentes.
A opção de adotar ou não o Design e seu local devem refletir a orientação do
usuário e o conteúdo aproveitado. Preserve design existente válido; não o descarte
por ser opcional. Ausência de Design não dispensa requisitos, arquitetura ou a
definição suficiente das tarefas obrigatórias.

Padrões: [template DESIGN](padroes/DESIGN.md),
[template SPEC](padroes/SPEC.md),
[método Design](padroes/CONTRATOS.md#design) e
[skill SDD](../.agents/skills/sdd/SKILL.md).

### Execução
1. Localize solução técnica existente e a orientação do usuário. Recomende o Design, aproveite conteúdo válido e identifique sua adoção por entrega, sem condicionar a continuidade do fluxo à sua produção.
2. Se não adotado, indique design: none na SPEC e siga os itens obrigatórios, preservando conteúdo e decisões existentes. Não transforme a ausência em pendência nem declare um Design inexistente como concluído.
3. Se adotado, descreva contexto, solução e contratos, decisões e alternativas, riscos e verificação pelo template DESIGN, inline na SPEC com design: inline ou em DESIGN.md com design: separate e link na SPEC. Justifique o local escolhido.
4. Relacione a solução aos requisitos e critérios de aceitação da SPEC e aos contratos da arquitetura. Inclua migração, compatibilidade e recuperação quando a solução as exigir; referencie decisões transversais reais sem duplicar ADRs.
5. Confira referências, riscos e viabilidade da verificação planejada. Encaminhe às Tasks as obrigações do Design adotado, sem inventar aprovação, execução ou resultado.

### Critério de pronto
Quando o Design for adotado, a tarefa está resolvida quando:
- a solução segue o template DESIGN, inline ou em documento separado, com conteúdo real e sem campos por preencher;
- o metadado design e o link da SPEC correspondem ao local real da solução;
- requisitos e aceitação da SPEC estão relacionados à solução, coerente com a arquitetura;
- decisões necessárias estão aceitas, alternativas e riscos pertinentes estão tratados e referências são válidas;
- se houver migração, preservação, compatibilidade e recuperação em falha estão definidas;
- a verificação planejada é clara, o conteúdo essencial está preservado e não há contradição ou decisão impeditiva na solução adotada.
<!-- SDD:ITEM:design:END -->

<!-- SDD:ITEM:tasks:START -->
<!-- SDD:USES:["docs/padroes/TASK.md", "docs/padroes/CONTRATOS.md#tasks", "docs/padroes/CONTRATOS.md#testes-automatizados"] -->
## 5. Tasks

### Objetivo
Preparar tarefas executáveis que cubram as obrigações das SPECs e do Design quando adotado,
com limites, dependências, responsabilidades e verificação definidos.

### Objeto de saída
specs/NNN-nome/tasks/T-NNN.md, pelo template TASK do SDD Framework.
A ausência de Design não bloqueia sua preparação. Os tickets são a fonte de
estado, autorização e evidências de cada tarefa;
prepará-los não significa implementar o produto nem concluir seu trabalho.

### Requisitos e insumos
Use requisitos e critérios de aceitação das SPECs, Design quando adotado, decisões
aceitas, regras permanentes de AGENTS e restrições de execução. Se essas regras
ainda precisarem de definição, coordene o conteúdo com o item 7 e os arquivos de
configuração, sem inventar comandos para preparar o ticket. Aproveite tarefas, resultados e evidências
existentes. Dependências devem representar impedimentos reais, sem impor uma
sequência entre trabalhos independentes. Não prepare como executável uma tarefa
cuja definição dependa de decisão ainda não tomada.

Padrões: [template TASK](padroes/TASK.md),
[método Tasks](padroes/CONTRATOS.md#tasks) e
[skill SDD](../.agents/skills/sdd/SKILL.md).

### Execução
1. Localize tickets e planos de trabalho; identifique quais obrigações da SPEC e do Design adotado já estão cobertas e onde falta cobertura, preservando IDs, estados, autorizações, resultados e evidências válidos.
2. Decomponha as obrigações sem cobertura em ações limitadas. Identifique requisitos e critérios de aceitação cobertos por cada ticket e documentos afetados, sem inventar novo escopo de produto.
3. Construa os tickets pelo template próprio, com objetivo, escopo, critérios de aceitação, executor, responsabilidades e ações humanas necessárias. Para cada exigência de aceitação, defina cenário, teste ou revisão, comando/procedimento, diretório, pré-requisitos, resultado esperado e evidência prevista; aplique a política Testes automatizados dos contratos para identificar cobertura existente, testes a criar/ajustar ou alternativa justificada. Referencie as regras permanentes de AGENTS, sem copiá-las, e planeje os alvos temporários, recursos a encerrar e itens a preservar.
4. Defina dependencies por referências reais, sem ciclos, e priority como inteiro positivo (padrão 100, menor primeiro), preservando decisões existentes. Registre autorização e estado conforme as evidências disponíveis; prioridade pode antecipar task criada depois, mas não ignora dependências ou impedimentos. Identifique tarefas que podem começar e o que impede as demais; não fabrique aprovação nem reabra trabalho concluído por mudança de formato.
5. Confira a cobertura das obrigações e os vínculos com SPEC/design, incluindo verificações necessárias. Encaminhe o resumo ao ROADMAP do item 6. Preparar tickets não autoriza executar a implementação.

### Critério de pronto
A tarefa está resolvida quando:
- os tickets seguem o template próprio, sem campos por preencher, com IDs estáveis e referências válidas;
- todas as obrigações das SPECs e do Design adotado no escopo têm cobertura identificável nos tickets;
- cada ticket define ação limitada, escopo, requisitos e aceitação cobertos, responsabilidades e plano de verificação executável com cenário, comando/procedimento, diretório, pré-requisitos, resultado esperado e evidência;
- a escolha de automação ou alternativa tem justificativa concreta conforme Testes automatizados dos contratos, com cobertura existente ou testes necessários identificados; verificações durante a execução e antes da conclusão estão definidas, e limpeza/encerramento de recursos próprios têm alvos e método delimitados, com itens a preservar ou ausência de temporários declarados;
- priority é inteiro positivo com padrão 100 quando não houver prioridade definida, dependencies é real e sem ciclos, autorizações/estados refletem fatos e tarefas que podem começar ou seus impedimentos estão identificados;
- resultados e evidências anteriores estão preservados e nenhuma implementação foi declarada concluída apenas pela preparação do ticket;
- ações humanas necessárias estão explícitas e não há lacuna impeditiva na definição dos tickets. Tickets de implementação podem continuar pendentes.
<!-- SDD:ITEM:tasks:END -->

<!-- SDD:ITEM:roadmap:START -->
<!-- SDD:USES:["docs/padroes/ROADMAP.md", "docs/padroes/CONTRATOS.md#roadmap"] -->
## 6. ROADMAP

### Objetivo
Organizar objetivamente a execução das tasks, mostrando ordem por prioridade,
dependências, impedimentos e estado em tabelas vinculadas aos tickets reais.

### Objeto de saída
docs/ROADMAP.md pelo template ROADMAP do SDD Framework: fila de execução, tasks
encerradas e ações humanas. Priority e dependencies pertencem aos metadados dos
tickets; o ROADMAP apresenta posições derivadas dessa prioridade e as dependências,
sem manter outra fonte de planejamento ou um JSON paralelo. .sdd/execucao.json continua exclusivo do controle do framework.

### Requisitos e insumos
Use os tickets do escopo, suas SPECs e decisões reais de prioridade/adiamento.
Priority é inteiro positivo, padrão 100: menor número vem primeiro, mesmo para
task criada depois. Dependências e autorização continuam obrigatórias para executar.
Aproveite prioridades existentes e obtenha decisão indispensável que faltar, sem
inventar backlog, alterar IDs ou converter preferência de ordem em dependência.

Padrões: [template ROADMAP](padroes/ROADMAP.md),
[método ROADMAP](padroes/CONTRATOS.md#roadmap) e
[skill SDD](../.agents/skills/sdd/SKILL.md).

### Execução
1. Localize tickets e fontes de planejamento; preserve prioridades, dependências e adiamentos aceitos. Registre a prioridade e as dependências reais em priority/dependencies dos tickets, preservando vínculos e decisões existentes.
2. Construa a fila com as colunas do template e aplique ordenação, posições consecutivas em Ordem e tradução de estado/verificação pelo método ROADMAP dos contratos. Confira os valores nos tickets; bloqueios e ações humanas ficam visíveis, sem serem ignorados pela posição.
3. Separe as tarefas concluídas/canceladas da fila ativa, usando a tabela reduzida do template. Não reabra tarefas encerradas nem interrompa trabalho ativo por rotina para adequar a apresentação.
4. Preserve histórico detalhado e justificativas em specs/NNN-nome/tasks/T-NNN.md ou docs/decisions/ADR-NNN.md, conforme sua função definida nos contratos, com origem e referências, antes de retirar narrativas do ROADMAP. Não mantenha seção paralela de Prioridades e dependências ou diário de versões na fila.
5. Relacione ações humanas ao ticket e ao trabalho impedido; adiamentos sem task apontam sua fonte governada. Confira a tabela contra os tickets, sem fabricar avanço, prioridade especial ou autorização.

### Critério de pronto
A tarefa está resolvida quando:
- o ROADMAP segue o template com fila, tasks encerradas e ações humanas, sem campos por preencher ou histórico narrativo de execução;
- cada tarefa do escopo está representada uma única vez com link válido, trabalho, estado e verificação fiéis ao ticket, traduzidos pelo método ROADMAP;
- a fila tem posições consecutivas derivadas de priority/caminho e dependências e impedimentos explícitos, sem confundir posição com autorização para executar; as colunas das duas tabelas correspondem ao template;
- prioridades existentes, IDs, dependências e adiamentos estão preservados em suas fontes, sem JSON paralelo ou dependência técnica inventada para impor ordem;
- ações humanas indicam fonte, ação concreta e dependentes, ou sua ausência é declarada;
- o conteúdo retirado tem destino identificável nos tickets ou ADRs indicados na Execução, e não há contradição impeditiva com tickets ou SPECs.
<!-- SDD:ITEM:roadmap:END -->

<!-- SDD:ITEM:agents:START -->
<!-- SDD:USES:["docs/padroes/AGENTS.md", "docs/padroes/README.md", "docs/padroes/CONTRATOS.md#agents-e-readme", "docs/padroes/CONTRATOS.md#testes-automatizados", "docs/padroes/CONTRATOS.md#git-e-permissoes"] -->
## 7. AGENTS e README

### Objetivo
Dar ao agente instruções locais suficientes para trabalhar no projeto e ao usuário
informações reais para entender o produto e começar a usá-lo.

### Objeto de saída
AGENTS.md e README.md, pelos templates AGENTS e README do SDD Framework.
CLAUDE.md encaminha às instruções de AGENTS.md e ao acionamento explícito do
governador; não constitui um segundo procedimento. Preserve os blocos e as
configurações administrados pela CLI.

### Requisitos e insumos
Use PRD, arquitetura, convenções, restrições e decisões vigentes. Consulte arquivos
e configurações que definem os comandos reais, seus diretórios e pré-requisitos,
além de instruções e explicações de uso existentes. Aproveite configuração
particular; não copie instruções preenchidas do repositório do framework.

Padrões: [template AGENTS](padroes/AGENTS.md),
[template README](padroes/README.md),
[método AGENTS e README](padroes/CONTRATOS.md#agents-e-readme) e
[skill SDD](../.agents/skills/sdd/SKILL.md).

### Execução
1. Localize instruções e explicações de uso; identifique contexto, comandos, pré-requisitos, convenções e restrições válidos, bem como contradições que exijam decisão.
2. Construa AGENTS pelo template com contexto/escopo, comandos/verificações, higiene do workspace, qualidade/convenções, proteção/autorização e documentação/entrega. Derive dos arquivos reais os comandos, diretórios, pré-requisitos, momentos de execução e resultados esperados; defina alvos temporários permitidos, identificação e encerramento de recursos próprios e itens a preservar. Incorpore a política Testes automatizados dos contratos por referência em Comandos e verificações de AGENTS.md, com os comandos/gatilhos locais, instruções particulares compatíveis e referências ao Design System quando aplicável; substitua slogans por regras executáveis do projeto.
3. Construa o README pelo template: objetivo, público, pré-requisitos e comandos reais para começar. Distinga capacidades disponíveis de entregas futuras e explicite limites conhecidos de uso ou verificação, sem afirmar execução que não ocorreu.
4. Preserve os blocos administrados de AGENTS/CLAUDE e a configuração existente. Confira o encaminhamento de Git e permissões no bloco administrado de AGENTS.md, sem repeti-lo na seção própria ou duplicar a matriz de .codex/rules/sdd-git.rules; não presuma que a regra nativa do Codex se aplica a outras integrações. Ajuste o encaminhamento próprio de CLAUDE quando necessário, sem duplicar as instruções de AGENTS ou executar init/update como acionamento do governador.
5. Confira referências e coerência com os arquivos do projeto. Preserve conhecimento antes de substituir documentos concorrentes autorizados; mantenha processo divergente somente com decisão específica em ADR aceita.

### Critério de pronto
A tarefa está resolvida quando:
- AGENTS e README seguem seus templates, com conteúdo próprio real e sem campos por preencher;
- AGENTS cobre contexto/escopo, comandos/verificações, higiene do workspace, qualidade/convenções, proteção/autorização e documentação/entrega, com referências e parâmetros locais suficientes para executar tarefas;
- suas verificações têm comandos/procedimentos, diretórios, pré-requisitos, gatilhos e resultados esperados, distinguindo execução e conclusão; a limpeza delimita descartáveis e recursos próprios, preservando testes permanentes, fixtures úteis, evidências e trabalho anterior;
- AGENTS orienta selecionar a próxima task autorizada e sem impedimentos pela menor priority e desempate pelo caminho completo, respeitando dependencies;
- as regras permanentes de AGENTS orientam os planos específicos dos tickets, sem duplicação integral nem autorização automática de implementação, dependências, commit/push ou publicação;
- README explica propósito, público e como começar com os recursos efetivamente disponíveis, indicando limites pertinentes;
- comandos correspondem às configurações do projeto e verificações não executadas não são declaradas aprovadas;
- blocos administrados, configuração particular e conhecimento válido estão preservados, e CLAUDE encaminha às instruções locais sem outro procedimento;
- o acionamento do governador permanece explícito, tarefas comuns podem prosseguir independentemente do framework e não há referências inválidas ou contradições impeditivas.
<!-- SDD:ITEM:agents:END -->

<!-- SDD:ITEM:encerramento:START -->
<!-- SDD:USES:["docs/padroes/CHECKPOINT.md", "docs/padroes/ADR.md", "docs/padroes/INBOX.md", "docs/padroes/VALIDATION.md", "docs/padroes/CONTRATOS.md#encerramento"] -->
## 8. Encerramento e continuidade

### Objetivo
Concluir o escopo documental solicitado e deixar uma passagem fiel ao estado real,
com próxima ação clara para a execução independente do projeto.

### Objeto de saída
CHECKPOINT.md pelo template CHECKPOINT do SDD Framework, com referências aos
objetos entregues e aos tickets em specs/NNN-nome/tasks/T-NNN.md. Decisões transversais ficam em
docs/decisions/ADR-NNN.md; propostas ainda não aceitas em docs/inbox/ITEM-NNN.md;
evidências extensas, quando necessárias, em specs/NNN-nome/validation/ pelo template
VALIDATION. Não crie esses documentos condicionais sem conteúdo que os justifique.

### Requisitos e insumos
Use o pedido autorizado, objetos dos itens abrangidos, tickets, decisões,
pendências e evidências reais. Confronte os registros com arquivos e Git quando
houver repositório; aproveite verificações válidas e seus limites. Um pedido
restrito a um artefato não exige organizar os demais nem permite declarar que
a organização integral está concluída.

Padrões: [CHECKPOINT](padroes/CHECKPOINT.md),
[ADR](padroes/ADR.md), [INBOX](padroes/INBOX.md),
[VALIDATION](padroes/VALIDATION.md),
[método de encerramento](padroes/CONTRATOS.md#encerramento) e
[skill SDD](../.agents/skills/sdd/SKILL.md).

### Execução
1. Delimite o conjunto solicitado e confronte os objetos entregues com seus vínculos, conteúdo aproveitado, decisões e remoções autorizadas. Identifique o que pertence ao pedido e o que continua fora dele.
2. Atualize tickets com ações e resultados reais e reflita seu resumo no ROADMAP. Relacione decisões às ADRs existentes; se houver proposta ainda não aceita ou evidência extensa que precise de arquivo próprio, use o template correspondente, sem transformar sugestão em requisito.
3. Construa o CHECKPOINT pelo template: objetivo e tarefa atual, estado real do trabalho, verificações e limites, decisões, pendências, próxima ação e leitura indispensável. Inclua alterações não commitadas e adiamentos pertinentes; não dependa de arquivos temporários como única fonte de continuidade.
4. Confira os vínculos entre CHECKPOINT, tickets, ROADMAP, decisões e evidências, sem copiar o histórico para o governador nem repetir suítes apenas para encerrar.
5. Entregue a passagem com o escopo efetivamente concluído e a próxima ação. A organização documental não exige produto implementado; o projeto volta à execução local e nova organização exige acionamento explícito.

### Critério de pronto
A tarefa está resolvida quando:
- os objetos obrigatórios do escopo solicitado atendem aos critérios próprios, independentemente da adoção de Design, com referências válidas e sem contradição ou decisão impeditiva;
- ações e resultados estão nos tickets, decisões transversais nas ADRs e propostas na INBOX, nos caminhos definidos em Objeto de saída e na Execução, sem relatório de aplicação no governador;
- o CHECKPOINT segue o template, sem campos por preencher, e corresponde ao estado real, incluindo verificações, limites e alterações não commitadas;
- pendências de implementação, ações humanas e adiamentos fora do escopo documental concluído estão visíveis, sem serem declarados resolvidos;
- se forem necessários ADR, INBOX ou relatório de validação, esses documentos seguem seus templates, preservam origem e evidências e estão referenciados;
- a próxima ação, suas dependências e a leitura indispensável estão claras, permitindo executar o projeto sem reiniciar a organização por rotina.
<!-- SDD:ITEM:encerramento:END -->

<!-- SDD:GOVERNADOR:END -->
