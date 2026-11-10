# Padrões documentais SDD

Consulte o template do documento antes de escrevê-lo. Os templates definem as
seções obrigatórias e os campos; o governador define a execução. Remova todos os
marcadores de preenchimento na versão final e não invente informação para completá-la.

## Escrita e fontes

Escreva para leitura humana: frases diretas, parágrafos curtos, termos consistentes
e detalhe proporcional. Use tabelas para comparar/mapeamentos e listas para ações
ou itens paralelos. Não duplique o procedimento, estados ou decisões em vários
arquivos. Preserve conteúdo essencial e permita seções adicionais compatíveis.

| Documento | Função e padrão |
|---|---|
| README.md | Objetivo e uso real; template README.md |
| AGENTS.md | Contexto, comandos, convenções e acionamento explícito; template AGENTS.md |
| docs/PRD.md | Contrato geral do produto; template PRD.md |
| docs/ARCHITECTURE.md | Componentes, contratos e restrições; template ARCHITECTURE.md |
| docs/ROADMAP.md | Entregas, prioridades e resumo dos tickets; template ROADMAP.md |
| specs/NNN-nome/SPEC.md | Contrato de uma entrega; template SPEC.md |
| specs/NNN-nome/DESIGN.md | Design separado quando necessário; template DESIGN.md |
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
- SPEC: id igual à pasta NNN-nome; design inline ou separate.
- Ticket: ID T-NNN único na entrega; identidade completa é seu caminho relativo.
  Dependências e requisitos devem apontar a itens existentes.
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

Em awaiting_user, explique a ação concreta necessária. Em blocked, registre causa
e desbloqueio. Continue tarefas independentes autorizadas. Ao alterar tickets,
reflita o resumo no ROADMAP, com links, estado, executor/verificação e ações humanas;
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
procedimento diferente nem dispensa a reconstrução na execução.

Considere a tarefa resolvida somente pelo critério de pronto do item. Se houver
pendência, indique condição não atendida e ação necessária; se pronto, indique a
evidência no PRD. Na reexecução, execute apenas operações alteradas e os ajustes
necessários aos critérios afetados, sem revisar ou refazer pontos intactos.

### SPEC
Delimite a entrega e associe cada obrigação a um critério verificável. Inclua
condições, resultado esperado, falhas e limites pertinentes. Separe comportamento
e solução; preserve IDs. Refine a aceitação com cenários reais do projeto e com
o template SPEC do SDD Framework.

### Arquitetura e design
Explicite invariantes, interfaces, restrições e decisões suficientes para executar
a SPEC. Reutilize soluções existentes e detalhe conforme a complexidade. Arquitetura
descreve contratos; design local explica a solução da entrega. Não replique o código.

### Tasks e ROADMAP
Decomponha obrigações em ações concretas com caminho, dependência e evidência
prevista. Priorize resultados úteis e trabalhos independentes. O roadmap resume
os tickets e decisões de prioridade; não é outra fonte de estado ou autorização.

### AGENTS e README
Separe instruções para a IA de explicação de uso para pessoas. Registre contexto e
comandos reais; não duplique o governador. Mantenha acionamento explícito e padrões
de manutenção documental, sem exigir organização antes de cada tarefa comum.

### Encerramento
Relacione afirmações a evidências proporcionais. Reutilize verificações válidas e
registre limites; não repita suítes apenas para escrever o encerramento. Passe o
contexto necessário à execução local, com pendências reais e próxima tarefa clara.

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
| remaining | Lista de strings com condições pendentes e ações necessárias. Mantida pela IA. |
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
somente as condições não atendidas; não registrar início ou etapas intermediárias.
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
