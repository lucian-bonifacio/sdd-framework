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
- `assets/governador.md`: único procedimento dirigido à IA, sem seção de aplicação.
- `assets/templates/` e `assets/standards/`: padrões canônicos.
- `assets/skill/`: uma skill; Codex recebe política de invocação explícita e Claude recebe o campo nativo equivalente.

A instalação coloca padrões em docs/padroes e a skill em ambas as integrações.
AGENTS/CLAUDE recebem só blocos de acionamento; seu conteúdo próprio é preservado.
Configuração Codex existente nunca é substituída.

O manifesto .sdd/manifest.json, formato 2, guarda versão e hashes de arquivos/blocos.
execution_hash protege a projeção installed de .sdd/execucao.json; campos da IA
permanecem editáveis. O antigo updates_hash é validado somente na migração do log.
Não contém fase, aprovação, plano, tarefas ou estado do produto. Update verifica
todos os conflitos antes de alterar arquivos e preserva bytes externos aos blocos.
governador.md contém instruções; trabalho particular fica nos tickets, decisões
nas ADRs e passagem no checkpoint. Update preserva conteúdo externo ao bloco.
O procedimento é organizado por artefato, começando por PRD e SPECs. Estados por
escopo ficam em .sdd/execucao.json e não são gates de implementação;
a operação localiza fontes e constrói o objeto pelo padrão, existam ou não
documentos anteriores. No PRD, pronto/pendente é determinado pelo critério de pronto;
reexecução trata apenas operações alteradas e impactos diretos.

A migração do formato 1 remove apenas recursos administrados com hash confirmado.
O bloco antigo de docs/FLUXO é substituído por aviso de desativação; o conteúdo
próprio permanece para migração explícita pela IA. Outros documentos, scripts e
configurações legados não são excluídos automaticamente em consumidores.

## Restrições e segurança
Não seguir symlinks nos artefatos ou no bundle. Não executar scripts da fonte.
Fonte de update é a distribuição instalada ou diretório local explicitamente
escolhido. Hash detecta conflito acidental; não é assinatura de autenticidade.
Lock coordena operações da CLI, não edições livres. Rollback cobre falhas
ordinárias, sem prometer transação contra queda de energia.

O controle nativo de invocação e as instruções impedem acionamento implícito
conforme o comportamento suportado por cada agente; a CLI não intercepta todas
as ações livres de uma IA. A qualidade semântica exige execução real e revisão.

## Verificação
`python3 -m unittest discover -s tests -v` verifica instalação, preservação,
invocação configurada, conflitos, migração, symlinks, rollback e zipapp fora do
checkout. `python3 tools/build_release.py` produz o pacote portátil.
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
registro e critérios. Mudança comum exige avaliar impacto direto, sem invalidar
tudo. Presença de hash/arquivo não comprova critério; não há chamada automática a LLM.
