# Current project state

- Repository: AIgnt OS, um meta-orquestrador CLI-first com AIgnt-Synapse-Flow como engine propria de pipeline.
- Branch atual observada: `main`, alinhada com `origin/main`.
- Worktree observada: limpa ao fim da frente anterior; esta sessao fecha apenas consolidacao de memoria e governanca operacional.
- Baseline atual: infraestrutura isolada do Codex, Branch Sync Gate, `memory-curator` e fluxo Git/GitHub validado no sandbox com `network-access = true`.

# Stable decisions

- `DOCKER_PREFLIGHT` continua obrigatorio antes da execucao pratica de uma feature.
- O preflight padrao segue leve por padrao.
- O Codex opera em fluxo container-first via `codex-dev`, separado do runtime `aignt-os`.
- No ambiente atual do Codex com `network-access = true`, `git push` e `gh pr create` funcionam no sandbox como caminho operacional padrao; fallback fora do sandbox fica restrito a contingencia por falha real de rede/sandbox.
- A Branch Sync Gate usa `./scripts/branch-sync-check.sh` e `./scripts/branch-sync-update.sh` como caminho padrao e conservador.
- `debug-failure` faz diagnostico inicial de falhas; `session-logger` continua responsavel pelo log operacional detalhado.
- O caminho operacional padrao para checks/testes locais passa a ser `./scripts/commit-check.sh --sync-dev`, mantendo `uv` como gerenciador de ambiente e evitando dependencia de virtualenv legada do host.
- `memory.md` permanece como memoria duravel e curta; `PENDING_LOG.md` e `ERROR_LOG.md` guardam o detalhe operacional da sessao.
- O fechamento de sessao pode usar a convencao `$memory-curator encerrar conversa` ou `$memory-curator close session` para atualizar memoria e gerar handoff.
- No ambiente atual do Codex com `network-access = true`, `git push` e `gh pr create` devem ser tentados normalmente no sandbox; fallback fora do sandbox fica apenas como contingencia.

# Active fronts

- Frente operacional principal: consolidacao do fluxo local de checks/testes e da governanca de fechamento Git/GitHub.
- Estado atual: a frente foi concluida e mergeada; nao ha frente ativa registrada nesta worktree em `main`.

# Open decisions

- Validar se o job `branch-validation` continua correto em GitHub Actions real.

# Recurrent pitfalls

- `uv` pode falhar no sandbox por cache fora da workspace ou falta de rede.
- `.venv` legada pode apontar para interpreter invalido.
- Subir `codex-dev` manualmente em paralelo ao launcher pode causar corrida operacional.
- Branches com worktree suja impedem atualizacao segura pela Branch Sync Gate.

# Next recommended steps

- Validar `./scripts/docker-preflight.sh` sem `--dry-run` em ambiente com Docker acessivel.
- Validar `uv sync --locked --extra dev` e o caminho `./scripts/commit-check.sh --sync-dev` em ambiente com rede liberada.
- Confirmar em GitHub Actions real o comportamento do job `branch-validation`.
- Manter `memory.md` como resumo duravel e continuar deixando o detalhe operacional em `PENDING_LOG.md` e `ERROR_LOG.md`.

# Last handoff summary

- A frente operacional de checks locais foi concluida com `./scripts/commit-check.sh --sync-dev` como caminho padrao e gate de branch antes de qualquer `uv sync`.
- A governanca de Git/GitHub foi ajustada: com `network-access = true`, `git push` e `gh pr create` funcionam no sandbox; fallback fora do sandbox fica reservado a contingencias reais.
- A branch `main` permaneceu alinhada com `origin/main`; as pendencias abertas restantes continuam operacionais e pequenas.
