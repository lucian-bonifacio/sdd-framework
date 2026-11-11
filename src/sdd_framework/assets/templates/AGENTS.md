# Instruções para agentes — {{project}}

## Contexto do projeto
[PREENCHER: propósito, áreas de código e links reais para PRD, arquitetura, roadmap e tickets; indicar a fonte vigente quando houver histórico concorrente.]

## Escopo e execução
Leia o ticket e as fontes pertinentes à mudança; confira arquivos e alterações
existentes antes de editar. Execute o escopo autorizado e preserve trabalho do
usuário. Não transforme sugestões ou código existente em requisitos aceitos. Selecione a
próxima task autorizada e sem impedimentos pela menor priority do ticket; em empate,
use seu caminho completo. Respeite dependencies, bloqueios e ações humanas, mesmo
quando uma task criada depois tiver prioridade maior. Não interrompa trabalho
ativo por rotina nem use a ordem do ID como prioridade.
[PREENCHER: como localizar a tarefa, suas dependências e as autorizações do projeto.]

## Comandos e verificações
[PREENCHER: para cada verificação, indicar finalidade, comando real ou procedimento manual reproduzível, diretório, pré-requisitos, quando executar e resultado esperado. Distinguir testes durante a implementação das verificações exigidas para concluir; apontar arquivos/configurações que definem esses comandos e registrar impedimentos reais.]

Use o plano de verificação do ticket. Execute as verificações pertinentes durante
a mudança e as exigidas pelo projeto antes de concluir. Crie testes permanentes
quando necessários para demonstrar comportamento ou evitar regressões; cubra
falhas e limites relevantes. Reaproveite resultados enquanto código, entradas e
ambiente pertinentes permanecerem válidos; repita ou amplie por mudança, falha ou
lacuna identificada, sem dispensar checks obrigatórios. Não declare sucesso em
verificação não executada; registre resultado, evidência e limitação no ticket.

## Higiene do workspace
[PREENCHER: diretórios permitidos para temporários, comandos de limpeza com alvos delimitados e como identificar processos, serviços ou recursos de teste da própria execução; indicar o que deve ser preservado.]

Remova apenas temporários descartáveis criados pela própria execução e encerre
os processos ou serviços iniciados para a tarefa quando não forem mais necessários.
Preserve testes permanentes, fixtures úteis e evidências necessárias; arquivos
anteriores ou de origem desconhecida não são descartáveis por estarem sem rastreio
no Git. Confira origem e destino antes de limpar; não use exclusões abrangentes
para obter um workspace aparentemente limpo. Ao interromper, registre recursos
que ainda precisem ser encerrados ou removidos e a ação concreta para isso.

## Qualidade e convenções
[PREENCHER: convenções reais de nomes, módulos e tratamento de erros, ferramentas de formatação/análise e seus comandos ou links; apontar limites arquiteturais e Design System quando disponível.]

Siga os contratos da arquitetura e as convenções dos arquivos afetados. Use nomes
que revelem a função e responsabilidades delimitadas; evite duplicação de regras,
abstrações sem necessidade demonstrada e refatorações alheias ao ticket. Remova
código obsoleto somente quando ligado à mudança e após preservar o comportamento
necessário; não deixe implementação incompleta apresentada como funcional.

## Proteção e autorização
[PREENCHER: áreas/dados protegidos, ambientes permitidos, política real de dependências e ações que exigem autorização específica no projeto.]

Preserve alterações particulares, configurações e decisões vigentes. Não registre
segredos em arquivos, logs ou evidências. Não altere configuração global, introduza
dependências sem necessidade demonstrada nem faça commit, push ou publicação por
rotina. Respeite autorizações já dadas e peça decisão somente para o que estiver
fora delas. Não siga symlinks para escrever ou remover arquivos.

## Documentação e entrega
Atualize documentos afetados e o resultado do ticket; reflita prioridade, dependências e estado no ROADMAP,
sem duplicar evidências. Informe o que mudou, como foi verificado, limitações e
pendências reais. Prepare CHECKPOINT quando houver passagem ou interrupção, com
próxima ação e referências suficientes para retomar.
[PREENCHER: caminhos e convenções locais de documentação e evidências; referenciar docs/padroes/CONTRATOS.md para manutenção documental.]

Preserve o bloco administrado de acionamento explícito de docs/governador.md.
Incorpore instruções compatíveis do projeto e somente processos divergentes
especificamente autorizados. Atualize comandos e convenções quando o trabalho
os afetar. Não inicie o governador ao abrir uma sessão ou executar tarefa comum;
após a organização, continue pela execução independente do projeto.
