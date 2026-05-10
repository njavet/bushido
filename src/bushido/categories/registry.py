from bushido.categories.cardio import cardio_registration
from bushido.categories.gym import gym_registration
from bushido.categories.lifting import lifting_registration
from bushido.categories.wimhof import wimhof_registration
from bushido.core.dtypes import CategoryHelp, CategoryRegistration
from bushido.settings import Category

REGISTRY: dict[str, CategoryRegistration] = {
    Category.gym: gym_registration,
    Category.cardio: cardio_registration,
    Category.lifting: lifting_registration,
    Category.wimhof: wimhof_registration,
}


UNIT_TO_CATEGORY: dict[str, str] = {
    unit_name: category
    for category, registration in REGISTRY.items()
    for unit_name in registration.unit_settings.keys()
}


def get_category_help() -> list[CategoryHelp]:
    result = []
    for category, registration in REGISTRY.items():
        unit_names = [unit_name for unit_name in registration.unit_settings.keys()]
        ch = CategoryHelp(
            name=category, grammar=registration.grammar, unit_names=unit_names
        )
        result.append(ch)
    return result
