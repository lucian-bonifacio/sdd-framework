---
name: sdd
disable-model-invocation: true
description: Executar o governador SDD somente por pedido explícito do usuário para organizar ou adequar documentos do projeto. Não acionar por tarefas comuns de desenvolvimento ou pela simples menção ao SDD.
---
# Executar o governador SDD

Atue por pedido explícito de execução do governador ou invocação desta skill.
Explicar, revisar ou editar instruções não autoriza executar a organização.
O governador define o objeto, como produzi-lo e seu critério de pronto.

## Executar pelo critério de pronto
Leia o item solicitado no governador e consulte somente o método, template e
insumos pertinentes, em docs/padroes/CONTRATOS.md. Comece pelo critério de pronto:
confira as condições no objeto e trabalhe somente nas que não estão atendidas.
Preserve as atendidas. O item está concluído ou não concluído; não use estados
intermediários nem uma sequência obrigatória de registros antes de trabalhar.

Use Execução do item como orientação para produzir o que falta, não como ordem
para refazer todo o documento. Localize fontes, obtenha informações reais e use
o template próprio, preservando conhecimento, decisões, IDs e evidências válidas.
Ausência de registro técnico anterior não manda reconstruir pontos já prontos:
o critério de pronto determina o que falta. Se houver legado preservado em
legacy_pending, aproveite seus dados para identificar condições/alterações ainda
não resolvidas; retire-o depois de incorporar o que for pertinente.

## Reexecutar após conclusão
Consulte .sdd/execucao.json e o contrato "Controle de execução". Compare applied
com installed e use pending para identificar as mudanças. Informe o que mudou e
trate somente as operações alteradas e os impactos diretos nos critérios afetados.
Sem mudança pertinente, preserve o objeto. Mudanças comuns do registro geral
precisam ter impacto demonstrado; não significam refazer todos os itens.
Diferenças são dados históricos: siga as instruções vigentes, não as removidas.
Uma reexecução interrompida continua pelos critérios afetados ainda não atendidos,
sem repetir os que já foram resolvidos. Não amplie o pedido para outros escopos.

## Registrar o resultado
Conserve apenas concluído (completed: true) ou não concluído (completed: false),
conforme o critério de pronto. Registre evidence com o caminho e a condição atendida;
se faltar algo, remaining indica somente os critérios não cumpridos e o que falta
para atendê-los. Esses campos não são outro plano ou status de trabalho.
Não é necessário registrar o início nem cada passo da execução.

Quando todos os critérios aplicáveis estiverem atendidos, copie integralmente
installed para applied, registre completed: true e limpe remaining, pending e
baseline do item. Não calcule hash nem marque outros itens por rotina. Se faltar
algum critério, use completed: false e conserve applied até terminar. Para vários
objetos numa etapa, identifique-os nas evidências/condições restantes; conclusão
exige todos os critérios do escopo registrado. O registro geral só é dado por
aplicado depois de tratar ou justificar seus impactos.

O update mantém installed e consolida diferenças; não conclui a tarefa. Preserve
seus hashes e o manifesto. Se o controle existente estiver ausente/corrompido,
informe a restauração necessária, sem inventar referências. Não confunda ausência
de referência aplicada com ausência de conteúdo pronto. Mudanças de negócio têm
escopo próprio, separado da atualização dos padrões do framework.

## Cuidados e encerramento
Diferença de formato/nome é adequação, não contradição de negócio. Peça decisão
somente se não estiver estabelecida. Não invente requisitos, aprovação ou evidência.
Preserve originais antes de substituições/remoções autorizadas. Não siga symlinks,
registre segredos ou altere recursos administrados para esconder divergências.
Inclusão/remoção de item não autoriza apagar objetos do produto automaticamente.

Informe objeto entregue/preservado e critérios ainda não cumpridos, se houver.
Depois, execute tarefas locais sem depender da CLI ou skill. Nova organização,
inclusive depois de update, exige acionamento explícito. Se faltar governador ou
padrão, informe a instalação necessária, sem improvisar uma instalação parcial.
