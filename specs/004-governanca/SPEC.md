---
id: 004-governanca
status: accepted
design: inline
---
# Contratos, tarefas e trabalho humano

## Objetivo e escopo
Entregar contratos, tarefas e trabalho humano no framework genérico, conforme o [PRD](../../docs/PRD.md). Não implementar software do consumidor nem presumir aprovação de requisitos novos.

## Requisitos
- RF-001: Distribuir layout e instruções de preenchimento de cada artefato aplicável, com exigência progressiva por etapa.
- RF-002: Representar cada tarefa por ticket com requisito, estado, autorização, executor, dependências, aceitação, verificação e resultado.
- RF-003: Orientar execução contínua de trabalho autorizado, pausando apenas dependências afetadas por bloqueios ou ações humanas.
- RF-004: Orientar revisão antes, durante e após o lote, com evidências reais e atualização dos documentos afetados.
- RF-005: Registrar referência e versão do Design System quando disponível, sem criar o contrato visual.

## Critérios de aceitação
- CA-001: Dado bundle instalado, quando o agente consulta um artefato aplicável, então encontra template, seções e regras; gates exigem preenchimento no momento devido.
- CA-002: Dado ticket de produto, quando check executa, então valida ID, estado, executor, autorização, dependências, requisitos, verificação e seções obrigatórias.
- CA-003: Dado ticket conjunto em awaiting_user, quando o agente continua, então mantém pedido explícito, preserva progresso parcial e seleciona trabalho independente autorizado.
- CA-004: Dada conclusão declarada, quando a entrega é revisada, então há resultado, verificação planejada/executada e reconciliação documental; testes não executados não viram sucesso.
- CA-005: Dada interface com referência local de Design System inexistente, quando check executa, então aponta o caminho ausente sem gerar um Design System.

## Design técnico
Uma skill sdd lê referências WORKFLOW e ARTIFACTS e usa treze templates. Estados estáveis em inglês nos metadados e texto em português. TASKS é índice; tickets são fonte de estados. Executor agent/user/joint e estado awaiting_user explicitam colaboração. CLI não testa o consumidor nem transforma evidência em autorização. Campos de Design System são referência externa na configuração e nos artefatos relevantes.

Contratos e limites compartilhados estão na [arquitetura](../../docs/ARCHITECTURE.md) e no [fluxo](../../docs/WORKFLOW.md). Metadados e seções são definidos pela política versionada.

## Pendências
Nenhuma decisão bloqueante de implementação. Validação real em agentes e CI remoto permanece um limite declarado, não um sucesso presumido.
