import datetime
from typing import Any

from rich.text import Text


def add_tree_node(name: Any, node: Any, data: Any) -> None:
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
    """
    def build_tree(self):
        def add_node(name, node, data):
            if isinstance(data, dict):
                if isinstance(name, str):
                    node.label = Text(name, style="cyan")
                if node.data < 2:
                    node.expand()
                for key, value in data.items():
                    new_node = node.add("", data=(node.data + 1))
                    add_node(key, new_node, value)
            elif isinstance(data, list):
                if isinstance(name, datetime.datetime):
                    node.label = Text(
                        datetime.datetime.strftime(name, "%d.%m.%y %H:%M")
                    )
                else:
                    node.label = name

                for index, value in enumerate(data):
                    new_node = node.add("", data=(node.data + 1))
                    add_node(str(index), new_node, value)

            else:
                node.allow_expand = False
                if name:
                    try:
                        data_str = str(data.liftsset)
                    except:
                        data_str = str(data)

                    label = Text.assemble(
                        str(len(str(data))),
                        Text.from_markup(f"[b]{name}[/b] = ", style="blue"),
                        data_str,
                        style="cyan",
                    )
                else:
                    label = Text(repr(data))
                node.label = label

        tree = self.query_one(Tree)
        tree.root.expand()
        add_node("Units", tree.root, {})


    def action_toggle_tree(self):
        self.show_tree = not self.show_tree
    """
