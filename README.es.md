# PromptStrike

[English](README.md) · **Español**

> Un scanner de vulnerabilidades para aplicaciones LLM — como `nmap`, pero para prompt injection y jailbreaks.

**Estado:** en desarrollo — Fase 0 de 7 (cimientos).

## Qué hace

Le apuntas a una aplicación basada en un LLM y PromptStrike:

1. **La ataca** con un catálogo de técnicas conocidas (fuga del system prompt, sobrescritura de instrucciones, jailbreaks).
2. **Juzga** cada respuesta para decidir si el ataque ha funcionado, y guarda la evidencia.
3. **Genera un informe** con cada hallazgo, su impacto, una mitigación y su categoría de OWASP LLM.
4. **Mide** el porcentaje de ataques con éxito (Attack Success Rate, ASR) antes y después de aplicar defensas, para que una mitigación quede demostrada y no supuesta.

## Por qué existe

Un LLM recibe las instrucciones del desarrollador y el texto del usuario por el **mismo canal**: una única secuencia de texto. El modelo no tiene una forma fiable de distinguir una instrucción de un dato, así que un usuario puede colar instrucciones que se salten las reglas de la aplicación.

Es la misma causa que la SQL injection: mezclar código y datos. La SQL injection se resolvió con las prepared statements; **los LLMs todavía no tienen un equivalente**. Las defensas solo reducen el riesgo, y por eso hay que probar las aplicaciones de forma sistemática y medir los resultados.

## Cómo funciona

```
  corpus/*.yaml  ──►  Runner  ──►  [ Adapter ]  ──►  App LLM objetivo
   (ataques)            │          local | ollama | api
                        ▼
                     Oráculo  ──►  ¿éxito? + evidencia
                        │
                        ▼
                  results.json  ──►  Reporter  ──►  informe.md
```

Cada pieza es independiente y se comunica con las demás a través de una interfaz clara. Cambiar el modelo objetivo es cambiar un fichero de configuración, no el código.

## Hoja de ruta

| Fase | Entregable | Estado |
|---|---|---|
| 0 | Montaje del proyecto + un bot vulnerable a propósito (`vuln_bot`) | En curso |
| 1 | Catálogo de ataques en YAML, validado, con injection indirecta | Pendiente |
| 2 | Adaptadores para varios proveedores (local, Ollama, API) | Pendiente |
| 3 | Runner + CLI `promptstrike scan` | Pendiente |
| 4 | Oráculo: canary tokens + LLM como juez, con su precisión medida | Pendiente |
| 5 | Informe profesional mapeado al OWASP LLM Top 10 | Pendiente |
| 6 | Defensas + ASR antes/después, comparado con Garak | Pendiente |
| 7 | Atacante automático que reescribe los ataques fallidos (PAIR simplificado) | Pendiente |

Plan completo: [ROADMAP.md](ROADMAP.md).

## Stack (previsto)

Python 3.13 · httpx · PyYAML · Pydantic · Typer · pytest · rich · ruff · Ollama

## Uso responsable

- PromptStrike solo debe usarse contra sistemas **propios o con autorización explícita** para probarlos.
- Los jailbreaks del catálogo persiguen **objetivos inofensivos** (canary tokens, tareas inocuas prohibidas por el system prompt). El catálogo no contiene contenido dañino.

## Referencias

- [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- Herramientas relacionadas: [Garak](https://github.com/NVIDIA/garak) (NVIDIA) · [PyRIT](https://github.com/Azure/PyRIT) (Microsoft)
