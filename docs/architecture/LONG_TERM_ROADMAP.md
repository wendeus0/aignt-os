# Roadmap de Longo Prazo - Fase 4 e Fase 5

## Sobre este documento
Este documento estabelece o planejamento estratégico para as fases subsequentes ao ciclo atual (Fase 3 - Resiliência e Controle). Ele segue a filosofia do projeto: evolução feature-by-feature, CLI-first e Spec-Driven Development.

## Fase 4: Hardening e Ecossistema
**Foco**: Segurança robusta, integração com ferramentas externas e experiência de desenvolvimento (DX).

### P0 - Segurança e Compliance (Core Hardening)
1.  **F47 - Advanced RBAC**: Granularidade de permissões por comando e por recurso (não apenas roles estáticas).
    *   *Dependência*: F29 (Auth Foundation).
    *   *Valor*: Permite uso em times maiores com perfis restritos.
2.  **F48 - Audit Logging Export**: Integração com sistemas de SIEM (formato CEF/JSON estruturado) e exportação de logs de auditoria.
    *   *Dependência*: F34/F39 (Logs).
    *   *Valor*: Requisito corporativo para rastreabilidade.
3.  **F49 - Secret Rotation & Vault Integration**: Suporte nativo a HashiCorp Vault ou AWS Secrets Manager para injeção de segredos em tempo de execução.
    *   *Dependência*: F23 (Sanitization).
    *   *Valor*: Elimina segredos estáticos em variáveis de ambiente.

### P1 - Observabilidade Distribuída
1.  **F50 - OpenTelemetry Tracing**: Instrumentação do runtime para exportar traces (Jaeger/Tempo).
    *   *Dependência*: F34 (Logs).
    *   *Valor*: Visualização de gargalos em steps longos ou concorrentes.
2.  **F51 - Prometheus Metrics**: Exposição de endpoint `/metrics` no runtime residente.
    *   *Dependência*: F08 (Runtime Dual).
    *   *Valor*: Monitoramento de saúde, fila de steps e uso de recursos.
3.  **F52 - Performance Profiling CLI**: Comando `aignt runs profile <run_id>` para análise de consumo de CPU/Memória por step.
    *   *Dependência*: F41 (Dashboard Artifacts).
    *   *Valor*: Otimização de custos e recursos.

### P2 - Developer Experience (DX)
1.  **F53 - Interactive Spec Wizard**: Comando `aignt spec new` interativo para gerar esqueletos de features válidos.
    *   *Dependência*: F02 (Spec Engine).
    *   *Valor*: Reduz barreira de entrada para novos desenvolvedores.
2.  **F54 - Local Playground**: Ambiente sandbox isolado para testar steps individuais sem criar uma run completa.
    *   *Dependência*: F24 (Workspace Boundary).
    *   *Valor*: Acelera o ciclo de feedback de desenvolvimento de prompts.
3.  **F55 - Plugin System Architecture**: Arquitetura para carregar adapters de terceiros via `entry_points` do Python.
    *   *Dependência*: F05 (CLI Adapter).
    *   *Valor*: Permite extensão do ecossistema sem inchar o core.

### P3 - Integrações de Ecossistema
1.  **F56 - GitHub App Native**: Adapter oficial para atuar como GitHub App (comentários em PR, checks).
    *   *Dependência*: F55 (Plugin System).
    *   *Valor*: Integração fluida com CI/CD.
2.  **F57 - Notification Channels**: Suporte a Webhooks para Slack/Discord em eventos de run (start, fail, success).
    *   *Dependência*: F40 (Lifecycle).
    *   *Valor*: Notificação proativa para o operador.
3.  **F58 - Issue Tracker Adapter**: Integração básica com Jira/Linear para criar tickets a partir de falhas.
    *   *Dependência*: F55 (Plugin System).
    *   *Valor*: Conecta a operação de IA ao fluxo de trabalho humano.

### P4 - Agendamento Avançado
1.  **F59 - Cron Trigger**: Capacidade de agendar runs recorrentes nativamente no runtime residente.
    *   *Dependência*: F32 (Resident Runtime).
    *   *Valor*: Automação de tarefas de manutenção ou relatórios.
2.  **F60 - Run Dependencies (DAG)**: Permitir que uma run inicie apenas após o sucesso de outra.
    *   *Dependência*: F06 (Pipeline Engine).
    *   *Valor*: Orquestração de fluxos complexos multi-passo.
