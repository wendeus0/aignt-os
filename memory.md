# Current project state

## Global project state

- AIgnt OS continua como meta-orquestrador CLI-first; o AIgnt-Synapse-Flow segue como a engine propria de pipeline do projeto.
- A baseline operacional atual combina `DOCKER_PREFLIGHT` leve por padrao, fluxo container-first para o Codex, Branch Sync Gate e separacao entre memoria duravel (`memory.md`) e log operacional (`PENDING_LOG.md` e `ERROR_LOG.md`).
- A governanca de prompts dos agents segue formato contextual explicito, com contexto, leituras obrigatorias, objetivo, escopo, nao-faca, criterios de aceite e formato de entrega.
- O MVP de produto agora chega ate `DOCUMENT`: a F10 adicionou `RUN_REPORT.md` por run e o primeiro adapter real via `CodexCLIAdapter`.

## Local snapshot

- A PR `#36` (`feature/f10-run-report-one-real-adapter` -> `main`) esta aberta e ainda nao foi mergeada.
- A worktree local desta sessao esta na branch `chore/post-f10-handoff-logs-memory`, criada para alinhar `PENDING_LOG.md` e `memory.md` sem contaminar a PR da F10.

# Stable decisions

- `DOCKER_PREFLIGHT` continua obrigatorio antes da execucao pratica de uma feature; o modo padrao permanece leve.
- O Codex opera em fluxo container-first via `./scripts/dev-codex.sh`, separado do servico `aignt-os`, onde o AIgnt-Synapse-Flow roda como engine propria de pipeline do AIgnt OS.
- A Branch Sync Gate usa `./scripts/branch-sync-check.sh` para detectar drift e `./scripts/branch-sync-update.sh` apenas quando a worktree estiver limpa e segura para atualizacao.
- `memory.md` guarda memoria duravel e reaproveitavel; `PENDING_LOG.md` e `ERROR_LOG.md` guardam detalhe operacional da sessao.
- O `memory-curator` pode ser acionado por `$memory-curator encerrar conversa` ou `$memory-curator close session` para atualizar `memory.md` e gerar handoff de encerramento.
- Com `network-access = true`, `git push` e `gh pr create` devem ser tentados primeiro no sandbox; fallback fora do sandbox fica restrito a falha real de rede ou sandbox.
- A F10 fecha o MVP de observabilidade local com `DOCUMENT`, `RUN_REPORT.md` deterministico e persistencia de metadados minimos por step.
- O `CodexCLIAdapter` e o primeiro adapter real priorizado no happy path final do MVP.
- Os artefatos operacionais padrao em `.aignt-os/` devem permanecer fora do versionamento.

# Active fronts

- Revisar e mergear a PR `#36` da `F10-run-report-one-real-adapter`.
- Concluir a chore `post-f10-handoff-logs-memory`, mantendo os registros operacionais e a memoria duravel alinhados ao estado real do repositório.

# Open decisions

- Definir qual sera a proxima frente de produto apos o merge da F10; a triagem deve ser refeita em `main` com backlog e memoria ja atualizados.
- Decidir se o caminho real nao mockado de `codex exec` dentro da pipeline deve virar gate operacional obrigatorio ou permanecer como smoke opcional.

# Recurrent pitfalls

- `memory.md` perde valor quando mistura decisao estavel com snapshot local ou log de conversa.
- `memory.md` e `PENDING_LOG.md` ficam rapidamente obsoletos quando merges e PRs mudam o estado real do repositório e o handoff nao e consolidado em seguida.
- `uv` pode falhar no sandbox por cache fora da workspace ou indisponibilidade de rede.
- `branch-sync-update` nao e seguro com worktree suja, mesmo quando o drift contra `main` parece pequeno.
- Subir `codex-dev` manualmente em paralelo ao launcher pode causar corrida operacional.

# Next recommended steps

- Revisar e mergear a PR `#36`.
- Depois do merge da F10, rerodar `technical-triage` em `main` para escolher a proxima frente de produto.
- Manter limpezas amplas de docs/logs historicos fora do caminho critico ate a frente seguinte estar definida.

# Last handoff summary

- Read before acting: releia `AGENTS.md`, `CONTEXT.md`, `memory.md`, `PENDING_LOG.md`, `ERROR_LOG.md`, `git status` e `git diff --stat`.
- Current state: a F10 foi implementada, validada e promovida para a PR `#36`, adicionando `DOCUMENT`, `RUN_REPORT.md` e `CodexCLIAdapter`; esta chore branch so alinha logs e memoria.
- Open points: mergear a PR `#36`, decidir se o smoke real do Codex vira gate e escolher a proxima frente apos a F10.
- Recommended next front: concluir o merge da F10 e so entao rerodar `technical-triage` em `main`.
