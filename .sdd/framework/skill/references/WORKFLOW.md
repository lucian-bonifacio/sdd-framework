# Fluxo SDD obrigatório — versão 1

## Entradas
Projeto novo começa pela concepção. Projeto existente começa por inventário:
código, comandos, testes, documentação e decisões vigentes. Classifique lacunas
e conflitos; aproveite equivalências comprovadas, sem reconstruir a história por
suposição. Registre mapeamentos de documentos em `.sdd/config.json`, campo
`document_paths`, somente depois de revisar seu conteúdo e suas referências.

O init instala recursos e um plano de adequação, não um produto fictício.
Autorização dos tickets iniciais cobre organização documental, nunca escolha
silenciosa de requisitos importantes, implementação, publicação ou deploy.

## Etapas e condições de avanço
Os nomes em inglês são valores estáveis da configuração/CLI; os textos são PT-BR.

| Etapa | Trabalho e saída | Condição para avançar |
|---|---|---|
| discovery | Concepção ou inventário e plano de adequação | Problema, público e situação atual compreendidos |
| requirements | README e PRD | Escopo, requisitos e pendências explícitos; PRD aceito para arquitetura |
| architecture | Arquitetura e decisões relevantes | Orientação técnica verificável e sem escolhas bloqueantes em aberto |
| planning | Roadmap | Entregas e dependências priorizadas |
| specification | SPEC da entrega selecionada | Comportamento e aceitação claros |
| design | Design inline ou separado | Solução proporcional coerente com arquitetura e Design System disponível |
| tasks | Índice e tickets | Toda obrigação da SPEC coberta por tarefas verificáveis |
| implementation | Execução pelo agente do projeto | Tickets autorizados, prontos e dependências concluídas |
| validation | Evidências por ticket e verificação do conjunto | Requisitos, testes e documentos reconciliados; limites declarados |
| delivery | Transferência independente | Nenhum trabalho obrigatório pendente; aceite humano quando exigido |

O agente verifica os pré-requisitos documentais antes de entrar em cada etapa.
`sdd check --phase X` é auxiliar opcional de conferência; sem `--phase`, usa
`phase` da configuração. Se a configuração estiver presente, o agente atualiza
esse campo depois de revisar o gate, sem pular etapas para esconder pendências. Documentos já
existentes também são validados, mesmo antes de se tornarem obrigatórios.
O resultado da CLI nunca prova completude semântica nem autoriza execução.
Após `tasks`, a seleção por dependências substitui uma fila global rígida.

## Revisão e mudança
Pode-se voltar a qualquer etapa. Mudança aceita exige avaliar SPEC, design,
tarefas, testes, roadmap e decisões afetadas. Não adaptar o contrato apenas para
aceitar código incompleto. Escopo novo vira ticket pendente de autorização.
Tarefa aprovada continua autorizada ao trocar de sessão; registre a origem da
autorização no ticket. Não pedir permissão repetida por rotina.

## Ciclo de cada tarefa
1. Conferir Definition of Ready: requisito identificado, escopo, insumos,
   dependências, autorização e evidência de conclusão planejada.
2. Marcar `in_progress`; executar somente o escopo autorizado.
3. Verificar a alteração com testes/revisão adequados ao risco. Para correção de
   comportamento, demonstrar a regressão quando viável. Usar comandos reais do
   projeto; não impor linguagem, stack, TDD ou ferramenta a todos os consumidores.
4. Concluir somente com os critérios satisfeitos, verificação registrada e
   documentos atualizados. Não marcar sucesso de teste que não foi executado.
   Quando esses critérios forem suficientes no ticket, o resultado é aceito sem
   confirmação humana adicional. Pedir validação humana apenas se a tarefa a exigir.
5. Prosseguir com a próxima tarefa pronta. Ao bloquear, registrar causa, ação
   concreta de desbloqueio e continuar as independentes.
6. Atualizar o acompanhamento com `python3 scripts/atualizar_roadmap.py`, ferramenta
   autônoma entregue ao consumidor. Conferir saída e diff; tratar falhas, preservando
   planejamento e modelo. Não exigir CLI SDD para essa rotina.

## Trabalho humano
`executor` distingue `agent`, `user` e `joint`. Ticket conjunto mantém listas
claras da parte do agente e do usuário. Em `awaiting_user`, explicar o que fazer,
pré-requisitos, evidência a devolver e quais tarefas dependem disso. Expor esse
grupo no relatório de conferência. O usuário não precisa ler logs para saber
qual é sua próxima ação. Retomar após resposta real, sem interpretar tempo
decorrido como consentimento. Conclusão do código não dispensa aceite pendente.

## Verificação do conjunto
Antes: analisar consistência de requisitos, design e tarefas. Durante: verificar
cada alteração. Ao terminar o lote: testar integração e regressões relevantes no
estado final; registrar revisão e possíveis interações. Reutilizar evidências
somente enquanto o estado relevante não mudou. Não executar todas as verificações
a cada edição sem motivo; não presumir que testes isolados provam integração.
Usar `passed`, `failed`, `not_verified` e `not_applicable` com razões explícitas.
Achados adicionais recebem tickets; conservar IDs e histórico. Nenhum mecanismo
do SDD publica, mergeia, faz deploy ou executa comandos de aplicação sozinho.

## Pausa e retomada
CHECKPOINT é acionado expressamente pelo usuário ou antes de uma passagem de
contexto combinada. É um retrato atual, não um diário. Consultar estado real de
arquivos/Git (se disponível), registrar alterações não commitadas, verificações,
tentativas relevantes, decisões, bloqueios e próximo passo. Atualizar o ticket
também. Na retomada, conferir fontes porque o checkpoint pode estar desatualizado.
Depois de concluir o trabalho descrito, marcar o checkpoint `closed`.
Sessões simultâneas devem usar ramos/worktrees independentes; um checkpoint único
não coordena múltiplos escritores.

## INBOX e decisões
Criar um ITEM por pesquisa ou proposta ainda em avaliação, com fonte, data e
impacto. Fatos e hipóteses devem ser distintos. Avaliar a INBOX na conferência
e quando o assunto se tornar relevante. Ao aceitar, atualizar o documento
governado e marcar `incorporated` com destino; ao rejeitar, `discarded` com motivo.
Decisão local fica no DESIGN; transversal/duradoura em ADR. Preservar registros
substituídos. Memória externa, incluindo AI Memory, é apenas contexto consultável.

## Interface
O SDD não cria Design System. Em projeto com interface, perguntar se existe e
registrar sua referência e versão em `design_system` da configuração. Se houver,
os artefatos de front-end devem referenciá-lo; divergências precisam de decisão.
Ausência é pendência visível, não permissão para fabricar aprovação visual.
Projeto sem interface registra `interface: false`.

## Conformidade e proporcionalidade
Obrigatoriedade é definida por etapa e aplicabilidade. DESIGN separado, ADR e
evidência separada são condicionais; omissão exige justificativa quando relevante.
Documento vazio, rascunho ou modelo por preencher não satisfaz gate de avanço.
A conferência gera tarefas de adequação, não decisões aprovadas automaticamente.
Documentos aprovados não são reescritos por update. Conteúdo e instruções externos
aos blocos administrados pertencem ao consumidor e devem ser preservados.
