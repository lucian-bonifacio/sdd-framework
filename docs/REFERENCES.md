# Referências

Este arquivo é uma bibliografia de desenvolvimento do mantenedor, não distribuída
aos consumidores nem consultada pela IA para executar o governador. O procedimento
vigente é docs/governador.md; padrões e métodos são próprios do SDD Framework e vêm de
src/sdd_framework/assets. Links abaixo registram origem de inspiração e consultas
técnicas; não são templates, skills ou procedimentos do projeto.

- [Claude Code: skills e controle de invocação](https://code.claude.com/docs/en/skills): configuração disable-model-invocation, consultada em 2026-11-10.
- Política de invocação do Codex: referência local da skill skill-creator, openai_yaml.md, consultada nesta sessão; a distribuição fornece allow_implicit_invocation false.
- [Agent Skills](https://agentskills.io): formato comum das skills.

Padrões reaproveitados do próprio framework: PRD, arquitetura, SPEC, design,
tickets, decisões, propostas, evidências, checkpoint e instruções dos agentes.
A reformulação não pressupõe certificação externa ou sucesso do piloto.

## Histórico de inspiração de desenvolvimento — revisão 0.2.1

Fontes primárias em refs fixadas, consultadas em 2026-11-10. Templates próprios
continuam sendo o padrão; não foram importados processos, agentes ou dependências.

| Escopo | Referência e princípio aproveitado |
|---|---|
| PRD | [BMAD PRD](https://github.com/bmad-code-org/BMAD-METHOD/blob/bab9082c3e884e0d72c759bcd1a6d90bcc01be84/src/bmm-skills/plan/bmad-prd/assets/prd-template.md): substância, propósito e delimitação proporcionais |
| SPECs | [Spec Kit SPEC](https://github.com/github/spec-kit/blob/c8ffef79381363d4d376a5e830490ec9e5212e83/templates/spec-template.md): condições observáveis, cenários e limites |
| Arquitetura/design | [BMAD arquitetura](https://github.com/bmad-code-org/BMAD-METHOD/blob/bab9082c3e884e0d72c759bcd1a6d90bcc01be84/src/bmm-skills/plan/bmad-architecture/assets/spine-template.md): invariantes e detalhe proporcional |
| Tasks/ROADMAP | [Spec Kit tarefas](https://github.com/github/spec-kit/blob/c8ffef79381363d4d376a5e830490ec9e5212e83/templates/tasks-template.md): caminhos concretos e unidades verificáveis, sem importar suas fases |
| Encerramento | [Akita verification-planning](https://github.com/akitaonrails/my-skills/blob/1aba042a77754408af6ddc887d235345e89642ab/verification-planning/SKILL.md): evidência proporcional à afirmação e limites reais |
| AGENTS/README | Templates próprios e documentação nativa de skills: separar instruções para IA e uso humano, com acionamento explícito |

Na correção 0.2.2, os links externos foram retirados do governador e de sua
orientação de execução. Os princípios úteis já estão expressos nos templates,
contratos e na skill próprios. A bibliografia permanece apenas como histórico de
desenvolvimento, sem papel normativo para o agente ou dependência externa.

## Testes automatizados e política Git — T-020/T-021
Consultadas em 2026-11-11, como bibliografia de desenvolvimento, não como instruções
externas obrigatórias para consumidores:

- [Akita — Verification Planning](https://github.com/akitaonrails/my-skills/blob/1aba042a77754408af6ddc887d235345e89642ab/verification-planning/SKILL.md): escolher evidência pela afirmação, risco, observabilidade e repetibilidade; não impor técnica ou verificação duplicada.
- [Akita — Release Smoke Test](https://github.com/akitaonrails/my-skills/blob/1aba042a77754408af6ddc887d235345e89642ab/release-smoke-test/SKILL.md): verificar o artefato empacotado em ambiente isolado e registrar versão/comando/limites; comandos específicos de OpenCode não foram importados.
- [Python — unittest](https://docs.python.org/3/library/unittest.html): entradas, preparação, asserções e resultado do executor de testes.
- [OpenAI — Rules](https://learn.chatgpt.com/docs/agent-configuration/rules): prefix_rule, decisões, camadas confiáveis, precedência e codex execpolicy check. Verificado localmente com codex-cli 0.167.1; não presumir equivalência entre superfícies do produto.
- [OpenAI — Permissions](https://learn.chatgpt.com/docs/permissions): perfil de filesystem/rede separado de regras por comando e políticas externas.

O template de tarefas do Spec Kit já referenciado acima trata testes como opcionais
quando solicitados na especificação. Essa regra não foi adotada pelo SDD: a decisão
de automação/alternativa deriva do comportamento, risco e cobertura existente,
conforme o contrato próprio, sem importar fases ou outro framework de execução.
