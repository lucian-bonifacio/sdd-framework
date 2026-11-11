---
status: draft
---
# Roadmap

## Fila de execução
Apresentação em revisão: o mantenedor não aprovou o novo layout, especialmente
as colunas Prioridade e Dependências/impedimentos. Revisão registrada em T-017;
nenhuma nova proposta de layout foi aplicada nesta sessão.

| Prioridade | Tarefa | Trabalho | Dependências/impedimentos | Estado | Executor | Verificação |
|---|---|---|---|---|---|---|
| 10 | [T-017](../specs/001-governador/tasks/T-017.md) | Rever a apresentação do ROADMAP | T-016 concluída; formato e execução a definir com o mantenedor | pending | joint | not_verified |

## Tasks concluídas ou canceladas

| Prioridade | Tarefa | Trabalho | Dependências/impedimentos | Estado | Executor | Verificação |
|---|---|---|---|---|---|---|
| 100 | [T-001](../specs/001-governador/tasks/T-001.md) | Reformular e aplicar o governador | — | done | agent | passed |
| 100 | [T-002](../specs/001-governador/tasks/T-002.md) | Corrigir e validar CI Windows | [T-001](../specs/001-governador/tasks/T-001.md) | done | agent | passed |
| 100 | [T-003](../specs/001-governador/tasks/T-003.md) | Centrar o governador nos artefatos | [T-001](../specs/001-governador/tasks/T-001.md) | done | agent | passed |
| 100 | [T-004](../specs/001-governador/tasks/T-004.md) | Executar somente padrões próprios do SDD Framework | [T-003](../specs/001-governador/tasks/T-003.md) | done | agent | passed |
| 100 | [T-005](../specs/001-governador/tasks/T-005.md) | Tratar o item PRD como uma tarefa orientada ao objeto | [T-004](../specs/001-governador/tasks/T-004.md) | done | agent | passed |
| 100 | [T-006](../specs/001-governador/tasks/T-006.md) | Identificar alterações e limitar a reexecução | [T-005](../specs/001-governador/tasks/T-005.md) | done | agent | passed |
| 100 | [T-007](../specs/001-governador/tasks/T-007.md) | Simplificar operação e concentrar conclusão no critério de pronto | [T-006](../specs/001-governador/tasks/T-006.md) | done | agent | passed |
| 100 | [T-008](../specs/001-governador/tasks/T-008.md) | Centralizar reexecução e manter controle fora do governador | [T-007](../specs/001-governador/tasks/T-007.md) | done | agent | passed |
| 100 | [T-009](../specs/001-governador/tasks/T-009.md) | Conclusão pelo critério de pronto | [T-008](../specs/001-governador/tasks/T-008.md) | done | agent | passed |
| 100 | [T-010](../specs/001-governador/tasks/T-010.md) | Retirar aplicação do governador e registrar a continuidade | [T-009](../specs/001-governador/tasks/T-009.md) | done | agent | passed |
| 100 | [T-011](../specs/001-governador/tasks/T-011.md) | Explicitar comprovação e pendências do PRD | [T-010](../specs/001-governador/tasks/T-010.md) | done | agent | passed |
| 100 | [T-012](../specs/001-governador/tasks/T-012.md) | Adequar seções 2 a 7 às decisões do PRD | [T-010](../specs/001-governador/tasks/T-010.md), [T-011](../specs/001-governador/tasks/T-011.md) | done | agent | passed |
| 100 | [T-013](../specs/001-governador/tasks/T-013.md) | Separar Arquitetura obrigatória e Design opcional | [T-012](../specs/001-governador/tasks/T-012.md) | done | agent | passed |
| 100 | [T-014](../specs/001-governador/tasks/T-014.md) | Exigir instruções concretas em AGENTS e nos documentos | [T-013](../specs/001-governador/tasks/T-013.md) | done | agent | passed |
| 100 | [T-015](../specs/001-governador/tasks/T-015.md) | Instalar o governador em docs | [T-014](../specs/001-governador/tasks/T-014.md) | done | agent | passed |
| 10 | [T-016](../specs/001-governador/tasks/T-016.md) | Organizar ROADMAP pela prioridade de execução das tasks | [T-002](../specs/001-governador/tasks/T-002.md), [T-015](../specs/001-governador/tasks/T-015.md) | done | agent | passed |

## Ações pendentes do usuário
Definir a apresentação de Prioridade e Dependências para a revisão de
[T-017](../specs/001-governador/tasks/T-017.md); implementação ainda não iniciada.

Piloto no tax segue com o mantenedor, separado das tasks concluídas; fonte em
[PRD](PRD.md#restrições-e-pendências). Publicação, licença e memória permanecem
adiadas. A correção Windows está validada na branch isolada, conforme
[T-002](../specs/001-governador/tasks/T-002.md); merge não foi realizado.
