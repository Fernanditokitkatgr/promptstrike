# PromptStrike

[English](README.md) · **Español**

> Un scanner de vulnerabilidades para aplicaciones LLM — como `nmap`, pero para prompt injection y jailbreaks.

**Estado:** en desarrollo — Fase 2 de 7 (adaptadores de objetivo).

## Qué hace

Le apuntas a una aplicación basada en un LLM y PromptStrike:

1. **La ataca** con un catálogo de técnicas conocidas (fuga del system prompt, sobrescritura de instrucciones, jailbreaks).
2. **Juzga** cada respuesta para decidir si el ataque ha funcionado, y guarda la evidencia.
3. **Genera un informe** con cada hallazgo, su impacto, una mitigación y su categoría de OWASP LLM.
4. **Mide** el porcentaje de ataques con éxito (Attack Success Rate, ASR) antes y después de aplicar defensas, para que una mitigación quede demostrada y no supuesta.

Los pasos 2–4 están en la hoja de ruta; en "Qué funciona hoy" tienes lo que ya se ejecuta.

## Qué funciona hoy

- Un **bot de demostración vulnerable a propósito** (`vuln_bot`) con un secreto escondido en su system prompt (`SECRETO-42`), usado como objetivo de prácticas seguro.
- Un **catálogo de ataques en YAML** repartido en tres suites — 13 ataques en total: `system-prompt-leak` (5), `instruction-override` (5, con un caso de "eco" pensado para hacer caer a un oráculo ingenuo en un falso positivo) e `indirect-injection` (3, órdenes escondidas dentro de un documento que el bot debe resumir).
- Un **cargador del catálogo tipado** que valida cada ataque con modelos de Pydantic (`DirectAttack` / `IndirectAttack`) y listas de técnicas con `Literal`, de modo que un ataque mal formado o mal etiquetado falla de forma ruidosa.
- **Adaptadores de objetivo tras una única interfaz** (la ABC `Target`): `LocalTarget` (bot determinista offline), `OllamaTarget` (modelos locales vía Ollama), `DocumentTarget` (injection indirecta a través de un documento) y `APITarget` (OpenAI, `gpt-4o-mini`), elegidos con una factoría `create_target` gobernada por `config.yaml` (`local | ollama | api`).
- Un **script de escaneo** (`python -m promptstrike.scan`) que lanza la suite `system-prompt-leak` contra el objetivo configurado y la suite `indirect-injection` a través de `DocumentTarget`, imprimiendo la respuesta de cada ataque. Juzgar esas respuestas de forma automática es la Fase 4.
- **14 tests unitarios que pasan**, cubriendo el cargador y los adaptadores de objetivo.

## Puesta en marcha

```bash
# 1. Clona el repositorio
git clone https://github.com/Fernanditokitkatgr/promptstrike.git
cd promptstrike

# 2. Crea y activa un entorno virtual (Python 3.13)
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows (PowerShell)
# source .venv/bin/activate     # macOS / Linux

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Ejecuta los tests
python -m pytest

# 5. Lanza un escaneo
python -m promptstrike.scan
```

El escaneo lee `config.yaml`, que elige el objetivo:

- `target: local` — se ejecuta totalmente offline contra el `vuln_bot` incluido (el valor por defecto; no necesita nada más).
- `target: ollama` — necesita una instancia de [Ollama](https://ollama.com) en marcha.
- `target: api` — necesita una `OPENAI_API_KEY` en un fichero `.env` en la raíz del repositorio.

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
| 0 | Montaje del proyecto + un bot vulnerable a propósito (`vuln_bot`) | ✅ Hecho |
| 1 | Catálogo de ataques en YAML, validado, con injection indirecta | ✅ Hecho |
| 2 | Adaptadores para varios proveedores (local, Ollama, API) | 🚧 En curso |
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
