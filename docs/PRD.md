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
- RF-001: Instalar docs/governador.md, padrões e integrações, preparando somente diretórios de apoio; não gerar documentos de produto fictícios.
- RF-002: Acionar a organização somente por pedido explícito do usuário ou invocação da skill; sessão, leitura e init/update não constituem acionamento.
- RF-003: Dirigir as instruções à IA, com ações, condições, limites e critérios de conclusão; manter escrita clara, objetiva e revisável por humanos.
- RF-004: Distribuir padrões de README, AGENTS, PRD, arquitetura, roadmap, SPEC, design, tickets, decisões, propostas, evidências e checkpoint.
- RF-005: Na execução, localizar documentos e funções, classificar conteúdo útil e contradições reais e construir sempre o objeto pelo template próprio, exista ou não documento anterior. Aproveitar informações, preservar decisões e retirar concorrentes após conferência e autorização. Reexecução de tarefa concluída trata somente operações alteradas e impactos diretos.
- RF-006: Manter governador somente como instrução, sem seção de aplicação particular; registrar ações/resultados nos tickets, decisões nas ADRs e passagem no CHECKPOINT; manter referências, evidências e pendências técnicas em .sdd/execucao.json. Depois, executar tarefas locais sem dependência operacional da CLI/skill ou repetição da organização.
- RF-007: Atualizar somente recursos e trechos administrados, preservando documentos próprios, aplicação do governador e configuração existente. Update não executa organização; nova avaliação exige acionamento.
- RF-008: Entregar apenas init/update, runtime Python stdlib e pacote portátil. Manter uma skill genérica em ambas as integrações; sem fases, tickets de adoção ou índices obrigatórios criados pela CLI.
- RF-009: Iniciar o governador por PRD e depois SPECs. Cada item define objetivo, objeto de saída/caminho, requisitos e insumos, padrão próprio, operações específicas e critério de pronto. A operação é unificada pela existência de documentos e informação, sem separar projetos novos/existentes. Em todos os itens, pendência e conclusão são determinadas somente pelas exigências do critério de pronto, sem classificação de situações ou seção separada de resultado. No acionamento completo, concluir cada item antes de avançar na ordem do governador e continuar automaticamente até concluir todos os itens obrigatórios; pedidos expressamente limitados preservam seu escopo. Preservar aplicação e usar somente padrões/métodos próprios do SDD Framework.
- RF-010: Detectar automaticamente alterações por item e recursos associados, sem revisão manual por item. Manter controle em .sdd/execucao.json com hashes e referências instaladas/aplicadas, evidências, pendências e diferenças consolidadas. Não acumular histórico no governador; preservar registros antigos uma única vez para reconciliação. No acionamento explícito, informar mudanças e executar somente operações afetadas/impactos diretos; update nunca registra conclusão pela IA.
- RF-011: Centralizar execução, retomada e reexecução em orientação geral, sem repetir a mecânica nos itens. Determinar conclusão exclusivamente pelo critério de pronto: concluído ou não concluído. Tratar somente condições não atendidas; depois da conclusão, reexecutar apenas mudanças do framework e impactos diretos. Diante de decisão indispensável ausente, perguntar ao usuário sem esperar cobrança, resolver o critério do item atual e só então avançar. draft/accepted são metadados editoriais, sem dispensar critérios nem criar aprovação adicional. Interrupção registra item e lacuna em CHECKPOINT.md e items.<id>.remaining de .sdd/execucao.json, para retomar o mesmo pedido sem nova autorização. A skill registra referência aplicada apenas após critérios cumpridos; migração preserva informações e condições atendidas, sem criar estados intermediários ou reconstrução automática. A introdução define quando agir; Execução do PRD define como atender aos critérios, sem obrigar reconstrução integral.
- RF-012: Separar Arquitetura e Design em itens próprios. Arquitetura é obrigatória; Design é o único item opcional do fluxo e é recomendado. Sem Design, SPEC, Tasks e encerramento continuam; não exigir solução inline ou arquivo separado nem fabricar conclusão. Os demais sete itens são obrigatórios no fluxo completo, respeitando pedidos de escopo restrito e registros auxiliares condicionais. Preservar conhecimento e aplicação anterior na atualização.
- RF-013: Exigir conteúdo específico e verificável em todos os documentos produzidos, sem slogans ou marcadores; toda orientação de registro identifica arquivo e campos de destino, ajustando regras existentes e referenciando-as em vez de duplicá-las. Informação indispensável ausente é pendência, sem inventar parâmetros do consumidor. AGENTS define contexto/escopo, verificações, higiene, qualidade, proteção e entrega com regras permanentes e parâmetros locais. Tasks referenciam AGENTS e definem cenários, comandos/procedimentos, diretórios, pré-requisitos, resultados esperados, evidências e limpeza próprios. Preservar testes permanentes, fixtures, evidências e alterações particulares; limitar a limpeza a descartáveis e recursos da execução. Instalação continua sem produzir esses documentos nem executá-los.
- RF-014: Localizar o governador em docs/governador.md por padrão. Update migra o procedimento administrado antigo da raiz, preservando conteúdo particular e registros, recusando arquivos alterados/ausentes, conflito no destino e symlinks, com rollback. Atualizar referências para o novo caminho sem executar a organização.
- RF-015: ROADMAP organiza tarefas em fila com Ordem, Tarefa, Trabalho, Dependências e impedimentos, Estado e Verificação, e tabela de concluídas ou canceladas apenas com Tarefa, Trabalho, Estado e Verificação. Ordem exibe posições consecutivas (1ª, 2ª…), recalculadas a partir dos tickets, sem exibir a prioridade numérica ou Executor. Estado e Verificação aparecem em português sem alterar os valores técnicos dos tickets. Manter Ações pendentes do usuário com decisão/informação necessária, fonte e trabalho impedido; sem seção narrativa de Prioridades e dependências ou diário de versões. Priority e dependencies têm fonte única nos tickets; menor inteiro positivo executa primeiro, padrão 100 e desempate pelo caminho completo. Task criada depois pode ter prioridade maior, sem ignorar autorização, dependências e impedimentos. Preservar conhecimento retirado nos registros pertinentes; não adicionar JSON paralelo nem usar o controle do framework para planejar produto.
- RF-016: Definir testes automatizados por entradas/estado, execução e comparação automática com resultado esperado. Governador exige planejar cobertura, testes necessários ou alternativa justificada nos tickets e incorporar comandos/gatilhos em AGENTS.md; implementação exige executar testes pertinentes e checks obrigatórios, com evidências no Resultado do ticket. Reproduzir defeitos antes da correção quando viável, preservar testes permanentes e evitar duplicação, TDD universal, cobertura percentual ou stack impostos por rotina.
- RF-017: Distribuir política Git do Codex em .codex/rules/sdd-git.rules, preservando config.toml existente e outras regras particulares. Consultas usuais permanecem no sandbox sem aprovação adicional do SDD; mutações de estado local/remoto e configuração exigem aprovação, incluindo operações ainda não liberadas. Não autorizar elevação ampla de Git, alterar configuração global ou presumir autorização de escopo por permissão técnica. Init/update protegem a política administrada por hashes, conflitos, symlinks e rollback; registrar limites da versão/plataforma do Codex.
- RNF-001: Recusar conflitos e symlinks antes de escrever; proteger contra escritores concorrentes e reverter falhas ordinárias de escrita/remoção.
- RNF-002: Não apagar conhecimento essencial, inventar aprovação/evidência ou alterar configurações globais.
- RNF-003: Documentos permanecem legíveis e utilizáveis independentemente do pacote.

