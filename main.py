import arcade
import enum


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Coin Quest"
PLAYER_SPEED = 300
PLAYER_JUMP_SPEED = 10000
GRAVITY = 5


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.2
        self.idle_texture = arcade.load_texture(
            "images/characters/character_1.png")
        self.texture = self.idle_texture
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.face_direction = FaceDirection.RIGHT
        self.jump_able = True

    def update_animation(self, delta_time: float = 1/60):
        if self.face_direction == FaceDirection.RIGHT:
            self.texture = self.idle_texture
        else:
            self.texture = self.idle_texture.flip_horizontally()

    def update(self, keys_pressed, delta_time: float = 1 / 60):
        dx, dy = 0, 0
        dy -= GRAVITY
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= PLAYER_SPEED * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += PLAYER_SPEED * delta_time
        if arcade.key.SPACE in keys_pressed:
            if self.jump_able and self.center_y <= self.height / 2:
                dy += PLAYER_JUMP_SPEED * delta_time
                self.jump_able = False
        else:
            self.jump_able = True

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy

        # Ограничение в пределах экрана
        top = self.center_y + self.height // 4
        bottom = self.center_y - self.height // 4
        left = self.center_x - self.width // 8
        right = self.center_x + self.width // 8
        if top > SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT - 45
        elif bottom <= 0:
            self.center_y = 45
        if right > SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH - 40
        elif left < 0:
            self.center_x = 40

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
