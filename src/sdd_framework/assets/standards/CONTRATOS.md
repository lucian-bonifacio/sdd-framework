# Padrões documentais SDD

Consulte o template do documento antes de escrevê-lo. Os templates definem as
seções obrigatórias e os campos; o governador define a execução. Remova todos os
marcadores de preenchimento na versão final e não invente informação para completá-la.

## Escrita e fontes

Escreva para leitura humana: frases diretas, parágrafos curtos, termos consistentes
e detalhe proporcional. Use tabelas para comparar/mapeamentos e listas para ações
ou itens paralelos. Não duplique o procedimento, estados ou decisões em vários
arquivos. Preserve conteúdo essencial e permita seções adicionais compatíveis.

Todo documento produzido deve identificar concretamente o objeto, a ação ou regra,
as referências pertinentes e como verificar o cumprimento, conforme sua função.
Substitua slogans como "seguir boas práticas", "testar o necessário" e "limpar
temporários" por regras, cenários, comandos/procedimentos e alvos reais do projeto.
Não invente comandos, caminhos, metas, stack ou aprovação para preencher seções:
informação indispensável ausente é pendência com ação necessária. Orientações de
preenchimento e marcadores pertencem aos templates; retire-os do documento entregue.
Regras permanentes aplicáveis podem ser preservadas, mas precisam das referências
e parâmetros locais necessários à execução. Ausência ou não aplicabilidade deve
ser explícita e justificada quando permitida, sem criar documento condicional vazio.

| Documento | Função e padrão |
|---|---|
| README.md | Objetivo e uso real; template README.md |
| AGENTS.md | Contexto, comandos, convenções e acionamento explícito; template AGENTS.md |
| docs/PRD.md | Contrato geral do produto; template PRD.md |
| docs/ARCHITECTURE.md | Componentes, contratos e restrições; template ARCHITECTURE.md |
| docs/ROADMAP.md | Fila objetiva de tasks por prioridade e resumo dos tickets; template ROADMAP.md |
| specs/NNN-nome/SPEC.md | Contrato de uma entrega; template SPEC.md |
| specs/NNN-nome/DESIGN.md | Design opcional e recomendado; template DESIGN.md |
| specs/NNN-nome/tasks/T-NNN.md | Tarefa, estado e evidências; template TASK.md |
| docs/decisions/ADR-NNN.md | Decisão transversal real; template ADR.md |
| docs/inbox/ITEM-NNN.md | Proposta ainda não aceita; template INBOX.md |
| specs/NNN-nome/validation/ | Evidência extensa quando necessária; template VALIDATION.md |
| CHECKPOINT.md | Passagem de contexto, inclusive encerramento; template CHECKPOINT.md |

TASKS.md e documentos de memória não são obrigatórios. Caminho, função ou processo
divergente precisa de decisão específica em ADR aceita e ações nos tickets pertinentes.

## Metadados e identificação

Use YAML simples entre linhas ---: escalares em uma linha e listas de strings
na notação JSON. Os templates exemplificam o formato; não há parser de fases da CLI.

- Documentos com status: draft, accepted ou superseded. Accepted registra uma
  decisão real; seções preenchidas não fabricam aprovação.
- Requisitos: RF-NNN/RNF-NNN no PRD e, com escopo local, na SPEC; critérios CA-NNN.
- SPEC: id igual à pasta NNN-nome; design none (não adotado), inline ou separate.
  Design é o único item opcional e é recomendado; Arquitetura é obrigatória.
- Ticket: ID T-NNN único na entrega; identidade completa é seu caminho relativo.
  Dependências e requisitos devem apontar a itens existentes. Priority é inteiro
  positivo, padrão 100; menor número representa maior prioridade de execução.
  Dependencies registra dependências técnicas reais; não usar prioridade como
  dependência nem inferir ordem pelo ID/data de criação. Ao adequar tickets antigos,
  preservar prioridade existente; usar 100 somente quando não houver prioridade
  definida. Reconhecer o alias legado depends_on sem perder seus vínculos; escrever
  dependencies como campo canônico.
