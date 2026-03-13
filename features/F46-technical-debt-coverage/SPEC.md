---
id: F46-technical-debt-coverage
type: feature
summary: "Sprint dedicada a limpeza de código, aumento de cobertura de testes e atualização de deps"
inputs:
  - Relatório de coverage atual
  - Relatório de lint atual
outputs:
  - Coverage > 85%
  - Dependências atualizadas (uv lock)
  - Remoção de código morto ou não utilizado
acceptance_criteria:
  - "Coverage report deve indicar cobertura global acima de 85%"
  - "Nenhum erro crítico ou warning severo no linter"
  - "Dependências de dev e runtime atualizadas e testadas"
non_goals:
  - Refatoração arquitetural profunda (F47+ cuidará disso se necessário)
  - Alterar contratos públicos da CLI
---

# Contexto

Ao final da Fase 3b, acumulamos funcionalidades e possivelmente débito técnico. Antes de iniciar a Fase 4 (Hardening e Ecossistema), que introduz complexidade de segurança e observabilidade, precisamos garantir que a base atual esteja sólida, bem testada e com dependências atualizadas.

# Objetivo

Executar uma rodada de limpeza e melhoria de qualidade:
1.  Identificar e cobrir áreas críticas com baixa cobertura de testes.
2.  Atualizar dependências do projeto via `uv`.
3.  Sanar quaisquer pendências de linting ou typing que foram suprimidas ou ignoradas.
