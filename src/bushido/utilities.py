import datetime

from rich.text import Text


def add_tree_node(name, node, data):
    if isinstance(name, datetime.datetime):
        name = name.strftime("%d.%m.%y %H:%M")
    else:
        name = name.capitalize()

    if isinstance(data, dict):
        node.set_label(name)
        for key, value in data.items():
            new_node = node.add("")
            add_tree_node(key, new_node, value)
    elif isinstance(data, list):
        node.set_label(Text(name))
        for index, item in enumerate(data):
            new_node = node.add("")
            add_tree_node(str(index), new_node, item)
    else:
        node.allow_expand = False
        node.set_label(Text.assemble(Text.from_markup(f"[b]{name}[/b]: "), str(data)))
