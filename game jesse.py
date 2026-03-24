# Dingen om te onthouden:
# 1: Entity = Is de basis voor elk object in de 3d of 2d wereld. Het is een container voor verschillende eigenschappen
# en componenten die een object kan hebben zoals bijvoorbeeld kleur, teks, model. Het zorgt ervoor dat het object zichtbaar word
# en dat je er fysiek in de wereld iets mee kan.
# 2: Super() = Super() zorgt ervoor dat hij de basisconcepten van Entity pakt zoals model, color, scale. Als je dat niet zou doen
# dan moet je alles handmatig zelf invullen zoals self.model = 'quad'.
# 3: **kwargs gebruik je waneer je niet precies weet hoeveel argumenten je gaat doorgeven, dit zorgt voor flexibiliteit
# 4: TO DO: hoi
# yo hoe gaat het

import pygame
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from datetime import datetime, timedelta
import os, sys, json

app = Ursina()

joffrey_texture = load_texture("assets/Joffrey.jpg")
joffrey_sky = load_texture("assets/God.jpg")

flycam = EditorCamera(enabled=False)

window.exit_button.visible = True
window.fps_counter.enable = False
pink = color.rgb(255, 105, 180)
tree_texture = None
sword_texture = None


# Om vallende blokken te maken
class FallingBlock(Entity):
    def __init__(self, position=(0, 0, 0), player=None, fall_delay=2, **kwargs):
        super().__init__(
            model="cube",
            texture="brick",
            color=color.pink,
            collider="box",
            position=position,
            **kwargs,
        )
        self.original_y = self.y
        self.player = player
        self.fall_delay = fall_delay
        self.triggered = False

    def update(self):
        if (
            not self.triggered
            and distance(self, self.player) < 1
            and self.player.y > self.y
        ):
            self.triggered = True
            invoke(self.fall, delay=self.fall_delay)

    def fall(self):
        self.animate_y(self.y - 20, duration=1)
        invoke(destroy, self, delay=2)


# Klasse voor het tonen van de score
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


