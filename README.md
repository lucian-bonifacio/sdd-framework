# SDD Framework

## Objetivo
Organizar projetos com padrões documentais e um procedimento único dirigido à IA:
[governador.md](governador.md). Versão **0.4.2**, Python 3.11+ e biblioteca padrão.

O usuário aciona o governador. Ele orienta criação ou reconstrução de PRD,
arquitetura, roadmap, SPECs, tarefas e instruções dos agentes. Ao concluir a
organização, o projeto segue pela execução local, independente do framework.

## Como começar
Na raiz do projeto consumidor, instale a distribuição deste checkout:

```bash
python3 /caminho/sdd-framework/sdd.py init .
```

Depois, abra seu agente e solicite:

> Execute governador.md para organizar este projeto conforme os padrões SDD.

Também é possível invocar explicitamente a skill SDD. Ler o arquivo, iniciar uma
sessão e executar init/update não acionam o procedimento.

A instalação prepara somente:
- `governador.md`: instruções para a IA;
- `docs/padroes/`: contratos e doze templates de documentos;
- `.agents/skills/sdd/` e `.claude/skills/sdd/`: a mesma skill, com controles nativos de acionamento explícito;
- `.codex/config.toml`, se ausente; configurações existentes são preservadas;
- blocos de entrada em AGENTS.md e CLAUDE.md, preservando o conteúdo próprio;
- `.sdd/manifest.json`: inventário de arquivos e hashes, usado pelo update;
- `.sdd/execucao.json`: referências instaladas/aplicadas, evidências e pendências por etapa.

Não são criados PRD, SPECs, tickets, código ou diretórios funcionais fictícios.
O agente cria esses artefatos quando o usuário aciona o governador. Não são
necessários TASKS.md, controle de fases na CLI ou um atualizador de roadmap.

## Atualização
Depois de obter a nova distribuição, execute em cada consumidor:

```bash
python3 /caminho/sdd-framework/sdd.py update .
```

Para aplicar recursos de outro checkout local compatível:

```bash
python3 /caminho/sdd-framework/sdd.py update . --source /caminho/nova-distribuicao
```

Update modifica recursos e trechos administrados, preservando conteúdo próprio
e os documentos do produto. Não chama a IA nem reabre organização.
O usuário precisa acionar novamente o governador para avaliar exigências novas.

O controle fica em `.sdd/execucao.json`, mantendo por etapa o padrão instalado,
o aplicado e a diferença pendente. O hash identifica mudanças; as referências
limitadas ao atual/aplicado guardam texto suficiente para explicá-las. Updates
sucessivos consolidam o delta, sem acumular histórico dentro do governador.

Quando acionada, a skill parte do critério de pronto: concluído ou não concluído.
Se faltar alguma condição, trabalha só nela e preserva as atendidas. Depois da
conclusão, ajusta somente alterações do framework; sem alteração, preserva o objeto. A IA registra conclusão e evidências
somente após cumprir o critério de pronto. O update não conclui tarefas.
Mudanças comuns são avaliadas pelo impacto direto; não refazem todos os itens.

Na migração de 0.3, o antigo bloco de diferenças sai do governador e é preservado
uma única vez em legacy_pending no controle técnico. A IA reconcilia esse registro
no próximo acionamento a partir do critério de pronto, sem refazer condições
atendidas nem inventar conclusões anteriores. Depois,
retira esse campo. Registro técnico existente mas perdido/corrompido exige restauração.

Personalizações em recursos administrados geram conflito antes de qualquer
escrita. Reconcilie as fontes; não altere hashes para ocultar diferenças. Os
templates são administrados, mas os documentos preenchidos pertencem ao projeto.

Na migração de 0.1, os antigos recursos administrados intactos são removidos e
o procedimento de docs/FLUXO.md é desativado, preservando o plano do consumidor.
Configuração, tickets e scripts legados permanecem como dados do projeto até
migração pelo agente explicitamente acionado. Nenhuma regra antiga continua
sendo exigida pela CLI nova.

## Padrões e documentos
O [governador](governador.md) é o único procedimento. Os
[contratos](docs/padroes/CONTRATOS.md) e templates definem a forma dos documentos;
a skill orienta como aplicar o procedimento e registrar evidências. O governador escreve instruções para
a IA, com linguagem clara para revisão e contestação humanas.
Na execução, são usados exclusivamente os templates, contratos e a skill próprios
do SDD Framework. Repositórios externos servem somente de inspiração ao desenvolvimento;
não são consultas, templates alternativos ou procedimentos do consumidor.

O procedimento começa por PRD e SPECs. Cada artefato tem seu próprio objetivo,
objeto, templates/skill/referências e operação unificada, com ou sem documentos
anteriores. A regra de execução/reexecução é única, anterior aos itens, e trata
somente operações alteradas e impactos diretos. Ações e resultados ficam nos tickets, decisões nas ADRs e passagem no checkpoint;
estado técnico, evidências e pendências ficam em .sdd/execucao.json.

Projetos existentes têm conteúdo classificado como aproveitar ou conflito.
Conhecimento útil migra para os documentos padrão; arquivos de mesma função
são removidos após preservação e conferência, no escopo autorizado. Divergências
de processo precisam de decisão explícita. Documentos condicionais não são
fabricados para preencher modelos.

## Desenvolvimento
As fontes distribuídas estão em `src/sdd_framework/assets/`; não editar cópias
instaladas em `docs/padroes/` ou nas integrações para contornar conflitos.

```bash
python3 -m unittest discover -s tests -v
python3 tools/build_release.py
python3 sdd.py update .
```

O pacote portátil `dist/sdd.pyz` aceita os mesmos comandos init/update e funciona
fora deste checkout, sem instalação ou dependências externas de runtime.
A CLI não executa testes, código ou deploy de consumidores.

## Contrato do projeto
- [PRD](docs/PRD.md), [arquitetura](docs/ARCHITECTURE.md) e [roadmap](docs/ROADMAP.md).
- [SPEC do governador](specs/001-governador/SPEC.md).
- [Decisão da reformulação](docs/decisions/ADR-003.md) e [referências](docs/REFERENCES.md).
