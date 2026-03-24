from ursina import *


class ScoreCounter(Entity):
    def __init__(self, total_pages=5, **kwargs):
        super().__init__(parent=camera.ui, position=(0.7, 0.48), scale=2, **kwargs)
        self.total_pages = total_pages
        self.collected_pages = 0
        self.text = Text(
            text=f"{self.collected_pages}/{self.total_pages}",
            parent=self,
            scale=1.5,
            color=color.white,
        )

    def update_score(self):
        self.collected_pages += 1
        self.text.text = f"{self.collected_pages}/{self.total_pages}"