# Wapen klasse voor aanvallen
class Weapon(Entity):
    def __init__(self, player, weapon_type="sword", damage=10, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.weapon_type = weapon_type
        self.damage = damage
        self.model = "cube"
        self.color = color.gray
        self.scale = Vec3(0.2, 0.2, 1)
        self.parent = camera
        self.position = (0.5, -0.5, 1)

    def attack(self):
        self.deal_damage()

    def deal_damage(self):
        pass


# Player specificaties
class Player(FirstPersonController):
    def __init__(self, health=100, **kwargs):
        super().__init__(**kwargs)
        self.health_bar = HealthBar(max_health=health)
        self.health = health
        self.jump_height = 2
        self.weapon = Weapon(player=self, weapon_type="sword", damage=20)
        self.collected_pages = []
        self.speed = 7  # Normale snelheid
        self.sprint_speed = 14  # Sprint snelheid
        self.score_text = Text(
            f"{len(self.collected_pages)}/5",
            parent=camera.ui,
            position=(0.7, 0.48),
            scale=2,
            color=color.white,
        )
        self.is_dead = False
        self.pause_menu = PauseMenu(self)
        self.page_text = Text(
            parent=camera.ui,
            scale=1,
            color=color.yellow,
            position=(-0.8, 0.2),
            text="",
            visible=False,
        )
        self.timer = None  # Later ingesteld door Level1

    def aglezen_van_de_file(self):
        try: 
            with open("opgepakte_bookpage_coordinaten.json", "r+", encoding="utf-8") as json_file:
                data= json.load(json_file)
                x_as:float = data["x-as"]
                y_as:float = data["y-as"] 
                z_as:float = data["z-as"]
                return x_as,y_as,z_as
        except Exception as e:
            print(e)
            return 0, 0, 0

    def return_to_checkpoint(self):
        self.position = Vec3(*self.aglezen_van_de_file())

    def collect_book_page(self, page):
        self.collected_pages.append(page)
        self.score_text.text = f"{len(self.collected_pages)}/5"
        self.page_text.text = page.text
        self.page_text.visible = True
        invoke(self.hide_page_text, delay=25)

        # button zie je pas wanneer je de page hebt opgepakt
        if len(self.collected_pages) == 1 and hasattr(
            self.pause_menu, "first_book_page_button"
        ):
            self.pause_menu.first_book_page_button.visible = True
        if len(self.collected_pages) == 2 and hasattr(
            self.pause_menu, "second_book_page_button"
        ):
            self.pause_menu.second_book_page_button.visible = True
        if len(self.collected_pages) == 3 and hasattr(
            self.pause_menu, "third_book_page_button"
        ):
            self.pause_menu.third_book_page_button.visible = True

        # Voeg extra tijd toe aan timer (bijv. 30 seconden per pagina)
        if self.timer:
            self.timer.add_time(30)

        if len(self.collected_pages) == 5:
            self.show_victory_screen()

    def hide_page_text(self):
        self.page_text.visible = False

    def take_damage(self, amount):
        self.health -= amount
        self.health_bar.update_health(amount)

    def input(self, key):
        if self.is_dead:
            return
        if key == "q":
            self.take_damage(10)
        if key == "mouse_left":
            if self.weapon:
                self.weapon.attack()
        if key == "space":
            self.jump()
        if key == "m":
            self.pause_menu.toggle()
        if key == "shift":
            self.sprinting(True)  # Start sprinten
        if key == "shift up":  # Als de shift-toets losgelaten wordt
            self.sprinting(False)  # Stop sprinten

    def sprinting(self, is_sprinting):
        if is_sprinting:
            self.speed = self.sprint_speed  # Verhoog snelheid bij sprinten
        else:
            self.speed = 6  # Zet terug naar normale snelheid

    def jump(self):
        super().jump()

    def show_victory_screen(self):
        self.is_dead = True  # Blokkeer verdere input
        mouse.locked = False

        # Laad de texture (je victory-afbeelding)
        victory_texture = joffrey_texture
        # Maak een quad voor de afbeelding
        self.victory_image = Entity(
            parent=camera.ui,
            model="quad",  # Gebruik een vlak voor de afbeelding
            texture=victory_texture,
            scale=(2, 2),  # Je kunt de schaal aanpassen afhankelijk van je afbeelding
            z=0.5,  # Zet de z-waarde zodat deze voor de andere elementen komt
        )


# Gezondheidsbalk klasse die reageert op schade
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
        self.death_text = Text_voor_game.text_voor_game_opzet((0, 0), color.red)
        self.death_text.enabled = False
        self.black_screen = Entity(
            parent=camera.ui,
            model="quad",
            color=color.black,
            scale=(2, 2),
            enabled=False,
        )
        self.game_paused = False

    def update_health(self, amount):
        self.current_health = max(0, self.current_health - amount)
        self.scale_x = (self.current_health / self.max_health) * 0.4

        if self.current_health <= 0 and not self.game_paused:
            self.black_screen.enabled = True
            self.game_paused = True
            self.death_text.text = "YOU DIED"
            self.death_text.enabled = True
            invoke(self.restart_game, delay=3)

    def restart_game(self):
        app.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)


