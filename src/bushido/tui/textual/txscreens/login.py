from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Static


class LoginScreen(ModalScreen[bool]):
    def __init__(self, tg_client):
        super().__init__()
        self.tg_client = tg_client

    def compose(self) -> ComposeResult:
        yield LoginForm()

    async def on_button_pressed(self, event):
        phone = self.query_one("#phone", Input).value
        if event.button.id == "request_code":
            await self.tg_client.send_code_request(phone)
        elif event.button.id == "login":
            code = self.query_one("#code", Input).value
            user = await self.tg_client.sign_in(phone=phone, code=code)
            self.dismiss(True)


class LoginForm(Container):
    def compose(self):
        yield Static("Phone", classes="label")
        yield Input(placeholder="+41 xxx xx xx", id="phone")
        yield Static()
        yield Button("Request access code", variant="primary", id="request_code")
        yield Static("Auth Code", classes="label")
        yield Input(placeholder="telegram code", id="code")
        yield Static()
        yield Button("Login", variant="primary", id="login")
