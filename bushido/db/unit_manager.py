
# project imports
from bushido.keikolib.filters import preprocess_string


class UnitManager:
    def __init__(self, emoji2key: dict, emoji2proc: dict) -> None:
        self.emoji2key = emoji2key
        self.emoji2proc = emoji2proc

    def log_unit(self, unix_timestamp: float, input_string: str) -> str:
        """
        interface for users of the library
        """
        try:
            emoji, words, comment = preprocess_string(input_string)
        except ValueError as err:
            return str(err)

        try:
            emoji_key = self.emoji2key[emoji]
            processor = self.emoji2proc[emoji]
            processor.process_unit(unix_timestamp, emoji_key, words, comment)
        except KeyError:
            return 'unknown emoji'
        except ValueError as err:
            return str(err)
        else:
            return 'Unit confirmed!'
