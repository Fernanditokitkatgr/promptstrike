import yaml
from pydantic import BaseModel


class IndirectAttack(BaseModel):
    id: str
    name: str
    technique: str
    user_request: str
    document: str


class DirectAttack(BaseModel):
    id: str
    name: str
    technique: str
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
