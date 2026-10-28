from typing import Literal
from pydantic import BaseModel
import yaml


DirectTechnique = Literal[
    "repetition", "translation", "obfuscation", "authority",
    "direct-override", "identity-override", "instruction-update",
    "conditional-trigger", "echo",
]

IndirectTechnique = Literal["hidden-instruction", "fake-email"]


class IndirectAttack(BaseModel):
    id: str
    name: str
    technique: IndirectTechnique
    user_request: str
    document: str


class DirectAttack(BaseModel):
    id: str
    name: str
    technique: DirectTechnique
    payload: str


class Suite(BaseModel):
    name: str
    canary: str
    attacks: list[DirectAttack | IndirectAttack]


def load_suite(path):
    with open(path, encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if data["suite"] == "indirect-injection":
        attack_model = IndirectAttack
    else:
        attack_model = DirectAttack

    attacks = []
    for raw_attack in data["attacks"]:
        attack = attack_model.model_validate(raw_attack)
        attacks.append(attack)
    return Suite(name=data["suite"], canary=data["canary"], attacks=attacks)


if __name__ == "__main__":
    paths = [
        "corpus/indirect-injection.yaml",
        "corpus/instruction-override.yaml",
        "corpus/system-prompt-leak.yaml",
    ]
    for path in paths:
        suite = load_suite(path)
        for attack in suite.attacks:
            print(attack.id, "→", attack.technique)
