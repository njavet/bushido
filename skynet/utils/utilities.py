# general imports
import collections
import datetime
from rich.text import Text

# project imports
import config


def add_tree_node(name, node, data):
    if isinstance(name, datetime.datetime):
        name = name.strftime('%d.%m.%y %H:%M')
    else:
        name = name.capitalize()

    if isinstance(data, dict):
        node.set_label(name)
        for key, value in data.items():
            new_node = node.add('')
            add_tree_node(key, new_node, value)
    elif isinstance(data, list):
        node.set_label(Text(name))
        for index, item in enumerate(data):
            new_node = node.add('')
            add_tree_node(str(index), new_node, item)
    else:
        node.allow_expand = False
        node.set_label(Text.assemble(
            Text.from_markup(f'[b]{name}[/b]: '),
            str(data)))


def parse_module_dix():
    dix = collections.defaultdict(list)
    for emoji, compound_name in config.emojis.items():
        module_name, unit_name = compound_name.split('.')
        dix[module_name].append((emoji, unit_name))
    return dix


def find_previous_sunday(dt):
    """
    Finds the previous sunday of the given date
    e.g. input: 01.01.2020
    returns: 29.12.2019

    """
    if dt.weekday() != 6:
        days = dt.weekday() + 1
        return dt - datetime.timedelta(days=days)
    else:
        return dt


def find_next_saturday(dt):
    if dt.weekday() != 6:
        days = 5 - dt.weekday()
        return dt + datetime.timedelta(days=days)
    else:
        return dt + datetime.timedelta(days=6)
