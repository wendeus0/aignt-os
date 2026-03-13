---
name: session-primer
description: Use esta skill no início de uma sessão para orientar o trabalho lendo memória persistente, estado do branch e feature atual. Não substitui `technical-triage` para priorização de backlog.
---

# Objetivo

Iniciar ou retomar uma sessão de trabalho com contexto completo: quem é o usuário, o que está em andamento, onde o branch está e qual o próximo passo recomendado.

# Quando esta skill deve ser usada

Use esta skill quando:

- for o início de uma nova sessão de trabalho
- a sessão foi interrompida e o contexto ficou difuso
- um agente novo assumiu o trabalho e precisa de orientação
- o usuário pedir explicitamente para "resumir o estado" ou "qual é o próximo passo"

# Quando esta skill NÃO deve ser usada

Não use esta skill para:

- priorizar backlog ou decidir qual feature atacar (use `technical-triage`)
- registrar ou consolidar memória após a sessão (use `memory-curator`)
- diagnosticar falhas de CI ou runtime (use `debug-failure`)
- substituir a leitura completa de SPEC ou arquitetura quando a implementação exige isso

# Processo

Execute nesta ordem, sem pular etapas:

## 1. Ler memória persistente

```bash
cat ~/.claude/projects/*/memory/MEMORY.md 2>/dev/null || echo "(sem memória persistente)"
```

Leia também os arquivos de memória referenciados no índice `MEMORY.md` que forem relevantes para a sessão atual.

## 2. Ler contexto do projeto

Leia nesta ordem:

1. `CONTEXT.md`
2. `CLAUDE.md` (seção de arquitetura e convenções)

## 3. Inspecionar estado do Git

```bash
git log --oneline -10
git status
git diff --stat
```

Identifique:
- branch atual e se há drift em relação a `origin/main`
- arquivos modificados / não rastreados
- feature em andamento (pelo nome do branch ou pela presença de `features/<feature>/`)

## 4. Identificar feature ativa

Se houver `features/<feature>/SPEC.md`, leia-a.

Se houver `features/<feature>/NOTES.md` ou `features/<feature>/PENDING.md`, leia-os também.

## 5. Produzir resumo de orientação

Produza um resumo conciso com:

- **Feature atual**: ID, título e estado no fluxo (`SPEC → TEST_RED → CODE_GREEN → ...`)
- **Branch**: nome, commits recentes, drift estimado
- **Próximo passo recomendado**: a etapa mais imediata do fluxo oficial de desenvolvimento
- **Pendências abertas**: itens de `PENDING_LOG.md` ou memória que afetam a continuidade
- **Alertas**: drift de branch, inconsistências detectadas, decisões abertas críticas

# Restrições obrigatórias

- Não tome decisões de backlog — apenas oriente.
- Não edite código, testes ou SPEC durante esta skill.
- Se o estado do branch indicar drift relevante em relação a `origin/main`, recomende `branch-sync-guard` antes de qualquer trabalho.
- Se houver ambiguidade sobre qual feature está ativa, pergunte ao usuário antes de prosseguir.
- Mantenha o resumo curto: o objetivo é orientar em segundos, não substituir a leitura completa dos artefatos.

# Saída final esperada

Entregue apenas:

1. Resumo de orientação (feature, branch, próximo passo, pendências, alertas)
2. Recomendação de skill a invocar em seguida