## Restrições e pendências
Reformulação direta autorizada pelo mantenedor em 2026-11-10 nesta conversa:
reutilizar o que servir, substituir a arquitetura e retirar controles desnecessários,
sem obrigação de compatibilidade com a versão inicial. A última orientação reforça
que o governador instrui a IA e deve ser legível para revisão humana.

[ADR-003](decisions/ADR-003.md) registra a decisão. Piloto no tax permanece sob
condução do mantenedor; investigação da CI Windows autorizada especificamente
após T-015, independentemente do piloto. Publicação, licença e
integração de memória não são autorizadas por esta implementação.

Separação de Arquitetura obrigatória e Design opcional/recomendado autorizada
explicitamente pelo mantenedor e registrada em T-013. Impacto: oito itens,
metadado design: none/inline/separate, dependências, templates, métodos, skill e
detecção de mudanças; sem execução do governador ou migração semântica automática.

Instruções concretas para AGENTS, planos de verificação/limpeza nos tickets e
especificidade em todos os documentos autorizados pelo mantenedor em T-014.
Impacto em todos os templates, métodos, regra geral, itens Tasks/AGENTS e skill;
sem executar testes ou limpeza do consumidor pela CLI e sem inventar seus dados.

Mudança do governador para docs/governador.md autorizada pelo mantenedor em T-015,
com impacto na CLI, migração, links, instruções instaladas e distribuição portátil.

Reorganização do ROADMAP autorizada em T-016 após T-015 e T-002, com prioridade de
execução independente da criação. Fonte única nos tickets (priority/dependencies),
sem novo JSON; impacto em templates, métodos, AGENTS, skill e governador.
Apresentação revista e aceita em T-017: ordinais na fila, colunas reduzidas nas
encerradas, Estado/Verificação em português e ações humanas com desbloqueios
concretos. Priority permanece técnico nos tickets; mudança visual não altera
responsabilidades nem autorizações.

Continuidade integral e sequencial autorizada pelo mantenedor em T-019 em
2026-11-11, incluindo perguntas para resolver decisões indispensáveis antes do
avanço. Impacto na regra geral do governador, skill, contratos, templates PRD,
AGENTS/CHECKPOINT e blocos de entrada; nenhuma nova fase, estado técnico ou
execução automática da IA pela CLI. Regras de registro devem nomear caminhos e
campos e reutilizar orientações existentes sem duplicação.

Testes automatizados e política Git em rules autorizados pelo mantenedor em
T-020/T-021 nesta conversa. Impacto em contratos, itens Tasks/AGENTS, templates,
skill e distribuição da política pela CLI; runtime permanece stdlib e config.toml
particular permanece preservado. Referências externas constam apenas da
bibliografia de desenvolvimento em docs/REFERENCES.md.
