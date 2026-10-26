def repeat_attack(target, payload, n):
    respuestas = []
    for _ in range(n):
        respuesta = target.send(payload)
        respuestas.append(respuesta)
    return respuestas


def attack_success_rate(responses, canary):
    successes = []
    for response in responses:
        successes.append(canary in response)
    return successes.count(True) / len(successes) * 100
