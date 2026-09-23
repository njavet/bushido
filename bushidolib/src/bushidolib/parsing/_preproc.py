from typing import NamedTuple

from bushidolib.exceptions import UnitParsingError


class PreprocResult(NamedTuple):
    tokens: tuple[str, ...]
    flags: list[str]
    options: dict[str, str]


def split_words(words: tuple[str, ...]) -> PreprocResult:
    tokens: list[str] = []
    flags: list[str] = []
    options: dict[str, str] = {}
    i = 0
    while i < len(words):
        word = words[i]
        if word.startswith("--"):
            if i + 1 >= len(words):
                raise UnitParsingError(f"Missing value for option {word}")
            options[word] = words[i + 1]
            i += 2
        elif word.startswith("-"):
            flags.append(word)
            i += 1
        else:
            tokens.append(word)
            i += 1
    return PreprocResult(tuple(tokens), flags, options)
