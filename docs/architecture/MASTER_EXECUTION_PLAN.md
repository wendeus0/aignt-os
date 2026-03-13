# Master Execution Plan: Fase 3b à Fase 5

Este documento consolida o plano de execução encadeado para levar o AIgnt OS do estado atual (pós-F40) até a conclusão da Fase 5 (Plataforma Inteligente). Ele preenche as lacunas de definição entre a Fase 3 e a Fase 4 e detalha a estratégia de implementação.

## Estado Atual
- **Fase 2**: Concluída (F15-F22).
- **Fase 3a (Parcial)**: Em andamento/Specada (F23-F40). Foco em TUI, Logs e Cancelamento.
- **Próximo Passo Imediato**: Fase 3b (Consolidação da Experiência e Preparação para Hardening).

---

## Fase 3b: Consolidação da Experiência (F41-F46)
**Objetivo**: Polir a experiência do operador (TUI/CLI) e preparar o terreno arquitetural para o RBAC da Fase 4.

### F41 - Dashboard Artifacts Explorer
- **Resumo**: Navegação e visualização de artefatos gerados (arquivos, imagens) diretamente na TUI.
- **Valor**: Evita sair do terminal para ver resultados.
- **Dependência**: F39 (Dashboard Logs), F17 (Artifact Preview CLI).

### F42 - Real-time Output Streaming
- **Resumo**: Suporte a streaming de logs em tempo real na CLI (`runs follow`) e na TUI.
- **Valor**: Feedback imediato para runs longas.
- **Dependência**: F40 (Cancellation), F34 (Async Submit).

### F43 - Runtime Robustness (Timeouts & Retries)
- **Resumo**: Configuração granular de timeouts por step e políticas de retry exponencial.
- **Valor**: Resiliência contra falhas transientes de LLMs/APIs.
- **Dependência**: F09 (Supervisor).

### F44 - Auth Backend Abstraction
- **Resumo**: Refatoração do módulo de auth para suportar múltiplos providers (preparação para F47).
- **Valor**: Desacoplamento necessário para RBAC e SSO.
- **Dependência**: F29 (Auth Foundation).

### F45 - TUI Performance Optimization
- **Resumo**: Otimização de renderização da TUI para logs massivos e listas longas de steps.
- **Valor**: Fluidez operacional em runs complexas.
- **Dependência**: F39, F41.

### F46 - Technical Debt & Coverage Boost
- **Resumo**: Sprint dedicada a limpeza de código, aumento de cobertura de testes e atualização de deps.
- **Valor**: Base sólida antes da complexidade da Fase 4.
- **Meta**: Coverage > 85%, Zero Critical Issues no linter.

---

## Fase 4: Hardening e Ecossistema (F47-F61)
**Objetivo**: Segurança corporativa, observabilidade distribuída e extensibilidade.

### P0 - Segurança e Compliance
- **F47 - Advanced RBAC**: Permissões granulares por comando/recurso.
- **F48 - Audit Logging Export**: Exportação CEF/JSON para SIEM.
- **F49 - Secret Rotation & Vault**: Integração com Vault/AWS Secrets.

### P1 - Observabilidade
- **F50 - OpenTelemetry Tracing**: Tracing distribuído do runtime.
- **F51 - Prometheus Metrics**: Endpoint `/metrics`.
- **F52 - Performance Profiling CLI**: Análise de consumo de recursos por run.

### P2 - Developer Experience
- **F53 - Interactive Spec Wizard**: `aignt spec new`.
- **F54 - Local Playground**: Sandbox para testes de steps isolados.
- **F55 - Plugin System Architecture**: Carregamento dinâmico de adapters.

### P3 - Integrações
- **F56 - GitHub App Native**: Adapter oficial.
- **F57 - Notification Channels**: Webhooks (Slack/Discord).
- **F58 - Issue Tracker Adapter**: Jira/Linear.

### P4 - Agendamento
- **F59 - Cron Trigger**: Agendamento nativo.
- **F60 - Run Dependencies (DAG)**: Dependências entre runs.
- **F61 - Resource Quotas**: Limites por tenant.

---

## Fase 5: Plataforma e Inteligência (F62-F76)
**Objetivo**: Transformação em plataforma multi-tenant com inteligência autônoma.

### P0 - Núcleo Semântico
- **F62 - Vector DB Integration**: Memória de longo prazo (Chroma/Qdrant).
- **F63 - Semantic Memory Recall**: Injeção automática de contexto.
- **F64 - History-based Auto-Correction**: Auto-cura baseada em histórico.

### P1 - Runtime Distribuído
- **F65 - Remote Worker Nodes**: Workers em hosts distintos.
- **F66 - Multi-Tenant Control Plane**: Isolamento lógico.
- **F67 - Artifact Sync (S3)**: Persistência em Object Storage.

### P2 - Inteligência Adaptativa
- **F68 - Dynamic Spec Refinement**: Agente propõe melhorias na SPEC.
- **F69 - Cost Optimization Agent**: Escolha dinâmica de modelos.
- **F70 - Security Auto-Remediation**: Correção automática de vulnerabilidades.

### P3 - Mercado e Colaboração
- **F71 - Skill Registry**: Catálogo de skills.
- **F72 - Team Workspaces**: Espaços colaborativos.
- **F73 - Collaborative TUI**: `watch` compartilhado.

### P4 - Enterprise Readiness
- **F74 - SSO/SAML Integration**: Okta/AzureAD.
- **F75 - Compliance Reporting**: Relatórios SOC2/ISO.
- **F76 - High Availability (HA)**: Failover de control plane.

---

## Estratégia de Execução

1. **Sequencialidade**: As features devem ser implementadas na ordem numérica (F41 -> F76) salvo bloqueios externos.
2. **Spec-First**: Nenhuma linha de código sem `SPEC.md` aprovada (usar `spec-editor`).
3. **Quality Gates**: Manter `TEST_RED -> CODE_GREEN -> REFACTOR` rigorosamente.
4. **Documentação**: Atualizar `docs/` a cada marco (P0, P1, etc).

Este plano serve como a fonte da verdade para a execução das próximas etapas.