- Ticket status: pending, ready, in_progress, awaiting_user, blocked, done ou cancelled.
  Executor: agent, user ou joint. Authorization: pending ou approved.
  Verification: not_verified, passed, failed ou not_applicable.
- ADR: ID ADR-NNN; proposta ITEM-NNN, com created em data ISO e status pending,
  incorporated ou discarded; registrar destino/motivo ao resolver.
- CHECKPOINT: status active ou closed, updated em data ISO e task com caminho real
  ou none. Relatório: verification e revision do estado efetivamente verificado.

## Execução dos tickets e manutenção

Só execute tarefa autorizada e com dependências atendidas. Use in_progress durante
o trabalho; done exige critérios cumpridos, evidência real, passed ou not_applicable
justificado e nenhuma ação humana obrigatória pendente. Cancelar exige motivo e
não satisfaz uma dependência. Não fabrique aceite, resultado ou autorização.

Antes de executar, confira o plano de verificação do ticket e as regras permanentes
de AGENTS. Durante a execução, use testes proporcionais à mudança; antes de done,
cumpra as verificações obrigatórias do projeto e os critérios do ticket. Crie ou
ajuste testes permanentes quando necessários para demonstrar comportamento ou
evitar regressões. Resultado anterior só vale enquanto código, entradas e ambiente
pertinentes forem válidos; amplie ou repita por mudança, falha ou lacuna concreta.
Teste não aplicável exige justificativa e revisão alternativa; teste obrigatório
não executado é pendência, não passed ou not_applicable.

Registre no resultado os comandos/procedimentos executados, resultado observado,
evidência, limitações e limpeza. Remova apenas descartáveis da própria execução
nos alvos previstos e encerre seus processos/serviços quando dispensáveis. Preserve
testes permanentes, fixtures úteis, evidências e arquivos anteriores ou de origem
desconhecida; Git sem rastreio não autoriza exclusão. Recursos ainda necessários
devem ter destino ou próxima ação explícitos. Não limpe arquivos particulares para
simular repositório sem alterações nem descarte a única evidência de uma falha.

Selecione a próxima task entre as autorizadas, com dependências concluídas e sem
impedimento, pela menor priority; empate usa caminho completo do ticket. Alterar
priority pode colocar uma task criada depois na frente das anteriores. Não execute
blocked/awaiting_user, não interrompa trabalho ativo por rotina e não fabrique
aprovação, conclusão ou dependência para satisfazer a ordem. Trabalhos independentes
continuam podendo ser executados no escopo autorizado.

Em awaiting_user, explique a ação concreta necessária. Em blocked, registre causa
e desbloqueio. Continue tarefas independentes autorizadas. Ao alterar tickets,
reflita a fila no ROADMAP, com prioridade, dependências/impedimentos, links, estado,
executor/verificação e ações humanas;
não é obrigatório um script ou pacote do framework.

A execução não depende de o projeto ser novo ou existente: localizar fontes,
aproveitar conteúdo útil quando houver e construir o documento pelo template
próprio. Preserve regras, decisões, IDs e evidências; não invente informação.
Reexecução de tarefa já concluída segue somente as operações alteradas e impactos
diretos. Mudar formato não autoriza alterar o negócio ou apagar conhecimento.

## Estados dos escopos do governador
O controle técnico por item fica em .sdd/execucao.json. Decisões e exceções ficam
nas ADRs; ações e resultados nos tickets, resumo no ROADMAP e passagem no CHECKPOINT.
O governador contém somente instruções, sem seção de aplicação do projeto. Não duplicar estados/versões em tabelas
paralelas. Registre evidências por objeto quando houver várias SPECs ou instruções;
conclusão parcial não conclui a etapa inteira. Não confundir organização concluída
com produto implementado, aprovação ou dispensa de artefato obrigatório.

