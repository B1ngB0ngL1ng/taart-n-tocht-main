from ursina import *


class Text_voor_game:
    def text_voor_game_opzet(positie, kleur):
        return Text(
            "",
            parent=camera.ui,
            position=positie,
            scale=2,
            color=kleur,
            origin=(0, 0),
            enabled=False,
        )
