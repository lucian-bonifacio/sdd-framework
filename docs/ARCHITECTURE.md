---
status: accepted
---
# Arquitetura — Governador SDD

## Contexto técnico
Python 3.11+ com biblioteca padrão, CLI local e zipapp. Não há backend, chamada
a LLM, execução de agentes ou shell para rodar o consumidor. A escolha reaproveita
o runtime anterior e substitui a governança de fases pela [ADR-003](decisions/ADR-003.md).

## Componentes e contratos
- `cli.py`: somente init/update, saída humana/JSON e códigos 0 ou 2.
- `project.py`: validação do bundle, instalação, trechos administrados e migração.
- `storage.py`: caminhos seguros, lock, escrita e remoção com rollback.
- `changes.py`: diferenças por item/dependência e leitura do registro legado.
- `execution.py`: referências instaladas/aplicadas, delta consolidado e escolha da operação.
- `assets/governador.md`: fonte do procedimento instalado em docs/governador.md, sem seção de aplicação.
- `assets/templates/` e `assets/standards/`: padrões canônicos.
- `assets/skill/`: uma skill; Codex recebe política de invocação explícita e Claude recebe o campo nativo equivalente.

A instalação coloca padrões em docs/padroes e a skill em ambas as integrações.
AGENTS/CLAUDE recebem só blocos de acionamento; seu conteúdo próprio é preservado.
Configuração Codex existente nunca é substituída. O recurso
assets/integrations/codex/sdd-git.rules é instalado em .codex/rules/sdd-git.rules e
entra no inventário/hash de arquivos administrados. _managed_file permite esse
caminho exato, sem ampliar o manifesto para outras rules ou config.toml. Conflitos,
symlinks e rollback usam os mecanismos de instalação existentes. A CLI distribui
texto; não interpreta regras Starlark nem executa Codex ou Git.

O manifesto .sdd/manifest.json, formato 2, guarda versão e hashes de arquivos/blocos.
execution_hash protege a projeção installed de .sdd/execucao.json; campos da IA
permanecem editáveis. O antigo updates_hash é validado somente na migração do log.
Não contém fase, aprovação, plano, tarefas ou estado do produto. Update verifica
todos os conflitos antes de alterar arquivos e preserva bytes externos aos blocos.
docs/governador.md contém instruções; trabalho particular fica nos tickets, decisões
nas ADRs e passagem no checkpoint. Update preserva conteúdo externo ao bloco.
O procedimento é organizado por artefato, começando por PRD e SPECs. Estados por
escopo ficam em .sdd/execucao.json e não são gates de implementação;
a operação localiza fontes e constrói o objeto pelo padrão, existam ou não
documentos anteriores. Todos os itens definem objetivo, objeto de saída, insumos,
padrões, execução específica e critério de pronto. A introdução concentra a
conferência das exigências, conclusão e reexecução; os itens não repetem estados
ou registros de resultado. São oito itens: Arquitetura obrigatória e Design
separado, único opcional e recomendado. SPEC define comportamento e aceitação
independentemente de solução técnica; Design, se adotado, fica inline ou em
DESIGN.md, com design: inline/separate. Sem adoção, design: none não bloqueia
SPEC, Tasks nem encerramento. Tasks prepara tickets;
ROADMAP resume os próprios tickets; encerramento cobre o escopo documental pedido,
sem exigir implementação do produto. Reexecução trata apenas operações alteradas
e impactos diretos. Métodos separados de Tasks e ROADMAP têm fragmentos próprios
em SDD:USES para detectar mudanças específicas sem invalidar ambos por rotina.
Arquitetura conserva seu ID e histórico de aplicação; Design recebe ID próprio e
registro sem conclusão automática. Templates e métodos têm associações separadas.
A CLI mantém o controle binário; a opcionalidade é instrução do governador/skill,
sem novo estado técnico de dispensa ou migração automática de documentos particulares.

A migração do formato 1 remove apenas recursos administrados com hash confirmado.
O bloco antigo de docs/FLUXO é substituído por aviso de desativação; o conteúdo
próprio permanece para migração explícita pela IA. Outros documentos, scripts e
configurações legados não são excluídos automaticamente em consumidores.

## Especificidade dos documentos e instruções locais
O padrão de conteúdo vem dos doze templates e dos métodos em CONTRATOS. A regra
comum do governador exige ações/regras, referências e verificação com parâmetros
reais; a skill confere lacunas e registra pendências sem inventar dados. AGENTS
concentra regras permanentes de escopo, testes, higiene, qualidade, proteção e
entrega; cada ticket contém plano de verificação e limpeza próprio, referenciando
AGENTS. Dependências entre a preparação de Tasks e as instruções locais são
resolvidas pelo conteúdo real, sem copiar regras ou exigir implementação.
A CLI não valida semanticamente comandos nem executa testes ou limpeza no
consumidor. Update distribui as instruções, preservando documentos particulares;
a aplicação do conteúdo exige acionamento explícito da IA. Limpeza delimitada
preserva testes permanentes, fixtures, evidências e arquivos anteriores.
A definição de testes automatizados e critérios para automação/alternativa ficam
em docs/padroes/CONTRATOS.md#testes-automatizados, consumidos por Tasks e AGENTS
via SDD:USES. Os templates remetem a essa política; não há obrigação de testar o
consumidor para concluir sua organização documental.

