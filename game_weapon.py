from ursina import *


class Weapon(Entity):
    def __init__(self, player, weapon_type="sword", damage=10, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.weapon_type = weapon_type
        self.damage = damage
        self.model = "cube"
        self.color = color.gray
        self.scale = Vec3(0.2, 0.2, 1)  # Afmetingen wapen
        self.parent = camera  # Het wapen beweegt met de camera mee (volgt de speler)
        self.position = (0.5, -0.5, 1)  # Het wapen bevindt zich voor de speler

    def attack(self):
        self.deal_damage()

    def deal_damage(self):
        # Voeg hier de logica toe om te controleren of het wapen iets raakt en zo ja, schade aan te richten.
        pass
