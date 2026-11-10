---
id: ITEM-003
status: pending
created: 2026-11-09
---
# Discutir as permissões locais do config.toml

## Informação ou proposta
O mantenedor pediu retomar a explicação das permissões criadas no config.toml,
para compreender seus efeitos e limites. O pedido refere-se ao arquivo do projeto,
.codex/config.toml, e não ao arquivo global ~/.codex/config.toml.
Este item registra discussão sobre a configuração implementada, sem nova decisão
ou autorização para ampliar permissões.

O modelo atual seleciona project-agents, estende :workspace e declara write em
.codex, .agents e .claude sob :workspace_roots. O config local deste framework
corresponde ao modelo após update manual. Na última leitura do tax, seu perfil
próprio tax declarava read em :root e write na raiz daquele projeto, com rede
habilitada; o arquivo foi preservado. Isso não comprova enforcement numa sessão.

## Fontes
- Pedido explícito do mantenedor nesta conversa, em 2026-11-09.
- [Modelo TOML distribuído](../../src/sdd_framework/assets/integrations/codex/config.toml).
- [Configuração local deste projeto](../../.codex/config.toml).
- [Decisão operacional vigente](../decisions/ADR-003.md).
- [Perfis de permissões do Codex](https://learn.chatgpt.com/docs/permissions),
  consultados nesta sessão em 2026-11-09; conferir novamente antes de orientar mudanças.

## Impacto e discussão
Explicar default_permissions, o nome do perfil, extends, :workspace_roots e o
significado de write (leitura e modificação), com exemplos no próprio projeto.
Distinguir permissão técnica, autorização do trabalho nos tickets e aprovação de
plano: configurar escrita não autoriza escopo novo, publicação ou sobrescrita.

Esclarecer o que o perfil base herda, quais caminhos foram sobrescritos e os efeitos
sobre .git/.aws sem prometer proteção adicional não verificada. Distinguir arquivo
local e global, confiança no projeto, carregamento em nova sessão, políticas
administradas e prevalência de sandbox_mode/--sandbox quando aplicável.

Comparar project-agents com o perfil tax preservado, inclusive limites de escrita
e rede, antes de decidir qualquer reconciliação. Não alterar o tax ou o global.
Explicar por que a sessão aberta ainda podia exigir permissão para sincronizar
pastas protegidas. Os testes TOML e de migração passaram; o probe nativo não
iniciou por restrição do socket do app-server. Não declarar enforcement validado.

## Destino ou justificativa
A reformulação 0.2 preservou os bytes da configuração local existente e não ampliou
permissões. Os testes de 2026-11-09 abaixo são históricos; não certificam sessões futuras.
Pendente de discussão. Manter a configuração atual até decisão explícita sobre
qualquer alteração futura, após os esclarecimentos e a avaliação de impacto.

### Conferência nesta retomada — 2026-11-09
A pedido do mantenedor, leitura e abertura para escrita do próprio
.codex/config.toml passaram sem escalonamento. Foram escritos os mesmos bytes,
com flush/fsync e comparação posterior idêntica. TOML válido e arquivo igual ao
modelo distribuído. Esse teste comprova acesso ao arquivo nesta sessão, sem
atribuir sua causa exclusivamente ao perfil ou testar negações em outros caminhos.

Revisão técnica com a
[documentação oficial](https://learn.chatgpt.com/docs/permissions), relida nesta
data: default_permissions seleciona project-agents; extends herda :workspace;
as três entradas write permitem ler/modificar esses subdiretórios em cada raiz
efetiva. .git/.aws não receberam sobrescrita; rede e aprovação não são configuradas
explicitamente neste arquivo. Configurações legadas/superiores podem prevalecer.
O arquivo é coerente com a finalidade aprovada e foi mantido. A discussão sobre
limites desejados e eventual reconciliação do tax não foi encerrada por esse teste.