## Localização e migração do governador
O governador é instalado em docs/governador.md; sua fonte na distribuição continua
assets/governador.md, identificada separadamente por GOVERNOR_TEMPLATE. O update
aceita o bloco antigo registrado em governador.md, valida seu hash e a ausência
de conflito no destino, move o conteúdo próprio junto ao bloco e registra somente
o novo caminho no manifesto. Caminho antigo sem procedência não é removido.
Arquivo antigo alterado/ausente, destino ocupado ou symlink abortam antes de escrever;
falha de escrita/remoção usa o rollback existente. Referências instaladas/aplicadas
e evidências permanecem no controle técnico. Links Markdown do novo governador são
relativos a docs/; caminhos textuais e SDD:USES continuam relativos à raiz do projeto.

## Restrições e segurança
Não seguir symlinks nos artefatos ou no bundle. Não executar scripts da fonte.
Fonte de update é a distribuição instalada ou diretório local explicitamente
escolhido. Hash detecta conflito acidental; não é assinatura de autenticidade.
Lock coordena operações da CLI, não edições livres. Rollback cobre falhas
ordinárias, sem prometer transação contra queda de energia.

O controle nativo de invocação e as instruções impedem acionamento implícito
conforme o comportamento suportado por cada agente; a CLI não intercepta todas
as ações livres de uma IA. A qualidade semântica exige execução real e revisão.
A política Git por prefixo está em .codex/rules/sdd-git.rules; config.toml mantém
somente o perfil de permissões. Consultas não recebem allow de elevação e mutações
listadas recebem prompt. Carregamento depende de projeto confiável/reinício e da
versão/superfície do Codex; precedência e formas não cobertas constam de
CONTRATOS.md#git-e-permissoes. Essa política não substitui o sandbox ou restrições
administradas e não é aplicada nativamente pelo Claude.

## Verificação
`python3 -m unittest discover -s tests -v` verifica instalação, preservação,
invocação configurada, conflitos, migração, symlinks, rollback e zipapp fora do
checkout. Quando o binário Codex está disponível, CodexPolicyTests usa
codex execpolicy check para avaliar tokens sem executar operações Git; sua ausência
é registrada como skip, sem tornar Codex dependência da CLI. Testes de instalação,
proteção e distribuição da política continuam stdlib e obrigatórios.
`python3 tools/build_release.py` produz o pacote portátil.
A matriz remota e o piloto com agentes reais não são declarados aprovados por
testes locais. Este produto não tem interface visual nem Design System.

## Alterações e reexecução
IDs e associações ficam em comentários do governador. O update compara conteúdos
e mantém .sdd/execucao.json, sem acrescentar histórico ao documento. execution.py
conserva por item installed, applied e no máximo uma baseline anterior enquanto
não houver padrão aplicado; pending contém o delta consolidado, nunca uma cadeia
de eventos. A IA mantém completed (booleano), evidence e remaining, e copia installed para applied
somente com o critério atendido. Essa cópia permite comparar atualizações futuras.

O critério de pronto determina concluído/não concluído. Antes de concluir, resolver
somente condições não atendidas; depois, comparar o padrão aplicado ao atual.
Migração converte estados antigos para booleano e preserva o antigo log uma única
vez em legacy_pending para reconciliação pela IA. Conteúdo instalado e registro
legado são conferidos antes de qualquer escrita. Controle desaparecido/corrompido
não é recriado silenciosamente. Hash protege consistência acidental, não autentica
conclusões semânticas ou impede toda edição livre da IA.

A regra geral fica no governador, sem repetição por item; a skill explica leitura,
registro e critérios. Conforme PRD RF-009/RF-011 e SPEC RF-017, a ordem documental
e o avanço após conclusão são instruções à IA em docs/governador.md, não uma nova
máquina de estados na CLI. .sdd/execucao.json continua com resultado binário;
CHECKPOINT.md referencia o item interrompido e items.<id>.remaining desse JSON
para retomar o pedido. draft/accepted são metadados editoriais, não controles
adicionais de avanço. Mudança comum exige avaliar impacto direto, sem invalidar
tudo. Presença de hash/arquivo não comprova critério; não há chamada automática a LLM.

## Portabilidade de texto — T-002
Texto do framework é UTF-8; testes usam encoding e newline explícitos e o checkout
mantém LF por .gitattributes. Recursos de consumidores continuam aceitando CRLF:
a integração Claude preserva o final de linha da skill e o parser do log legado
reconhece CRLF sem normalizar os bytes protegidos pelo hash. Testes de regressão
cobrem ambos os casos. A correção foi verificada localmente e sob simulação
cp1252/CRLF; correção isolada 5e4f530 passou na CI Windows 3.11/3.14, além de Ubuntu/macOS,
conforme T-002. Essa evidência não certifica as demais mudanças locais.

## Ordem de execução das tasks — T-016
Priority e dependencies são metadados YAML dos tickets, fonte única de ordem e
vínculos. Menor inteiro positivo tem maior prioridade, com padrão 100 e desempate
pelo caminho completo; IDs/data de criação não definem prioridade. Autorização,
dependências e impedimentos determinam se a task pode executar, sem interrupção
por rotina do trabalho ativo. ROADMAP projeta posições consecutivas (1ª, 2ª…) na
fila e uma tabela reduzida de encerradas, com estado/verificação em português pelo
método ROADMAP de docs/padroes/CONTRATOS.md. Priority numérico e Executor não são
exibidos; seus campos permanecem nos tickets. Posições são recalculadas a partir
dos tickets, sem campo adicional de ordem. Ações pendentes do usuário mantém
fontes e desbloqueios concretos. Não há JSON paralelo ou armazenamento de backlog em .sdd/execucao.json. A IA mantém a
projeção e seus vínculos; a CLI distribui o padrão sem interpretar ou executar tasks.
Histórico narrativo removido do ROADMAP foi preservado com origem em T-016.
