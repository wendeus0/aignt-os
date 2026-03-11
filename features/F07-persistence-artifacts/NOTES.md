# F07 Notes

## Decisoes locais

- A F07 persiste apenas dados operacionais da pipeline: `runs`, `run_steps`, `run_events` e artefatos por step.
- O arquivo `runtime-state.json` da F11 permanece exclusivo do lifecycle do runtime e nao participa do `RunRepository`.
- O lock da F07 e booleano e local por run; lease, polling e retomada ficam para a F08.
- O artifact store usa paths sanitizados e arquivos separados para `raw`, `clean` e artefatos nomeados.

## Validacao esperada

- testes unitarios do repositório e artifact store
- teste de integração da pipeline persistida até `PLAN`
- teste de falha com SPEC inválida
- checks locais padrão do repositório
