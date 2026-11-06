---
status: accepted
---
# PRD — SDD Framework 0.1

## Problema e público
Projetos conduzidos por agentes perdem contexto entre sessões, repetem pesquisa,
divergem na documentação e deixam trabalho humano ou requisitos sem acompanhamento.
O público são mantenedores que usam agentes como Codex e Claude Code, em projetos
novos ou em andamento, independentemente de linguagem ou domínio.

## Objetivos e escopo
Entregar um processo SDD obrigatório, proporcional e verificável, com três entradas:
Inicie, Update e Conferência. Organizar concepção, requisitos, arquitetura, roadmap,
especificações, tarefas, validação documental, decisões, propostas e retomada.
As definições desta conversa governam o produto; IDEIA.md é inspiração.

Sucesso: um consumidor pode iniciar/adequar seu projeto, continuar sem contexto
anterior, localizar tarefas e ações humanas, preservar decisões e atualizar os
recursos sem perder conteúdo. O projeto continua implementável sem CLI/skill.

Fora do escopo: executar código do consumidor, gerenciar agentes, deploy, publicar
automaticamente, criar Design System e exigir serviços de memória. As instruções
geradas orientam o agente executor a verificar seu próprio trabalho.

## Requisitos
- RF-001: Iniciar projetos novos/existentes com plano obrigatório de adequação progressiva.
- RF-002: Padronizar nomes, caminhos, templates, metadados e preenchimento de artefatos.
- RF-003: Integrar uma skill SDD genérica a Codex/Claude e orientar continuidade no AGENTS.md.
- RF-004: Manter um ticket por tarefa, índice, dependências, autorização e evidências.
- RF-005: Permitir trabalho autorizado contínuo e mostrar ações humanas sem bloquear independentes.
- RF-006: Fornecer CHECKPOINT com acionamento explícito, preenchimento e retomada padronizados.
- RF-007: Preservar pesquisas/propostas na INBOX, distinguindo-as de decisões aceitas.
- RF-008: Conferir obrigatoriedade por etapa, consistência estrutural e cobertura declarada; consolidar no ROADMAP todas as tarefas e ações pendentes do usuário por visão gerada dos tickets.
- RF-009: Gerar tickets de adequação ao conferir com --fix, sem aprovar ou fabricar documentos.
- RF-010: Atualizar recursos versionados com preservação e detecção de conflitos.
- RF-011: Integrar documentos existentes por equivalência explicitamente revisada.
- RF-012: Receber referência/versão de Design System, sem criá-lo.
- RF-013: Distribuir CLI local e executável portátil, sem dependências operacionais de IA; entregar ferramentas autônomas ao consumidor para operações mecânicas, com instruções locais de execução e verificação pelo agente.
- RF-014: Preparar diretórios nativos e config.toml neutro para Codex conforme integração selecionada, preservando configurações do consumidor e antecipando falta de escrita.
- RNF-001: Runtime em Python 3.11+ sem dependências externas; funcionamento offline para operações locais.
- RNF-002: Init repetido não altera arquivos; update não sobrescreve documentos do consumidor.
- RNF-003: Recusar escape de diretório, symlinks em artefatos e escritores concorrentes.
- RNF-004: Documentos permanecem texto legível e utilizável sem framework.
- RNF-005: Evidência não executada não pode ser reportada como teste aprovado.

## Restrições e pendências
O usuário autorizou consolidar, especificar e implementar em 2026-11-06. A escolha
técnica de Python é registrada no ADR-001. Não há requisito de automação por MCP.
O verificador é estrutural. Critérios de aceitação, testes e revisões aplicáveis
atendidos permitem concluir sem aceite manual adicional. Quando a tarefa depender
do usuário, registrar sua execução e verificar o resultado antes de concluir.
O AI Memory é proposta em ITEM-001, sem dependência obrigatória.
Publicação em registro, licença e teste real com sessões de cada agente precisam
de definição/acesso do mantenedor e não são simulados nesta entrega.
