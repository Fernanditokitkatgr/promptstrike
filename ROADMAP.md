# PromptStrike — Hoja de ruta

> **Un scanner de vulnerabilidades para aplicaciones LLM.**
> Como `nmap`, pero para prompt injection y jailbreaks.
> Le apuntas a un endpoint LLM, lanza ataques, decide cuáles funcionaron y genera un informe profesional.

**Autor:** Fernando · **Nivel de partida:** Python básico → objetivo: Python fluido + AI Security
**Ritmo estimado:** 5–8 h/semana · **Duración del sub-proyecto 1:** ~5,5–6,5 meses
**Filosofía:** conceptos antes que código. No copiar: entender. Tony Stark sabe física.

**Orden de proyectos:** PromptStrike primero (enseña el Python que Kaudal necesita). Después, Kaudal.
En el sub-proyecto 2, el agente de Kaudal será el objetivo de PromptStrike.

---

## Por qué este proyecto (validado contra ofertas reales, sept 2026)

Cruce directo con requisitos de ofertas reales (Amazon AI Red Team, U.S. Bank, guías 2026):

| Requisito de la oferta | Pieza del proyecto |
|---|---|
| Prompt injection, model evaluation, adversarial testing | Núcleo del scanner |
| Frameworks tipo Garak / PyRIT | Construyes una versión mínima entendida por dentro |
| Python para automatización de seguridad | Todo el proyecto |
| API security, autenticación, secretos | Runner + Adapter |
| Multi-provider (no atarse a un proveedor) | Capa de adaptadores |
| Traducir hallazgos a recomendaciones claras | Reporter (vuln → evidencia → impacto → mitigación) |
| Jailbreaks, data leakage, system prompt leak | Suites del corpus |
| Attack Success Rate como métrica | Output principal |

**Frameworks de referencia del sector:** OWASP Top 10 for LLM Applications (2025), OWASP Top 10 for Agentic Applications (2026), MITRE ATLAS, NIST AI RMF.

**Posicionamiento honesto:** con este proyecto no se apunta a "red teamer senior" (suele pedir años de
experiencia en seguridad). Se apunta a **AI Engineer junior que sabe atacar y evaluar LLMs**, y a puestos
de evaluación y seguridad de IA.

---

## Arquitectura

```
  corpus/*.yaml  ──►  Runner  ──►  [ Adapter ]  ──►  TARGET
   (los ataques)        │          local | ollama | api
                        ▼
                     Oráculo  ──►  ¿éxito? (+ evidencia)
                        │
                        ▼
                     results.json ──► Reporter ──► informe .md
```

**Principio de diseño clave:** el ataque (corpus), el envío (runner/adapter), el juicio (oráculo)
y el informe (reporter) son piezas **separadas** que se comunican por interfaces claras.
Esto no es capricho: es lo que hace la herramienta mantenible, testeable y multi-provider.

**Stack:** Python 3.13 · `httpx` · `PyYAML` · `Pydantic` · `Typer` · `pytest` · `rich` · `ruff` · Ollama.
Todo estándar de industria, nada exótico.

**Lo que NO entra en el sub-proyecto 1 (YAGNI):** RAG, agentes con tools, vector DB, interfaz web, Docker.
Eso es sub-proyecto 2 y 3. Ahora: una CLI terminada, tuya y explicable línea a línea.

---

## Uso responsable (no negociable)

- PromptStrike se usa **solo** contra sistemas propios o con autorización explícita. Queda escrito en el
  `README` desde el primer commit y la CLI lo recuerda al ejecutarse.
- Los jailbreaks del corpus persiguen **objetivos proxy inofensivos** (canaries, tareas prohibidas por el
  system prompt pero inocuas), nunca contenido dañino real. Así trabaja la gente seria del sector.

---

## Fases del sub-proyecto 1

Cada fase sigue el bucle: **fundamento → práctica → ataque → defensa → explicación → siguiente nivel.**
Cada fase deja algo commiteado en git. Nada de "lo termino todo y subo al final".
Cada fase se cierra con un **post corto** (LinkedIn o blog) explicando lo aprendido: si no sabes
contarlo, no lo has entendido.

### Fase 0 — Cimientos (setup + primer contacto) · 1–2 semanas
- **Construyes:** entorno Python (venv, pip), repo git, estructura de carpetas, `README` inicial con la política de uso responsable.
- **Python que aprendes:** cómo se organiza un proyecto real, entornos virtuales, imports, `git` básico.
- **Seguridad que aprendes:** qué es un system prompt, superficie de ataque de un LLM, terminología (payload, ASR, target).
- **Entrevista — te pueden preguntar:** "¿Qué es el prompt injection y por qué es distinto de un jailbreak?"
- **Entregable:** repo inicializado + `vuln_bot` de ~30 líneas con un secreto en el system prompt: primero simulado
  (para entender el flujo) y después contra un **modelo real en Ollama**. Tu primer ataque, a mano, a un LLM de verdad.

