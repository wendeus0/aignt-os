# F32 Notes

- O recorte fica restrito ao lifecycle local do runtime; nao ha socket nem IPC novos.
- `started_by` registra `principal_id`, nao `token_id`, para evitar ampliar acoplamento do estado do runtime ao auth registry.
- O fallback para estado legado sem `started_by` e obrigatorio para nao quebrar runtimes ja persistidos.
- `runtime status` so deve renderizar informacao de `started_by` quando auth estiver habilitada.
