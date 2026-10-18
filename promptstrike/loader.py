import yaml
from pydantic import BaseModel
from typing import Literal


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


def load_suite(ruta):
    with open(ruta, encoding="utf-8") as fichero:
        datos = yaml.safe_load(fichero)

    if datos["suite"] == "indirect-injection":
        molde = IndirectAttack
    else:
        molde = DirectAttack

    ataques = []
    for ataque_crudo in datos["attacks"]:
        ataque = molde.model_validate(ataque_crudo)
        ataques.append(ataque)
    return ataques


rutas = [
    "corpus/indirect-injection.yaml",
    "corpus/instruction-override.yaml",
    "corpus/system-prompt-leak.yaml",]

for ruta in rutas:
    ataques = load_suite(ruta)
    for ataque in ataques:
        print(ataque.id, "→", ataque.technique)
