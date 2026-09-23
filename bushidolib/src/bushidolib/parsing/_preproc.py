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
            # catch --option0 --option1 (option follows empty option)
            if words[i + 1].startswith("--"):
                raise UnitParsingError(
                    f"Invalid value for option {word}: {words[i + 1]}"
                )
            # catch --option0 -g (flag follows empty option)
            if words[i + 1].startswith("-"):
                try:
                    _ = float(words[i + 1])
                except ValueError as e:
                    raise UnitParsingError(
                        f"Invalid value for option {word}: {words[i + 1]}"
                    ) from e
            # catch --avghr 140 --avghr 150 errors
            if word[2:] in options:
                raise UnitParsingError(f"duplicated option {word[2:]}")
            options[word[2:]] = words[i + 1]
            i += 2
        # -5 is not a flag
        elif word.startswith("-") and word[1:].isalpha():
            flags.append(word[1:])
            i += 1
        else:
            tokens.append(word)
            i += 1
    return PreprocResult(tuple(tokens), flags, options)
