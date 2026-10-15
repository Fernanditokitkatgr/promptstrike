import yaml
from pydantic import BaseModel


class Attack(BaseModel):
    id: str
    name: str
    technique: str
    user_request: str
    document: str


def load_suite(ruta):
    with open(ruta, encoding="utf-8") as fichero:
        datos = yaml.safe_load(fichero)

    ataques = []
    for ataque_crudo in datos["attacks"]:
        ataque = Attack.model_validate(ataque_crudo)
        ataques.append(ataque)
    return ataques


ataques = load_suite("corpus/indirect-injection.yaml")

for ataque in ataques:
    print(ataque.id, "→", ataque.document)
