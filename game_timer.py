from ursina import *
from datetime import datetime, timedelta


app = Ursina()


class Timer(Entity):
    def __init__(self, start_minutes, **kwargs):
        super().__init__(**kwargs)
        self.end_time = datetime.now() + timedelta(minutes=start_minutes)
        self.text = Text(
            text=str(start_minutes * 60),
            position=(-0.7, 0.40),
            color=color.white,
            scale=2,
        )
        self.text.text = str(start_minutes * 60)
        self.update_timer()

    def opnieuw(self):
        app.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def update_timer(self):
        remaining_time = self.end_time - datetime.now()
        if remaining_time > timedelta(seconds=0):
            self.text.text = str(remaining_time.seconds)
            invoke(self.update_timer, delay=1)
        else:
            over = "RAN OUT OF TIME YOU DIED"
            self.text = Text(text=over, position=(0, 0), color=color.red, scale=5)
            self.opnieuw()

    def restart_game(self):
        app.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)
