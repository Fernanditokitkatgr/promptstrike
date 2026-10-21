from promptstrike.loader import load_suite
from promptstrike.targets import LocalTarget, OllamaTarget, create_target
from vuln_bot.bot import SYSTEM_PROMPT
import yaml

if __name__ == "__main__":
    with open("config.yaml", encoding="utf-8") as fichero:
        config = yaml.safe_load(fichero)

    target = create_target(config["target"], SYSTEM_PROMPT)

    ataques = load_suite("corpus/system-prompt-leak.yaml")
    for ataque in ataques:
        respuesta = target.send(ataque.payload)
        print(ataque.id, "respuesta de modelo:", respuesta)
