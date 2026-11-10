---
status: accepted
---
# PRD — Governador SDD

## Problema e público
Mantenedores que trabalham com IA precisam organizar projetos novos e existentes
com padrões claros. A implementação anterior acumulou controles de fases e
instalação que dificultavam distinguir instruções distribuídas de trabalho
executado pelo agente.

## Objetivos e escopo
Entregar um governador único, acionado explicitamente pelo usuário, acompanhado
de padrões e uma skill SDD para Codex e Claude. A CLI instala/atualiza esses
recursos; a IA executa o procedimento. A organização termina com documentação
coerente e tarefas preparadas, sem exigir produto implementado.

Fora do escopo: executar código do consumidor pela CLI, iniciar agentes, publicar
automaticamente, criar Design System, impor serviços de memória ou atualizar
todos os projetos silenciosamente.

## Requisitos
- RF-001: Instalar governador.md, padrões e integrações, preparando somente diretórios de apoio; não gerar documentos de produto fictícios.
- RF-002: Acionar a organização somente por pedido explícito do usuário ou invocação da skill; sessão, leitura e init/update não constituem acionamento.
- RF-003: Dirigir as instruções à IA, com ações, condições, limites e critérios de conclusão; manter escrita clara, objetiva e revisável por humanos.
- RF-004: Distribuir padrões de README, AGENTS, PRD, arquitetura, roadmap, SPEC, design, tickets, decisões, propostas, evidências e checkpoint.
- RF-005: Na execução, localizar documentos e funções, classificar conteúdo útil e contradições reais e construir sempre o objeto pelo template próprio, exista ou não documento anterior. Aproveitar informações, preservar decisões e retirar concorrentes após conferência e autorização. Reexecução de tarefa concluída trata somente operações alteradas e impactos diretos.
- RF-006: Manter governador somente como instrução, sem seção de aplicação particular; registrar ações/resultados nos tickets, decisões nas ADRs e passagem no CHECKPOINT; manter referências, evidências e pendências técnicas em .sdd/execucao.json. Depois, executar tarefas locais sem dependência operacional da CLI/skill ou repetição da organização.
- RF-007: Atualizar somente recursos e trechos administrados, preservando documentos próprios, aplicação do governador e configuração existente. Update não executa organização; nova avaliação exige acionamento.
- RF-008: Entregar apenas init/update, runtime Python stdlib e pacote portátil. Manter uma skill genérica em ambas as integrações; sem fases, tickets de adoção ou índices obrigatórios criados pela CLI.
- RF-009: Iniciar o governador por PRD e depois SPECs, com mapa por artefato, objeto de saída, requisitos, padrão, operação e critério de pronto. A operação é unificada pela existência de documentos e informação, sem separar projetos novos/existentes. No PRD, pendência e conclusão são determinadas somente pelo critério de pronto, sem classificação de situações ou seção separada de resultado. Preservar aplicação e usar somente padrões/métodos próprios do SDD Framework.
- RF-010: Detectar automaticamente alterações por item e recursos associados, sem revisão manual por item. Manter controle em .sdd/execucao.json com hashes e referências instaladas/aplicadas, evidências, pendências e diferenças consolidadas. Não acumular histórico no governador; preservar registros antigos uma única vez para reconciliação. No acionamento explícito, informar mudanças e executar somente operações afetadas/impactos diretos; update nunca registra conclusão pela IA.
- RF-011: Centralizar execução, retomada e reexecução em orientação geral, sem repetir a mecânica nos itens. Determinar conclusão exclusivamente pelo critério de pronto: concluído ou não concluído. Tratar somente condições não atendidas; depois da conclusão, reexecutar apenas mudanças do framework e impactos diretos. A skill registra referência aplicada apenas após critérios cumpridos; migração preserva informações e condições atendidas, sem criar estados intermediários ou reconstrução automática. A introdução define quando agir; Execução do PRD define como atender aos critérios, sem obrigar reconstrução integral.
- RNF-001: Recusar conflitos e symlinks antes de escrever; proteger contra escritores concorrentes e reverter falhas ordinárias de escrita/remoção.
- RNF-002: Não apagar conhecimento essencial, inventar aprovação/evidência ou alterar configurações globais.
- RNF-003: Documentos permanecem legíveis e utilizáveis independentemente do pacote.

## Restrições e pendências
Reformulação direta autorizada pelo mantenedor em 2026-11-10 nesta conversa:
reutilizar o que servir, substituir a arquitetura e retirar controles desnecessários,
sem obrigação de compatibilidade com a versão inicial. A última orientação reforça
que o governador instrui a IA e deve ser legível para revisão humana.

[ADR-003](decisions/ADR-003.md) registra a decisão. Piloto no tax permanece sob
condução do mantenedor; CI Windows depois do piloto. Publicação, licença e
integração de memória não são autorizadas por esta implementação.
