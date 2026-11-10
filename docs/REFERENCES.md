# Referências

Este arquivo é uma bibliografia de desenvolvimento do mantenedor, não distribuída
aos consumidores nem consultada pela IA para executar o governador. O procedimento
vigente é governador.md; padrões e métodos são próprios do SDD Framework e vêm de
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
