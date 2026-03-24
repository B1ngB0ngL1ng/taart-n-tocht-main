from ursina import *
import sys, os
from game_text import Text_voor_game

app = Ursina()


class HealthBar(Entity):
    def __init__(self, max_health=100, **kwargs):
        super().__init__(
            parent=camera.ui,
            model="quad",
            color=color.red,
            scale=(0.4, 0.02),
            position=(-0.8, 0.45),
            origin=(-0.5, 0),
        )
        self.max_health = max_health
        self.current_health = max_health

    def update_health(self, amount):
        self.current_health = max(
            0, self.current_health - amount
        )  # Zorgt ervoor dat de health niet negatief kan worden.
        self.scale_x = (
            self.current_health / self.max_health
        ) * 0.4  # Hoe wijd de bar is.

        if self.current_health <= 0:
            self.death_text = Text(
                text="YOU DIED", position=(-0.5, 0), color=color.red, scale=7
            )
            invoke(self.restart_game, delay=3)

    def restart_game(self):
        app.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)
