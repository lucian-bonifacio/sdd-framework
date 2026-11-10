# Desenvolvimento do SDD Framework

## Contexto do projeto
Ferramenta de organização documental para agentes de IA. Contrato vigente em
docs/PRD.md e specs/001-governador/SPEC.md. Responder ao mantenedor em português,
de forma breve. IDEIA.md é histórico, não procedimento ou requisito vigente.

As fontes distribuídas estão em src/sdd_framework/assets/. Recursos instalados
em docs/padroes/ e nas skills são administrados pela CLI; altere fontes e use update.
Não copiar README/AGENTS preenchidos deste repositório para consumidores.

## Comandos e verificações
Python 3.11+, runtime somente stdlib; executar sem instalação:

- Testes: `python3 -m unittest discover -s tests -v`.
- Build: `python3 tools/build_release.py`.
- Instalação/update: `python3 sdd.py init .` e `python3 sdd.py update .`.
- Governador: acionamento explícito pelo usuário na IA, não um comando da CLI.

Verifique instalação em consumidores temporários e o pacote portátil fora do
checkout. Não executar testes, código ou deploy do consumidor pela CLI.
Se a sincronização das integrações exigir permissão, use o terminal autorizado;
não contorne proteções nem altere hashes do manifesto para esconder conflito.

## Convenções e restrições
Leia CHECKPOINT.md ao retomar e confronte-o com arquivos e Git; respeite adiamentos.
Tickets são fonte de estado/evidências; ROADMAP resume execução e ações humanas.
Use docs/padroes/CONTRATOS.md para manter documentos. Propostas em docs/inbox
não viram requisitos automaticamente. Requisitos novos exigem impacto e autorização.

Mudança em documento governado também exige adequação dos templates, contratos,
skill ou código pertinente para consumidores, sem copiar conteúdo deste projeto.
Uma skill SDD genérica em ambas as integrações; não adicionar skills sem necessidade.
Preserve conhecimento, decisões e configuração particular. Não seguir symlinks,
registrar segredos, alterar configuração global, publicar ou fazer commit/push
por rotina. Não executar ações no tax sem solicitação. Piloto a cargo do mantenedor;
CI Windows somente depois dele. ADR-003 substitui a arquitetura operacional antiga.

<!-- SDD:START -->
Execute governador.md somente quando o usuário solicitar expressamente o
governador SDD ou invocar a skill SDD. Ler arquivos, abrir uma sessão e executar
init/update não acionam o governador. Fora dessa execução, trabalhe nas tarefas
autorizadas do projeto e mantenha seus documentos atualizados.
<!-- SDD:END -->
