from ursina import *
from game_bookpage import BookPage
from game_player import Player
from game_platform import Platform
from game_timer import Timer
from game_enemy import Enemy
import pygame


# Dingen om te onthouden:
# 1: Entity = Is de basis voor elk object in de 3d of 2d wereld. Het is een container voor verschillende eigenschappen
# en componenten die een object kan hebben zoals bijvoorbeeld kleur, teks, model. Het zorgt ervoor dat het object zichtbaar word
# en dat je er fysiek in de wereld iets mee kan.
# 2: Super() = Super() zorgt ervoor dat hij de basisconcepten van Entity pakt zoals model, color, scale. Als je dat niet zou doen
# dan moet je alles handmatig zelf invullen zoals self.model = 'quad'.
# 3: **kwargs gebruik je waneer je niet precies weet hoeveel argumenten je gaat doorgeven, dit zorgt voor flexibiliteit

# Het programma


# voor het geven van text in het schem hoef je vanaf nu alleen maar eerst de positie in te vullen en de color en dan gewoon de class en ingevulde fiunctie aanroepen.
app = Ursina()

# Scherm settings
window.exit_button.visible = True
window.fps_counter.enable = False


class Level1(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player(position=(0, 0, 0))  # Voeg de speler toe
        self.player.position.z = 10
        window.fullscreen = True

        self.environment()
        self.platforms()
        self.muziek()

        self.enemy = Enemy(position=(7, 0.5, 5), target=self.player)
        self.enemy.enabled = True
        self.book_page = BookPage(position=(2, 1, 2), player=self.player)
        self.timer = Timer(position=(-0.7, 0.45), start_minutes=2)

    def update(self):
        self.timer.update_timer()

    def environment(self):
        Sky(texture="sky_default")
        self.ground = Entity(
            model="plane", texture="grass", collider="mesh", scale=Vec3(17, 124, 19)
        )

    def muziek(self):
        pygame.mixer.init()
        pygame.mixer.music.load(
            "assets\music-loop-bundle-download_2024_q1\Sketchbook 2024-03-30_01_L01.ogg"
        )
        pygame.mixer.music.play(
            -1
        )  # -1 betekent dat het blijft loopen en daardoor constant door gaat want als het voorbij is gaat het 1 nummer terug.

    def platforms(self):
        platforms = [
            (4, 1, 0),
            (5.7, 1.6, 0),
            (7.4, 2.2, 0),
            (9.1, 2.8, 0),
        ]
        for position in platforms:
            Platform.het_platform_om_op_te_springen(*position, Vec3(1, 1, 2.8))

        self.platform5 = Platform.het_platform_om_op_te_springen(
            12.5, 3.4, 0, Vec3(5, 1, 5)
        )
        platforms = [
            (12.5, 4, 5),
            (12.5, 4.6, 6.7),
            (12.5, 5.2, 8.4),
            (12.5, 5.8, 10.1),
            (12.5, 6.4, 11.8),
            (12.5, 7, 13.5),
            (12.5, 7.6, 15.2),
            (12.5, 8.2, 16.9),
            (12.5, 8.8, 18.6),
            (12.5, 9.4, 20.3),
            (12.5, 10, 22),
        ]
        for position in platforms:
            Platform.het_platform_om_op_te_springen(*position, Vec3(5, 1, 1))

    def input(self, key):
        if key == "q":  # Om te testen of damage werkt.
            self.player.take_damage(10)


# Start game.
# def levels_aanroepen():
#     global bij_welk_level_we_zijn
#     bij_welk_level_we_zijn = 1
#     if bij_welk_level_we_zijn == 1:
#         level = Level1()
#     if bij_welk_level_we_zijn == 2:
#         #level = level2()
#         pass


# Start game.
def levels_aanroepen():
    level = Level1()


levels_aanroepen()
app.run()


def platforms(self):
    # rechtdoor
    platforms = [
        (4, 1, 0),
        (5.7, 1.6, 0),
        (7.4, 2.2, 0),
        (9.1, 2.8, 0),
    ]
    for position in platforms:
        Platform.het_platform_om_op_te_springen(*position, Vec3(1, 1, 2.8))

    # bocht naar links maken
    self.platform5 = Platform.het_platform_om_op_te_springen(
        12.5, 3.4, 0, Vec3(5, 1, 5)
    )
    platforms = [
        (12.5, 4, 5),
        (12.5, 4.6, 6.7),
        (12.5, 5.2, 8.4),
        (12.5, 5.8, 10.1),
        (12.5, 6.4, 11.8),
        (12.5, 7, 13.5),
        (12.5, 7.6, 15.2),
        (12.5, 8.2, 16.9),
        (12.5, 8.8, 18.6),
        (12.5, 9.4, 20.3),
        (12.5, 10, 22),
    ]
    for position in platforms:
        Platform.het_platform_om_op_te_springen(*position, Vec3(5, 1, 1))

    # bocht maken naar links nogmaals
    self.platform5 = Platform.het_platform_om_op_te_springen(
        12.5, 11, 25, Vec3(5, 1, 5)
    )

    platforms = [
        (9.1, 11.6, 25),
        (7.4, 12.2, 25),
        (5.7, 13, 25),
        (4, 13.6, 25),
        (2.3, 14.2, 25),
        (0.6, 14.8, 25),
        (-1.1, 15.4, 25),
        (-2.8, 16, 25),
        (-4.5, 16.6, 25),
        (-6.2, 17.2, 25),
        (-7.9, 17.8, 25),
    ]
    for position in platforms:
        Platform.het_platform_om_op_te_springen(*position, Vec3(1, 1, 2.8))

    # dit is het platform voor het tweede stukje waarop je dan een soortvan kan rusten.
    groter_platform = self.platform5 = Platform.het_platform_om_op_te_springen(
        -28, 18, 25, Vec3(37, 1, 37)
    )
