---
id: 003-conferencia
status: accepted
design: inline
---
# Conferência e acompanhamento

## Objetivo e escopo
Entregar conferência e acompanhamento no framework genérico, conforme o [PRD](../../docs/PRD.md). Não implementar software do consumidor nem presumir aprovação de requisitos novos.

## Requisitos
- RF-001: Verificar artefatos por etapa, seções obrigatórias, metadados e campos ainda por preencher.
- RF-002: Detectar referências quebradas, requisitos sem cobertura, dependências inexistentes/cíclicas e conclusões sem evidência declarada.
- RF-003: Apresentar estados, tarefas prontas e ações humanas pendentes sem dashboard manual duplicado.
- RF-004: Gerar tickets de adequação deduplicados em --fix, preservando os documentos diagnosticados.
- RF-005: Distinguir conformidade estrutural, revisão semântica e verificação do produto; permitir foco numa SPEC sem exigir aceite de futuras entregas.
- RF-006: Consolidar todas as tarefas e estados por entrega no ROADMAP, incluindo ações pendentes do usuário, por seção gerada sem alterar planejamento ou estados dos tickets.
- RF-007: Entregar script autônomo no consumidor e instruir seu agente a usá-lo após alterações de tickets, sem depender de pacote/CLI SDD; preservar customizações locais.

## Critérios de aceitação
- CA-001: Dado PRD ausente ou modelo por preencher, quando check --phase architecture é executado, então retorna exit 1 com caminho e achado correspondente.
- CA-002: Dadas dependências cíclicas/inexistentes, requisito sem ticket ou tarefa concluída sem evidência, quando check executa, então cada inconsistência aparece explicitamente.
- CA-003: Dada tarefa pronta independente e outra aguardando usuário, quando check executa, então apresenta ambas nos grupos corretos, sem ocultar a tarefa executável.
- CA-004: Dados achados estruturais, quando check --fix é repetido, então cria tickets apenas para achados ainda sem ticket corretivo ativo e preserva o documento original.
- CA-005: Dada SPEC futura em draft, quando check focaliza outra entrega válida, então não exige aceite da futura; toda saída continua indicando que revisão semântica é necessária.
- CA-006: Dadas tarefas de várias entregas, quando check --roadmap é executado, então atualiza somente o bloco de acompanhamento do roadmap com links, estados e ações humanas; execuções repetidas não duplicam o bloco. Roadmap equivalente configurado é respeitado.
- CA-007: Dado consumidor sem .sdd/ e sem SDD importável, quando seu script local é executado em Python isolado de outra pasta, então atualiza tarefas/ações humanas e preserva planejamento. Erros em tickets não alteram o roadmap; update não substitui script próprio.

## Design técnico
checks.inspect lê a política suportada pela CLI, percorre somente áreas documentais e calcula grafo de dependências. Saída texto/JSON apresenta severidade, caminhos e mensagens. Gates estruturais não autorizam execução. --spec seleciona a entrega para exigências de avanço; documentos presentes das demais continuam sujeitos à validação estrutural. create_remediation cria tickets no plano de adequação com chave estável por código/caminho.

Contratos e limites compartilhados estão na [arquitetura](../../docs/ARCHITECTURE.md) e no [fluxo](../../docs/WORKFLOW.md). Metadados e seções são definidos pela política versionada.

`progress.py` produz uma visão derivada dos tickets. `--roadmap` é uma escrita
explícita num bloco delimitado; a conferência comum permanece somente leitura.
Os links são relativos ao caminho configurado do roadmap. Conteúdo externo ao
bloco é preservado; marcadores malformados causam erro. Não criar STATUS.md nem
relatório global de validação. Evidência extensa fica junto à entrega/ticket.

A rotina usa `scripts/atualizar_roadmap.py`, cópia autônoma de
`consumer_roadmap.py`, que também fornece o renderizador à CLI. A ferramenta usa
biblioteca padrão, caminhos relativos seguros, escrita atômica e lock local no
roadmap. Configuração SDD é dado opcional; sem ela usa docs/ROADMAP.md ou --roadmap.
O arquivo entregue pertence ao consumidor; update cria se ausente e preserva
versão existente. O bloco AGENTS contém procedimento suficiente sem CLI/skill
central. Operações mecânicas podem receber scripts locais conforme necessidade;
o framework não tenta automatizar decisões semânticas.

## Pendências
Nenhuma decisão bloqueante de implementação. Validação real em agentes e CI remoto permanece um limite declarado, não um sucesso presumido.
