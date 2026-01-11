import arcade
import enum

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Coin Quest"
PLAYER_SPEED = 300
GRAVITY = 2500
JUMP_FORCE = 900
MAX_FALL_SPEED = -1200
CUT_JUMP_FACTOR = 0.7


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.2
        self.idle_texture = arcade.load_texture(
            "images/characters/character_1.png"
        )
        self.texture = self.idle_texture
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 45
        self.face_direction = FaceDirection.RIGHT
        self.velocity_y = 0.0
        self.on_ground = True
        self.jump_pressed = False

    def update_animation(self, delta_time: float = 1 / 60):
        if self.face_direction == FaceDirection.RIGHT:
            self.texture = self.idle_texture
        else:
            self.texture = self.idle_texture.flip_horizontally()

    def update(self, keys_pressed, delta_time: float = 1 / 60):
        dx = 0
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= PLAYER_SPEED * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += PLAYER_SPEED * delta_time
        if arcade.key.SPACE in keys_pressed:
            if self.on_ground and not self.jump_pressed:
                self.velocity_y = JUMP_FORCE
                self.on_ground = False
                self.jump_pressed = True
        else:
            if self.velocity_y > 0:
                self.velocity_y *= CUT_JUMP_FACTOR
            self.jump_pressed = False
        self.velocity_y -= GRAVITY * delta_time
        if self.velocity_y < MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
        self.center_x += dx
        self.center_y += self.velocity_y * delta_time
        if self.center_y <= 45:
            self.center_y = 45
            self.velocity_y = 0
            self.on_ground = True
        self.center_x = max(40, min(SCREEN_WIDTH - 40, self.center_x))
        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AZURE)
        self.player = None
        self.player_list = arcade.SpriteList()
        self.keys_pressed = set()

    def setup(self):
        self.player = Player()
        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update(self.keys_pressed, delta_time)
        self.player_list.update_animation()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