# Pauze menu met knoppen en inventory functionaliteit
class PauseMenu(Entity):
    def __init__(self, player: Player, **kwargs):
        super().__init__(parent=camera.ui, enabled=False)
        self.black_bg = Entity(
            parent=self, model="quad", color=color.black, scale=(2, 2), z=1
        )
        self.player = player
        self.paused = False

        self.text_inventory = Button(
            text="Inventory",
            scale=(0.1, 0.05),
            position=(0, 0.3),
            on_click=self.toggle_inventory,
            visible=False,
        )
        self.resume_button = Button(
            text="Resume",
            scale=(0.1, 0.05),
            position=(-0.3, 0.3),
            on_click=self.resume_game,
            visible=False,
        )
        self.exit_button = Button(
            text="Exit",
            scale=(0.1, 0.05),
            position=(0.3, 0.3),
            on_click=self.exit_game,
            visible=False,
        )
        self.checkpoint_button = Button(
            text="Return to checkpoint",
            scale=(0.1, 0.05),
            position =(0.6, 0.3),
            on_click= player.return_to_checkpoint,
            visible=False,
        )

        self.inventory_screen = None

    def toggle(self):
        self.paused = not self.paused
        self.enabled = self.paused
        mouse.locked = not self.paused
        self.player.enabled = not self.paused

        self.resume_button.visible = self.paused
        self.exit_button.visible = self.paused
        self.text_inventory.visible = self.paused
        self.checkpoint_button.visible = self.paused

    def toggle_inventory(self):
        if self.inventory_screen is None:
            self.inventory_screen = Entity(parent=camera.ui, enabled=True)
            Entity(
                parent=self.inventory_screen,
                model="quad",
                color=color.black,
                scale=(2, 2),
                z=1,
            )
            Text(
                parent=self.inventory_screen,
                text="Inventory Screen",
                scale=2,
                origin=(0, -6),
            )
            Button(
                parent=self.inventory_screen,
                text="Back to Pause Menu",
                scale=(0.1, 0.05),
                position=(0, -0.3),
                on_click=self.toggle_inventory,
            )
            self.first_book_page_button = Button(
                parent=self.inventory_screen,
                text="First Book Page",
                scale=(0.1, 0.05),
                position=(0, 0),
                on_click=self.show_first_book_page,
                visible=False,
            )
            self.second_book_page_button = Button(
                parent=self.inventory_screen,
                text="Second Book Page",
                scale=(0.1, 0.05),
                position=(0, -0.04),
                on_click=self.show_second_book_page,
                visible=False,
            )
            self.third_book_page_button = Button(
                parent=self.inventory_screen,
                text="Third Book Page",
                scale=(0.1, 0.05),
                position=(0, -0.08),
                on_click=self.show_third_book_page,
                visible=False,
            )

        if not self.inventory_screen.enabled:
            self.inventory_screen.enabled = True
            self.enabled = False
            self.resume_button.visible = False
            self.exit_button.visible = False
            self.text_inventory.visible = False
            self.checkpoint_button.visible = False
            if hasattr(self, "first_book_page_button") and self.first_book_page_button:
                self.first_book_page_button.visible = (
                    len(self.player.collected_pages) >= 1
                )
            if (
                hasattr(self, "second_book_page_button")
                and self.second_book_page_button
            ):
                self.second_book_page_button.visible = (
                    len(self.player.collected_pages) >= 2
                )
            if hasattr(self, "third_book_page_button") and self.third_book_page_button:
                self.third_book_page_button.visible = (
                    len(self.player.collected_pages) >= 3
                )
        else:
            self.inventory_screen.enabled = False
            self.enabled = True
            self.resume_button.visible = True
            self.exit_button.visible = True
            self.text_inventory.visible = True
            self.checkpoint_button.visible = True
            self.first_book_page_button.visible = False
            self.second_book_page_button.visible = False
            self.third_book_page_button.visible = False

    def show_first_book_page(self):
        if self.player.collected_pages:
            self.player.page_text.text = self.player.collected_pages[0].text
            self.player.page_text.visible = True
            invoke(self.player.hide_page_text, delay=10)

    def show_second_book_page(self):
        if self.player.collected_pages:
            self.player.page_text.text = self.player.collected_pages[1].text
            self.player.page_text.visible = True
            invoke(self.player.hide_page_text, delay=10)

    def show_third_book_page(self):
        if self.player.collected_pages:
            self.player.page_text.text = self.player.collected_pages[2].text
            self.player.page_text.visible = True
            invoke(self.player.hide_page_text, delay=10)

    def resume_game(self):
        self.toggle()

    def exit_game(self):
        application.quit()


# Klasse voor een verzamelbare pagina in het spel
class BookPage(Entity):
    def __init__(self, number: int, position=(), player=None, text=""):
        super().__init__(
            model="quad",
            texture="white_cube",
            color=color.white,
            scale=(0.5, 0.7),
            position=position,
            double_sided=True,
        )
        self.player = player
        self.text = text
        self.pick_up_text = Text_voor_game.text_voor_game_opzet((0, 0.4), color.yellow)
        self.page_text = Text(
            parent=self,
            text=self.text,
            position=(0, 0),
            scale=(0.1, 0.1),
            visible=False,
        )
        self.bookpagenumber = number
        self.bookpage_filemaker = json_file_edits(number)

    def update(self):
        if distance(self, self.player) < 2:
            self.pick_up_text.text = "[E] Pick Up"
            self.pick_up_text.enabled = True
        else:
            self.pick_up_text.enabled = False
        self.look_at(self.player.position)

    def input(self, key):
        if key == "e" and distance(self, self.player) < 2:
            self.player.collect_book_page(self)
            self.page_text.visible = True
            self.pick_up_text.enabled = False
            self.bookpage_filemaker.writer_bookpage_in_file()
            destroy(self)


