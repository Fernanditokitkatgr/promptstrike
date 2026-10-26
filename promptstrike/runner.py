def repeat_attack(target, payload, n):
    responses = []
    for _ in range(n):
        response = target.send(payload)
        responses.append(response)
    return responses


def attack_success_rate(responses, canary):
    successes = []
    for response in responses:
        successes.append(canary in response)
    return successes.count(True) / len(successes) * 100
