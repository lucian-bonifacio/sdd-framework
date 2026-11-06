---
status: accepted
---
# Arquitetura — SDD Framework

## Contexto técnico
Python 3.11+ e biblioteca padrão, com entrada de pacote e console `sdd`. Escolha
do [ADR-001](decisions/ADR-001.md). Pacote instalável via pyproject/setuptools em
ambientes com ferramentas de empacotamento; zipapp portátil sem dependências.
Não há backend, banco, MCP, chamada a LLM ou frontend obrigatório.

## Componentes e contratos
- `cli.py`: argparse, aliases PT-BR, JSON e códigos de saída.
- `project.py`: bundles, configuração, integração e atualização controlada.
- `storage.py`: caminhos restritos, lock e aplicação de arquivos com rollback.
- `markdown.py`: metadados YAML restritos e seções Markdown.
- `checks.py`: diagnóstico, dependências, cobertura, visão geral e tickets corretivos.
- `consumer_roadmap.py`: ferramenta autônoma entregue como scripts/atualizar_roadmap.py;
  somente biblioteca padrão, sem imports do framework. A CLI reutiliza seu renderizador.
- `assets/`: política declarativa, treze templates e uma skill com duas referências.

Configuração em `.sdd/config.json`; inventário/hashes em `.sdd/manifest.json`.
O CLI é centralmente instalável; cada projeto recebe snapshot versionado dos
recursos para portabilidade, leitura offline e evolução controlada. A atualização
central não altera todos os consumidores silenciosamente. O snapshot pode ser
desvinculado sem apagar documentos; esta versão não oferece comando detach.

Cada tarefa tem caminho global relativo, ID local T-NNN e referências à SPEC.
Codex recebe `.codex/config.toml` neutro quando ausente. O modelo está em
`assets/integrations/codex/config.toml`; o arquivo no consumidor não integra o
inventário de recursos sobrescrevíveis. A conferência usa tomllib (stdlib) para
validar TOML sem impor valores. Preflight verifica acesso de escrita antes de
aplicar arquivos; a CLI não contorna pastas protegidas por sandbox.
ROADMAP concentra acompanhamento derivado dos tickets, sem estados mantidos
manualmente em dois lugares. O agente é instruído pelo AGENTS/skill a executar
o script local do consumidor após alterações em tickets e conferir saída/diff.
A continuidade não exige pacote SDD, CLI, checkout ou configuração .sdd. A
conferência explícita produz texto/JSON; --roadmap é um auxiliar opcional.
Scripts locais existentes pertencem ao consumidor e são preservados pelo update.
Evidências extensas são vinculadas aos tickets. Scripts atendem operações
mecânicas bem delimitadas; análise e decisões continuam com agente/usuário.
Contratos detalhados: [WORKFLOW.md](WORKFLOW.md).

## Restrições e segurança
Sem shell para executar comandos do consumidor. Atualização remota somente de
fonte HTTPS/ref explícitas via Git, com timeout; lê dados do bundle sem executar
scripts. Política incompatível exige atualização da CLI; downgrade é recusado.
Fontes novas são material de instrução que o mantenedor deve revisar.

Hash de arquivo e bloco detecta conflito acidental; não é assinatura ou atestado
de autenticidade. Caminhos com travessia ou symlinks são recusados. Lock evita
operações CLI concorrentes. Rollback protege falhas ordinárias de escrita; não
há garantia transacional contra queda de energia nem sandbox de processos hostis.
Múltiplas sessões humanas/agentes devem coordenar Git/worktrees; o lock da CLI não
coordena edições livres do editor.

Design System é referência externa opcional, condicionada a interface existente;
este projeto não possui interface e registra `interface: false`.

## Verificação
Suite stdlib: `python3 -m unittest discover -s tests -v`. Conferência própria:
`python3 sdd.py check . --phase delivery`. Build: `python3 tools/build_release.py`.
Testes incluem consumidor novo/existente, conflitos, rollback, dependências,
trabalho humano, metadados, atualização e execução zipapp fora do checkout.
A CI configura matriz Linux/macOS/Windows com Python 3.11/3.14; execução local
comprovada consta em [ticket de distribuição](../specs/006-distribuicao/tasks/T-002.md), sem presumir CI remoto verde.
