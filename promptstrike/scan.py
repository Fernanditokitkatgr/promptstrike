from promptstrike.loader import load_suite
from promptstrike.runner import repeat_attack, attack_success_rate
from promptstrike.targets import create_target, DocumentTarget
from vuln_bot.bot import SYSTEM_PROMPT
import yaml

if __name__ == "__main__":
    # --- Direct scan ---
    print("=== SUITE: system-prompt-leak ===")

    with open("config.yaml", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    target = create_target(config["target"], SYSTEM_PROMPT)
    suite = load_suite("corpus/system-prompt-leak.yaml")
    attack_asrs = []
    for attack in suite.attacks:
        responses = repeat_attack(
            target, attack.payload, config["number_of_repeats"])
        asr = attack_success_rate(responses, suite.canary)
        print(attack.id, "→ ASR", asr, "%")
        attack_asrs.append(asr)
    suite_asr = sum(attack_asrs) / len(attack_asrs)
    print("SUITE ASR →", suite_asr, "%")

    # --- Indirect scan ---
    print("\n=== SUITE: indirect-injection ===")
    suite = load_suite("corpus/indirect-injection.yaml")
    attack_asrs = []
    for attack in suite.attacks:
        target = DocumentTarget(SYSTEM_PROMPT, attack.document)
        responses = repeat_attack(
            target, attack.user_request, config["number_of_repeats"])
        asr = attack_success_rate(responses, suite.canary)
        print(attack.id, "→ ASR", asr, "%")
        attack_asrs.append(asr)
    suite_asr = sum(attack_asrs) / len(attack_asrs)
    print("SUITE ASR →", suite_asr, "%")
