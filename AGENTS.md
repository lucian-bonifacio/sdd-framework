# Desenvolvimento do SDD Framework


## Contexto do projeto
Este repositório implementa uma ferramenta genérica de organização documental.
PRD e specs representam o contrato atual. IDEIA.md é contexto histórico, não
procedimento obrigatório. Responder ao mantenedor de forma breve e em português.

## Retomada de sessão
Antes de iniciar trabalho, ler CHECKPOINT.md da raiz se existir, mesmo sem acesso
à conversa anterior. Conferir seu estado com os arquivos, tickets e Git atuais;
o checkpoint orienta a retomada, mas não substitui as fontes vigentes.
Respeitar adiamentos e limites ali registrados. Não iniciar piloto, Release ou
publicação apenas porque uma sessão nova foi aberta; aguardar nova solicitação
do mantenedor quando essas ações tiverem sido adiadas. Ao pedido de checkpoint,
registrar trabalho parcial, resultados reais, pendências e próximo passo.

## Fontes de edição neste repositório

Este projeto desenvolve o framework e utiliza uma instalação local dele. Antes
de editar, identifique a finalidade da mudança:

| Mudança | Fonte correta |
|---|---|
| Comportamento da CLI ou verificações | Código em `src/sdd_framework/` |
| Template, skill ou regra entregue aos consumidores | `src/sdd_framework/assets/` |
| Requisito, arquitetura, decisão ou tarefa do próprio framework | `docs/` e `specs/` |
| Instrução operacional ou passagem de contexto deste projeto | `AGENTS.md` e `CHECKPOINT.md` da raiz |
| Configuração da instalação local | `.sdd/config.json` |
| Adequação deste repositório ao padrão | Tickets em `.sdd/adoption/tasks/` |

`.sdd/framework/` é uma cópia administrada das fontes em assets; não editar essa
cópia nem o manifesto para contornar conflitos. Depois de alterar recursos nas
fontes, sincronizar com `python3 sdd.py update .` e executar conferência.
Os tickets em `specs/*/tasks/` tratam da construção do produto, não da adoção local.

Estas instruções são específicas do desenvolvimento do SDD Framework. Não copiar
o README ou este AGENTS.md da raiz para consumidores; a distribuição usa os
templates, a skill e o bloco genérico produzidos pela implementação.

## Comandos e verificações
- Python 3.11+, biblioteca padrão no runtime; usar `python3 sdd.py` sem instalação.
- Testes: `python3 -m unittest discover -s tests -v`.
- Conferência: `python3 sdd.py check . --phase delivery`.
- Distribuição: `python3 tools/build_release.py`.
- Não executar código, comandos de testes ou deploy de consumidores pela CLI.
- Nunca sobrescrever documentos do consumidor, skills locais conflitantes ou
  conteúdo externo aos blocos administrados. Não seguir symlinks em artefatos.
- Não registrar segredos, instalar globalmente ou publicar pacotes por rotina.
- Recursos são mantidos em `src/sdd_framework/assets/`. Depois de mudar recursos,
  atualizar o snapshot do próprio projeto com `python3 sdd.py update .`.
  Não editar os recursos sob `.sdd/framework/` diretamente.
- Este checkout usa `agent: none` porque `.agents/` é somente leitura no ambiente
  de criação. Integrações Codex/Claude são testadas em consumidores temporários.
- O contexto de retomada está em CHECKPOINT.md; propostas pendentes em docs/inbox/.
  Estados ficam nos tickets; TASKS.md é índice. Requisitos novos precisam de
  avaliação de impacto, sem herdar autorização de implementação anterior.

## Convenções e restrições
Autorização e verificação são distintas. Conformidade estrutural não é aceite
semântico. Configuração deve permitir adoção progressiva, projetos existentes,
tarefas humanas, referências externas de Design System e independência operacional.
Não aumentar o número de skills sem necessidade: uma skill SDD genérica é a
interface atual. IA não transforma uma proposta de INBOX em requisito aceito.


<!-- SDD:START -->
## Fluxo SDD
Se `.sdd/framework/` existir, leia `skill/references/WORKFLOW.md` e
`skill/references/ARTIFACTS.md` dentro dele e use seus templates.
Sem esses recursos, continue pelos documentos e tickets do projeto;
instruções essenciais de execução devem estar neste AGENTS.md.
Consulte CHECKPOINT.md (se existir) ao retomar.
Comece pelas tarefas de `.sdd/adoption/TASKS.md`; depois siga docs/ROADMAP.md
e os tickets em specs/*/tasks/. Execute trabalho autorizado e pronto por
dependência, sem repetir pedidos de autorização. Ações humanas pendentes ficam
no ticket; prossiga com tarefas independentes. Propostas não aceitas vão para
docs/inbox/. Ao pedir pausa ou passagem de contexto, atualize CHECKPOINT.md.
## Continuidade independente
A CLI SDD não é requisito para executar tarefas ou manter os documentos. Leia
os tickets, verifique seus requisitos/dependências e execute os testes do próprio
projeto. Critérios de aceitação, testes e revisões aplicáveis atendidos permitem
concluir sem confirmação manual adicional, salvo ação humana exigida no ticket.
Não declare conclusão com checagens pendentes nem mude requisitos para aceitar código.

Depois de criar ou alterar um ticket, atualize diretamente o acompanhamento no
roadmap indicado pelo projeto (padrão: docs/ROADMAP.md). Leia todos os tickets
em specs/*/tasks/ e os de .sdd/adoption/tasks/ quando existirem. Use os estados
dos tickets; não os deduza da posição no roadmap ou de um resumo anterior.
Preserve entregas, prioridades e conteúdo fora do bloco SDD:PROGRESS. Atualize
ou crie esse bloco usando os marcadores HTML SDD:PROGRESS:START/END. Dentro dele:
- Cabeçalho: Acompanhamento das tarefas; data e contagem de concluídas/total.
- Um grupo por entrega e outro para adequação inicial, quando houver.
- Tabela: Tarefa (link relativo ao ticket), Trabalho, Estado, Execução, Verificação.
- Seção Ações pendentes do usuário: ticket, ação concreta e estado; escrever
  Nenhuma quando não houver. Incluir awaiting_user e trabalho humano ainda aberto.
- Manter bloqueios e ação de desbloqueio nos tickets, sem inventar respostas,
  aprovação humana ou resultado de testes. Tickets são a fonte; roadmap é resumo.
Após criar/alterar tickets, o agente executa `python3 scripts/atualizar_roadmap.py`
na raiz do projeto e confere a saída e o diff. Esse script autônomo pertence ao
consumidor e funciona sem pacote SDD ou .sdd/. Para caminho alternativo,
execute com --roadmap caminho/ROADMAP.md. Preserve customizações do script e não
o substitua automaticamente. Em erro, corrija a causa ou mantenha o resumo pelas
ferramentas habituais, sem declarar atualização que não aconteceu.
Use scripts locais para operações mecânicas definidas; análise de requisitos,
decisões e interpretação das evidências continuam com agente e usuário.
Ferramentas SDD são opcionais para manutenção
expressamente solicitada. Documentos e instruções locais sustentam a continuidade.
<!-- SDD:END -->
