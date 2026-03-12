---
name: repo-preflight
description: Use esta skill quando a tarefa exigir validação operacional ligada a Docker, imagem, boot, ciclo de vida, persistência ou integração. Ela executa e interpreta o DOCKER_PREFLIGHT do projeto, mantendo o preflight leve por padrão e promovendo build ou runtime completo apenas quando explicitamente necessário.
---

# Objetivo
Executar o gate operacional `DOCKER_PREFLIGHT` do projeto com o menor custo e risco possíveis.

## Leia antes de agir
1. `AGENTS.md`
2. `README.md`
3. `compose.yaml`
4. `compose.dev.yaml`
5. `Dockerfile`
6. `scripts/docker-preflight.sh`
7. scripts operacionais relacionados, se existirem

## Use esta skill quando
- a tarefa depender de Docker ou container de forma prática
- for necessário validar `compose config`
- for necessário validar build de imagem
- for necessário validar boot, ciclo de vida, persistência ou integração em runtime
- a mudança tocar infraestrutura operacional de container

## Não use esta skill quando
- a tarefa ainda estiver em `SPEC`
- a tarefa for apenas criar testes RED
- a tarefa for lógica de produto sem dependência prática de Docker
- a tarefa for fluxo final de commit/push/PR
- a tarefa for apenas automação de workflow sem necessidade de preflight real

## Regras obrigatórias
- O preflight padrão deve ser leve.
- Comece por validação estática.
- Só promova para build quando houver necessidade explícita.
- Só promova para runtime completo quando a tarefa tocar boot, ciclo de vida, persistência ou integração.
- Diferencie claramente:
  - validado estaticamente
  - buildado
  - iniciado em runtime completo

## Estratégia
1. Descobrir o nível mínimo de validação necessário.
2. Executar o preflight mais barato que responde à pergunta operacional.
3. Registrar resultado objetivo.
4. Se houver falha, encaminhar para `debug-failure` quando a causa ainda não estiver classificada.

## Saída esperada
Produza um resultado em um destes formatos:

- `PREFLIGHT_OK_STATIC`
- `PREFLIGHT_OK_BUILD`
- `PREFLIGHT_OK_RUNTIME`
- `PREFLIGHT_BLOCKED`

Inclua:
- comandos executados
- nível validado
- evidências objetivas
- riscos remanescentes
- próximo passo recomendado
