---
id: 001-governador
status: accepted
design: inline
---
# Governador explícito e distribuição de padrões

## Objetivo e escopo
Substituir a arquitetura 0.1 por governador, padrões e uma skill, conforme
[PRD](../../docs/PRD.md) RF-001 a RF-011. Reformulação direta autorizada pelo
mantenedor em 2026-11-10; não preservar mecanismos que perderam a função.

## Requisitos
- RF-001: Init prepara governador, padrões, ambas as integrações e configuração local ausente, sem criar arquivos funcionais ou executar organização.
- RF-002: Governador contém passos completos para IA, com operação unificada pela existência de documentos e informação, reconstrução pelo padrão, contradições reais, referências, autorização e encerramento.
- RF-003: Skill e blocos dos agentes exigem acionamento explícito; configurar também as políticas nativas disponíveis para Codex e Claude.
- RF-004: Templates/contratos definem padrões e conteúdo mínimo; governador contém somente instruções; tickets, ADRs e checkpoint guardam trabalho, decisões e passagem.
- RF-005: Update preserva documentos e bytes próprios, recusa conflitos/symlinks/downgrade e não aciona IA.
- RF-006: Migração 0.1 remove somente recursos administrados intactos e desativa o procedimento antigo, preservando plano/configuração/tickets particulares para migração pela IA.
- RF-007: CLI expõe só init/update, com JSON, lock e rollback; zipapp funciona sem checkout/dependências.
- RF-008: Aplicar a reformulação neste repositório e retirar a documentação/código de controles antigos. Preservar decisões atuais e adiamentos reais.
- RF-009: Investigar CI Windows somente após piloto e autorização específica, sem presumir sucesso remoto.
- RF-010: Organizar o governador por artefato, começando por PRD e SPECs. Em cada operação, localizar fontes e construir o objeto pelo template, aproveitando conteúdo quando houver, sem separar projetos novos/existentes. No PRD, manter objetivo, objeto de saída, insumos, operação e critério de pronto; execução/reexecução seguem orientação geral única; retirar classificação de situações e resultado separado. Reexecução trata só operações alteradas/impactos diretos. Usar padrões próprios e preservar registros particulares, sem gates de fases.

- RF-011: Detectar diferenças por ID/dependências e guardar em .sdd/execucao.json apenas referências limitadas e pendências consolidadas. O update mantém installed; a IA mantém applied, completed, evidence e remaining, sem concluir por instalação. Dois updates comparam desde applied até o padrão atual, sem cadeia de eventos.
- RF-012: Centralizar roteamento no governador e operacionalização na skill; a conclusão tem apenas duas situações, determinadas pelo critério de pronto. Antes da conclusão, executar só condições não atendidas; depois, reexecutar apenas mudanças do framework. Preservar estado/evidências, recusar controle ausente/corrompido e proteger installed pelo manifesto; copiar referência para applied somente após critérios cumpridos. Migrar log antigo intacto para legacy_pending e exigir reconciliação única sem fabricar conclusão.

## Critérios de aceitação
- CA-010: Update identifica itens por ID estável e detecta mudança isolada de instrução, template ou método. Diferenças ficam no controle técnico, fora do governador. Inclusão/remoção não apaga documentos do produto; ordem é mudança comum.
- CA-011: Updates sucessivos consolidam o delta desde o padrão aplicado e preservam estado/evidências. Reversão elimina diferença, mudança só de versão não exige reexecução e update idempotente não modifica recursos. Conclusão pela IA elimina delta; ausência de registro não fabrica primeira execução/conclusão.
- CA-012: Critério de pronto determina concluído/não concluído; condições atendidas são preservadas. Depois de concluído, alteração encaminha à reexecução e referências iguais à preservação. Estados antigos são convertidos sem perder evidências ou condições pendentes. Controle ausente/inválido, installed modificado ou conclusão sem evidência abortam antes de escrever. Log antigo íntegro migra uma única vez; log adulterado impede a migração. Skill/regra geral preservam aplicação e limitam impacto.
- CA-001: Consumidor vazio recebe instruções/padrões/skills e nenhuma pasta de produto, PRD ou ticket fictício; init repetido não modifica a instalação.
- CA-002: Codex recebe allow_implicit_invocation false; Claude recebe disable-model-invocation true. Blocos de entrada não exigem iniciar organização para tarefas comuns.
- CA-003: Update modifica procedimento e recursos, preserva bytes particulares de AGENTS/governador e configuração; falha antes de mutações em conflito.
- CA-004: Migração mantém informação própria do antigo FLUXO e desativa seu procedimento; arquivos não administrados não são apagados.
- CA-005: Testes demonstram symlinks recusados, rollback de escrita/remoção, bloqueio concorrente e execução do zipapp fora do checkout.
- CA-006: Governador dirige ações à IA com linguagem legível; cobre os padrões e separa encerramento documental de implementação do produto.
- CA-007: Este repositório usa o novo governador; documentação vigente não depende de fases, CLI check, TASKS ou tickets de adoção.
- CA-008: Windows permanece pendência explícita até execução e evidências reais após o piloto.
- CA-009: Primeira etapa é PRD, segunda SPECs; inventário e verificações pertencem ao artefato correspondente. Todos os escopos têm objetivo, estado, apoio, condicionais e conclusão. O PRD define o objeto e os insumos necessários; somente o critério de pronto determina pendência ou conclusão. A operação é unificada, e a reexecução trata só operações alteradas/impactos diretos. Update preserva estados particulares; o governador e os recursos distribuídos não remetem a templates/skills externos como orientação de execução; padrões e métodos são próprios do SDD Framework.

## Design técnico
[Arquitetura](../../docs/ARCHITECTURE.md) e [ADR-003](../../docs/decisions/ADR-003.md).
O governador é administrado por bloco, sem seção de aplicação. Conteúdo próprio
externo ao bloco continua preservado pelo update; exclusão local exige autorização.
Padrões têm cópia única em docs/padroes. As duas skills encaminham ao mesmo arquivo.
A CLI não interpreta requisitos nem executa o processo SDD. Não há novas
dependências ou comandos de aplicação automática.

changes.py compara IDs SDD:ITEM e referências SDD:USES, incluindo fragmentos.
execution.py mantém snapshots normalizados com SHA-256 em .sdd/execucao.json.
Cada item guarda installed, applied, baseline anterior quando ainda não aplicado,
completed (booleano), evidence, remaining e pending. O manifesto guarda execution_hash somente
da projeção installed; campos da IA permanecem editáveis. completed registra o resultado do critério de pronto, sem estados intermediários.

O update recalcula o delta entre applied (ou baseline) e installed. A IA copia
installed para applied ao concluir, limpa pending/baseline e registra evidência.
Não há histórico crescente; mudanças revertidas deixam de exigir adequação.
Diferenças comuns não invalidam todos os itens. Migração preserva o log antigo em
legacy_pending e conserva evidências anteriores; ausência de conclusão não manda refazer critérios atendidos.
Roteiro, decisões e exceções próprios ficam nos tickets, ADRs e checkpoint.

## Pendências
Piloto no tax e CI Windows depois dele; sem publicação autorizada.
