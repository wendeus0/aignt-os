---
id: F20-public-onboarding
type: feature
summary: Criar um onboarding publico curto e oficial para a primeira run, deixando explicito o boundary entre diagnostico local e preflight operacional.
inputs:
  - CONTEXT.md
  - docs/architecture/SDD.md
  - docs/architecture/TDD.md
  - docs/architecture/SPEC_FORMAT.md
  - docs/architecture/PHASE_2_ROADMAP.md
  - README.md
  - features/F18-canonical-happy-path/SPEC.md
  - features/F19-environment-doctor/SPEC.md
outputs:
  - public_onboarding_quickstart_contract
  - onboarding_troubleshooting_contract
  - feature_notes
constraints:
  - "manter o Synapse-Flow como a engine propria de pipeline do SynapseOS"
  - "manter o recorte restrito a onboarding publico curto, sem documentacao enciclopedica"
  - "usar o caminho canonico atual da CLI publica sem inventar comandos novos"
  - "explicitar no onboarding que `synapse doctor` e diagnostico local e advisory, nao preflight operacional completo"
  - "encaminhar tarefas dependentes de Docker, container, build, boot, persistencia operacional ou integracao para `repo-preflight`, sem duplicar esse fluxo na F20"
  - "nao introduzir auto-setup, script de bootstrap novo, TUI nem validacao pratica dependente de Docker"
acceptance_criteria:
  - "Existe um quickstart publico curto e oficial que orienta a primeira run usando a CLI publica atual, do diagnostico inicial ate a inspecao do resultado."
  - "O onboarding explica explicitamente o boundary entre `synapse doctor` e `repo-preflight`, incluindo quando o doctor basta e quando o operador deve escalar para preflight operacional."
  - "O onboarding inclui troubleshooting essencial para os checks de `runtime_state`, `runs_db` e `artifacts_dir`, sem prometer auto-correcao."
  - "A documentacao resultante continua alinhada ao caminho canonico da F18 e nao contradiz os contratos publicos de erro e exit code da F21."
  - "A frente deixa claro que o fluxo minimo atual continua local e sync-first, e que Docker, credenciais externas e runtime completo so entram quando houver necessidade operacional explicita."
non_goals:
  - "escrever documentacao completa de arquitetura, instalacao ou operacao avancada"
  - "alterar o comportamento de `synapse doctor`, `synapse runs submit` ou `synapse runs show`"
  - "substituir `repo-preflight` por checklist manual no quickstart"
  - "introduzir exemplos multiplos de adapters reais, TUI ou quickstart paralelo para modos async"
security_notes:
  - "nao instruir o operador a expor credenciais, tokens ou segredos em comandos de exemplo"
  - "nao transformar o onboarding em bypass de `repo-preflight` para cenarios que dependam de Docker ou container"
dependencies:
  - F18-canonical-happy-path
  - F19-environment-doctor
  - F21-cli-error-model-and-exit-codes
---

# Contexto

Depois de `F15`, `F16`, `F21`, `F18` e `F19`, o SynapseOS ja possui um caminho publico minimo para diagnosticar o ambiente local, submeter uma run e inspecionar o resultado, enquanto o Synapse-Flow continua sendo a engine propria de pipeline do SynapseOS. O risco residual remanescente nao e de falta de comando, e sim de expectativa: um operador novo pode supor que `synapse doctor` substitui preflight operacional completo ou que o quickstart precisa cobrir todos os cenarios de Docker, runtime persistente e credenciais externas.

A `F20` existe para reduzir esse atrito de entrada sem ampliar o produto. O objetivo nao e escrever documentacao extensa, mas consolidar um caminho curto, oficial e coerente com o baseline atual, deixando claro quando o fluxo minimo e suficiente e quando o operador precisa sair do onboarding e seguir um gate operacional proprio.

# Objetivo

Entregar um onboarding publico curto e oficial para a primeira run, capaz de orientar um operador externo pelo caminho canonico atual da CLI e de explicitar o boundary entre diagnostico local (`synapse doctor`) e preflight operacional (`repo-preflight`) sem alterar o comportamento dos comandos existentes.

# Escopo

## Incluido

