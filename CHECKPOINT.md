---
status: active
updated: 2026-11-10
task: specs/001-governador/tasks/T-017.md
---
# Checkpoint — Encerramento da sessão e revisão pendente do ROADMAP

## Objetivo e tarefa atual
Sessão encerrada com versão 0.4.2 mantida. T-001 a T-016 concluídas; T-017
registrada como pending, executor joint e authorization pending. O mantenedor
não gostou da apresentação de T-016, especialmente das colunas Prioridade e
Dependências/impedimentos. Registrar a pendência não autoriza escolher e implementar
outro layout agora. ROADMAP marcado draft; não considerar sua apresentação final aceita.

O pedido atual autoriza um commit local de todos os ajustes desta sessão, incluindo
este checkpoint, a pendência T-017 e a movimentação de governador.md. Não autoriza
push desse conjunto, merge da branch Windows ou release. Consultar git log/status
para confirmar o commit; este arquivo não tenta registrar seu próprio hash.

## Estado do trabalho
- T-011: conferência e conclusão centralizadas em passos nas regras gerais. Usar
  “exigências do critério de pronto”, evidências por caminho/seção/IDs e pendências
  com lacuna e ação; nenhuma conclusão por simples status, hash ou declaração.
- T-012: decisões do PRD aplicadas às demais seções, métodos, templates e skill.
  Cada item tem objetivo, objeto de saída, requisitos/insumos/padrões, execução
  específica e critério de pronto. Regras comuns não se repetem nos itens.
- T-013: oito itens. Arquitetura obrigatória no item 3; Design opcional e recomendado
  no item 4, único item opcional do fluxo. SPEC aceita design none/inline/separate;
  ausência de Design não bloqueia os demais nem autoriza apagar conhecimento.
- T-014: doze templates revisados para conteúdo concreto. AGENTS concentra contexto/
  escopo, verificações, higiene, qualidade, proteção e entrega com parâmetros locais.
  Tasks detalham cenários, comandos/procedimentos, diretórios, pré-requisitos,
  resultados esperados, evidências e limpeza. Testes permanentes, fixtures úteis,
  evidências e trabalho anterior são preservados. Informação indispensável ausente
  é pendência, sem inventar parâmetros. AGENTS deste projeto também foi ajustado.
- T-015: governador instalado em docs/governador.md por padrão e já movido neste
  projeto por update. Fonte permanece src/sdd_framework/assets/governador.md.
  Migração valida o caminho antigo registrado, recusa alterações/ausência, destino
  ocupado ou symlinks, preserva conteúdo próprio e tem rollback. Arquivo antigo sem
  procedência não é removido. Links Markdown partem de docs/; caminhos textuais e
  SDD:USES partem da raiz. AGENTS/CLAUDE, skill e referências foram alinhados.
- T-002: pendência Windows encerrada após autorização expressa de antecipar a
  investigação, sem declarar o piloto concluído. Corrigidos encoding implícito
  dos testes, tradução de newline das fixtures, injeção Claude com CRLF e leitura
  do registro legado CRLF sem alterar bytes protegidos pelo hash. .gitattributes
  mantém LF no checkout; consumidores continuam aceitando CRLF.
- T-016: ROADMAP passou a fila e encerradas, com priority/dependencies nos tickets
  YAML, menor inteiro positivo primeiro, padrão 100 e desempate por caminho.
  Prioridade não ignora autorização, dependência ou impedimento. Tickets anteriores
  preservados e alias depends_on normalizado. Histórico narrativo retirado foi
  preservado literalmente no próprio T-016. Templates, contratos, skill e governador
  sincronizados por update, sem JSON paralelo. A implementação está concluída,
  mas o mantenedor pediu nova revisão visual em T-017; não repetir o layout por rotina.

A CLI foi instalada/atualizada, mas o governador não foi executado nesta sessão.
Os documentos reais, inclusive ROADMAP e tickets, já são usados e mantidos
normalmente; não dependem de um acionamento completo para “entrar em funcionamento”.

Evidência remota de T-002: commit 5e4f530edaa049722f1ddcd7ea8772f2623a2c49 na
branch autorizada codex/t002-windows-utf8, sobre 48d13f1. Somente .gitattributes,
changes.py, project.py e tests/test_framework.py foram enviados. CI 42938396599
passou nos seis jobs Windows/Ubuntu/macOS com Python 3.11/3.14; cada job Windows
executou 50 testes e build. Essa CI certifica o commit isolado, não todo o conjunto
local desta sessão. Não houve merge/release. A correção equivalente está no checkout.

