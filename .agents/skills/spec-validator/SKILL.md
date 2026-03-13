---
name: spec-validator
description: Use esta skill quando a tarefa for validar uma SPEC.md existente com `validate_spec_file()` antes de passar para TDD. Não use esta skill para editar a SPEC, implementar código ou validar qualidade de código.
---

# Objetivo

Executar `validate_spec_file()` sobre a SPEC da feature atual, interpretar os erros retornados e garantir que a SPEC está pronta para alimentar `test-red`.

# Leia antes de agir

Leia nesta ordem:

1. `docs/architecture/SPEC_FORMAT.md`
2. `features/<feature>/SPEC.md`

# Quando esta skill deve ser usada

Use esta skill quando:

- `spec-editor` produziu ou atualizou uma `SPEC.md`
- a SPEC existe mas nunca foi validada programaticamente
- um erro de validação bloqueou `test-red` ou `green-refactor`
- for necessário confirmar que o YAML frontmatter e as seções obrigatórias estão corretos

# Quando esta skill NÃO deve ser usada

Não use esta skill para:

- editar ou reescrever a SPEC (use `spec-editor`)
- validar código, testes ou qualidade técnica (use `quality-gate`)
- validar imagem Docker ou runtime (use `repo-preflight`)
- resolver ambiguidades de requisito sem antes consultar o usuário

# Restrições obrigatórias

- Execute sempre com `uv run --no-sync` para não alterar o ambiente.
- Nunca edite `SPEC.md` diretamente nesta skill — apenas reporte os erros.
- Se a validação falhar, entregue a lista de erros completa e pare: não tente corrigir automaticamente sem instrução do usuário.
- Trabalhe uma feature por vez.

# Processo

1. Identifique o caminho da SPEC: `features/<feature>/SPEC.md`.
2. Execute:

```bash
uv run --no-sync python -c "
from pathlib import Path
from aignt_os.specs.validator import validate_spec_file
result = validate_spec_file(Path('features/<feature>/SPEC.md'))
print(result)
"
```

3. Interprete a saída:
   - Se `validate_spec_file` retornar sem exceção: SPEC válida — registre o resultado e sinalize que `test-red` pode prosseguir.
   - Se levantar exceção ou retornar erros: liste cada erro com descrição clara do campo ou seção afetada.
4. Não prossiga para testes ou código.

# Erros comuns e como reportá-los

| Erro | Significado | O que reportar |
|---|---|---|
| Campo YAML ausente | `id`, `type`, `summary`, `inputs`, `outputs`, `acceptance_criteria` ou `non_goals` faltando | Nome do campo ausente |
| Seção de corpo ausente | `# Contexto` ou `# Objetivo` como H1 não encontrada | Nome da seção ausente |
| Heading com nível errado | Seção obrigatória escrita como `##` em vez de `#` | Linha e nível encontrado vs. esperado |
| YAML inválido | Frontmatter malformado | Mensagem de erro do parser |

# Saída final esperada

Entregue:

1. Resultado bruto do comando (`print(result)`)
2. Interpretação: SPEC válida ou lista de erros classificados
3. Próximo passo recomendado: `test-red` se válida, ou `spec-editor` com lista de correções se inválida
