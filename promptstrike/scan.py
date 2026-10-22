from promptstrike.loader import load_suite
from promptstrike.targets import create_target, DocumentTarget
from vuln_bot.bot import SYSTEM_PROMPT
import yaml

if __name__ == "__main__":
    # --- Escaneo DIRECTO ---
    print("=== SUITE: system-prompt-leak ===")
    with open("config.yaml", encoding="utf-8") as fichero:
        config = yaml.safe_load(fichero)
    target = create_target(config["target"], SYSTEM_PROMPT)
    ataques = load_suite("corpus/system-prompt-leak.yaml")
    for ataque in ataques:
        respuesta = target.send(ataque.payload)
        print(ataque.id, "→", respuesta)

    # --- Escaneo INDIRECTO ---
    print("\n=== SUITE: indirect-injection ===")
    ataques = load_suite("corpus/indirect-injection.yaml")
    for ataque in ataques:
        target = DocumentTarget(SYSTEM_PROMPT, ataque.document)
        respuesta = target.send(ataque.user_request)
        print(ataque.id, "→", respuesta)