### Fase 1 — El corpus de ataques · 2–3 semanas
- **Construyes:** ficheros YAML con ataques organizados por suite (system-prompt-leak, instruction-override, **indirect-injection**: el ataque va escondido dentro de un documento), y el cargador Python que los lee y los **valida con Pydantic**.
- **Python que aprendes:** leer ficheros, diccionarios, listas, parsear YAML, validar datos de entrada, **primeros tests con pytest**.
- **Seguridad que aprendes:** anatomía de un prompt injection directo; por qué separar *datos* (el ataque) de *código* (el runner); objetivos proxy para jailbreaks.
- **Entrevista:** "¿Por qué existe el prompt injection a nivel conceptual?" → mismo canal para instrucciones y datos.
- **Entregable:** `corpus/` con 3 suites y ≥15 payloads; script que los lista; tests del cargador (un YAML mal escrito falla con un error claro).

### Fase 2 — El Adapter (la jugada estrella) · 2–3 semanas
- **Construyes:** una interfaz `Target` con implementaciones intercambiables: `LocalTarget`, luego `OllamaTarget` (el objetivo real por defecto), luego `APITarget`.
- **Python que aprendes:** clases, herencia/interfaces, abstracción, por qué programar contra una interfaz y no contra una implementación.
- **Seguridad que aprendes:** por qué las herramientas pro (PyRIT, Garak, promptfoo) son multi-provider.
- **Entrevista:** "¿Cómo diseñarías una herramienta de red teaming que no dependa de un solo proveedor?"
- **Entregable:** cambiar de target = cambiar un YAML de config, sin tocar la lógica. Tests con un target falso. El `vuln_bot` gana un **modo "resume este documento"**, para poder probar la injection indirecta.

### Fase 3 — El Runner + la CLI · 3 semanas
- **Construyes:** el motor que coge cada payload del corpus y lo manda al target vía el adapter, **N veces por payload** (los LLMs no son deterministas). Y el comando `promptstrike scan` con **Typer** y `pyproject.toml`.
- **Python que aprendes:** bucles, peticiones HTTP (`httpx`), manejo de errores de red, timeouts, secretos por variable de entorno, empaquetado y entry points.
- **Seguridad que aprendes:** API security, autenticación, rate limits, gestión de secretos (nunca hardcodear keys); por qué un ataque que falla 7 veces puede funcionar a la 8ª.
- **Entrevista:** "¿Cómo gestionas credenciales en una herramienta de seguridad?" · "¿Cómo tratas el no determinismo de un LLM al evaluarlo?"
- **Entregable:** `promptstrike scan` lanza el corpus entero contra el `vuln_bot`, con repeticiones y temperatura configurables, y guarda las respuestas.

### Fase 4 — El Oráculo ⭐ (la joya) · 3–4 semanas
- **Construyes:** el juez que decide, por cada respuesta, si el ataque tuvo éxito, con su evidencia. Tres piezas:
  - **Canary tokens**: una cadena única en el secreto; si aparece en la respuesta, hay fuga. Preciso y barato.
  - **LLM-as-judge** para los jailbreaks, donde un regex no llega.
  - **Medir al juez**: un pequeño dataset etiquetado a mano para calcular su precisión y su recall. Un oráculo sin medir es una opinión.
- **Python que aprendes:** lógica de detección, regex, casos límite, funciones puras y **TDD** (el test primero, luego el código).
- **Seguridad que aprendes:** el CONCEPTO profundo del prompt injection; falsos positivos/negativos; por qué no hay solución sintáctica completa (paralelo con SQLi antes de prepared statements).
- **Entrevista:** "¿Cómo determinas automáticamente si un prompt injection funcionó? ¿Cómo manejas falsos positivos?"
- **Entregable:** oráculo que marca cada ataque como VULNERABLE/resistente con la evidencia adjunta, y la precisión/recall del juez medidas.

### Fase 5 — El Reporter · 2 semanas
- **Construyes:** los resultados se guardan en **`results.json` (fuente de verdad)** y el informe Markdown se genera a partir de él: por vuln → payload, respuesta (evidencia), impacto, mitigación y **su ID de OWASP LLM** (p. ej. LLM01 injection, LLM07 fuga de system prompt).
- **Python que aprendes:** serialización JSON, plantillas, formateo de texto/f-strings, escritura de ficheros.
- **Seguridad que aprendes:** reporting profesional — la habilidad que pide casi toda oferta y casi nadie entrena; taxonomías OWASP y MITRE ATLAS.
- **Entrevista:** "Enséñame un informe tuyo de una vulnerabilidad." (literalmente enseñas el fichero)
- **Entregable:** `reports/*.md` con formato profesional + salida bonita en terminal (`rich`).

