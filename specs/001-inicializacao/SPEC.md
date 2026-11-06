---
id: 001-inicializacao
status: accepted
design: inline
---
# Inicialização e adoção

## Objetivo e escopo
Entregar inicialização e adoção no framework genérico, conforme o [PRD](../../docs/PRD.md). Não implementar software do consumidor nem presumir aprovação de requisitos novos.

## Requisitos
- RF-001: Iniciar projeto novo ou existente, criando somente recursos e plano de adequação necessários.
- RF-002: Instalar a skill genérica para Codex, Claude ou ambos, com referências e instruções no AGENTS.md.
- RF-003: Preservar documentação, instruções e skills locais; permitir equivalências explicitamente configuradas.
- RF-004: Repetir init sem mutações e sem promover rascunhos a documentos aceitos.
- RF-005: Preparar `.codex/config.toml` para integração Codex e a pasta `.claude/` para Claude, conforme agentes selecionados; preservar configurações existentes.
- RF-006: Identificar diretórios sem permissão antes de aplicar arquivos, com orientação para inicialização no terminal antes da sessão do agente.

## Critérios de aceitação
- CA-001: Dado um diretório vazio, quando init termina, então existem configuração, manifesto, skill e seis tickets de adequação, sem PRD/SPEC vazios.
- CA-002: Dado --agent both, quando init termina, então Codex e Claude recebem SKILL.md e referências; CLAUDE.md encaminha ao AGENTS.md.
- CA-003: Dado AGENTS/PRD/skill existente, quando houver conflito, então conteúdo do consumidor é preservado e o comando informa o impedimento antes de instalar recursos.
- CA-004: Dado projeto já inicializado, quando init é repetido, então a lista changed é vazia e sua versão instalada não sofre downgrade.
- CA-005: Dado --agent both, quando init termina, então `.codex/config.toml` é TOML válido e `.claude/skills/sdd/` existe; configurações Codex próprias permanecem byte a byte após init e update.
- CA-006: Dada `.codex/` sem escrita, quando init precisa criar seu config, então informa o caminho bloqueado antes de instalar recursos; nenhum mecanismo tenta contornar a proteção do agente.

## Design técnico
project.initialize e _install constroem um plano de mutações, verificam conflitos e aplicam sob lock. Snapshot em .sdd/framework, metadados JSON e seis tickets iniciais de adequação. Integração Codex em .agents/skills/sdd; Claude em .claude/skills/sdd e ponte CLAUDE.md. Modo automático usa presença de arquivos, mas é substituível explicitamente. Equivalências de documentos são revisadas pelo agente e registradas em document_paths.

Contratos e limites compartilhados estão na [arquitetura](../../docs/ARCHITECTURE.md) e no [fluxo](../../docs/WORKFLOW.md). Metadados e seções são definidos pela política versionada.

Configuração nativa é criada a partir de `assets/integrations/codex/config.toml`,
um TOML neutro que herda configurações existentes sem fixar modelo ou permissões.
O arquivo do consumidor não é recurso administrado por hash: update não o
sobrescreve, e a conferência valida sua presença e sintaxe. Atualização prepara
o arquivo quando ausente em consumidores já inicializados. O preflight verifica
permissão do ancestral existente antes de qualquer escrita de recurso.

## Pendências
Nenhuma decisão bloqueante de implementação. Validação real em agentes e CI remoto permanece um limite declarado, não um sucesso presumido.
