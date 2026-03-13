---
id: F30-auth-registry-cli
type: feature
summary: Adicionar CLI local para inicializar, emitir e desabilitar tokens do auth registry sem editar JSON manualmente.
inputs:
  - CONTEXT.md
  - docs/architecture/SDD.md
  - docs/architecture/TDD.md
  - docs/architecture/SPEC_FORMAT.md
  - docs/IDEAS.md
  - features/F29-auth-rbac-foundation/SPEC.md
  - src/aignt_os/auth.py
  - src/aignt_os/cli/app.py
outputs:
  - auth_registry_cli
  - auth_registry_token_lifecycle
  - feature_notes
constraints:
  - "manter o AIgnt-Synapse-Flow como a engine propria de pipeline do AIgnt OS"
  - "nao introduzir socket, daemon remoto, auth remota, SQLite nova ou RBAC distribuido"
  - "manter a persistencia do registry em JSON local com escrita atomica e permissoes privadas"
  - "nao persistir token bruto em disco, logs ou mensagens de erro"
  - "preservar o comportamento atual de `runs submit` e `runtime start|run|stop` quando auth ja estiver configurada"
  - "nao exigir DOCKER_PREFLIGHT porque a frente nao depende de Docker, boot em container ou integracao externa"
acceptance_criteria:
  - "Existe um grupo publico `aignt auth` com os comandos `init`, `issue` e `disable`."
  - "`aignt auth init --principal-id <id>` cria um registry novo, falha se o arquivo ja existir e imprime um token bruto apenas uma vez junto do `token_id` gerado."
  - "`aignt auth issue --principal-id <id>` emite um novo token para principal existente; quando o principal nao existir, o comando exige `--role viewer|operator`, cria o principal e retorna token bruto apenas uma vez com `token_id`."
  - "`aignt auth issue` falha com erro de uso quando `--role` conflita com o principal ja persistido."
  - "`aignt auth disable --token-id <id>` marca o token como desabilitado sem remover historico e retorna `Not found:` quando o token nao existir."
  - "O registry persiste `token_id`, `principal_id`, `token_sha256` e `disabled`, sem token bruto em claro."
  - "Um token desabilitado deixa de autenticar `runs submit` e `runtime start|run|stop`, retornando `Authentication error:`."
  - "Existe cobertura unitaria para inicializacao, emissao, conflito de role e disable; e cobertura de integracao para a nova CLI publica."
non_goals:
  - "adicionar operacao remota, socket autenticado ou handshake entre processos"
  - "criar gestao ampla de usuarios, grupos ou multiplas politicas de RBAC"
  - "listar tokens em claro ou permitir recuperar token bruto depois da emissao"
  - "mudar os comandos publicos de leitura (`doctor`, `version`, `runs list|show`, `runtime status|ready`)"
security_notes:
  - "o token bruto deve ser exibido somente no stdout nominal de `init` e `issue`"
  - "mensagens de erro nao devem vazar token bruto, hash SHA-256 ou payload completo do registry"
  - "disable deve manter comportamento fail-closed: token desabilitado passa a ser tratado como invalido"
dependencies:
  - F29-auth-rbac-foundation
  - F21-cli-error-model-and-exit-codes
---

# Contexto

A `F29-auth-rbac-foundation` introduziu a fundacao local de auth opt-in para os comandos mutaveis da CLI, mas deixou o provisionamento do registry como edicao manual de JSON. Isso cria atrito operacional desnecessario e torna a rotacao ou revogacao de tokens mais propensa a erro humano, embora o AIgnt-Synapse-Flow continue sendo a engine propria de pipeline do AIgnt OS e o baseline atual ja tenha enforcement de auth funcionando.

O residual pequeno e coerente com o estado do repositorio nao e abrir auth remota nem socket. O menor recorte util e fornecer uma CLI local para bootstrap do registry e lifecycle basico de tokens, mantendo o storage atual, as roles atuais e o boundary local da `F29`.

# Objetivo

Adicionar uma CLI local de provisionamento para o auth registry, cobrindo bootstrap, emissao e disable de tokens sem editar JSON manualmente, preservando a fundacao de auth local opt-in da `F29`.

# Escopo

## Incluido

- grupo publico `aignt auth`
- comandos `init`, `issue` e `disable`
- persistencia de `token_id` estavel por token
- criacao implicita de principal em `issue` quando `--role` for informado
- desabilitacao de token sem apagar historico
- testes unitarios e de integracao da nova superficie publica
- alinhamento de `docs/IDEAS.md` ao baseline pos-`F28`/`F29`
- `NOTES.md`, `CHECKLIST.md` e `REPORT.md` proprios da feature

## Fora de escopo

- socket, auth remota e operacao entre hosts
- rotacao automatica em lote
- policy engine generica
- recovery de token bruto depois da emissao
- listagem administrativa completa de principals e tokens

# Requisitos funcionais

1. O sistema deve permitir inicializar um registry novo pela CLI.
2. O sistema deve emitir token novo para principal existente.
3. O sistema deve permitir criar principal novo em `issue` quando `--role` for informado.
4. O sistema deve impedir mudanca silenciosa de role para principal existente.
5. O sistema deve permitir desabilitar token por `token_id`.
6. O token desabilitado deve falhar na autenticacao dos comandos mutaveis ja protegidos pela `F29`.
7. O sistema deve manter apenas hash SHA-256 do token persistido em disco.

# Requisitos nao funcionais

- a feature deve caber em 1 a 3 dias
- o registry deve continuar usando escrita atomica e permissoes privadas
- a implementacao deve permanecer local e CLI-first
- a mudanca deve ser reversivel e sem ADR nova

# Casos de erro

- `auth init` com registry ja existente
- `auth issue` para principal novo sem `--role`
- `auth issue` com `--role` conflitante para principal existente
- `auth disable` para `token_id` inexistente
- registry ausente ou corrompido nas operacoes de issue/disable

# Cenarios verificaveis

## Cenario 1: bootstrap inicial do registry

- Dado que auth ainda nao foi provisionada localmente
- Quando `aignt auth init --principal-id local-operator` for executado
- Entao um registry novo e criado com um principal `operator`
- E o comando retorna um `token_id`
- E o comando imprime um token bruto apenas nessa execucao

## Cenario 2: emissao para principal existente

- Dado um registry valido com principal `operator-user`
- Quando `aignt auth issue --principal-id operator-user` for executado
- Entao um novo token e emitido para esse principal
- E o token bruto nao fica persistido no arquivo

## Cenario 3: criacao explicita de principal novo

- Dado um registry valido sem principal `viewer-user`
- Quando `aignt auth issue --principal-id viewer-user --role viewer` for executado
- Entao o principal e criado
- E um token novo e emitido para ele

## Cenario 4: conflito de role falha como uso invalido

- Dado um registry valido com principal `viewer-user`
- Quando `aignt auth issue --principal-id viewer-user --role operator` for executado
- Entao a CLI retorna `Usage error:`
- E nenhum novo token e persistido

## Cenario 5: disable revoga autenticacao

- Dado um token emitido para um principal `operator`
- Quando `aignt auth disable --token-id <id>` for executado
- Entao o token fica marcado como desabilitado no registry
- E futuras chamadas autenticadas com esse token retornam `Authentication error:`

# Observacoes

Esta frente fecha apenas a ergonomia local do registry de auth. Operacao remota, socket autenticado, provisao entre hosts e ampliacao de RBAC continuam explicitamente adiados para uma frente propria futura.
