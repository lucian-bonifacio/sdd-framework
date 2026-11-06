---
id: 006-distribuicao
status: accepted
design: inline
---
# CLI, distribuição e qualidade

## Objetivo e escopo
Entregar cli, distribuição e qualidade no framework genérico, conforme o [PRD](../../docs/PRD.md). Não implementar software do consumidor nem presumir aprovação de requisitos novos.

## Requisitos
- RF-001: Fornecer três comandos com aliases em português e saída JSON utilizável em automação.
- RF-002: Operar em Python 3.11+ sem dependências externas no runtime e oferecer zipapp portátil.
- RF-003: Recusar travessia/symlinks em artefatos e impedir escritores CLI concorrentes; recuperar conteúdo após falhas ordinárias de escrita.
- RF-004: Testar contratos de preservação e executar o pacote fora do checkout; preparar CI multiplataforma sem presumir seu resultado remoto.

## Critérios de aceitação
- CA-001: Dados comandos init/inicie, update e check/conferencia, quando usados com --json, então retornam JSON e exit 0, 1 ou 2 conforme resultado; erros não imprimem traceback.
- CA-002: Dado zipapp construído, quando copiado para diretório fora do checkout e executado com Python, então inicializa e confere um consumidor sem instalar dependências.
- CA-003: Dado symlink, travessia de caminho, lock concorrente ou falha simulada de escrita, quando a operação executa, então recusa escape/concorrência e recupera conteúdo já alterado em falha ordinária.
- CA-004: Dado candidato final, quando a suíte é executada, então cenários de consumidores temporários passam e o relatório distingue ambiente local de CI e agentes não executados.

## Design técnico
argparse expõe init/inicie, update, check/conferencia/conferência. Exit codes 0/1/2 distinguem estrutura conforme, pendência e erro operacional. tools/build_release.py cria zipapp, usando importlib.resources para ler o bundle também em arquivo comprimido. pyproject fornece instalação central via pip quando disponível. unittest usa diretórios temporários e subprocessos isolados; CI tem matriz Python e sistema operacional.

Contratos e limites compartilhados estão na [arquitetura](../../docs/ARCHITECTURE.md) e no [fluxo](../../docs/WORKFLOW.md). Metadados e seções são definidos pela política versionada.

## Pendências
Nenhuma decisão bloqueante de implementação. Validação real em agentes e CI remoto permanece um limite declarado, não um sucesso presumido.
