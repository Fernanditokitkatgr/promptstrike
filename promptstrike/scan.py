from promptstrike.loader import load_suite, IndirectAttack
from promptstrike.runner import repeat_attack, attack_success_rate
from promptstrike.targets import create_target, DocumentTarget
from vuln_bot.bot import SYSTEM_PROMPT
import yaml


def scan_suite(route_yaml, target, repeats):
    suite = load_suite(route_yaml)
    print("\n=== SUITE:", suite.name, "===")
    attack_asrs = []
    for attack in suite.attacks:
        if isinstance(attack, IndirectAttack):
            attack_target = DocumentTarget(SYSTEM_PROMPT, attack.document)
            message = attack.user_request
        else:
            attack_target = target
            message = attack.payload
        responses = repeat_attack(attack_target, message, repeats)
        asr = attack_success_rate(responses, suite.canary)
        print(attack.id, "→ ASR", asr, "%")
        attack_asrs.append(asr)
    suite_asr = sum(attack_asrs) / len(attack_asrs)
    print("SUITE ASR →", suite_asr, "%")
    return suite_asr


if __name__ == "__main__":
    with open("config.yaml", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    target = create_target(config["target"], SYSTEM_PROMPT)
    repeats = config["number_of_repeats"]
    scan_suite("corpus/system-prompt-leak.yaml", target, repeats)
    scan_suite("corpus/instruction-override.yaml", target, repeats)
    scan_suite("corpus/indirect-injection.yaml", target, repeats)
