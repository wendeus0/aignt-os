---
name: branch-sync-guard
description: Use esta skill quando a tarefa exigir verificar drift da branch atual em relação a origin/main, especialmente antes de trabalho relevante, antes de commit/push/PR e depois de mudanças estruturais. Ela decide se a branch está alinhada, se pode ser atualizada com segurança ou se deve parar e escalar.
---

# Objetivo
Aplicar o Branch Sync Gate do projeto de forma conservadora e auditável.

## Leia antes de agir
1. `AGENTS.md`
2. `README.md`
3. `scripts/branch-sync-check.sh`
4. `scripts/branch-sync-update.sh`

## Use esta skill quando
- a branch atual não for `main`
- antes de `commit`
- antes de `push`
- antes de abrir/preparar PR
- depois de mudanças estruturais com risco de drift
- quando houver dúvida se a branch ficou atrasada em relação a `origin/main`

## Não use esta skill quando
- a tarefa for apenas SPEC local e sem mudança relevante
- a branch atual já for `main`
- o problema principal for uma falha ainda não classificada
- a tarefa for quality gate, security review ou report

## Regras obrigatórias
- Sempre rode `./scripts/branch-sync-check.sh` primeiro.
- Só use `./scripts/branch-sync-update.sh` quando:
  - a branch não for `main`
  - a working tree estiver limpa
  - não houver conflito imediato detectável
- Se a atualização não for claramente segura, pare e reporte.
- Não esconda risco de merge/rebase manual.

## Estratégia
1. Detectar a branch atual.
2. Executar a checagem de drift.
3. Classificar o estado.
4. Tentar atualização conservadora apenas se for seguro.
5. Retornar estado final com recomendação explícita.

## Estados de saída
- `SYNC_OK`
- `SYNC_UPDATED_SAFE`
- `SYNC_LAGGING_MANUAL_ACTION`
- `SYNC_BLOCKED`

## Saída esperada
Inclua:
- branch atual
- resultado da checagem
- se houve atualização automática ou não
- bloqueios encontrados
- próximo passo obrigatório
