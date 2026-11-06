---
id: 002-atualizacao
status: accepted
design: inline
---
# Atualização controlada

## Objetivo e escopo
Entregar atualização controlada no framework genérico, conforme o [PRD](../../docs/PRD.md). Não implementar software do consumidor nem presumir aprovação de requisitos novos.

## Requisitos
- RF-001: Atualizar recursos a partir da distribuição instalada, de diretório local ou fonte Git HTTPS/ref explícita.
- RF-002: Preservar documentos governados, tickets e conteúdo externo aos blocos administrados.
- RF-003: Recusar conflitos, distribuição incompleta, política incompatível e downgrade; falha de rede não altera o projeto.
- RF-004: Registrar versão e fonte configurada, sem executar código da fonte de atualização.

## Critérios de aceitação
- CA-001: Dada distribuição local compatível 0.1.1, quando update usa --source, então versão e recursos administrados são atualizados; fonte remota exige HTTPS/ref explícitos.
- CA-002: Dado PRD aprovado e instruções externas ao bloco SDD, quando update termina, então os bytes desses conteúdos permanecem preservados.
- CA-003: Dado recurso editado, downgrade, política incompatível ou falha de rede, quando update é solicitado, então retorna erro e não sobrescreve recursos ou documentos anteriores.
- CA-004: Dada fonte Git configurada, quando update busca a distribuição, então usa timeout e lê somente arquivos de dados permitidos, sem executar scripts da fonte.

## Design técnico
project.update valida configuração e bundle antes de _install. Manifesto mantém hashes de recursos e blocos; escrita usa rollback de conteúdo em falhas ordinárias. Fontes remotas são obtidas com Git e timeout, sem shell e com hooks desabilitados. Apenas arquivos de texto conhecidos do bundle são aceitos. Mudança de política requer outra CLI. Sem fonte configurada não se presume repositório nem atualização online.

Contratos e limites compartilhados estão na [arquitetura](../../docs/ARCHITECTURE.md) e no [fluxo](../../docs/WORKFLOW.md). Metadados e seções são definidos pela política versionada.

## Pendências
Nenhuma decisão bloqueante de implementação. Validação real em agentes e CI remoto permanece um limite declarado, não um sucesso presumido.