Verificação local final de T-016: 56 testes passaram (6,171 s), pacote reconstruído
e verificado por init/update fora do checkout. Update idempotente; campos da IA
preservados nos nove registros. Dezesseis tickets com dependências válidas sem
ciclos, tabela e histórico conferidos. Desde então, as alterações são documentais:
registro de T-017, sinalização da apresentação não aceita e fechamento da sessão.
Reaproveitar essas evidências enquanto código/assets/ambiente pertinentes forem válidos.

Dist/sdd.pyz é gerado e ignorado pelo Git; não vem no clone. Gerar com
python3 tools/build_release.py quando necessário. Consumidores/pacotes temporários
de teste foram descartados; cópias de preservação /tmp/sdd-antes-* e o diretório
isolado /tmp/sdd-t002-correcao-87e5v59u foram mantidos para recuperação/revisão.
O resultado e a continuidade estão nos arquivos e tickets, não dependem dessas cópias.

## Decisões e pendências
Controle em .sdd/execucao.json, formato 2: installed/applied guardam hash e conteúdo;
baseline limita a referência anterior quando não há applied; completed é booleano;
evidence comprova as exigências atendidas, remaining indica apenas as faltantes e
pending consolida diferenças. Update mantém installed sem concluir aplicação;
a IA copia para applied somente após cumprir critérios. execution_hash protege
installed no manifesto; não adulterar hashes para esconder conflitos. Legacy_pending
preserva uma única vez o registro antigo até reconciliação, sem inventar conclusões.

Critério de pronto é o ponto de partida: preservar conteúdo atendido e executar
somente o que falta. Após conclusão, tratar apenas alterações pertinentes do framework
e impactos diretos; sem mudança pertinente, preservar. Não separar projeto novo/
existente, adotar formato antigo como padrão alternativo ou refazer tudo por falta
de registro. Preservar conhecimento, decisões, IDs, configurações e evidências.

Fontes canônicas em src/sdd_framework/assets; cópias instaladas via update.
Uma skill SDD genérica em ambas as integrações. Padrões e métodos próprios;
referências externas são bibliografia de desenvolvimento, não dependência de execução.
Governador contém somente instruções, sem relatório de aplicação; ações/resultados
ficam nos tickets, decisões nas ADRs, resumo no ROADMAP e passagem no CHECKPOINT.
ADR-003 substitui a arquitetura operacional antiga; ADR-001/002 são históricas.

T-017 é a próxima pendência: rever apresentação do ROADMAP, principalmente Prioridade
e Dependências. Preservar prioridade/dependências nos tickets e histórico até definir
novo formato; a rejeição das colunas não autoriza remover esses dados. A revisão
futura deve alcançar os recursos pertinentes distribuídos aos consumidores.

Piloto no tax continua com o mantenedor, sem execução nesta sessão. Release,
licença e memória continuam adiadas. Autorização da branch isolada Windows não
permite merge ou outros envios. A autorização atual é somente para o commit local
do conjunto desta sessão; nenhum push novo foi solicitado.

## Próximo passo
Retomar por T-017 e perguntar ao mantenedor pelo formato desejado ou apresentar
uma proposta concreta antes de implementar nova apresentação. Não executar essa
revisão, o governador ou ações no tax por mera retomada. Conferir Git e arquivos
reais; não reabrir T-002 nem repetir correções já comprovadas sem motivo novo.

## Leitura para retomada
[AGENTS](AGENTS.md), [ROADMAP](docs/ROADMAP.md),
[T-017](specs/001-governador/tasks/T-017.md),
[T-016](specs/001-governador/tasks/T-016.md),
[T-002](specs/001-governador/tasks/T-002.md),
[governador](docs/governador.md), [contratos](docs/padroes/CONTRATOS.md),
[skill](.agents/skills/sdd/SKILL.md), [PRD](docs/PRD.md),
[SPEC](specs/001-governador/SPEC.md) e [ADR-003](docs/decisions/ADR-003.md).
Evidências detalhadas da sessão em T-011 a T-016.