# de json file die je nieuwe respawn punten kan geven. 
class json_file_edits:
    def __init__(self, bookpage_number: int):
        match bookpage_number:
            case 1:
                self.book_page = {"x-as": 0, 
                                  "y-as": 0, 
                                  "z-as": 0}
            case 2:
                self.book_page = {"x-as": 12.5, 
                                  "y-as": 13, 
                                  "z-as": 25}
            case 3:
                self.book_page = {"x-as": -43.6, 
                                  "y-as": 25.4, 
                                  "z-as": 22}
            case 4:
                self.book_page = {"x-as": -64, 
                                  "y-as": 32.2, 
                                  "z-as": 22}
            case 5:
                self.book_page = {"x-as": -25.75, 
                                  "y-as": 39.4, 
                                  "z-as": -73}

    def writer_bookpage_in_file(self):
        try: 
            with open("opgepakte_bookpage_coordinaten.json", "w", encoding="utf-8") as json_file:
                json.dump(self.book_page, json_file, indent=4)
        except Exception as e:
            print(e)


# Platform klasse voor springbare objecten
class Platform:
    def het_platform_om_op_te_springen(x_as, y_as, z_as, schaal):
        Entity(
            model="cube",
            collider="box",
            texture="brick",
            color=color.pink,
            scale=schaal,
            x=x_as,
            y=y_as,
            z=z_as,
        )


# Klasse voor alle teksten in de game
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


# Timer klasse voor countdown
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
        self.update_timer()

    def update_timer(self):
        remaining_time = self.end_time - datetime.now()
        if remaining_time > timedelta(seconds=0):
            self.text.text = str(remaining_time.seconds)
            invoke(self.update_timer, delay=1)
        else:
            self.text = Text(
                text="RAN OUT OF TIME YOU DIED",
                position=(0, 0),
                color=color.red,
                scale=5,
            )
            invoke(self.restart_game, delay=3)

    def add_time(self, seconds):
        self.end_time += timedelta(seconds=seconds)

    def restart_game(self):
        app.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)

