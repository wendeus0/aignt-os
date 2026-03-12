---
name: report-writer
description: Use esta skill depois de SECURITY_REVIEW para consolidar o resultado da feature ou da tarefa em um relatório curto e auditável: o que mudou, por que mudou, como foi validado, quais riscos restaram e quais são os próximos passos. Não use para commitar, revisar segurança ou executar automação operacional.
---

# Objetivo
Fechar a frente atual com um relatório técnico curto, útil e auditável.

## Leia antes de agir
1. `AGENTS.md`
2. `SPEC.md` da feature, se existir
3. diff final
4. saída do `quality-gate`
5. saída do `security-review`
6. `NOTES.md`, `RUN_REPORT.md` ou artefatos equivalentes, quando relevantes

## Use esta skill quando
- a implementação já terminou
- o quality gate já terminou
- a security review já terminou
- for hora de preparar handoff, registro técnico ou fechamento da feature

## Não use esta skill quando
- a tarefa ainda estiver em SPEC
- a mudança ainda estiver em RED ou GREEN
- a revisão de segurança ainda estiver pendente
- o objetivo for commit/push/PR

## Estrutura do relatório
Produza:
1. objetivo da mudança
2. escopo alterado
3. validações executadas
4. riscos residuais
5. follow-ups
6. status final da frente

## Regras obrigatórias
- Seja factual.
- Não esconda lacunas.
- Diferencie claramente o que foi validado do que foi apenas inferido.
- Mantenha o texto curto e útil para revisão futura.

## Saída esperada
Um relatório conciso com:
- resumo executivo
- arquivos/áreas afetadas
- evidências de validação
- riscos remanescentes
- recomendação final (`READY_FOR_COMMIT` ou `NOT_READY_FOR_COMMIT`)
