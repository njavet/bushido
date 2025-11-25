# general import*s
import datetime

import core
import secconf
from rich.text import Text
from textual.screen import Screen
from textual.widgets import *
from textual.widgets import Tree
from widgets import stats


class Weights(Screen):
    """
    accesses units:
        balance / cali / gym / lifts

    """

    BINDINGS = [("b", "app.pop_screen", "Back")]

    def compose(self):
        yield Header()
        yield Tree("", data=0, id="unit-tree")
        yield stats.LiftStats(core.ugn2un2umoji["lifts"].values())
        yield Footer()

    def build_tree(self):
        def add_node(name, node, data):
            """Adds a node to the tree.

            Args:
                name (str): Name of the node.
                node (TreeNode): Parent node.
                data (object): Data associated with the node.
            """
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
        dt2units = {}
        for ugn, dix in core.ugn2un2umoji.items():
            dt2units[ugn.capitalize()] = {}
            for un, umoji in dix.items():
                dt2units[ugn.capitalize()][un] = umoji.get_dt2units(secconf.user_id)
