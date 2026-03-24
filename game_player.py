from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from game_healthbar import HealthBar
from game_weapon import Weapon


class Player(FirstPersonController):
    def __init__(self, health=100, **kwargs):
        super().__init__(**kwargs)
        self.health_bar = HealthBar(max_health=health)
        self.health = health
        self.jump_height = 2
        self.speed = 6
        self.weapon = Weapon(player=self, weapon_type="sword", damage=20)
        self.collected_pages = 0  # Score teller
        self.score_text = Text(
            f"{self.collected_pages}/5",
            parent=camera.ui,
            position=(0.7, 0.48),
            scale=2,
            color=color.white,
        )

    def collect_book_page(self):
        self.collected_pages += 1
        self.score_text.text = f"{self.collected_pages}/5"  # Update score weergave

    def take_damage(self, amount):
        self.health -= amount
        self.health_bar.update_health(amount)

    def input(self, key):
        super().input(key)

        if key == "q":  # Om te testen of damage werkt.
            self.take_damage(10)

        if key == "mouse_left":
            if self.weapon:
                self.weapon.attack()

        if key == "space":
            self.jump()

        if key == "esc":
            pass  # misschien leuk om een soortvan menu te maken in esc waardoor je de game opnieuw kan starten of kan stoppen. misschien ook kijken voor later een optie om game te saven.
        # sprint = False
        # if key == "shift":
        #     sprint = True
        #     self.speed = 40
