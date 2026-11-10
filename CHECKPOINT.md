---
status: active
updated: 2026-11-10
task: none
---
# Checkpoint — Decisões do governador e continuidade

## Objetivo e tarefa atual
Sessão encerrada com versão 0.4.2 aplicada. T-001 e T-003 a T-010 concluídas.
Próximo trabalho: aplicar a todas as demais seções do governador as decisões
consolidadas na seção 1. PRD, incluindo seus vínculos com os documentos governados,
templates, contratos, skill e código pertinente. Esta adequação ainda não foi feita
integralmente. Não confundir ajustes gerais já distribuídos com a revisão de cada seção.

## Estado do trabalho
Governador é um mapa de instruções para IA, legível e contestável por humanos.
Seção Aplicação neste projeto removida do governador local e da fonte distribuída
por pedido explícito. Não recriar essa seção ou outro relatório dentro do governador.
Ações/resultados ficam nos tickets, decisões nas ADRs, resumo no ROADMAP e passagem
aqui. Histórico da reformulação consta dos tickets e ADR-003; cópia temporária da
seção removida: /tmp/sdd-aplicacao-removida-cv7ye3j1.md.

Controle de mudanças em .sdd/execucao.json, formato 2: installed/applied guardam
hash e conteúdo; baseline é limitada à referência anterior quando ainda não há
applied; completed é booleano; evidence demonstra condições atendidas, remaining
indica somente critérios ainda não cumpridos e pending é a diferença consolidada.
Update mantém o padrão instalado; IA registra padrão aplicado somente ao concluir.
Updates sucessivos não acumulam histórico no governador; reversão limpa o delta.
execution_hash no manifesto protege installed; não alterar hashes para esconder conflito.
O log antigo permanece uma única vez em legacy_pending até aproveitamento de dados
pertinentes; não inventar conclusões nem reconstruir pontos prontos por falta de registro.

48 testes passaram no ajuste binário; depois da remoção da seção, 3 testes
direcionados passaram (0,482 s): preservação, idempotência e zipapp fora do checkout.
Pacote dist/sdd.pyz reconstruído. Governador não foi acionado nesta manutenção.
Sem acesso ao tax, CI remota, publicação ou commit/push.

## Decisões e pendências
As decisões abaixo devem orientar TODAS as seções restantes, e não só o PRD:

- Cada seção deve definir objetivo, objeto de saída/caminho, requisitos e insumos pertinentes, padrão próprio, operações específicas e critério de pronto claro, com detalhe proporcional.
- Só há concluído ou não concluído. O critério de pronto é o ponto de partida: conferir o documento real, executar somente condições não atendidas e preservar as atendidas. Não criar estados intermediários ou registros obrigatórios de início/progresso.
- O documento produzido demonstra cumprimento; o JSON guarda o resultado e monitora alterações do framework. Arquivo presente, hash, versão ou declaração de conclusão não substituem conteúdo/evidência.
- Não separar projeto novo/existente. Localizar fontes, aproveitar conteúdo válido, obter informação faltante e produzir pelo template SDD. Formato antigo não substitui o padrão; preservar conhecimento, decisões, IDs, evidências e configurações particulares.
- Introdução comum define quando agir; Execução de cada item explica como produzir o necessário. Não duplicar regras de reexecução nem ordenar reconstrução integral de condições já atendidas. No PRD, essa ambiguidade foi corrigida explicitamente.
- Após conclusão, reexecução trata somente alterações do framework e impactos diretos nos critérios afetados; sem alteração pertinente, preservar. Mudança comum não invalida todos os itens. Mudanças de negócio têm escopo próprio.
- Preservar objeto de saída explícito. No PRD foram removidos tabela/classificação de situações e Resultado a registrar; não reintroduzir redundâncias nas outras seções. Pendência/conclusão decorrem do critério de pronto.
- Usar exclusivamente templates, contratos e skill próprios. Repositórios externos inspiram o desenvolvimento, não são recursos obrigatórios de execução. Skill explica como cumprir o mapa e registrar resultado, sem competir com o governador.
- Ao adequar cada seção, revisar relações com documentos de entrada/saída, dependências reais e condicionais, templates, método correspondente em CONTRATOS e skill. Atualizar metadados SDD:ITEM/USES se necessário para detectar corretamente mudanças e impactos, sem copiar conteúdo particular para consumidores.
- Fonte canônica em src/sdd_framework/assets; sincronizar por update. Init/update não executam IA. Executar governador exige pedido explícito; encerramento devolve o projeto à execução independente.

ADR-003 substitui arquitetura operacional antiga; ADR-001/002 são históricas.
Piloto no tax continua a cargo do mantenedor; T-002/Windows somente após piloto e
autorização específica. Publicação, licença e integração de memória permanecem adiadas.

## Próximo passo
Na próxima tarefa, reler seção 1. PRD, regra geral, contratos e skill; adequar
seções 2 a 7 (SPECs, arquitetura/design, tasks, ROADMAP, AGENTS/README e encerramento)
segundo todas as decisões acima, respeitando particularidades de cada objeto.
Conferir fontes/recursos associados, distribuir por update e verificar os impactos
reais. Não executar o governador do projeto nem ampliar para tax/Windows por retomada.

Git: o mantenedor autorizou explicitamente um commit local de toda a reformulação
pendente, até 0.4.2, incluindo exclusões intencionais, novos recursos e este checkpoint.
Revisão pré-commit: 48 testes passaram (2,852 s), pacote reconstruído, diff conferido
e padrões usuais de credenciais/symlinks sem ocorrências. dist/ e arquivos .env
permanecem ignorados. Commit não autoriza push/publicação; próximos commits exigem
pedido ou autorização vigente, sem rotina automática. Consulte git log/status para
a confirmação do commit; este checkpoint não tenta registrar seu próprio hash.
Cópia temporária da arquitetura anterior: /tmp/sdd-anterior-kq0x2nt0.tar.gz;
o histórico Git preserva a versão anterior ao commit e não depende dessa cópia.

## Leitura para retomada
[AGENTS](AGENTS.md), [governador](governador.md),
[contratos](docs/padroes/CONTRATOS.md), [skill](.agents/skills/sdd/SKILL.md),
[PRD](docs/PRD.md), [SPEC](specs/001-governador/SPEC.md),
[roadmap](docs/ROADMAP.md), [T-009](specs/001-governador/tasks/T-009.md),
[T-010](specs/001-governador/tasks/T-010.md) e [ADR-003](docs/decisions/ADR-003.md).
