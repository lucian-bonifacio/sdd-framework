---
status: closed
updated: 2026-11-11
task: none
---
# Checkpoint — Encerramento da sessão

## Objetivo e tarefa atual
Sessão encerrada a pedido do mantenedor, com T-017, T-019, T-020 e T-021 concluídas.
Sem tarefa em execução. Pendentes apenas T-018 (init/update pelo GitHub) e T-022
(planejar Design System), na ordem apresentada em docs/ROADMAP.md. Ambas têm
status pending e authorization pending; retomada não autoriza implementar.
Versão 0.4.2 mantida, sem release.

O mantenedor autorizou um commit local com os ajustes desta sessão e este checkpoint.
Conferir git log -1 --oneline e git status --short ao retomar para confirmar o hash
e o estado resultante; este documento não registra seu próprio hash. Não há
pedido de push, merge, publicação ou alteração global de configuração.

## Estado do trabalho
- T-019: governador completo segue os itens na ordem, concluindo os critérios do
  item atual antes de avançar e prosseguindo sem novo pedido de continuação.
  Decisão indispensável ausente exige pergunta concreta e retomada do mesmo item;
  não encerrar após formatar o PRD nem avançar com lacunas. draft/accepted são
  metadados editoriais, sem terceira condição operacional. Pedidos limitados e
  Design não adotado preservam seu escopo. Regra geral centralizada, sem repetição
  em cada item; evidência em specs/001-governador/validation/T-019.md.
- T-017: ROADMAP aceito, com Ordem (1ª, 2ª…) na fila; dependências/impedimentos
  visíveis; sem Executor ou prioridade numérica nas tabelas. Encerradas têm somente
  Tarefa, Trabalho, Estado e Verificação. Tradução centralizada em
  docs/padroes/CONTRATOS.md#roadmap. Ações pendentes do usuário mostram fonte,
  decisão/informação e trabalho dependente. Prioridade técnica permanece nos
  tickets; não mover só a linha para alterar a fonte. Evidência em
  specs/001-governador/validation/T-017.md; histórico anterior em T-016.
- T-020: Testes automatizados definidos em
  docs/padroes/CONTRATOS.md#testes-automatizados. Governador exige planejar cobertura,
  automação ou alternativa justificada; implementação executa o plano/checks e
  registra resultados no ticket. Templates TASK/AGENTS e skill referenciam essa
  política, com parâmetros locais. Não há TDD universal, cobertura percentual ou
  stack obrigatórios; testes existentes válidos são reaproveitados. Evidência em
  specs/001-governador/validation/T-020.md.
- T-021: política Git em .codex/rules/sdd-git.rules, distribuída por init/update
  e incluída no pacote portátil. Fonte em
  src/sdd_framework/assets/integrations/codex/sdd-git.rules; project.py administra
  somente esse caminho em .codex, com hashes, conflitos, symlinks e rollback.
  Consultas usuais ficam no sandbox sem allow de elevação; mutações e variantes
  listadas recebem prompt no avaliador Codex. Encaminhamento único no bloco SDD
  de AGENTS, sem matriz copiada. config.toml existente e outras rules particulares
  preservados. Codex precisa reiniciar em projeto confiável para carregar rules;
  limites por prefixo/superfície em CONTRATOS.md#git-e-permissoes. Evidência em
  specs/001-governador/validation/T-021.md.

Essas entregas estão incorporadas às fontes distribuídas em
src/sdd_framework/assets e ao dist/sdd.pyz reconstruído; as cópias deste projeto
foram sincronizadas por update. Consumidores recebem os recursos via update;
a aplicação dos padrões aos seus documentos próprios exige acionar o governador.
Rules Git são carregadas pelo Codex ao reiniciar. Os testes do framework em tests/
não são instalados no consumidor; este recebe instruções para os testes do produto.

### Verificações e limites
Última suíte: python3 -m unittest discover -s tests -v, 67 testes OK/código 0,
15,195 s, sem skips, Linux/Python 3.14.4. Inclui 28 avaliações de tokens em quatro
testes com codex-cli 0.167.1, sem executar as mutações Git representadas.
python3 tools/build_release.py retornou 0 após a última alteração distribuída.
Consumidor anterior e zipapp fora do checkout aprovados; updates idempotentes,
configuração e nove registros da IA preservados. Update local final repetido
manteve 23 arquivos byte a byte idênticos. Procedimentos em validação T-021.

dist/sdd.pyz tem SHA-256 e6c0e493a56c56351a3c82d1568cfaeef6d0e209ab64305e2fbbc9d9b137e097.
É gerado e ignorado pelo Git; preservar para entrega, sem adicioná-lo ao commit.
Não vem em clone; reconstruir com python3 tools/build_release.py quando necessário.
Após essas verificações, somente documentos de registro/passagem foram alterados;
reaproveitar as evidências enquanto código/assets/entradas pertinentes forem válidos.
Conferência de fechamento: links locais, fila/tickets e git diff --check, esperado
código 0 sem diagnóstico. Nenhuma nova suíte/build é exigida por esta passagem.

Não houve execução do governador, agente no consumidor real, prompts em sessão
nova, piloto no tax ou CI remota nova. O piloto está sendo conduzido pelo mantenedor;
não atribuir sua conclusão aos testes locais. A CLI não executa código/testes do
consumidor e não intercepta todas as ações livres de IA.

