import arcade

class DummySound:
    def play(self, volume=1.0, pan=0.0, loop=False):
        pass

def safe_load_sound(path):
    try:
        return arcade.load_sound(path)
    except Exception as e:
        print(f"Warning: Could not load sound {path}: {e}")
        return DummySound()

press_button_1 = safe_load_sound("sounds/button_1.mp3")
press_button_2 = safe_load_sound("sounds/button_2.mp3")
cristall = safe_load_sound("sounds/cristall.mp3")
game_over = safe_load_sound("sounds/game_over.mp3")
water = safe_load_sound("sounds/water.mp3")
win = safe_load_sound("sounds/win.mp3")
step = safe_load_sound("sounds/step.mp3")
change_skin = safe_load_sound("sounds/change_skin.mp3")
jump = safe_load_sound("sounds/jump.mp3")
