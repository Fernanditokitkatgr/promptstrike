from promptstrike.loader import load_suite
from promptstrike.targets import create_target, DocumentTarget
from vuln_bot.bot import SYSTEM_PROMPT
import yaml

if __name__ == "__main__":
    # --- Direct scan ---
    print("=== SUITE: system-prompt-leak ===")
    with open("config.yaml", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    target = create_target(config["target"], SYSTEM_PROMPT)
    attacks = load_suite("corpus/system-prompt-leak.yaml")
    for attack in attacks:
        response = target.send(attack.payload)
        print(attack.id, "→", response)

    # --- Indirect scan ---
    print("\n=== SUITE: indirect-injection ===")
    attacks = load_suite("corpus/indirect-injection.yaml")
    for attack in attacks:
        target = DocumentTarget(SYSTEM_PROMPT, attack.document)
        response = target.send(attack.user_request)
        print(attack.id, "→", response)
