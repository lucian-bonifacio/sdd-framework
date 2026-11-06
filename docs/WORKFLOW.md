# Fluxo e formatos do framework

As fontes canônicas distribuídas são:
- [Fluxo SDD](../src/sdd_framework/assets/skill/references/WORKFLOW.md)
- [Contratos dos artefatos](../src/sdd_framework/assets/skill/references/ARTIFACTS.md)
- [Política verificável](../src/sdd_framework/assets/policy.json)
- [Templates](../src/sdd_framework/assets/templates/)
- [Skill SDD](../src/sdd_framework/assets/skill/SKILL.md)

Não duplicar esses contratos neste documento. A cópia `.sdd/framework/` é o
snapshot instalado e deve ser atualizada pela CLI quando as fontes mudarem.

## Leitura do fluxo
```mermaid
flowchart TD
  A[Inicie] --> B{Projeto existente?}
  B -->|Sim| C[Inventário e equivalências]
  B -->|Não| D[Concepção]
  C --> E[PRD e arquitetura]
  D --> E
  E --> F[Roadmap e SPEC]
  F --> G[Design e tickets]
  G --> H{Pronta e autorizada?}
  H -->|Sim| I[Agente executa e verifica]
  H -->|Ação humana| J[Registrar pedido e dependências]
  I --> K[Revisão do conjunto e resultados]
  K --> L{Existe trabalho autorizado?}
  L -->|Sim| H
  L -->|Não| M[Transferência ou conclusão]
  J --> H
```

Revisões podem retornar à etapa que possui a decisão; devem reconciliar os
artefatos afetados. CHECKPOINT registra pausa/retomada; INBOX preserva propostas
não incorporadas. Conferência estrutural pode ser executada em qualquer etapa,
com exigências progressivas e correções por tickets.