## Métodos da skill por documento

### PRD
Transforme problema e resultado esperado em requisitos observáveis. Use o template
PRD próprio, com detalhe proporcional e sem confundir hipótese com decisão.
Localize fontes do produto, existam ou não documentos anteriores, e construa o PRD
pelo padrão incorporando o conteúdo útil. A existência de documento não cria um
procedimento diferente: aproveite o conteúdo válido sem adotar o formato anterior
como padrão alternativo.

### SPEC
Delimite a entrega a partir do PRD e vincule requisitos locais aos requisitos do
produto. Associe cada obrigação a critérios CA-NNN com contexto, ação e resultado
observável, incluindo falhas e limites pertinentes. Preserve IDs e decisões de
fontes anteriores ao incorporar o conteúdo no template SPEC. Separe comportamento
e solução: a SPEC define o contrato de comportamento independentemente da adoção
do Design. Use design: none quando não adotado, inline para solução na SPEC ou
separate com link para DESIGN.md. Não exija solução técnica para concluir a SPEC
nem fabrique aceite sobre o comportamento.

### Arquitetura
Construa obrigatoriamente docs/ARCHITECTURE.md pelo template ARCHITECTURE, com
contratos, componentes, tecnologias justificadas, restrições e verificação do
projeto. Aproveite invariantes, interfaces, decisões e configurações válidas;
relacione os contratos ao PRD e às SPECs sem depender de Design. Registre decisões
transversais reais pelo template ADR, com origem da aceitação. Se houver interface
visual, identifique Design System e versão; se não houver referência disponível,
trate a decisão necessária sem criá-lo implicitamente. Inclua preservação,
compatibilidade e recuperação quando houver migração arquitetural. Planeje
verificações reais, sem alegar execução nem replicar código como arquitetura.

### Design
Recomende o detalhamento técnico da entrega, único item opcional do fluxo. Quando
adotado, use o conteúdo do template DESIGN inline na SPEC ou em DESIGN.md, com
contexto, solução e contratos, decisões e alternativas, riscos e verificação.
Relacione a solução aos requisitos e à aceitação da SPEC e à arquitetura obrigatória;
justifique o local e mantenha design: inline ou separate e o link correspondente.
Se não adotado, use design: none na SPEC, sem exigir solução fictícia ou documento
vazio. Preserve design existente válido. A ausência não bloqueia SPEC, Arquitetura,
Tasks ou encerramento; decisões de produto e definições obrigatórias das tarefas
continuam necessárias. Não declare concluído um Design que não foi produzido.

### Tasks e ROADMAP

#### Tasks
Relacione obrigações da SPEC e do Design, quando adotado, aos tickets que as cobrem. Para lacunas,
decomponha o trabalho em ações limitadas pelo template TASK, com requisitos,
aceitação, verificação prevista, responsabilidades e ações humanas. Preserve IDs,
estados, autorizações e resultados comprovados dos tickets existentes. Confira
dependências reais e sem ciclos e identifique tarefas executáveis ou impedimentos.
Preparação documental não autoriza implementação nem exige tickets concluídos.
Design ausente não bloqueia preparar tarefas; sua definição suficiente continua
obrigatória, usando SPEC e arquitetura como insumos.
Cada ticket referencia AGENTS para regras permanentes e descreve seu plano concreto:
exigência/cenário, comando ou procedimento, diretório, ambiente/pré-requisitos,
resultado esperado e evidência. Defina os testes a criar/ajustar quando necessários
e os momentos de execução. Planeje alvos descartáveis e encerramento de recursos,
distinguindo testes permanentes e evidências a preservar. Não substitua esse plano
por "executar testes" nem preencha Resultado com sucesso ainda não observado.

