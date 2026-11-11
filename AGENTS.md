# Desenvolvimento do SDD Framework

## Contexto do projeto
Ferramenta de organização documental para agentes de IA. Contrato vigente em
docs/PRD.md e specs/001-governador/SPEC.md. Responder ao mantenedor em português,
de forma breve. IDEIA.md é histórico, não procedimento ou requisito vigente.

As fontes distribuídas estão em src/sdd_framework/assets/. Recursos instalados
em docs/padroes/ e nas skills são administrados pela CLI; altere fontes e use update.
Não copiar README/AGENTS preenchidos deste repositório para consumidores.

## Comandos e verificações
Python 3.11+, runtime somente stdlib; executar sem instalação:

- Testes: `python3 -m unittest discover -s tests -v`, na raiz; sucesso exige saída
  OK e código 0. Durante mudanças de CLI/distribuição, selecione cenários de
  tests/test_framework.py; antes de concluir essas mudanças, execute a suíte.
- Build: `python3 tools/build_release.py`, na raiz; saída esperada dist/sdd.pyz.
  Reconstrua quando houver mudança no código ou nos assets distribuídos.
- Instalação/update: `python3 sdd.py init .` e `python3 sdd.py update .`, na raiz
  do alvo; sucesso exige código 0 e governador não executado. Para manutenção
  dos assets deste repositório, sincronize por update e confira idempotência.
- Governador: acionamento explícito pelo usuário na IA, não um comando da CLI.

Verifique instalação em consumidores temporários e o pacote portátil fora do
checkout. Não executar testes, código ou deploy do consumidor pela CLI.
Se a sincronização das integrações exigir permissão, use o terminal autorizado;
não contorne proteções nem altere hashes do manifesto para esconder conflito.

## Convenções e restrições
Leia CHECKPOINT.md ao retomar e confronte-o com arquivos e Git; respeite adiamentos.
Tickets são fonte de priority, dependencies, estado e evidências; ROADMAP apresenta
a fila e as encerradas, além de ações humanas. Menor priority vem primeiro entre
tasks autorizadas e sem impedimentos; empate usa o caminho completo. Respeite
dependências e não interrompa trabalho ativo por rotina. IDs não definem prioridade.
Use docs/padroes/CONTRATOS.md para manter documentos. Propostas em docs/inbox
não viram requisitos automaticamente. Requisitos novos exigem impacto e autorização.

Mudança em documento governado também exige adequação dos templates, contratos,
skill ou código pertinente para consumidores, sem copiar conteúdo deste projeto.
Uma skill SDD genérica em ambas as integrações; não adicionar skills sem necessidade.
Preserve conhecimento, decisões e configuração particular. Não seguir symlinks,
registrar segredos, alterar configuração global, publicar ou fazer commit/push
por rotina. Não executar ações no tax sem solicitação. Piloto a cargo do mantenedor;
A investigação Windows foi autorizada depois de T-015 e concluída em T-002 por
CI real na branch isolada codex/t002-windows-utf8. A autorização não inclui merge,
release ou envio das demais mudanças locais. ADR-003 substitui a arquitetura antiga.

## Escopo e qualidade
Confira ticket, dependências e Git antes de editar; preserve as mudanças anteriores
do mantenedor. Vincule o trabalho aos RF/CA da SPEC e mantenha funções de instalação,
comparação e armazenamento em seus módulos existentes de src/sdd_framework.
Para testes, aplique docs/padroes/CONTRATOS.md#testes-automatizados e os comandos
obrigatórios acima.
Use Python 3.11+ e stdlib, preservando estilos e nomes dos módulos afetados; não
adicione abstrações, comandos ou refatorações alheios ao ticket. Comente motivos
que não sejam evidentes no código. Testes permanentes devem verificar comportamento,
preservação ou falhas relevantes, sem apenas repetir o texto das instruções.

## Higiene do workspace
Use tempfile.TemporaryDirectory para consumidores, builds de teste e arquivos
descartáveis; encerre processos de teste próprios quando não forem necessários.
Limpe somente os alvos criados pela execução e identificados no ticket. Preserve
tests/, fixtures, evidências dos tickets e dist/sdd.pyz reconstruído para entrega.
Cópias /tmp/sdd-antes-* de alterações não commitadas permanecem recuperáveis
enquanto forem necessárias à preservação; registre o destino no ticket/checkpoint
antes de removê-las. Arquivo sem rastreio no Git não é autorização de exclusão.

## Documentação e entrega
Cada ticket deve prever cenário, procedimento/comando, diretório, pré-requisitos,
resultado esperado e evidência para seus critérios, além dos recursos temporários.
Antes de done, registre os resultados observados e limites; teste obrigatório não
executado continua pendência. Reaproveite evidências válidas e repita verificações
quando mudança, falha ou lacuna justificar, respeitando as verificações acima.
Atualize ROADMAP ao mudar tickets e CHECKPOINT na passagem/interrupção. Confira
git diff --check antes de entregar; resultado esperado é código 0, sem diagnóstico.

<!-- SDD:START -->
Execute docs/governador.md somente quando o usuário solicitar expressamente o
governador SDD ou invocar a skill SDD. Ler arquivos, abrir uma sessão e executar
init/update não acionam o governador. Quando acionado, siga a sequência e a regra
de avanço de docs/governador.md#obrigatoriedade-dos-itens.
Fora dessa execução, trabalhe nas tarefas autorizadas do projeto e mantenha seus
documentos atualizados. Para autorização de operações Git, aplique
docs/padroes/CONTRATOS.md#git-e-permissoes.
<!-- SDD:END -->
