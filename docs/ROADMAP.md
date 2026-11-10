---
status: accepted
---
# Roadmap

## Entregas
A versão 0.2 substitui a arquitetura anterior pelo governador explicitamente
acionado. Contrato em [SPEC](../specs/001-governador/SPEC.md).
A versão inicial não precisa continuar como processo paralelo.

## Prioridades e dependências
Reformulação 0.2 implementada e aplicada localmente em 2026-11-10. O mantenedor
conduz o piloto no tax. Investigar Windows somente após esse piloto.
Publicação e integração de memória permanecem decisões futuras.
Refinamento 0.2.1 concluído: governador centrado nos artefatos, com PRD primeiro, estados
legíveis e referências por escopo; solicitado após a conclusão da reformulação.

Correção 0.2.2 concluída: execução usa exclusivamente padrões e skill próprios;
referências externas permanecem somente como bibliografia de desenvolvimento.

Ajuste 0.2.3 concluído: item PRD como tarefa com requisitos, objetivo, situação
do objeto, operação novo/existente, reexecução e critério de pronto.

Versão 0.3.0 concluída: update detecta mudanças por item e recurso associado,
registra diferenças no governador e orienta reexecução restrita ao impacto.
Versão 0.3.1 concluída: operação unificada pela existência de fontes; PRD mantém
objeto explícito e determina pendências pelo critério de pronto. Skill reforçada.

Versão 0.4.0: controle limitado ao padrão instalado/aplicado em .sdd/execucao.json,
sem histórico crescente no governador. Mecânica geral única; skill registra
conclusão pelos critérios e diferenças são consolidadas até a execução.

Versão 0.4.1 concluída: critério de pronto determina concluído/não concluído,
sem estados intermediários. Retomada trata só condições não atendidas; depois da
conclusão, reexecução depende das alterações do framework. Introdução orienta
quando agir, Execução do PRD explica como produzir o necessário.

Versão 0.4.2 concluída: removida seção Aplicação neste projeto, inclusive na fonte
distribuída. Próximo trabalho registrado no CHECKPOINT: estender às seções 2 a 7
todas as decisões do PRD e conferir seus recursos/documentos relacionados.

## Acompanhamento das tarefas
| Tarefa | Trabalho | Estado | Executor | Verificação |
|---|---|---|---|---|
| [T-001](../specs/001-governador/tasks/T-001.md) | Reformular e aplicar o governador | done | agent | passed |
| [T-002](../specs/001-governador/tasks/T-002.md) | Investigar CI Windows depois do piloto | pending | agent | not_verified |
| [T-003](../specs/001-governador/tasks/T-003.md) | Refinar governador por artefato | done | agent | passed |
| [T-004](../specs/001-governador/tasks/T-004.md) | Usar somente padrões próprios na execução | done | agent | passed |
| [T-005](../specs/001-governador/tasks/T-005.md) | Organizar o PRD como tarefa orientada ao objeto | done | agent | passed |
| [T-006](../specs/001-governador/tasks/T-006.md) | Detectar alterações e limitar reexecução | done | agent | passed |
| [T-007](../specs/001-governador/tasks/T-007.md) | Unificar operação e simplificar o critério de pronto | done | agent | passed |
| [T-008](../specs/001-governador/tasks/T-008.md) | Centralizar reexecução e controle técnico | done | agent | passed |
| [T-009](../specs/001-governador/tasks/T-009.md) | Conclusão pelo critério de pronto | done | agent | passed |
| [T-010](../specs/001-governador/tasks/T-010.md) | Remover aplicação e registrar continuidade | done | agent | passed |

## Ações pendentes do usuário
Piloto no tax e eventual autorização da investigação Windows, depois dele.
Não há aceite adicional requerido para concluir a reformulação já autorizada.
