---
status: accepted
---
# Roadmap

## Fila de execução
A primeira linha tem maior prioridade. A posição expressa a ordem desejada;
dependências, autorização e impedimentos determinam o que pode ser executado.

| Ordem | Tarefa | Trabalho | Dependências e impedimentos | Estado | Verificação |
|---|---|---|---|---|---|
| 1ª | [T-018](../specs/001-governador/tasks/T-018.md) | Disponibilizar init e update diretamente pelo GitHub | Sem dependências; aguarda definição do procedimento de obtenção pelo GitHub | Pendente | Não verificada |
| 2ª | [T-022](../specs/001-governador/tasks/T-022.md) | Planejar Design System no fluxo do governador | Sem dependências; aguarda definição do papel e formato do Design System | Pendente | Não verificada |

## Concluídas ou canceladas

| Tarefa | Trabalho | Estado | Verificação |
|---|---|---|---|
| [T-001](../specs/001-governador/tasks/T-001.md) | Reformular e aplicar o governador | Concluída | Aprovada |
| [T-002](../specs/001-governador/tasks/T-002.md) | Corrigir e validar CI Windows | Concluída | Aprovada |
| [T-003](../specs/001-governador/tasks/T-003.md) | Centrar o governador nos artefatos | Concluída | Aprovada |
| [T-004](../specs/001-governador/tasks/T-004.md) | Executar somente padrões próprios do SDD Framework | Concluída | Aprovada |
| [T-005](../specs/001-governador/tasks/T-005.md) | Tratar o item PRD como uma tarefa orientada ao objeto | Concluída | Aprovada |
| [T-006](../specs/001-governador/tasks/T-006.md) | Identificar alterações e limitar a reexecução | Concluída | Aprovada |
| [T-007](../specs/001-governador/tasks/T-007.md) | Simplificar operação e concentrar conclusão no critério de pronto | Concluída | Aprovada |
| [T-008](../specs/001-governador/tasks/T-008.md) | Centralizar reexecução e manter controle fora do governador | Concluída | Aprovada |
| [T-009](../specs/001-governador/tasks/T-009.md) | Conclusão pelo critério de pronto | Concluída | Aprovada |
| [T-010](../specs/001-governador/tasks/T-010.md) | Retirar aplicação do governador e registrar a continuidade | Concluída | Aprovada |
| [T-011](../specs/001-governador/tasks/T-011.md) | Explicitar comprovação e pendências do PRD | Concluída | Aprovada |
| [T-012](../specs/001-governador/tasks/T-012.md) | Adequar seções 2 a 7 às decisões do PRD | Concluída | Aprovada |
| [T-013](../specs/001-governador/tasks/T-013.md) | Separar Arquitetura obrigatória e Design opcional | Concluída | Aprovada |
| [T-014](../specs/001-governador/tasks/T-014.md) | Exigir instruções concretas em AGENTS e nos documentos | Concluída | Aprovada |
| [T-015](../specs/001-governador/tasks/T-015.md) | Instalar o governador em docs | Concluída | Aprovada |
| [T-016](../specs/001-governador/tasks/T-016.md) | Organizar ROADMAP pela prioridade de execução das tasks | Concluída | Aprovada |
| [T-019](../specs/001-governador/tasks/T-019.md) | Concluir cada item e prosseguir até encerrar o governador | Concluída | Aprovada |
| [T-017](../specs/001-governador/tasks/T-017.md) | Rever a apresentação do ROADMAP | Concluída | Aprovada |
| [T-020](../specs/001-governador/tasks/T-020.md) | Definir testes automatizados no fluxo SDD | Concluída | Aprovada |
| [T-021](../specs/001-governador/tasks/T-021.md) | Distribuir política Git em rules do Codex | Concluída | Aprovada |

## Ações pendentes do usuário

| Ação necessária | Fonte | Trabalho que depende dela |
|---|---|---|
| Definir origem, política de versão e procedimento de obtenção pelo GitHub; autorizar a implementação concreta | [T-018](../specs/001-governador/tasks/T-018.md#ação-humana-pendente) | Implementação de init/update diretamente pelo GitHub |
| Definir como Design System deve funcionar no governador e autorizar o escopo concreto futuro | [T-022](../specs/001-governador/tasks/T-022.md#ação-humana-pendente) | Planejamento e posterior adequação do item Design para telas, padrões visuais e cores |
| Conduzir o piloto no tax e trazer os resultados observados | [PRD — Restrições e pendências](PRD.md#restrições-e-pendências) | Validação do framework no projeto piloto; não impede tarefas independentes autorizadas |

Publicação/release, licença e memória permanecem adiadas conforme
[PRD — Restrições e pendências](PRD.md#restrições-e-pendências), sem ação solicitada
agora. A correção Windows está concluída, com CI real na branch isolada e
correções equivalentes na main local, conforme
[T-002](../specs/001-governador/tasks/T-002.md). O merge formal da branch isolada
não representa pendência técnica da correção Windows.
