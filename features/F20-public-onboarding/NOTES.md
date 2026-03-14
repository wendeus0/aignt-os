# F20 Notes

- A mitigacao do risco residual da F19 entra na F20 pelo eixo de onboarding: explicitar o que `synapse doctor` garante e o que continua pertencendo ao `repo-preflight`.
- O quickstart da F20 deve continuar sync-first e local-first, porque esse e o caminho canonico hoje; fluxos async, Docker-first ou runtime persistente nao podem virar caminho principal por inercia.
- Se a fase futura exigir Docker ou runtime completo como requisito minimo da primeira run, a revisao correta sera de contrato entre F19 e F20, nao um ajuste textual isolado em README.
