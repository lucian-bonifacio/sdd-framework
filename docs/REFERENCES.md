# Referências e limites da inspiração

Consulta em 2026-11-06; contagens e comportamentos podem mudar. Foram usados
conceitos e contratos, sem copiar integralmente skills ou código de terceiros.

| Fonte | Referência consultada | Aproveitamento |
|---|---|---|
| GitHub Spec Kit | commit c8ffef79381363d4d376a5e830490ec9e5212e83 | Templates, requisitos/plano/tarefas, análise antes e convergência após execução |
| OpenSpec | commit 3e4d5f0769e2857c8eb54f149cbf5e4f703fa04c | Adoção incremental, alterações explícitas, execução até bloqueio e limites de verificação |
| Akita my-skills | commit 1aba042a77754408af6ddc887d235345e89642ab | Planejar evidência, resolver trabalho aprovado, revisar lote final e aprender com falhas |

Links:
- [Spec Kit implementação](https://github.com/github/spec-kit/blob/c8ffef79381363d4d376a5e830490ec9e5212e83/templates/commands/implement.md)
- [Spec Kit evolução](https://github.com/github/spec-kit/blob/c8ffef79381363d4d376a5e830490ec9e5212e83/docs/how-to/evolving-specs.md)
- [OpenSpec schema](https://github.com/Fission-AI/OpenSpec/blob/3e4d5f0769e2857c8eb54f149cbf5e4f703fa04c/schemas/spec-driven/schema.yaml)
- [Akita verificação](https://github.com/akitaonrails/my-skills/blob/1aba042a77754408af6ddc887d235345e89642ab/verification-planning/SKILL.md)
- [Akita workflow](https://ailair.akitaonrails.com/pt-br/workflow/)
- [Codex: skills locais e AGENTS](https://developers.openai.com/blog/skills-agents-sdk)
- [Diretórios de instalação de skills](https://developers.openai.com/api/reference/cli)
- [Configuração Codex por projeto](https://learn.chatgpt.com/docs/config-file/config-basic), consultada para o ajuste de `.codex/config.toml`.
- [Proteção de diretórios no sandbox](https://learn.chatgpt.com/docs/agent-approvals-security#protected-paths-in-writable-roots), consultada para o preflight e a orientação de init no terminal.

Tickets individuais, modelo específico de tarefas conjuntas, INBOX e CHECKPOINT
são definições próprias desta conversa. Não são apresentados como padrão único
ou certificação de mercado. Design System é contrato externo; sua criação não
pertence ao SDD. AI Memory é proposta pendente, não funcionalidade desta versão.
