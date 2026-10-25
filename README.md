# PromptStrike

**English** · [Español](README.es.md)

> A vulnerability scanner for LLM applications — like `nmap`, but for prompt injection and jailbreaks.

**Status:** in development — Phase 2 of 7 (target adapters).

## What it does

You point PromptStrike at an LLM-powered application. It then:

1. **Attacks** it with a corpus of known techniques (system prompt leakage, instruction override, jailbreaks).
2. **Judges** each response to decide whether the attack succeeded, and keeps the evidence.
3. **Reports** every finding with its impact, a mitigation and its OWASP LLM category.
4. **Measures** the Attack Success Rate (ASR) before and after applying defenses, so a mitigation is proven, not assumed.

Steps 2–4 are on the roadmap; see "What works today" below for what already runs.

## What works today

- A **deliberately vulnerable demo bot** (`vuln_bot`) with a secret hidden in its system prompt (`SECRETO-42`), used as a safe practice target.
- An **attack corpus in YAML** across three suites — 13 attacks in total: `system-prompt-leak` (5), `instruction-override` (5, including an "echo" case designed to trip a naive oracle into a false positive) and `indirect-injection` (3, orders hidden inside a document the bot is asked to summarize).
- A **typed corpus loader** that validates every attack with Pydantic models (`DirectAttack` / `IndirectAttack`) and `Literal` technique lists, so a malformed or mislabelled attack fails loudly.
- **Target adapters behind a single interface** (the `Target` ABC): `LocalTarget` (deterministic offline bot), `OllamaTarget` (local models via Ollama), `DocumentTarget` (indirect injection through a document) and `APITarget` (OpenAI, `gpt-4o-mini`), chosen with a `create_target` factory driven by `config.yaml` (`local | ollama | api`).
- A **scan script** (`python -m promptstrike.scan`) that runs the `system-prompt-leak` suite against the configured target and the `indirect-injection` suite through `DocumentTarget`, printing each attack's response. Judging those responses automatically is Phase 4.
- **14 passing unit tests** covering the loader and the target adapters.

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/Fernanditokitkatgr/promptstrike.git
cd promptstrike

# 2. Create and activate a virtual environment (Python 3.13)
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows (PowerShell)
# source .venv/bin/activate     # macOS / Linux

# 3. Install the dependencies
pip install -r requirements.txt

# 4. Run the tests
python -m pytest

# 5. Run a scan
python -m promptstrike.scan
```

The scan reads `config.yaml`, which selects the target:

- `target: local` — runs fully offline against the bundled `vuln_bot` (the default; no setup needed).
- `target: ollama` — needs a running [Ollama](https://ollama.com) instance.
- `target: api` — needs an `OPENAI_API_KEY` in a `.env` file at the repo root.

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
| 0 | Project setup + a deliberately vulnerable bot (`vuln_bot`) | ✅ Done |
| 1 | Attack corpus in YAML, validated, including indirect injection | ✅ Done |
| 2 | Multi-provider adapters (local, Ollama, API) | 🚧 In progress |
| 3 | Runner + `promptstrike scan` CLI | Planned |
| 4 | Oracle: canary tokens + LLM-as-judge, with measured accuracy | Planned |
| 5 | Professional report mapped to OWASP LLM Top 10 | Planned |
| 6 | Defenses + ASR before/after, compared against Garak | Planned |
| 7 | Automated attacker that rewrites failed attacks (simplified PAIR) | Planned |

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
