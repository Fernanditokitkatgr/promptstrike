from promptstrike.loader import load_suite
from promptstrike.targets import LocalTarget, OllamaTarget
from vuln_bot.bot import SYSTEM_PROMPT

if __name__ == "__main__":
    target = OllamaTarget(SYSTEM_PROMPT)

    ataques = load_suite("corpus/system-prompt-leak.yaml")
    for ataque in ataques:
        respuesta = target.send(ataque.payload)
        print(ataque.id, "respuesta de modelo:", respuesta)