### Fase 6 — Defensa y cierre (el bucle completo) · 3 semanas
- **Construyes:** mitigaciones en el `vuln_bot` (delimitadores, instrucciones defensivas, filtros) y vuelves a escanear para MEDIR cuánto baja el Attack Success Rate, **con repeticiones e intervalo de confianza** para que la mejora no sea suerte. Cierre: pasar **Garak** contra el mismo `vuln_bot` y comparar sus resultados con los tuyos.
- **Python que aprendes:** `pytest` a fondo, refactor, documentar.
- **Seguridad que aprendes:** defensa real, y lo más importante — **medir** que una mitigación funciona (antes X% ASR, después Y%).
- **Entrevista:** "Encontraste la vuln, ¿cómo la mitigas y cómo demuestras que la mitigación sirve?"
- **Entregable:** tests que pasan, `README` con GIF de la demo, tabla ASR antes/después, comparativa con Garak.

### Fase 7 — El atacante automático (estado del arte) · 3 semanas
- **Construyes:** un LLM atacante que, cuando un ataque falla, lo **reescribe** guiándose por el juez de la Fase 4, y repite hasta tener éxito o agotar intentos. Una versión simplificada de **PAIR**, una de las técnicas de referencia en red teaming automatizado (junto con TAP y Crescendo).
- **Python que aprendes:** bucles de optimización, gestión de estado entre intentos, límites de coste y de iteraciones.
- **Seguridad que aprendes:** cómo se hace el red teaming de verdad en 2026: atacante + juez + iteración. Por qué un catálogo fijo se queda corto.
- **Entrevista:** "¿Cómo automatizarías el descubrimiento de prompt injections?" · "¿Qué es PAIR / TAP?"
- **Entregable:** `promptstrike scan --auto` encuentra ataques que el catálogo fijo no encontraba, medido con el ASR. **Herramienta terminada.**

---

## Definición de "terminado" (sub-proyecto 1)

- [ ] `promptstrike scan` corre de principio a fin contra el `vuln_bot` en Ollama.
- [ ] Al menos 3 suites de ataque y ≥15 payloads en el corpus, validados con Pydantic.
- [ ] Adapter funciona contra local y Ollama; documentado cómo añadir una API.
- [ ] Cada ataque se repite N veces; el ASR se reporta con su intervalo de confianza.
- [ ] Oráculo con evidencia por cada hallazgo y la precisión/recall del juez medidas.
- [ ] `results.json` + informe Markdown profesional con IDs de OWASP LLM.
- [ ] Demostración del bucle defensa: ASR antes vs. después de mitigar.
- [ ] Comparativa con Garak.
- [ ] Suite de injection indirecta (ataque dentro de un documento).
- [ ] Atacante automático (PAIR simplificado) que mejora el ASR del catálogo fijo.
- [ ] Tests con `pytest` que pasan (desde la Fase 1).
- [ ] `README` con GIF de la demo, arquitectura y política de uso responsable.
- [ ] Un post publicado por fase.
- [ ] **Puedo explicar cada línea del repo en una entrevista.** ← el de verdad.

---

## Después (sub-proyectos futuros — NO ahora)

2. **El objetivo serio:** sustituir el `vuln_bot` por una app con RAG + vector DB + agente con tools (candidato: el agente de Kaudal).
   Nuevos ataques: injection indirecta contra agentes con herramientas (medir si EJECUTA acciones), RAG poisoning, tool abuse, data exfiltration. Ataques de varios turnos (Crescendo).
3. **Producción:** Docker, observabilidad, despliegue, CI (promptstrike como test que falla el build), salida SARIF.

Cada sub-proyecto: su propio diseño, su propio ciclo. No se diseña hoy lo que se construye dentro de un año.

---

## Registro de cambios

- **2026-09-25** — Incorporadas 8 mejoras: modelo real (Ollama) desde la Fase 0, tests desde la Fase 1,
  repeticiones por ataque, oráculo con canary + LLM-as-judge medido, `results.json` + IDs OWASP en el informe,
  política de uso responsable, comparativa con Garak, post por fase. Añadidos Pydantic, Typer y ruff al stack.
- **2026-10-01** — Para estar al día con el estado del arte de 2026: suite de injection indirecta en la Fase 1 (+ modo documento
  del `vuln_bot` en la Fase 2) y nueva **Fase 7: atacante automático** (PAIR simplificado). Duración: ~5,5–6,5 meses.

---

*Documento vivo. Se actualiza al cerrar cada fase.*
