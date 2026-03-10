# Current project state

## Global project state

- AIgnt OS continua como meta-orquestrador CLI-first; o AIgnt-Synapse-Flow segue como a engine propria de pipeline do projeto.
- A baseline operacional atual combina `DOCKER_PREFLIGHT` leve por padrao, fluxo container-first para o Codex, Branch Sync Gate e separacao entre memoria duravel (`memory.md`) e log operacional (`PENDING_LOG.md` e `ERROR_LOG.md`).
- A governanca de prompts dos agents segue formato contextual explicito, com contexto, leituras obrigatorias, objetivo, escopo, nao-faca, criterios de aceite e formato de entrega.

## Local snapshot

- A worktree atual esta em `chore/log-preflight-sync`, com `behind=1` em relacao a `origin/main`; o diff de arvore contra `origin/main` esta vazio, mas a branch deve ser sincronizada antes de nova frente ou fechamento operacional.
- Ha edicoes locais focadas apenas em normalizar `memory.md` e ajustar o contrato da skill `memory-curator`.

# Stable decisions

- `DOCKER_PREFLIGHT` continua obrigatorio antes da execucao pratica de uma feature; o modo padrao permanece leve.
- O Codex opera em fluxo container-first via `./scripts/dev-codex.sh`, separado do servico `aignt-os`, onde o AIgnt-Synapse-Flow roda como engine propria de pipeline do AIgnt OS.
- A Branch Sync Gate usa `./scripts/branch-sync-check.sh` para detectar drift e `./scripts/branch-sync-update.sh` apenas quando a worktree estiver limpa e segura para atualizacao.
- `memory.md` guarda memoria duravel e reaproveitavel; `PENDING_LOG.md` e `ERROR_LOG.md` guardam detalhe operacional da sessao.
- O `memory-curator` pode ser acionado por `$memory-curator encerrar conversa` ou `$memory-curator close session` para atualizar `memory.md` e gerar handoff de encerramento.
- Com `network-access = true`, `git push` e `gh pr create` devem ser tentados primeiro no sandbox; fallback fora do sandbox fica restrito a falha real de rede ou sandbox.

# Active fronts

- Normalizar a governanca de memoria duravel para que `memory.md` fique estavel e o `memory-curator` gere handoff de encerramento reutilizavel.
- Fechar validacoes operacionais ainda abertas do fluxo recente sem reabrir escopo de produto.

# Open decisions

- Validar em GitHub Actions real se o job `branch-validation` continua correto apos os ajustes recentes.
- Definir quando limpar ou re-sincronizar branches locais antigas e worktrees auxiliares para reduzir ruido operacional.

# Recurrent pitfalls

- `memory.md` perde valor quando mistura decisao estavel com snapshot local ou log de conversa.
- `uv` pode falhar no sandbox por cache fora da workspace ou indisponibilidade de rede.
- `branch-sync-update` nao e seguro com worktree suja, mesmo quando o drift contra `main` parece pequeno.
- Subir `codex-dev` manualmente em paralelo ao launcher pode causar corrida operacional.

# Next recommended steps

- Concluir esta normalizacao e manter o detalhe da sessao apenas em `PENDING_LOG.md` e `ERROR_LOG.md`.
- Sincronizar a branch local com `main` antes de iniciar nova frente ou finalizar entrega operacional.
- Validar em ambiente apropriado o job `branch-validation` e o fluxo `uv sync --locked --extra dev`.

# Last handoff summary

- Read before acting: releia `AGENTS.md`, `CONTEXT.md`, `memory.md`, `PENDING_LOG.md`, `ERROR_LOG.md`, `git status` e `git diff --stat`.
- Current state: a memoria duravel foi normalizada para separar baseline global, snapshot local, decisoes estaveis e proximo passo; a worktree ainda precisa sincronizar a branch antes da proxima frente.
- Open points: validar `branch-validation` em GitHub Actions real, revalidar `uv sync --locked --extra dev` em ambiente com rede e decidir limpeza de branches/worktrees antigas.
- Recommended next front: sincronize a branch com `main`, confirme os checks operacionais restantes e so entao abra a proxima feature ou ajuste operacional.
