import yaml
from promptstrike.oracle import canary_found

CANARY = "SECRETO-42"


def load_leak_labels(path):
    with open(path, encoding="utf-8") as file:
        data = yaml.safe_load(file)
        responses = data["responses"]
        return responses


responses = load_leak_labels("evals/leak_labels.yaml")
true_positives = 0
false_positives = 0
false_negatives = 0
true_negatives = 0

for item in responses:
    detected = canary_found(item["response"], CANARY)
    is_leak = item["label"] == "leak"

    if detected and is_leak:
        true_positives += 1
    elif detected and not is_leak:
        false_positives += 1
    elif not detected and is_leak:
        false_negatives += 1
    else:
        true_negatives += 1

print("true positives", true_positives)
print("false positives", false_positives)
print("false negatives", false_negatives)
print("true negatives", true_negatives)

total = true_positives + false_positives + false_negatives + true_negatives
assert total == len(
    responses), "every response must fall in exactly one bucket"
