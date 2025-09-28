import re


def regex_find(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None
