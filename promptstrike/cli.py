import typer
import yaml

from promptstrike.scan import scan_suite
from promptstrike.targets import create_target
from vuln_bot.bot import SYSTEM_PROMPT

SUITES = [
    "corpus/system-prompt-leak.yaml",
    "corpus/instruction-override.yaml",
    "corpus/indirect-injection.yaml",
]

with open("config.yaml", encoding="utf-8") as file:
    CONFIG = yaml.safe_load(file)

app = typer.Typer()


@app.callback()
def main():
    """PromptStrike: vulnerability scanner for LLM chatbots."""


@app.command()
def scan(target: str = CONFIG["target"], repeats: int = CONFIG["number_of_repeats"]):
    """Run every attack suite against a target and report the ASR."""
    llm_target = create_target(target, SYSTEM_PROMPT)
    for path in SUITES:
        scan_suite(path, llm_target, repeats)


if __name__ == "__main__":
    app()
