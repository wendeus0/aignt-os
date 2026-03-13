# F33 Notes

- A `F33` e propositalmente doc-only: ela nao muda CLI, runtime nem auth.
- O objetivo da frente e fechar drift de handoff apos a merge da `F32`, nao abrir uma nova feature de produto.
- `G-11` continua decomposto em buckets local, residente e remoto; a `F32` entra apenas como primeiro slice absorvido do bucket residente.
- A PR `#65` deve permanecer registrada como incidente historico, mas nao mais como bloqueio aberto, porque a baseline foi restaurada na `#66`.
- Depois desta frente, a proxima triagem precisa decidir explicitamente se ainda existe um recorte pequeno de `resident_transport_auth`.