#### ROADMAP
Construa a fila pelo template ROADMAP a partir dos próprios tickets. Prioridade e
dependências têm fonte única nos metadados dos tickets, em YAML: priority e
dependencies. Não crie JSON paralelo nem use .sdd/execucao.json para planejar
execução de produto. Ordene a fila por priority crescente e desempate pelo caminho
completo, destacando dependências, bloqueios e ações humanas; registre as encerradas
separadamente, sem reabrir trabalho para ordenar a fila. Links dos tickets identificam
suas SPECs, sem exigir seção narrativa de entregas ou prioridades/dependências.

Retire do ROADMAP o histórico detalhado após preservá-lo nos tickets/decisões
pertinentes com origem e referências. Resuma somente trabalho, estado, executor,
verificação e ordem reais. Adiamentos sem task devem apontar sua fonte governada;
não invente backlog ou autorização. Mantenha ações humanas concretas e vínculos
com dependentes. Atualize a tabela ao mudar priority, dependencies ou estado de
ticket; não é obrigatório outro arquivo, índice ou script de sincronização.

### AGENTS e README
Construa AGENTS e README pelos templates próprios, aproveitando instruções locais
e explicações válidas. AGENTS orienta a IA com contexto, referências, comandos,
diretórios, pré-requisitos, convenções e restrições; README explica propósito,
público e uso disponível. Confira comandos nas configurações e explicite limites
de verificação sem inventar sucesso. Preserve blocos administrados e configurações
particulares; CLAUDE encaminha a AGENTS e ao acionamento explícito do governador,
sem outro procedimento. Não copie instruções preenchidas do framework nem exija
organização antes de tarefas comuns.
AGENTS deve cobrir contexto/escopo, comandos/verificações, higiene do workspace,
qualidade/convenções, proteção/autorização e documentação/entrega. Derive comandos,
diretórios, gatilhos de execução e resultados esperados dos arquivos/configurações
reais; determine alvos temporários permitidos, identificação e encerramento de
recursos próprios e itens a preservar. Explicite convenções e limites reais, sem
slogans. AGENTS concentra regras permanentes; tickets detalham cenários, testes,
evidências e limpeza de cada tarefa. Não copie o conteúdo particular do framework
nem obrigue os consumidores a consultar sua bibliografia externa.

### Encerramento
Delimite o escopo autorizado e relacione os objetos entregues a tickets, decisões
e evidências reais. Atualize o resumo no ROADMAP e construa o CHECKPOINT pelo
template, confrontando registros com arquivos e Git quando disponível. Preserve
verificações válidas e seus limites, alterações não commitadas, adiamentos e leitura
indispensável; não dependa de temporários como única fonte de continuidade.
Use ADR, INBOX e VALIDATION apenas para decisões reais, propostas ainda não aceitas
e evidências extensas pertinentes. Não repita suítes apenas para encerrar nem
confunda pendências de implementação fora do escopo com lacunas documentais do
pedido. No fluxo completo, confira os sete itens obrigatórios; Design não adotado
não é pendência de encerramento nem conclusão fictícia. ADR, INBOX e VALIDATION
são registros auxiliares condicionais, não itens adicionais do fluxo. A próxima
ação deve permitir execução independente do projeto.

## Reconstrução e referências

Registre por origem/seção conteúdo a aproveitar ou conflito, destino e ação. Antes
de substituir ou remover, preserve os bytes originais em cópia recuperável; arquivo
removido permanece recuperável fora do projeto ou em histórico Git que contenha
o estado atual. Não fazer commit automaticamente. Alterações não commitadas precisam
de cópia própria. Não seguir symlinks, registrar segredos ou apagar a única cópia.

Incorpore conteúdo aproveitar e decisões reais dos conflitos. Confira significado,
regras, justificativas, exemplos, IDs e evidências; depois substitua o ativo,
remova arquivos concorrentes autorizados e corrija referências. Código, dados,
configurações e referências externas não são documentos a apagar por esta regra.

