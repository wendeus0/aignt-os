# PENDING_LOG.md

# Template

## Decisões incorporadas recentemente

Registre aqui um resumo curto das decisões que passaram a valer no projeto.

### [YYYY-MM-DD] Decisão

- **Resumo:** decisão tomada
- **Motivo:** por que ela foi adotada
- **Impacto:** onde ela afeta o projeto
- **Status:** ativa | revisar depois

---

## Pendências abertas

Registre aqui tudo o que ficou pendente e que pode virar:

- nova feature
- ajuste operacional
- revisão de arquitetura
- ponto de atenção futuro

### [P0 | P1 | P2] Título da pendência

- **Contexto:** onde surgiu
- **Descrição:** o que falta decidir ou implementar
- **Próximo passo sugerido:** ação concreta
- **Pode virar feature?:** sim | não | talvez
- **Status:** aberto | em análise | adiado

---

## Pontos de atenção futuros

Liste aqui observações que ainda não são tarefas, mas merecem monitoramento.

### Item

- **Risco ou atenção:** descrição curta
- **Quando revisar:** marco futuro

# Exemplo preenchido

## Decisões incorporadas recentemente

### [2026-03-09] Preflight Docker antes da execução prática

- **Resumo:** o fluxo oficial agora começa com DOCKER_PREFLIGHT antes de SPEC
- **Motivo:** reduzir risco de execução fora de ambiente controlado
- **Impacto:** AGENTS, CONTEXT, workflows, automação operacional
- **Status:** ativa

### [2026-03-09] Nome formal da engine

- **Resumo:** a engine própria de pipeline passa a se chamar Synapse-Flow
- **Motivo:** reduzir ambiguidade terminológica
- **Impacto:** SDD, TDD, AGENTS, CONTEXT e ADRs
- **Status:** ativa

## Pendências abertas

### [P1] Definir se o DOCKER_PREFLIGHT em CI sobe container completo

- **Contexto:** integração do repo-automation com workflows
- **Descrição:** decidir entre preflight leve com --skip-up ou subida real do container
- **Próximo passo sugerido:** manter leve no CI padrão e criar workflow dedicado de integração
- **Pode virar feature?:** talvez
- **Status:** em análise
