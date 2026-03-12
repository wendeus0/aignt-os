# F21 Notes

- A F21 deve centralizar o contrato de erro da CLI publica, evitando `typer.Exit(code=1)` espalhado.
- O recorte cobre `runs submit`, `runs show` e `runtime start|status|ready|stop`.
- Parse errors nativos do Typer podem continuar em `2`; o restante dos erros da aplicacao deve ser classificado explicitamente.
- O contrato recomendado para a feature e: `0` sucesso, `2` uso invalido, `3` recurso ausente, `4` validacao de entrada, `5` ambiente/precondicao e `6` execucao inesperada.
- As mensagens precisam ser curtas, sem traceback cru e com prefixo estavel por categoria.
- A frente nao deve alterar rendering de sucesso nem abrir modo verbose.
- O security review fechou sem ressalvas no recorte atual: a centralizacao de erros permaneceu restrita a mensagem/exit code da CLI e nao adicionou shell, subprocesso nem leitura nova de arquivo.
- A validacao local da frente fechou verde com `validate_spec_file()` da SPEC, a suite focada da F21, `./scripts/commit-check.sh --no-sync --skip-docker` e a revalidacao completa com `268` testes verdes mais `./scripts/security-gate.sh`.
