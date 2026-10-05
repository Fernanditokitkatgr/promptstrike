import yaml


def load_suite(ruta):
    with open(ruta, encoding="utf-8") as fichero:
        datos = yaml.safe_load(fichero)
    return datos["attacks"]


ataques = load_suite("corpus/system-prompt-leak.yaml")

for ataque in ataques:
    print(ataque["name"], "→", ataque["payload"])
