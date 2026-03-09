# ERROR_LOG.md

## Como usar

Registre apenas erros relevantes ocorridos durante o uso da IA/Codex, especialmente quando impactarem:

- execução da feature
- ambiente local
- Docker
- Git/worktree
- testes
- automações
- skills/agentes

Cada entrada deve ser curta e objetiva.

---

## [YYYY-MM-DD HH:MM] Título curto do erro

- **Contexto:** em que tarefa/feature isso ocorreu
- **Comando ou ação relacionada:** comando, prompt ou etapa
- **Erro observado:** mensagem resumida
- **Causa identificada:** causa raiz, se conhecida
- **Ação tomada:** o que foi feito para corrigir
- **Status:** resolvido | mitigado | pendente
- **Observação futura:** o que evitar ou monitorar depois

## Exemplo preenchido (avalie as informações abaixo apanas para fins de parametrização)

## [2026-03-09 03:49] Docker daemon não subia

- **Contexto:** preparação do ambiente para automação Docker
- **Comando ou ação relacionada:** `systemctl start docker`
- **Erro observado:** falha ao iniciar o docker.service
- **Causa identificada:** módulos do kernel fora de sincronia após atualização
- **Ação tomada:** reboot do sistema
- **Status:** resolvido
- **Observação futura:** sempre validar kernel/módulos após instalar Docker no Arch
