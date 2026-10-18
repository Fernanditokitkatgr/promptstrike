from promptstrike.loader import load_suite


def test_leak_suite_has_five_attacks():
    ataques = load_suite("corpus/system-prompt-leak.yaml")
    assert len(ataques) == 5


def test_override_suite_has_five_attacks():
    ataques = load_suite("corpus/instruction-override.yaml")
    assert len(ataques) == 5


def test_indirect_suite_has_three_attacks():
    ataques = load_suite("corpus/indirect-injection.yaml")
    assert len(ataques) == 3
