from datetime import datetime

from textual.app import ComposeResult
from textual.widgets import RichLog, Static
from textual.containers import ScrollableContainer

from db import Message
from txwidgets import styles


class LogHistory(Static):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def compose(self) -> ComposeResult:
        yield styles.Title('Unit History')
        yield RichLog()

    def on_mount(self):
        self.update_history()

    def update_history(self):
        rl = self.query_one(RichLog)
        rl.clear()
        query = (Message
                 .select()
                 .where(Message.user_id == self.user_id)
                 .order_by(Message.log_time)
                 )
        for msg in query:
            dt_str = datetime.strftime(msg.log_time, '%H:%M:%S - %d.%m.%y')
            msg_text = msg.msg
            rl.write(msg_text)
            rl.write(dt_str)

