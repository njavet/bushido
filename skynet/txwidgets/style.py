# general import*s
import datetime
from rich.text import Text
from rich.highlighter import ReprHighlighter

from textual.widgets import Static
import peewee as pw
import collections
from textual.screen import Screen, ModalScreen
from textual.validation import Function, Validator, ValidationResult
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.messages import Message
from textual.containers import *
from textual.widgets import *
from textual.widgets.tree import TreeNode
from textual.suggester import SuggestFromList, Suggester
from textual import on, events


class Title(Static):
    pass
