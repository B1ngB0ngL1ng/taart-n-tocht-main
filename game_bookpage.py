from ursina import *
from game_text import Text_voor_game
from game_player import Player


class BookPage(Entity):
    def __init__(self, position=(), player=None):
        super().__init__(
            model="quad",
            texture="white_cube",
            color=color.white,
            scale=(0.5, 0.7),
            position=position,
            double_sided=True,
        )
        self.player = player
        self.pick_up_text = Text_voor_game.text_voor_game_opzet((0, 0.4), color.yellow)

    def update(self):
        if distance(self, self.player) < 2:
            self.pick_up_text.text = "[E] Pick Up"
            self.pick_up_text.enabled = True
        else:
            self.pick_up_text.enabled = False

        self.look_at(self.player.position)

    def input(self, key):
        if key == "e" and distance(self, self.player) < 2:
            self.player.collect_book_page()  # Roep de functie aan
            destroy(self)
            self.pick_up_text.enabled = False
