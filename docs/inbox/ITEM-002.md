---
id: ITEM-002
status: incorporated
created: 2026-11-09
---
# Preservar conteúdo essencial durante adequação

## Informação ou proposta
O mantenedor esclareceu que a preservação abrange qualquer documento existente,
não somente config.toml. Mapear origem, conteúdo essencial e destino; explicitar
conflitos e conferir preservação de significado. Templates permitem seções
adicionais úteis sem duplicar responsabilidades.

## Fontes
Conversa de 2026-11-09: aprovação da recomendação de equilíbrio e pedido de
preservar as decisões. A versão 0.1 implementou a regra; sua evolução foi
substituída pelo governador explicitamente acionado em 2026-11-10.

## Impacto e discussão
A preservação semântica continua exigida na reconstrução documental. O agente
aproveita conteúdo e decide conflitos pelo usuário; init/update não realizam
análise semântica. Na versão 0.2, configuração existente é sempre preservada:
a antiga migração automática de modelo intacto deixou de ser o comportamento.
Nenhuma regra deste item autoriza alterar o tax ou configuração global.

## Destino ou justificativa
Incorporado no [PRD RF-005/007](../PRD.md), no governador e na
[ADR-003](../decisions/ADR-003.md). Os registros anteriores de implementação
permanecem na cópia de recuperação externa indicada no CHECKPOINT.
