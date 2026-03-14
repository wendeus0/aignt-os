# F14 Notes

- A F14 fecha a lacuna entre a persistencia ja existente e a CLI publica, sem ampliar o escopo para TUI.
- O foco e tornar consultavel, de forma humana, o que o Synapse-Flow ja persiste como engine propria de pipeline do SynapseOS.
- O recorte recomendado e pequeno: `synapse runs list` e `synapse runs show <run_id>`.
- A feature nao deve criar um novo service layer se `RunRepository` e `ArtifactStore` ja resolverem a leitura necessaria.
- Para erro de `run_id` ausente, o contrato deve ser operacional e previsivel, sem traceback de ORM vazando para a CLI.
- A saida precisa continuar legivel em captura de testes e fora de TTY; estilo visual e bonus, nao dependencia funcional.
- O security review desta frente deve confirmar que a CLI so le dados persistidos ja previstos por configuracao e nao amplia a superficie de paths arbitrarios.
- O security review fechou sem ressalvas: a F14 apenas le `runs_db_path` e `artifacts_dir` configurados e nao adiciona subprocesso, shell ou leitura arbitraria fora da persistencia ja suportada.