- quickstart oficial curto para a primeira run com a CLI publica atual
- troubleshooting essencial para `synapse doctor`, `synapse runs submit` e `synapse runs show`
- explicacao objetiva do boundary entre diagnostico local e preflight operacional
- alinhamento da documentacao publica ao caminho canonico sync-first atual
- `NOTES.md` da feature para registrar decisoes de recorte e linguagem

## Fora de escopo

- nova superficie de produto ou comando novo na CLI
- tutorial enciclopedico de arquitetura, adapters ou deploy
- automacao de bootstrap local, script de setup ou validacao pratica dependente de Docker
- cobertura detalhada de credenciais externas, providers reais ou fluxos async como onboarding principal

# Requisitos funcionais

1. A feature deve materializar um quickstart curto e oficial para a primeira run usando a CLI publica existente.
2. O quickstart deve seguir o caminho canonico atual:
   - diagnosticar o ambiente local
   - validar a leitura do estado resultante
   - submeter uma run
   - inspecionar a run criada
3. O onboarding deve usar `synapse doctor` como diagnostico local inicial e deixar explicito que ele nao substitui `repo-preflight`.
4. O onboarding deve definir quando escalar para preflight operacional, no minimo para cenarios que dependam de:
   - Docker ou container
   - build de imagem
   - boot ou lifecycle do runtime persistente
   - persistencia operacional ou integracao real em container
5. O troubleshooting essencial deve cobrir, no minimo:
   - `runtime_state` em `warn` ou `fail`
   - `runs_db` em `fail`
   - `artifacts_dir` em `fail`
   - falha de SPEC invalida no submit
6. A documentacao deve preservar o contrato publico atual de erro da F21, sem prometer tracebacks, auto-fix ou codigos de saida nao existentes.
7. O onboarding deve indicar explicitamente que o fluxo minimo atual e local e sync-first, e que cenarios mais pesados saem do quickstart.

# Requisitos nao funcionais

- O material deve permanecer curto, legivel e apto a manutencao sem drift rapido.
- O recorte deve ficar concentrado em onboarding e troubleshooting essencial, sem virar guia de operacao completo.
- A feature nao deve depender de DOCKER_PREFLIGHT para ser especificada, porque a F20 documenta o boundary operacional em vez de executar esse fluxo.

# Casos de erro

- operador interpreta `synapse doctor` como garantia de ambiente completo para Docker ou runtime persistente
- operador encontra `runtime_state=warn` e nao sabe se isso bloqueia a primeira run sync
- operador recebe `runs_db=fail` ou `artifacts_dir=fail` e nao encontra orientacao objetiva de correcao
- onboarding orienta fluxo que contradiz o caminho canonico da F18 ou o contrato de erro da F21
- onboarding cresce para um guia enciclopedico e perde clareza operacional

# Cenarios verificaveis

## Cenario 1: primeira run pelo caminho minimo atual

- Dado um operador sem contexto previo do projeto
- Quando ele seguir o quickstart oficial da F20
- Entao ele entende a ordem minima dos comandos publicos para diagnosticar, submeter e inspecionar a primeira run
- E o fluxo descrito permanece alinhado a F18 e F19

## Cenario 2: boundary entre doctor e preflight

- Dado um operador que precisa validar um cenario dependente de Docker ou runtime persistente
- Quando ele consultar o onboarding oficial
- Entao ele encontra uma orientacao explicita de que `synapse doctor` nao substitui `repo-preflight`
- E entende quando precisa sair do quickstart e escalar para preflight operacional

## Cenario 3: troubleshooting essencial do doctor

- Dado um operador que recebe `warn` ou `fail` em um dos checks do doctor
- Quando ele consultar o troubleshooting essencial do onboarding
- Entao ele encontra proximos passos objetivos para `runtime_state`, `runs_db` e `artifacts_dir`
- E a documentacao nao promete auto-correcao nem cobertura operacional fora do recorte

# Observacoes

Esta frente mitiga o risco residual da F19 pelo eixo correto: clareza de contrato e expectativa do operador, nao ampliacao silenciosa do `synapse doctor`. Se o projeto passar a exigir Docker, runtime persistente ativo ou credenciais externas como parte do fluxo minimo oficial, a revisao necessaria deve atingir explicitamente a F19 e a F20, em vez de tentar absorver esse crescimento por texto ambiguo no onboarding.
