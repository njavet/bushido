# project imports
from bushido.data.categories.log import KeikoModel


def create_keiko(words):
    try:
        log = words[0]
    except IndexError:
        log = None

    keiko = KeikoModel(log=log)
    return keiko
