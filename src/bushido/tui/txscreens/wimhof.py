import pygame
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Label


class WimhofScreen(Screen):
    BINDINGS = [("q", "app.pop_screen", "Back")]

    def __init__(self, user_id, units):
        super().__init__()
        self.user_id = user_id
        self.units = units
        self.current_round = 0

    def compose(self):
        yield Label("Wimhof")
        yield Button("Start", id="start")
        yield Container(Label("Rounds"), id="rounds")

    def on_button_pressed(self, event):
        if event.button.id == "start":
            pygame.init()
            pygame.mixer.init()
            self.wimhof_practice()

    def wimhof_practice(self):
        print("start")
        self.current_round += 1

        screen = pygame.display.set_mode([800, 600])
        b = pygame.mixer.music.load("audio/wimhof_breathing_30.mp3")
        # r = pyglet.media.load('audio/wimhof_retention_sound.mp3')
        pygame.mixer.music.play()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if pygame.mixer.music.get_busy():
                pass
            else:
                print("retention start")
                running = False

        pygame.mixer.music.stop()
        pygame.quit()

    def on_key(self, event):
        if event.key == "space":
            self.query_one("#round" + str(self.current_round)).end()
            self.wimhof_round()
        if event.key == "w":
            self.query_one("#round" + str(self.current_round)).end()
        if event.key == "q":
            pygame.mixer.music.stop()

    def on_mount(self):
        pass