# Eerste level
class Level1(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player()  # de position is gelijk aan het geen wat er wordt gereturned nadat de json file is afgelezen. 
        self.player.position.z = 10
        window.fullscreen = True
        self.timer = Timer(position=(0.7, 0.45), start_minutes=7)
        self.player.timer = self.timer
        self.environment()
        self.platforms()
        self.muziek()

        book_page_1_text = "Controls: Sprint(Shift), Movement(WSAD), Pause(M), Jump(Spacebar)"
        book_page_2_text = "Joffrey is de git bitch\nBla Bla Bla"
        book_page_3_text = "Joffrey houd er van om in de spotlight te staan.\nBla Bla Bla"
        book_page_4_text = "Wanneer koopt Joffrey weer eens een appelkruimeltaart?\nBla Bla Bla"
        book_page_5_text = "joffrey heeft een zieke bak\nBla Bla Bla"
        self.book_page_1 = BookPage(1,
            position=(2, 1, 2), player=self.player, text=book_page_1_text,
        )
        self.book_page_2 = BookPage(2,
            position=(12.5, 13, 25), player=self.player, text=book_page_2_text,
        )
        self.book_page_3 = BookPage(3,
            position=(-43.6, 25.4, 22), player=self.player, text=book_page_3_text,
        )
        self.book_page_4 = BookPage(4,
            position=(-64, 32.2, 22), player=self.player, text=book_page_4_text,
        )
        self.book_page_5 = BookPage(5,
            position=(-25.75, 39.4, -73), player=self.player, text=book_page_5_text,
        )
    def muziek(self):
        pygame.mixer.init()
        pygame.mixer.music.load(
            "assets/music-loop-bundle-download_2024_q1/Sketchbook 2024-03-30_01_L01.ogg"
        )
        pygame.mixer.music.play(-1)
    


    def update(self):
        self.timer.update_timer()

    def environment(self):
        Sky(texture=joffrey_sky)
        self.ground = Entity(
            model="plane",
            texture="grass",
            collider="mesh",
            scale=Vec3(200, 124, 200),
        )

    def platforms(self):
        # Vallende blokken
        FallingBlock(position=(-25.75, 36, -73), player=self.player, scale=Vec3(2, 1, 2))

        breedere_platforms_x_waarde = [
            # begin plaformen rechtdor, kant 1.1
            (4, 1, 0),
            (5.7, 1.6, 0),
            (7.4, 2.2, 0),
            (9.1, 2.8, 0),
            # de tweede hoek om gaan naar links (x waarde) kant 1.3
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
        for pos in breedere_platforms_x_waarde:
            Platform.het_platform_om_op_te_springen(
                *pos, Vec3(1, 1, 2.8)
            )  # het eerste hoekje naar links

        breedere_platforms_z_waarde = [
            # het platform dat de hoek om gaat links(z waarde) kant 1.2
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
        for pos in breedere_platforms_z_waarde:
            Platform.het_platform_om_op_te_springen(*pos, Vec3(5, 1, 1))
            # haii
            

        smallere_platforms_x_waarde = [
            # beginnen middenin 2e platform kant 2.1
            (-30, 18.6, 22),
            (-31.7, 19.2, 25),
            (-33.4, 19.8, 22),
            (-35.1, 20.4, 25),
            (-36.8, 21, 22),
            (-38.5, 21.6, 25),
            (-40.2, 22.2, 22),
            (-41.9, 22.8, 25),
            (-43.6, 23.4, 22),
            (-45.3, 24, 22),
            (-47, 24.6, 25),
            (-48.7, 25.2, 22),
            (-50.4, 25.8, 25),
            (-52.1, 26.4, 22),
            (-53.8, 27, 25),
            (-55.5, 27.6, 22),
            (-57.2, 28.2, 25),
            (-58.9, 28.8, 22),
            (-60.6, 29.4, 25),
        ]
        for pos in smallere_platforms_x_waarde:
            Platform.het_platform_om_op_te_springen(*pos, Vec3(1, 1, 1))

        smallere_platforms_z_waarde = [
            # verdere afstand (3.6) tussen de blokken. kant 2.2
            (-64, 30.6, 20.3),
            (-64, 31.2, 16.7),
            (-64, 31.8, 13.1),
            (-64, 31.8, 9.5),
            (-64, 32.4, 5.9),
            (-64, 33, 2.3),
            (-64, 33.6, -1.3),
            (-64, 33.6, -4.9),
            (-64, 34.2, -8.5),
            (-64, 34.8, -12.1),
            (-64, 34.8, -15.7),
            # de lange strook kant 2.3
        ]
        for pos in smallere_platforms_z_waarde:
            Platform.het_platform_om_op_te_springen(*pos, Vec3(1, 1, 1))

        # dit zijn alle apparte hoek platformen
        # hoek 1 deel 1
        Platform.het_platform_om_op_te_springen(12.5, 3.4, 0, Vec3(5, 1, 5))
        # hoek 2 deel 1
        Platform.het_platform_om_op_te_springen(12.5, 11, 25, Vec3(5, 1, 5))
        # het grote pauze platform deel 2
        Platform.het_platform_om_op_te_springen(-28, 18, 25, Vec3(37, 1, 37))
        # hoek 1 deel 2
        Platform.het_platform_om_op_te_springen(-64, 30.2, 23.5, Vec3(5, 1, 5))
        # hoek 2 deel 2
        Platform.het_platform_om_op_te_springen(-64, 35.4, -19.3, Vec3(5, 1, 5))

        # balk 2.1 deel 2
        Platform.het_platform_om_op_te_springen(-64, 35.4, -31.5, Vec3(0.5, 1, 20))
        # balk 2.2 deel 2
        Platform.het_platform_om_op_te_springen(-74, 35.4, -41.5, Vec3(20, 1, 0.5))
        # balk 2.3 deel 2
        Platform.het_platform_om_op_te_springen(-84, 35.4, -61.5, Vec3(0.5, 1, 40))
        # balk 2.4 deel 2
        Platform.het_platform_om_op_te_springen(-59, 35.4, -81.5, Vec3(50, 1, 0.5))
        # balk 2.5 deel 2
        Platform.het_platform_om_op_te_springen(-34, 35.4, -76.5, Vec3(0.5, 1, 10))
        # balk 2.6 deel 2
        Platform.het_platform_om_op_te_springen(-30.75, 35.4, -71.5, Vec3(6.5, 1, 0.5))

    def input(self, key):
        if key == "q":
            self.player.take_damage(10)
        if key == "f":
            self.toggle_flycam()

    def toggle_flycam(self):
        global flycam
        if self.player.enabled:
            self.player.enabled = False
            mouse.locked = False
            flycam.enabled = True
            flycam.position = self.player.position + Vec3(0, 2, 0)
        else:
            self.player.position = flycam.position
            flycam.enabled = False
            self.player.enabled = True
            mouse.locked = True


# Game starten
def levels_aanroepen():
    level1 = Level1()
levels_aanroepen()
app.run()