3.  **F61 - Resource Quotas**: Limites de concorrência e tempo de execução por usuário ou projeto.
    *   *Dependência*: F35 (Ownership Filter).
    *   *Valor*: Proteção contra abuso e controle de custos.

---

## Fase 5: Plataforma e Inteligência
**Foco**: Transformar o orquestrador em uma plataforma inteligente, multi-tenant e escalável.

### P0 - Núcleo Semântico
1.  **F62 - Vector DB Integration**: Integração nativa com Chroma/Qdrant para memória de longo prazo.
    *   *Dependência*: F55 (Plugins).
    *   *Valor*: Permite que agentes aprendam com runs passadas.
2.  **F63 - Semantic Memory Recall**: Injeção automática de contexto relevante (snippets de código, docs) no prompt.
    *   *Dependência*: F62 (Vector DB).
    *   *Valor*: Aumenta precisão e reduz alucinação.
3.  **F64 - History-based Auto-Correction**: Sugestão de correção de comandos baseada em falhas anteriores similares.
    *   *Dependência*: F62 (Vector DB).
    *   *Valor*: Resiliência autônoma.

### P1 - Runtime Distribuído
1.  **F65 - Remote Worker Nodes**: Capacidade de conectar workers em máquinas diferentes ao mesmo control plane.
    *   *Dependência*: F31 (Remote Auth).
    *   *Valor*: Escala horizontal de processamento.
2.  **F66 - Multi-Tenant Control Plane**: Isolamento lógico de dados e execuções por tenant/organização.
    *   *Dependência*: F47 (RBAC).
    *   *Valor*: Suporte a múltiplos times ou clientes.
3.  **F67 - Artifact Sync (S3)**: Armazenamento de artefatos em Object Storage compatível com S3.
    *   *Dependência*: F07 (Persistence).
    *   *Valor*: Persistência durável e desacoplada do disco local.

### P2 - Inteligência Adaptativa
1.  **F68 - Dynamic Spec Refinement**: O próprio agente pode propor melhorias na SPEC durante a execução.
    *   *Dependência*: F02 (Spec Engine).
    *   *Valor*: Evolução contínua dos requisitos.
2.  **F69 - Cost Optimization Agent**: Analisa gastos de tokens e sugere modelos mais baratos para tarefas simples.
    *   *Dependência*: F51 (Metrics).
    *   *Valor*: Eficiência financeira.
3.  **F70 - Security Auto-Remediation**: Detecção e correção automática de vulnerabilidades simples no código gerado.
    *   *Dependência*: F23 (Sanitization).
    *   *Valor*: Shift-left security autônomo.

### P3 - Mercado e Colaboração
1.  **F71 - Skill Registry**: Catálogo centralizado de skills/adapters compartilháveis.
    *   *Dependência*: F55 (Plugins).
    *   *Valor*: Reuso de capacidades comunitárias.
2.  **F72 - Team Workspaces**: Espaços de trabalho compartilhados com permissões e recursos dedicados.
    *   *Dependência*: F66 (Multi-Tenant).
    *   *Valor*: Colaboração em tempo real.
3.  **F73 - Collaborative TUI**: Múltiplos usuários assistindo (`watch`) a mesma run simultaneamente.
    *   *Dependência*: F45 (Output Streaming).
    *   *Valor*: Pair programming/debugging de agentes.

### P4 - Enterprise Readiness
1.  **F74 - SSO/SAML Integration**: Login via Okta/AzureAD/Google Workspace.
    *   *Dependência*: F29 (Auth).
    *   *Valor*: Requisito corporativo de identidade.
2.  **F75 - Compliance Reporting**: Relatórios automatizados para auditorias (SOC2, ISO).
    *   *Dependência*: F48 (Audit Logs).
    *   *Valor*: Redução de custo de conformidade.
3.  **F76 - High Availability (HA)**: Redundância de control plane e failover automático de workers.
    *   *Dependência*: F65 (Remote Workers).
    *   *Valor*: Garantia de SLA.

---

## Localização deste Documento
Este arquivo encontra-se em `docs/architecture/LONG_TERM_ROADMAP.md`.
A documentação da Fase 2 (`docs/architecture/PHASE_2_ROADMAP.md`) foi preservada como registro histórico do baseline.
