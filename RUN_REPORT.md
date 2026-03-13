# Relatório de Execução - Feature F40: Cancelamento Local de Runs

## Resumo
Implementação do mecanismo de cancelamento local de runs (`local_cancellation`), permitindo a interrupção graciosa da execução do pipeline via CLI (`aignt runs cancel`) e TUI (atalho `k`).

## Escopo Entregue
- **Core Pipeline**:
    - Suporte a `PipelineCancelledError` no engine.
    - Protocolo `CancellationChecker` para injeção de verificação externa.
- **Persistence & Runtime**:
    - Transição de estado `running` -> `cancelling` -> `cancelled`.
    - Método `cancel_run` no `RunRepository` e `RuntimeService`.
    - `PersistedPipelineRunner` agora injeta um checker que consulta o banco de dados.
- **Interface**:
    - Comando CLI: `aignt runs cancel <run_id>`.
    - Dashboard TUI: Tecla `k` aciona cancelamento da run selecionada.

## Alterações Técnicas
- Arquivos modificados: `src/aignt_os/pipeline.py`, `src/aignt_os/persistence.py`, `src/aignt_os/cli/app.py`, `src/aignt_os/cli/dashboard.py`.
- Novos testes:
    - `tests/unit/test_pipeline_cancellation.py`: Validação da lógica do engine.
    - `tests/integration/test_cli_cancellation.py`: Teste end-to-end do comando CLI.
    - `tests/integration/test_runtime_cancellation.py`: Teste de integração do runner com sinal de cancelamento.

## Revisão de Segurança
- **Controle de Acesso**: Cancelamento restrito a runs locais geridas pelo mesmo usuário/processo (implícito pelo acesso ao arquivo SQLite).
- **Graceful Shutdown**: O cancelamento ocorre entre steps, garantindo que nenhum step seja interrompido no meio de uma operação crítica de I/O (exceto se o step implementar seu próprio timeout/cancelamento, o que é futuro).
- **Integridade de Estado**: O estado `cancelled` é terminal e persistido, impedindo retomada acidental.

## Próximos Passos
- Refinar UX do cancelamento no Dashboard (feedback visual imediato).
- Implementar timeout de steps (futuro).

## Conclusão
Feature F40 implementada e validada, cobrindo todos os critérios de aceitação da SPEC. Pull Request #87 criado.
