# F30 Notes

- A F30 continua o recorte local da `F29`, sem abrir socket ou auth remota.
- A CLI publica nova fica restrita a `aignt auth init|issue|disable`.
- O registry continua persistindo apenas `token_sha256`, nunca token bruto.
- `token_id` existe apenas para identificar disable sem expor hash SHA-256.
- A criacao de principal novo em `issue` exige `--role`; conflito de role falha como uso invalido.
- O fluxo de encerramento deve seguir `quality-gate` -> review de seguranca -> `report-writer` -> `branch-sync-guard` -> PR.
