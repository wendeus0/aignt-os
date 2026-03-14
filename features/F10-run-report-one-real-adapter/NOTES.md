# F10 Notes

- A F10 fecha o MVP do Synapse-Flow com `DOCUMENT`, `RUN_REPORT.md` e um unico adapter real.
- O `CodexCLIAdapter` e o alvo escolhido porque o repositório ja possui launcher container-first versionado em `./scripts/dev-codex.sh`.
- `DOCUMENT` permanece um passo local e deterministico; o relatorio final nao depende de outra chamada agentica.
- Metadados de step entram apenas no nivel minimo necessario para auditoria local: ferramenta, return code, duracao e timeout.
