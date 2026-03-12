---
name: git-flow-manager
description: Use esta skill quando a tarefa estiver no fim do fluxo Git da feature atual, incluindo revisão final do escopo versionado, organização do commit, push da branch e abertura ou preparação de pull request. Não use para Docker preflight, branch sync, CI automations, SPEC, testes RED, implementação, quality gate ou security review.
---

# Objetivo
Executar e organizar o fluxo final de Git da feature atual com escopo limpo e auditável.

## Pré-condições
Use esta skill somente depois que os seguintes gates já tiverem terminado:
- `branch-sync-guard`
- `quality-gate`
- `security-review`
- `report-writer`

## Leia antes de agir
1. `AGENTS.md`
2. `git status`
3. `git diff --stat`
4. `git diff`
5. `git log --oneline -n 10`
6. `features/<feature>/SPEC.md`, se houver
7. relatório mais recente de `report-writer`

## Use esta skill quando
- a feature já foi implementada e validada
- for hora de preparar um commit limpo
- for hora de fazer push da branch
- for hora de abrir ou preparar a PR

## Não use esta skill quando
- ainda houver drift relevante com `main`
- ainda houver falha de quality gate
- ainda houver ressalva pendente de security review
- a tarefa principal ainda for código, testes, Docker, CI ou debug

## Regras obrigatórias
- Trabalhe apenas sobre a branch atual.
- Não commite arquivos fora de escopo.
- Não misture mudanças paralelas.
- Pare se houver bloqueio real.
- Deixe claro o que entrou no commit.

## Estratégia
1. Revisar o estado da branch.
2. Confirmar se o diff está coerente com a feature.
3. Preparar staging limpo.
4. Montar commit objetivo.
5. Fazer push.
6. Sugerir ou preparar título e descrição da PR.

## Saída esperada
Inclua:
- branch atual
- arquivos incluídos
- resumo do commit
- status do push
- sugestão de PR, quando aplicável
- bloqueios restantes, se houver
