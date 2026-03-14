# Operação e Ciclo de Vida (Lifecycle)

Este documento centraliza as instruções operacionais para desenvolvimento local (bootstrap), gerenciamento do runtime residente e controle de execução do pipeline (Synapse-Flow).

## 1. Bootstrap e Desenvolvimento Local

O projeto utiliza `uv` para gerenciamento de dependências e ambiente.

### Preparação do Ambiente

1.  **Instalar uv**: Siga as instruções oficiais (ex: `curl -LsSf https://astral.sh/uv/install.sh | sh`).
2.  **Sincronizar dependências**:
    ```bash
    # Cria/atualiza .venv e instala dependências (incluindo dev)
    uv sync --locked --extra dev
    ```

### Fluxo de Validação (Commit Check)

Antes de commitar ou abrir PR, execute o script de validação que roda formatação, lint, typecheck e testes:

```bash
# Modo padrão (garante sync antes de rodar)
./scripts/commit-check.sh --sync-dev

# Modo rápido (assume que o ambiente já está syncado)
./scripts/commit-check.sh --no-sync
```

### Docker Preflight

O `DOCKER_PREFLIGHT` é um gate operacional.

```bash
# Check leve (apenas config)
./scripts/docker-preflight.sh

# Com build de imagem
./scripts/docker-preflight.sh --build

# Com runtime completo (boot, persistência, integração)
./scripts/docker-preflight.sh --full-runtime
```

---

## 2. Runtime Lifecycle

O SynapseOS opera em modelo dual: **CLI Efêmera** (cliente) e **Runtime Residente** (servidor/worker).

O runtime residente é responsável por:
*   Executar o loop do Worker (processamento de steps).
*   Manter o estado da aplicação (Single Writer).
*   Gerenciar a persistência SQLite.

### Comandos de Runtime

| Comando | Descrição |
| :--- | :--- |
| `synapse runtime start` | Inicia o processo residente em background (daemon). |
| `synapse runtime stop` | Para o processo residente graciosamente. |
| `synapse runtime status` | Exibe o status do processo (PID, uptime) e do worker. |
| `synapse runtime run` | Executa o runtime em foreground (bloqueante), útil para debug. |
| `synapse runtime ready` | Verifica se o runtime está pronto para aceitar comandos (healthcheck). |

**Nota**: O runtime deve estar ativo (`start` ou `run`) para que as runs submetidas em modo `async` sejam processadas pelo worker. Runs em modo `sync` são processadas pelo próprio processo da CLI.

---

## 3. Pipeline Management (Runs)

O gerenciamento de execuções do Synapse-Flow é feito via subcomandos `runs`.

### Submissão de Runs

```bash
# Modo síncrono (bloqueia terminal, roda na CLI) - Ideal para debug/dev
synapse runs submit features/F00-exemplo/SPEC.md --mode sync

# Modo assíncrono (envia para fila, requer runtime start) - Produção
synapse runs submit features/F00-exemplo/SPEC.md --mode async

# Parada programada (Stop At)
synapse runs submit ... --stop-at PLAN
```

### Monitoramento e Controle

| Comando | Descrição |
| :--- | :--- |
| `synapse runs list` | Lista as runs recentes e seus status. |
| `synapse runs show <id>` | Exibe detalhes de uma run, incluindo status dos steps e artifacts. |
| `synapse runs watch` | Abre o Dashboard TUI para monitoramento em tempo real. |
| `synapse runs cancel <id>` | Solicita o cancelamento de uma run em execução. |

### Cancelamento (F40)

O cancelamento (`synapse runs cancel <id>` ou tecla `k` no TUI) envia um sinal para o motor de execução.
*   **Comportamento**: O cancelamento não é imediato (kill). O engine verifica o sinal entre steps.
*   **Estado Final**: A run transita para `cancelling` e termina como `cancelled`.
*   **Cleanup**: Artefatos gerados até o momento são preservados.

### Filtros de Dashboard (F42)

No comando `synapse runs watch`:
*   Use as teclas de seta para navegar.
*   Pressione `Enter` para ver logs do step.
*   Pressione `f` para filtrar steps (ex: mostrar apenas steps com falha).

---

## 4. Auth & RBAC (Local)

O sistema possui um Auth Registry local baseado em arquivo para controle de acesso via CLI.

*   `synapse auth init`: Inicializa o registry e cria o admin.
*   `synapse auth issue`: Emite novos tokens com roles (`viewer`, `operator`, `admin`).
*   `synapse auth disable`: Revoga tokens.

---

## 5. Resolução de Problemas

### Aignt Doctor

Use `synapse doctor` para diagnosticar o ambiente:
*   Verifica instalação do `uv`, `git`, `docker`.
*   Verifica integridade do banco de dados SQLite.
*   Verifica permissões de diretórios de artifacts e estado.

### Logs

*   **Logs da CLI**: Saída padrão no terminal.
*   **Logs do Runtime**: Se iniciado com `start`, os logs vão para onde o daemon gerenciador definir (ou stdout se usar `run`).
*   **Logs de Steps**: Acessíveis via `synapse runs show <id>` (caminhos dos arquivos de log) ou visualizador de logs no Dashboard (`Enter`).
