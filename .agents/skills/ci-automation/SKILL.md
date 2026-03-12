---
name: ci-automation
description: Use esta skill quando a tarefa envolver GitHub Actions, hooks locais, scripts operacionais, gatilhos de rebuild, validações automatizadas de repositório ou ajustes de automação de entrega. Não use para Docker preflight prático, implementação de lógica de produto ou fluxo final de commit/push/PR.
---

# Objetivo
Implementar ou ajustar automações operacionais do repositório com escopo estritamente de CI, hooks e scripts.

## Leia antes de agir
1. `AGENTS.md`
2. `README.md`
3. `.github/workflows/*`
4. `.githooks/*`
5. `scripts/*`
6. `pyproject.toml`
7. `compose.yaml` e `Dockerfile` apenas se a automação depender deles

## Use esta skill quando
- a tarefa pedir criação ou ajuste de GitHub Actions
- a tarefa pedir hooks locais
- a tarefa pedir scripts operacionais
- a tarefa pedir gatilhos de rebuild
- a tarefa pedir validações automatizadas de CI/CD do repositório

## Não use esta skill quando
- a tarefa exigir DOCKER_PREFLIGHT real
- a tarefa for branch sync
- a tarefa for commit/push/PR
- a tarefa for SPEC, RED, GREEN ou REFACTOR de produto
- a tarefa for revisão de segurança

## Regras obrigatórias
- Mantenha o escopo operacional.
- Prefira automações simples, auditáveis e baratas.
- Não crie pipelines pesados cedo demais.
- Preserve compatibilidade com o MVP e a fase atual do projeto.
- Não assuma acesso externo real; se faltar acesso, gere os arquivos prontos e documente o uso.

## Estratégia
1. Identificar o loop manual que está sendo automatizado.
2. Escolher a menor automação suficiente.
3. Ajustar workflow, hook ou script.
4. Validar impacto nos comandos já existentes.
5. Reportar mudanças, gatilhos e limitações.

## Saída esperada
Inclua:
- arquivos alterados
- gatilho da automação
- comportamento esperado
- riscos operacionais
- dependências externas, se houver
