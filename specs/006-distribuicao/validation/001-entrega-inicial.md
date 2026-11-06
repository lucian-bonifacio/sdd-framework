---
verification: passed
revision: local-working-tree-0.1.0
---
# Evidências da entrega inicial — T-002

## Escopo e revisão
Evidência técnica vinculada ao ticket de distribuição T-002. Este registro
preserva a execução anterior de 49 testes; o andamento atual é consultado no
ROADMAP e nos tickets. Não é um aceite manual geral do projeto.

Validar inicialização progressiva, preservação em projetos existentes, atualização,
gates documentais, dependências, trabalho humano, continuidade e distribuição.
Execução local em 2026-11-06, Linux e Python 3.14.4. Sem commit disponível.
Identidade SHA-256 agregada dos 28 arquivos de código, recursos, testes e build
(excluindo caches), ordenados por caminho, delimitando caminho e conteúdo por NUL:
`d405384ad8127a05f12c995e8a2ee7f5ed4154009bfdcf6d05b5517237490f6c`.

## Verificações
| Verificação | Resultado local |
|---|---|
| `python3 -m unittest discover -s tests -v` | 49 testes passaram |
| Init vazio/existente e repetição | Passou; não cria documentos de produto vazios |
| Preservação AGENTS/CLAUDE/PRD e CRLF | Passou, inclusive após atualização |
| Atualização local 0.1.0 → 0.1.1 | Passou; documentos do consumidor preservados |
| Atualização remota | Contrato de sucesso/falha simulado passou; sem acesso Git remoto real |
| Dependências, autorização e cobertura | Passou; ciclos e lacunas são reportados |
| Trabalho humano e tarefas independentes | Passou; pendências visíveis sem ocultar trabalho pronto |
| Escrita com rollback, lock e symlinks | Passou nos cenários locais |
| Configuração Codex e pastas protegidas | Passou: criação neutra, preservação, migração por update, TOML e preflight |
| CHECKPOINT, INBOX e relatório | Passou a validação estrutural; conteúdo é responsabilidade do agente |
| Zipapp em consumidor fora do checkout | Passou; init e check sem instalação |
| Validador da skill | `Skill is valid!` |
| `python3 tools/build_release.py` | Passou; dist/sdd.pyz gerado |
| `python3 dist/sdd.pyz --version` | 0.1.0 |

Artefato portátil: 35195 bytes; SHA-256
`15f3827ef65acc8de7a6123e98223e8ed4a714e29e65fde6e654e30c9b830fe6`. Checksum também em dist/SHA256SUMS.
A conferência de entrega `python3 sdd.py check . --phase delivery --json` passou:
19 tickets concluídos (seis de adoção e treze de implementação), zero impedimentos
estruturais e um item informativo de INBOX. Ela não substitui os testes acima.

## Resultados e limitações
As 49 verificações automatizadas locais passaram. Testes criam consumidores
isolados, não alteram configuração global e não executam código de aplicação.
A CLI é funcional dentro dos contratos da versão 0.1; o pacote portátil foi
executado fora do checkout. Documentos continuam disponíveis sem os recursos SDD.

Não verificado nesta sessão:
- CI remoto Linux/macOS/Windows e Python 3.11: matriz configurada, sem execução remota.
- Sessões reais de Codex/Claude: integrações e formato foram verificados; não houve
  avaliação comportamental por outra instância de agente.
- Instalação via pip: indisponível no ambiente original; zipapp foi validado.
- Download Git real de release: não há repositório público de distribuição presumido.
- Publicação de pacote, licença e commit/PR: não realizados nem necessários à entrega local.

Conformidade estrutural não prova qualidade semântica, aprovação humana ou
segurança de um consumidor. O gate final continua exigindo evidências específicas
do produto e análise dos documentos pelo agente e mantenedor.
