import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Coin Quest"
PLAYER_SPEED = 5
PLAYER_JUMP_SPEED = 15
GRAVITY = 1


class Player(arcade.Sprite):
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)
        self.change_x = 0
        self.change_y = 0
        self.facing_right = True

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_y -= GRAVITY
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        if self.change_x < 0 and self.facing_right:
            self.facing_right = False
            self.scale_x = -abs(self.scale_x)
        elif self.change_x > 0 and not self.facing_right:
            self.facing_right = True
            self.scale_x = abs(self.scale_x)


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AZURE)
        self.player = None
        self.player_list = arcade.SpriteList()
        self.keys_pressed = set()

    def setup(self):
        self.player = Player("images/characters/character_1.png", scale=0.2)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player.change_x = 0
        if arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed:
            self.player.change_x = -PLAYER_SPEED
        if arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed:
            self.player.change_x = PLAYER_SPEED
        if (arcade.key.UP in self.keys_pressed or arcade.key.W in self.keys_pressed):
            if self.player.bottom <= 0:
                self.player.change_y = PLAYER_JUMP_SPEED
        self.player_list.update(delta_time)

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