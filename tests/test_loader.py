
import pytest
from pydantic import ValidationError
from promptstrike.loader import load_suite, DirectAttack


def test_leak_suite_has_five_attacks():
    attacks = load_suite("corpus/system-prompt-leak.yaml")
    assert len(attacks) == 5


def test_override_suite_has_five_attacks():
    attacks = load_suite("corpus/instruction-override.yaml")
    assert len(attacks) == 5


def test_indirect_suite_has_three_attacks():
    attacks = load_suite("corpus/indirect-injection.yaml")
    assert len(attacks) == 3


def test_unknown_technique_is_rejected():
    ataque_falso = {
        "id": "fake-001",
        "name": "Técnica inventada",
        "technique": "esto-no-existe",
        "payload": "hola",
    }
    with pytest.raises(ValidationError):
        DirectAttack.model_validate(ataque_falso)