### Git e preservação
O conjunto autorizado para commit inclui fontes, código da CLI, testes, recursos
instalados (.agents/.claude, .codex/rules, .sdd, docs/padroes e blocos dos agentes),
documentação, T-017 atualizado, T-018 a T-022 e validações T-017/T-019/T-020/T-021.
Esses tickets/relatórios e a regra nova estavam sem rastreio antes do commit;
não excluir por essa condição. Base de trabalho antes do fechamento: 28bc1b7.

TemporaryDirectory de consumidores/pacotes/regras de teste foram descartados;
nenhum serviço de teste iniciado. Preservar tests/, fixtures, relatórios e pacote.
Cópias recuperáveis mantidas: /tmp/sdd-antes-t019-dvshuhwj,
/tmp/sdd-antes-t017-ikkevqz2 e /tmp/sdd-antes-t020-t021-pucsm1o0.
O checkpoint anterior integral foi preservado em /tmp/sdd-antes-encerramento-h3_hfw9j/CHECKPOINT.md antes de
consolidar esta passagem; manter recuperável enquanto necessário. Não remover
outras cópias /tmp/sdd-antes-* ou recursos antigos por rotina. A preparação Windows
em /tmp/sdd-t002-correcao-87e5v59u foi registrada anteriormente em T-002; sua evidência
durável está no ticket e na branch isolada, não depende do temporário.

## Decisões e pendências
1. T-018: definir origem GitHub, política de versão e procedimento para init/update
   sem checkout local; autorizar o escopo concreto antes de implementar.
2. T-022: Design pretendido pelo mantenedor é Design System (telas, padrões visuais
   e cores), diferente do design técnico atual. Planejar objetivo, objetos, condição
   de aplicação, critérios de pronto e relação com os demais itens; preservar o
   conhecimento técnico existente ao definir seu destino. Registro solicitado
   depois de T-020/T-021; não houve alteração do item Design ou de seu template.

Ambas têm priority 100, sem dependências técnicas; empate pelo caminho completo
mantém T-018 antes de T-022. Não inferir prioridade pelo ID nem usar preferência
como dependência técnica. Só executar tasks autorizadas, sem impedimentos; não
interromper trabalho ativo por rotina.

O piloto no tax permanece com o mantenedor. Publicação/release, licença e memória
continuam adiadas. Correção Windows já concluída em T-002: commit isolado
5e4f530edaa049722f1ddcd7ea8772f2623a2c49, branch codex/t002-windows-utf8,
CI 42938396599 aprovada nos seis jobs Windows/Ubuntu/macOS com Python 3.11/3.14.
Correções equivalentes estão na main local; merge formal da branch isolada não é
pendência técnica e não está autorizado. Essa CI não certifica as mudanças desta sessão.

ADR-003 substitui a arquitetura antiga; ADR-001/002 são históricas. Conhecimento e
resultados de T-001 a T-016 estão nos tickets, incluindo a preservação literal do
ROADMAP anterior em T-016. Governador contém instruções, sem relatório particular.
.sdd/execucao.json formato 2 guarda installed/applied/baseline, completed binário,
evidence/remaining e pending consolidado; somente update administra installed e
.sdd/manifest.json. Não editar hashes para esconder conflito nem concluir por
arquivo/status/hash. Preservar evidências válidas e tratar só critérios faltantes
ou alterações pertinentes/impactos diretos. Fontes canônicas são os assets; recursos
instalados são atualizados pela CLI, sem copiar conteúdo particular a consumidores.

Preferência de comunicação do mantenedor: dizer explicitamente se a mudança foi
incorporada à distribuição, se é entregue via init/update e como foi validada em
consumidor. Evitar apenas “fontes sincronizadas”. Toda orientação de registro deve
nomear arquivo/campos e reutilizar a regra existente em vez de duplicá-la.

## Próximo passo
Retomar por AGENTS, este checkpoint, ROADMAP e tickets, confrontando Git e arquivos.
Definir T-018 ou discutir T-022 conforme orientação do mantenedor; não implementar
por mera retomada nem reabrir tarefas concluídas. Não executar no tax ou acionar o
governador automaticamente. Respeitar adiamentos, versão e autorização só local.

## Leitura para retomada
[AGENTS](AGENTS.md), [ROADMAP](docs/ROADMAP.md),
[T-018](specs/001-governador/tasks/T-018.md),
[T-022](specs/001-governador/tasks/T-022.md),
[T-019](specs/001-governador/tasks/T-019.md),
[T-017](specs/001-governador/tasks/T-017.md),
[T-020](specs/001-governador/tasks/T-020.md),
[T-021](specs/001-governador/tasks/T-021.md),
[validação T-020](specs/001-governador/validation/T-020.md),
[validação T-021](specs/001-governador/validation/T-021.md),
[T-002](specs/001-governador/tasks/T-002.md),
[T-016](specs/001-governador/tasks/T-016.md),
[governador](docs/governador.md), [contratos](docs/padroes/CONTRATOS.md),
[skill](.agents/skills/sdd/SKILL.md), [PRD](docs/PRD.md),
[SPEC](specs/001-governador/SPEC.md) e [ADR-003](docs/decisions/ADR-003.md).
