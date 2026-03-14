---
id: F07-persistence-artifacts
type: feature
summary: Persistir runs, steps, eventos e artefatos do Synapse-Flow em SQLite + filesystem sem puxar escopo de worker.
workspace: .
inputs:
  - docs/architecture/SDD.md
  - docs/architecture/TDD.md
  - docs/architecture/SPEC_FORMAT.md
  - docs/architecture/IMPLEMENTATION_STACK.md
  - features/F06-pipeline-engine-linear/SPEC.md
  - features/f11-runtime-persistente-minimo/SPEC.md
outputs:
  - run_repository_sqlite
  - artifact_store_filesystem
  - pipeline_persistence_hooks
  - persistence_tests
constraints:
  - manter escopo estritamente na persistencia operacional da pipeline
  - nao substituir nem reutilizar o runtime-state.json da F11 como repositorio de runs
  - nao implementar worker, polling, lease, retomada ou scheduler
  - nao introduzir nova CLI publica nesta feature
  - manter o Synapse-Flow como engine propria de pipeline do SynapseOS
acceptance_criteria:
  - Existe um RunRepository em SQLite para persistir runs, steps e eventos da pipeline.
  - Existe um ArtifactStore em filesystem para persistir outputs raw, outputs clean e artefatos nomeados por run e step.
  - Existe lock inicial por run para impedir dupla aquisicao local da mesma run.
  - A PipelineEngine aceita integracao opcional de persistencia sem acoplar SQLite ao core da orquestracao.
  - Uma execucao persistida ate PLAN registra run, steps, eventos e artefatos relevantes.
  - Uma SPEC invalida marca a run como failed antes de PLAN e nao gera artefato de PLAN.
  - Os caminhos padrao de banco e artefatos ficam explicitados na configuracao da aplicacao.
non_goals:
  - worker residente
  - polling de runs pendentes
  - lease ou retomada de run
  - API de rede publica
  - supervisor, retry ou reroute
  - migracoes Alembic nesta feature
dependencies:
  - F06-pipeline-engine-linear
---

# Contexto

Depois da F06, o Synapse-Flow, a engine propria de pipeline do SynapseOS, ja consegue validar SPEC e encadear hand-offs minimos em memoria. O proximo incremento natural do MVP e tornar a run auditavel fora da memoria do processo, registrando metadados operacionais em SQLite e artefatos em filesystem.

Ja existe persistencia local endurecida para o lifecycle do runtime na F11, mas ela cobre apenas `runtime-state.json` do processo residente. Essa persistencia nao substitui a necessidade de um repositorio operacional para runs da pipeline.

# Objetivo

Entregar a base minima de persistencia operacional do SynapseOS para runs lineares:
- `RunRepository` em SQLite para runs, steps e eventos;
- `ArtifactStore` em filesystem para raw, clean e artefatos nomeados por step;
- lock inicial por run;
- integracao opcional com a PipelineEngine atual;
- testes cobrindo caminho feliz ate `PLAN` e falha em `SPEC_VALIDATION`.

# Escopo

## Incluido

- configuracao padrao de caminho para banco de runs e diretorio de artefatos
- repositorio SQLite com schema inicial autocontido
- artifact store em filesystem com paths por `run_id` e `step`
- persistencia de outputs raw e clean quando o step os fornecer
- persistencia de artefatos nomeados do hand-off do step
- lock booleano inicial por run
- observer opcional para registrar lifecycle da pipeline
- runner pequeno para executar pipeline persistida sem alterar a CLI publica
- testes unitarios e de integracao do recorte

## Fora de escopo

- worker, runtime dual, polling, fila ou retomada
- migracoes, versao de schema ou alembic operacional
- reporte final `RUN_REPORT.md`
- adapters reais, subprocessos reais ou parsing adicional
- integracao com Docker alem da validacao operacional padrao do projeto

# Requisitos funcionais

1. O sistema deve criar um identificador de run e persisti-lo antes da execucao da pipeline.
2. O sistema deve impedir a segunda aquisicao local do lock da mesma run.
3. O sistema deve registrar em SQLite o estado atual e o status final da run.
4. O sistema deve registrar em SQLite os steps concluidos da pipeline.
5. O sistema deve registrar em SQLite eventos relevantes como inicio, conclusao e falha.
6. O sistema deve persistir outputs raw e clean por run e step quando disponiveis.
7. O sistema deve persistir artefatos nomeados por run e step no filesystem.
8. O sistema deve marcar a run como `failed` quando a SPEC bloquear a pipeline em `SPEC_VALIDATION`.
9. O sistema nao deve gerar artefato de `PLAN` quando a SPEC for invalida.
10. O core da PipelineEngine deve continuar executavel sem repositorio ou artifact store.

# Requisitos nao funcionais

- A implementacao deve permanecer pequena e local ao MVP.
- O banco deve usar SQLite local sem depender de servico externo.
- O artifact store deve usar paths sanitizados para reduzir risco de path traversal.
- Diretorios e arquivos de artefatos devem usar permissoes restritas adequadas ao uso local.
- A integracao deve preservar o comportamento atual da F06 quando a persistencia estiver ausente.

# Casos de erro

- falha de validacao da SPEC antes de `PLAN`
- tentativa de dupla aquisicao do lock da mesma run
- nomes de step ou artefato com caracteres inseguros
- run inexistente ao consultar repositorio
- falha de escrita no artifact store

# Cenarios verificaveis

## Cenario 1: execucao persistida ate PLAN

- Dado uma SPEC valida
- E um executor fake para `PLAN`
- Quando a pipeline persistida executar ate `PLAN`
- Entao a run fica `completed`
- E os steps `SPEC_VALIDATION` e `PLAN` ficam registrados
- E existem evento de inicio, conclusao de step e conclusao da run
- E o artifact store salva output raw, output clean e `plan_md`

## Cenario 2: bloqueio por SPEC invalida

- Dado uma SPEC invalida
- Quando a pipeline persistida executar
- Entao a run fica `failed` em `SPEC_VALIDATION`
- E existe evento de falha
- E nenhum artefato de `PLAN` e gerado

## Cenario 3: lock inicial da run

- Dado uma run criada no repositório
- Quando o lock e adquirido pela primeira vez
- Entao a aquisicao retorna sucesso
- E uma segunda tentativa retorna falha previsivel

# Observacoes

Esta feature prepara a base operacional para a F08, mas nao entrega worker nem decisao sync/async. O lock aqui e local e inicial, suficiente apenas para evitar dupla aquisicao da mesma run no recorte atual.
