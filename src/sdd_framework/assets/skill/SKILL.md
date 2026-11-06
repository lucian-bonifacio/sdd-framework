---
name: sdd
description: Organizar projetos novos ou existentes no fluxo SDD, manter documentos e tickets, avaliar a INBOX e registrar ou retomar CHECKPOINTs quando o projeto adota este framework.
---
# SDD

Leia o AGENTS.md do consumidor. O framework governa planejamento e documentação;
o agente executor implementa segundo as instruções e autorizações do projeto.
Não adote uma stack ou regra de negócio por padrão.

## Inicie
1. Leia [o fluxo](references/WORKFLOW.md) e [os contratos](references/ARTIFACTS.md).
2. Se `.sdd/config.json` não existe, execute `sdd init .`; se a CLI não estiver
   disponível, informe como instalá-la pelo README do framework. Não improvise
   uma instalação incompleta nem altere configurações globais de agentes.
3. Leia `.sdd/adoption/TASKS.md` e os tickets correspondentes. Em projeto existente,
   inventarie código, testes e documentos equivalentes antes de propor migração.
4. Preencha os artefatos progressivamente a partir das evidências do projeto e
   da conversa. Use `.sdd/framework/templates/`. Modelos vazios não contam como
   conformidade. Não renomeie ou sobrescreva documentação existente sem avaliar
   referências e preservar o conteúdo.
5. Confira os critérios da etapa no fluxo e os artefatos locais. Resolva
   impedimentos mecânicos e revise decisões relevantes com o usuário. A CLI pode
   auxiliar uma conferência solicitada, mas sua execução não é um gate obrigatório.

## Continuidade
Ao retomar, leia CHECKPOINT.md se existir, reconcilie-o com os arquivos e tickets
atuais e consulte a INBOX. Memória e propostas não aprovam requisitos.
Escolha tarefas prontas e autorizadas por dependência; prossiga até concluir o
escopo autorizado ou ficar sem trabalho independente disponível. Não peça
novamente uma autorização já registrada. Escopo adicional não herda aprovação.
Depois de alterar tickets, execute `python3 scripts/atualizar_roadmap.py` na raiz
do consumidor, confira a saída e o diff. O script pertence ao projeto e funciona
com biblioteca padrão, sem pacote ou repositório SDD disponível. Preserve
planejamento, links, estados e ações humanas. Em falha, investigue ou atualize
pelas ferramentas habituais conforme AGENTS.md, sem inventar sucesso.

Para tarefa humana ou conjunta, prepare o necessário, registre exatamente a ação
do usuário, evidência esperada e dependentes. Marque `awaiting_user`, mantenha a
parte já realizada e execute tarefas independentes. Nunca simule uma resposta.

## Checkpoint e INBOX
Quando solicitado ("gere um checkpoint", "vou encerrar", "salve para retomar"),
atualize o CHECKPOINT com o estado real, inclusive trabalho parcial. Não invente
resultados nem espere um encerramento inesperado para salvar todo o conhecimento.
Registre fatos duradouros no destino correto durante o trabalho.
Pesquisa ou decisão ainda em avaliação recebe um ITEM na INBOX; incorporação e
descarte mantêm fonte, motivo e referência de destino.

## Conferência e atualização
"Conferência" revisa documentos e critérios de consistência. Se a CLI estiver
disponível, `sdd check .` pode auxiliar; `--fix` cria tickets de adequação sem
fabricar documentos aprovados. Sua ausência não impede revisão pelos arquivos.
"Update" atualiza recursos do framework com `sdd update .`; nova versão exige
fonte explícita conforme README. Update é manutenção opcional do framework.
Atualizações não reescrevem PRD, SPECs, tickets ou decisões do consumidor.
Relate separadamente a verificação estrutural e a revisão semântica.
O agente usa o script local para consolidar tarefas e ações humanas no ROADMAP;
os estados são editados somente nos tickets. `sdd check --roadmap` é auxiliar opcional de
conferência explícita, nunca dependência de execução do consumidor. Resultado com
critérios, testes e revisões aplicáveis atendidos pode ser concluído sem aceite
manual adicional, salvo dependência humana explícita no ticket.
