from abc import ABC


class InputProcessor:
    def __init__(self):
        self.emoji2processor = None

    def process_input(self, text):
        try:
            emoji, words, comment = self.preprocess_input(text)
        except ValueError as err:
            return str(err)

        try:
            processor = self.emoji2processor[emoji]
        except KeyError:
            return 'Unknown Emoji'

        try:
            processor.process_unit(emoji, words, comment)
            return 'Unit Confirmed'
        except ValueError as err:
            return str(err)

    @staticmethod
    def preprocess_input(text: str):
        parts = text.split('//', 1)
        emoji_payload = parts[0]
        if not emoji_payload:
            raise ValueError('Empty payload')
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None
        all_words = emoji_payload.split()
        emoji = all_words[0]
        words = all_words[1:]
        return emoji, words, comment


class AbsUnitProcessor(ABC):
    def __init__(self):
        pass

    def process_unit(self, emoji, words, comment):
        raise NotImplementedError


class AbsUnitParser(ABC):
    def __init__(self):
        pass

    def parse_unit(self, emoji, words, comment):
        raise NotImplementedError

