---
status: accepted
---
# Roadmap

## Entregas
| Entrega | Contrato | Resultado |
|---|---|---|
| 001 — Inicialização e adoção | [SPEC](../specs/001-inicializacao/SPEC.md) | Preparação progressiva e integrações |
| 002 — Atualização | [SPEC](../specs/002-atualizacao/SPEC.md) | Distribuição versionada sem perda de conteúdo |
| 003 — Conferência | [SPEC](../specs/003-conferencia/SPEC.md) | Gates, visão geral e adequação |
| 004 — Governança e execução | [SPEC](../specs/004-governanca/SPEC.md) | Contratos genéricos e trabalho humano |
| 005 — Continuidade | [SPEC](../specs/005-continuidade/SPEC.md) | CHECKPOINT e INBOX |
| 006 — Distribuição e qualidade | [SPEC](../specs/006-distribuicao/SPEC.md) | CLI, pacote portátil, testes e CI |

Estados de execução ficam nos tickets de cada entrega. A conferência consolida
os estados; esta tabela não é uma segunda fonte de progresso.

## Prioridades e dependências
Primeiro contratos e templates (004/005), depois inicialização (001), atualização
(002), conferência (003), distribuição e validação do conjunto (006). A entrega
0.1 é local, completa nesses limites; publicação externa fica para decisão do
mantenedor, não é inferida da autorização de desenvolvimento.

Propostas futuras: avaliar AI Memory em [ITEM-001](inbox/ITEM-001.md). Nenhuma
integração de memória é requisito para usar a versão atual.

<!-- SDD:PROGRESS:START -->
## Acompanhamento das tarefas

Visão derivada dos tickets, mantida pelo agente conforme AGENTS.md. Edite estados nos tickets e atualize este resumo; atualize com o script local indicado em AGENTS.md.

Atualizado em: 2026-11-06T19:37:57+00:00.

**21/21 tarefas concluídas.** Canceladas: 0. O resumo não substitui as evidências dos tickets.

### Adequação inicial ao SDD

| Tarefa | Trabalho | Estado | Execução | Verificação |
|---|---|---|---|---|
| [T-001](../.sdd/adoption/tasks/T-001.md) | Inventariar e integrar o projeto | Concluída | Agente | passed |
| [T-002](../.sdd/adoption/tasks/T-002.md) | Consolidar README e PRD | Concluída | Agente | passed |
| [T-003](../.sdd/adoption/tasks/T-003.md) | Definir arquitetura e instruções do projeto | Concluída | Agente | passed |
| [T-004](../.sdd/adoption/tasks/T-004.md) | Organizar roadmap | Concluída | Agente | passed |
| [T-005](../.sdd/adoption/tasks/T-005.md) | Especificar a primeira entrega | Concluída | Agente | passed |
| [T-006](../.sdd/adoption/tasks/T-006.md) | Preparar tickets e transferência | Concluída | Agente | passed |

### 001-inicializacao

| Tarefa | Trabalho | Estado | Execução | Verificação |
|---|---|---|---|---|
| [T-001](../specs/001-inicializacao/tasks/T-001.md) | Implementar contrato: Inicialização e adoção | Concluída | Agente | passed |
| [T-002](../specs/001-inicializacao/tasks/T-002.md) | Validar entrega: Inicialização e adoção | Concluída | Agente | passed |
| [T-003](../specs/001-inicializacao/tasks/T-003.md) | Preparar configuração nativa e antecipar pastas protegidas | Concluída | Agente | passed |

### 002-atualizacao

| Tarefa | Trabalho | Estado | Execução | Verificação |
|---|---|---|---|---|
| [T-001](../specs/002-atualizacao/tasks/T-001.md) | Implementar contrato: Atualização controlada | Concluída | Agente | passed |
| [T-002](../specs/002-atualizacao/tasks/T-002.md) | Validar entrega: Atualização controlada | Concluída | Agente | passed |

### 003-conferencia

| Tarefa | Trabalho | Estado | Execução | Verificação |
|---|---|---|---|---|
| [T-001](../specs/003-conferencia/tasks/T-001.md) | Implementar contrato: Conferência e acompanhamento | Concluída | Agente | passed |
| [T-002](../specs/003-conferencia/tasks/T-002.md) | Validar entrega: Conferência e acompanhamento | Concluída | Agente | passed |
| [T-003](../specs/003-conferencia/tasks/T-003.md) | Consolidar acompanhamento no roadmap | Concluída | Agente | passed |
| [T-004](../specs/003-conferencia/tasks/T-004.md) | Entregar ferramenta autônoma de acompanhamento | Concluída | Agente | passed |

### 004-governanca

| Tarefa | Trabalho | Estado | Execução | Verificação |
|---|---|---|---|---|
| [T-001](../specs/004-governanca/tasks/T-001.md) | Implementar contrato: Contratos, tarefas e trabalho humano | Concluída | Agente | passed |
| [T-002](../specs/004-governanca/tasks/T-002.md) | Validar entrega: Contratos, tarefas e trabalho humano | Concluída | Agente | passed |

### 005-continuidade

| Tarefa | Trabalho | Estado | Execução | Verificação |
|---|---|---|---|---|
| [T-001](../specs/005-continuidade/tasks/T-001.md) | Implementar contrato: CHECKPOINT e INBOX | Concluída | Agente | passed |
| [T-002](../specs/005-continuidade/tasks/T-002.md) | Validar entrega: CHECKPOINT e INBOX | Concluída | Agente | passed |

### 006-distribuicao

| Tarefa | Trabalho | Estado | Execução | Verificação |
|---|---|---|---|---|
| [T-001](../specs/006-distribuicao/tasks/T-001.md) | Implementar contrato: CLI, distribuição e qualidade | Concluída | Agente | passed |
| [T-002](../specs/006-distribuicao/tasks/T-002.md) | Validar entrega: CLI, distribuição e qualidade | Concluída | Agente | passed |

### Ações pendentes do usuário

Nenhuma ação humana pendente registrada nos tickets.

<!-- SDD:PROGRESS:END -->
