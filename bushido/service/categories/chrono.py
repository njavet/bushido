# project imports
from bushido.utils.parsing import parse_time_string
from bushido.data.categories.chrono import KeikoModel


def create_keiko(words):
    seconds = parse_time_string(words[0])
    keiko = KeikoModel(seconds=seconds)
    return keiko
