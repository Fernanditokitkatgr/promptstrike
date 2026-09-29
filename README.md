# PromptStrike

**English** · [Español](README.es.md)

> A vulnerability scanner for LLM applications — like `nmap`, but for prompt injection and jailbreaks.

**Status:** in development — Phase 0 of 6 (foundations).

## What it does

You point PromptStrike at an LLM-powered application. It then:

1. **Attacks** it with a corpus of known techniques (system prompt leakage, instruction override, jailbreaks).
2. **Judges** each response to decide whether the attack succeeded, and keeps the evidence.
3. **Reports** every finding with its impact, a mitigation and its OWASP LLM category.
4. **Measures** the Attack Success Rate (ASR) before and after applying defenses, so a mitigation is proven, not assumed.

## Why it exists

LLMs receive the developer's instructions and the user's input through the **same channel**: a single sequence of text. The model has no reliable way to tell an instruction from data, so a user can smuggle in instructions that override the application's rules.

It is the same root cause as SQL injection — mixing code and data. SQL injection was solved with prepared statements; **LLMs have no equivalent yet**. Defenses only reduce the risk, which is why applications need to be tested systematically and the results measured.

## How it works

```
  corpus/*.yaml  ──►  Runner  ──►  [ Adapter ]  ──►  Target LLM app
   (attacks)            │          local | ollama | api
                        ▼
                     Oracle  ──►  success? + evidence
                        │
                        ▼
                  results.json  ──►  Reporter  ──►  report.md
```

Each piece is independent and talks to the others through a clear interface. Changing the target model means changing a config file, not the code.

## Roadmap

| Phase | Deliverable | Status |
|---|---|---|
| 0 | Project setup + a deliberately vulnerable bot (`vuln_bot`) | In progress |
| 1 | Attack corpus in YAML, validated | Planned |
| 2 | Multi-provider adapters (local, Ollama, API) | Planned |
| 3 | Runner + `promptstrike scan` CLI | Planned |
| 4 | Oracle: canary tokens + LLM-as-judge, with measured accuracy | Planned |
| 5 | Professional report mapped to OWASP LLM Top 10 | Planned |
| 6 | Defenses + ASR before/after, compared against Garak | Planned |

Full plan: [ROADMAP.md](ROADMAP.md) (in Spanish).

## Tech stack (planned)

Python 3.13 · httpx · PyYAML · Pydantic · Typer · pytest · rich · ruff · Ollama

## Responsible use

- PromptStrike must only be used against systems **you own or are explicitly authorized to test**.
- Jailbreak suites use **harmless proxy objectives** (canary tokens, benign tasks forbidden by the system prompt). The corpus contains no harmful content.

## References

- [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- Related tools: [Garak](https://github.com/NVIDIA/garak) (NVIDIA) · [PyRIT](https://github.com/Azure/PyRIT) (Microsoft)
