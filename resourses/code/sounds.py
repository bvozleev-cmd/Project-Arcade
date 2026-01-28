import arcade
import os

BASE_DIR = os.path.dirname(__file__)
SOUNDS_DIR = os.path.join(BASE_DIR, "..", "assets", "sounds")

press_button_1 = arcade.load_sound(os.path.join(SOUNDS_DIR, "button_1.mp3"))
press_button_2 = arcade.load_sound(os.path.join(SOUNDS_DIR, "button_2.mp3"))
cristall = arcade.load_sound(os.path.join(SOUNDS_DIR, "cristall.mp3"))
game_over = arcade.load_sound(os.path.join(SOUNDS_DIR, "game_over.mp3"))
water = arcade.load_sound(os.path.join(SOUNDS_DIR, "water.mp3"))
win = arcade.load_sound(os.path.join(SOUNDS_DIR, "win.mp3"))
step = arcade.load_sound(os.path.join(SOUNDS_DIR, "step.mp3"))
change_skin = arcade.load_sound(os.path.join(SOUNDS_DIR, "change_skin.mp3"))
jump = arcade.load_sound(os.path.join(SOUNDS_DIR, "jump.mp3"))