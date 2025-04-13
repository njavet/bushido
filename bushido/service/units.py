from pathlib import Path
import importlib
import importlib.util

# project imports
from bushido.conf import KEIKO_PROCESSORS
from bushido.exceptions import ValidationError, UploadError
from bushido.schema.base import UnitSpec


class UnitProcessor:
    def __init__(self, dm):
        self.dm = dm
        self.processors = self.load_keiko_processors_from_package()

    def process_input(self, unit_spec: UnitSpec) -> str:
        category = self.dm.unit_name_to_category(unit_spec.name)

        try:
            keiko_orm = self.processors[category].process_input(unit_spec)
        except ValidationError as err:
            return err.message

        try:
            self.dm.upload_unit(unit_spec, keiko_orm)
            return 'Unit Confirmed'
        except UploadError as err:
            return err.message

    def preprocess_input(self, text: str):
        parts = text.split('#', 1)
        emoji_payload = parts[0]
        if not emoji_payload:
            raise ValidationError('Empty payload')
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None
        all_words = emoji_payload.split()
        emoji = all_words[0]
        unit_name = self.dm.emoji_to_unit_name(emoji)
        if unit_name is None:
            raise ValidationError('Invalid emoji')
        words = all_words[1:]
        return unit_name, words, comment

    def load_keiko_processors_from_package(self, package: str = KEIKO_PROCESSORS) -> dict:
        spec = importlib.util.find_spec(package)
        if spec is None or not spec.submodule_search_locations:
            raise ImportError(f'Could not find package {package}')

        package_path = Path(spec.submodule_search_locations[0])
        self.processors = {}

        for file in package_path.glob('*.py'):
            if file.name.startswith('_'):
                continue

            category_name = file.stem
            module_name = f'{package}.{file.stem}'
            module = importlib.import_module(module_name)

            if not hasattr(module, 'KeikoProcessor'):
                raise ImportError(f'{module_name} does not define KeikoProcessor')

            cls = getattr(module, 'KeikoProcessor')
            self.processors[category_name] = cls()
        return self.processors
