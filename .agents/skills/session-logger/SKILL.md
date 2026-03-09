---
name: session-logger
description: Use esta skill quando a tarefa for registrar, consolidar ou atualizar o histórico operacional da sessão de IA em ERROR_LOG.md e PENDING_LOG.md, incluindo erros relevantes, pendências abertas e um resumo curto das decisões incorporadas. Não use esta skill para implementar código de produto, criar SPECs de feature, escrever testes RED ou refatorar código.
---

# Objetivo

Registrar e organizar a memória operacional do uso da IA no projeto, sem alterar a lógica do produto.

Esta skill pode considerar a sessão inteira como fonte de contexto, mas sua função não é transcrever a conversa. Sua função é **organizar corretamente** as informações relevantes nos arquivos apropriados.

# Arquivos de responsabilidade

Esta skill atua somente sobre:
- `ERROR_LOG.md`
- `PENDING_LOG.md`

# Leia antes de agir

Leia nesta ordem:
1. `AGENTS.md`
2. `CONTEXT.md`
3. `ERROR_LOG.md`, se existir
4. `PENDING_LOG.md`, se existir
5. `git status`
6. `git diff --stat`
7. instrução atual do usuário
8. conteúdo relevante da sessão atual, quando necessário

# Quando esta skill deve ser usada

Use esta skill quando:
- o usuário pedir para registrar erros da sessão
- o usuário pedir para registrar pendências
- o usuário pedir para resumir decisões incorporadas
- a sessão estiver terminando e for necessário deixar um handoff operacional
- for necessário transformar observações soltas em backlog ou pontos de atenção

# Quando esta skill NÃO deve ser usada

Não use esta skill para:
- implementar código de produto
- editar `SPEC.md`
- escrever testes RED
- fazer GREEN/REFACTOR
- atualizar ADRs
- alterar arquitetura do projeto
- substituir logs técnicos de execução detalhada
- transcrever ou resumir integralmente a conversa

# Escopo de cada arquivo

## ERROR_LOG.md
Registre apenas erros relevantes ocorridos durante o uso da IA/Codex, especialmente os que impactaram:
- ambiente local
- Docker
- Git/worktrees
- testes
- automações
- skills/agentes
- execução prática da feature

## PENDING_LOG.md
Registre:
- pendências abertas
- ideias de futuras features
- pontos de atenção futuros
- resumo curto das decisões incorporadas recentemente

# Regras obrigatórias

- Você pode usar a sessão inteira como contexto, mas deve extrair apenas o que tem valor durável.
- Não transforme os arquivos em transcrição da conversa.
- Organize corretamente cada informação no arquivo e na seção adequados.
- Não misture erro com pendência.
- Não misture decisão incorporada com log técnico bruto.
- Seja curto, claro e útil.
- Não invente erro, decisão ou pendência que não ocorreu.
- Se faltar confirmação, marque como “a validar”.
- Não replique conteúdo já evidente em commits se isso não agregar contexto.
- Prefira atualizar entradas existentes a duplicar informação.

# Formato esperado

## ERROR_LOG.md
Cada erro deve conter:
- data/hora
- contexto
- ação/comando relacionado
- erro observado
- causa identificada (se conhecida)
- ação tomada
- status
- observação futura

## PENDING_LOG.md
Deve conter:
- seção de decisões incorporadas recentemente
- seção de pendências abertas
- seção de pontos de atenção futuros

# Processo

1. Analise a sessão atual e identifique apenas os fatos relevantes e duráveis.
2. Classifique cada item como:
   - erro relevante
   - decisão incorporada
   - pendência
   - ponto de atenção
3. Organize cada item no arquivo correto e na seção correta.
4. Reescreva de forma objetiva e limpa.
5. Atualize os arquivos sem duplicação desnecessária.
6. Não altere outros arquivos do projeto.

# Critérios de qualidade

Antes de encerrar, confirme:
- a sessão foi usada como contexto, mas não foi transcrita
- os registros estão curtos, úteis e organizados
- não há duplicação desnecessária
- os erros estão em `ERROR_LOG.md`
- as pendências e decisões estão em `PENDING_LOG.md`
- nenhum arquivo fora do escopo foi alterado

# Saída final esperada

Entregue apenas:
1. quais logs foram atualizados
2. como as informações foram organizadas
3. resumo do que foi registrado
4. itens que ficaram pendentes de validação, se houver