O pedido do usuário delimita a autorização. Não reaprovar o já decidido; aguardar
decisão para conflitos, exclusões não autorizadas e novo escopo. Processo divergente
só continua com decisão específica em ADR aceita.

Use exclusivamente os templates, a skill e os contratos do SDD Framework como
padrão e método de execução. Repositórios de outros frameworks podem inspirar o
desenvolvimento destes recursos pelo mantenedor; não são recursos de execução,
templates alternativos ou consultas exigidas do agente consumidor.

Documentos do produto e referências externas de Design System continuam sendo
insumos do projeto, sem substituir o padrão documental do SDD Framework.


## Controle de execução
O governador identifica itens com SDD:ITEM e associa templates/métodos com
SDD:USES. O update compara conteúdo instalado com o distribuído e mantém
.sdd/execucao.json (schema_version: 2), sem histórico crescente no governador.
A versão identifica a distribuição; diferenças são detectadas pelo conteúdo,
inclusive sem aumento de versão. Mudança só na versão não exige reexecução.

Cada entrada em items, incluindo geral para orientações comuns, contém:

| Campo | Significado e responsável |
|---|---|
| installed | Referência atual: hash SHA-256 e content (instruções, título, referências e recursos associados). Administrada pelo update; não editar. |
| applied | Cópia integral da referência efetivamente aplicada. A IA copia installed somente após cumprir o critério de pronto. null significa sem conclusão registrada. |
| baseline | Referência anterior limitada à comparação enquanto não houver applied. O update a preserva; a IA limpa ao concluir. |
| completed | IA: true quando todos os critérios de pronto do escopo estiverem atendidos; false quando faltar algum. Não há estados intermediários. |
| evidence | Lista de strings com caminhos dos objetos e evidências concretas. Mantida pela IA. |
| remaining | Lista de strings com exigências do critério de pronto pendentes e ações necessárias. Mantida pela IA. |
| pending | Diferença consolidada, com id, title, kind e details (recurso e diff), entre applied (ou baseline) e installed. O update recalcula; a IA limpa somente ao concluir. |

Campos superiores: schema_version e version administrados pelo update; items
contém os registros. legacy_pending, quando presente, preserva uma única vez o
antigo bloco de diferenças; a IA retira após reconciliar todas as suas pendências.
Os snapshots guardam texto suficiente para explicar a mudança; hash sozinho
apenas identifica diferença. Não há cadeia de eventos/versões. Dois updates antes
da execução consolidam o desvio desde a referência aplicada até a última instalada;
se a mudança for revertida, o delta desaparece. A referência aplicada e as evidências
não são redefinidas pelo update. Não editar o manifesto para esconder conflitos.

O critério de pronto determina se o item está concluído. Na retomada, resolva
somente as exigências do critério de pronto não atendidas; não registrar início ou etapas intermediárias.
A regra geral fica no governador; a skill explica como cumpri-la e
registrar o resultado. pending registra diferença de padrão; remaining indica somente critérios de pronto
ainda não cumpridos. completed: true exige applied, evidence real e remaining vazio; hashes iguais não provam o conteúdo nem a implementação do produto.
Itens removidos conservam registro para avaliação do impacto; não autorizam excluir
objetos do projeto. Reintrodução conserva identidade pelo ID.

Alterações comuns são avaliadas pelo impacto direto; não invalidam todos os itens.
A IA preserva partes não afetadas. O registro geral só é concluído após tratar ou
justificar seus impactos, mesmo quando o pedido atual cobre apenas parte deles.
O update não executa IA. Reexecução exige acionamento explícito; não inicia revisão
integral nem amplia escopo para mudanças de negócio ou pendências não relacionadas.

A migração converte estados antigos para concluído/não concluído e preserva
evidências e critérios restantes. Registro sem conclusão anterior não exige
reconstruir conteúdo pronto: confira o critério de pronto. Registro técnico
existente mas ausente/corrompido exige restauração, não reinicialização silenciosa.
