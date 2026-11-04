def normalize(text: str) -> str:
    return text.upper().replace("-", "").replace(" ", "")


def canary_found(response: str, canary: str) -> bool:
    if not isinstance(response, str) or not isinstance(canary, str):
        raise TypeError(
            f"response and canary must be strings, "
            f"got {type(response).__name__} and {type(canary).__name__}")
    return normalize(canary) in normalize(response)
