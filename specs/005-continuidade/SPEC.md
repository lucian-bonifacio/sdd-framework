---
id: 005-continuidade
status: accepted
design: inline
---
# CHECKPOINT e INBOX

## Objetivo e escopo
Entregar checkpoint e inbox no framework genérico, conforme o [PRD](../../docs/PRD.md). Não implementar software do consumidor nem presumir aprovação de requisitos novos.

## Requisitos
- RF-001: Padronizar CHECKPOINT acionado por pedido expresso de pausa ou passagem de contexto.
- RF-002: Orientar retomada sem contexto anterior com leitura do checkpoint e reconciliação com arquivos e tickets atuais.
- RF-003: Preservar propostas e pesquisas em itens individuais da INBOX com fontes, impacto, estado e resolução.
- RF-004: Não tratar memória ou proposta pendente como decisão aprovada; referências reais devem acompanhar incorporação ou descarte.

## Critérios de aceitação
- CA-001: Dado pedido explícito de pausa, quando o agente segue a skill, então preenche CHECKPOINT com objetivo, trabalho parcial, decisões, bloqueios, próximo passo e leituras.
- CA-002: Dada sessão nova sem contexto, quando segue AGENTS/skill, então consulta CHECKPOINT e confere estado real; referência a ticket inexistente é detectada pelo check.
- CA-003: Dada pesquisa ainda não aceita, quando registrada na INBOX, então tem ITEM-NNN, fonte, data, impacto e destino/justificativa; pendência é visível sem bloquear tudo.
- CA-004: Dada proposta incorporada/descartada, quando o item é encerrado, então registra destino ou motivo; memória externa não substitui documento governado aceito.

## Design técnico
Templates CHECKPOINT.md e INBOX.md e procedimentos na skill. CHECKPOINT é único por árvore de trabalho, com active/closed, data e ticket ou none. INBOX usa ITEM-NNN e pending/incorporated/discarded. Verificador valida estrutura, datas e ticket de retomada; item pending é informativo e não bloqueia todo o projeto. Registro semântico fica com agente e usuário, sem captura de sessão oculta ou serviço obrigatório.

Contratos e limites compartilhados estão na [arquitetura](../../docs/ARCHITECTURE.md) e no [fluxo](../../docs/WORKFLOW.md). Metadados e seções são definidos pela política versionada.

## Pendências
Nenhuma decisão bloqueante de implementação. Validação real em agentes e CI remoto permanece um limite declarado, não um sucesso presumido.
