from ursina import *


class Enemy(Entity):
    def __init__(self, position=(0, 0, 0), **kwargs):
        super().__init__(**kwargs)
        self.model = "cube"
        self.color = color.red
        self.scale = (1, 1, 1)
        self.position = position
        self.health = 100
        self.speed = 2
        self.target = None

    def update(self):
        if self.target:
            direction = self.target.position - self.position
            if direction.length() > 0:
                self.position += direction.normalized() * self.speed * time.dt

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.enabled = False
