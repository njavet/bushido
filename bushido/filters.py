from typing import Optional
from .exceptions import ProcessingError


def preprocess_string(input_string: str) -> Optional[tuple[str, list[str], str]]:
    """
    first filter, either it raises an exception when the input string is not
    in the required format: <emoji> <payload> // <comment>
    or it returns those 3 elements
    :param input_string:
    :return:
    """
    # input_string = <emoji> <payload> // <comment>
    parts = input_string.split('//', 1)
    emoji_payload = parts[0]
    if len(parts) > 1 and parts[1]:
        comment = parts[1].strip()
    else:
        comment = None

    if not emoji_payload:
        raise ProcessingError('Empty payload')

    all_words = emoji_payload.split()
    emoji = all_words[0]
    words = all_words[1:]
    return emoji, words, comment

