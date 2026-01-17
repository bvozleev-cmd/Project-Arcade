import arcade
import enum
import os

# --- Константы ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Coin Quest"

PLAYER_MOVEMENT_SPEED = 7
PLAYER_JUMP_SPEED = 25
GRAVITY = 1.2

TILE_SCALING = 0.5
TILE_WIDTH = 128
TILE_HEIGHT = 128
TILE_COLUMNS = 18
TILE_COUNT = 324
# Возвращаем 0, так как 1 сделал только хуже
TILE_SPACING = 0

PLAYER_SCALE = 0.4

LEVEL_MAP = [
    "........................................",
    "........................................",
    "........................................",
    "...................BBB..................",
    "..................#####.................",
    ".......BBB..............................",
    "......#####..................B..........",
    "............................BB..........",
    "P.....B....................BBB.......BBB",
    "########################################",
]


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(hit_box_algorithm="Simple")

        self.scale = PLAYER_SCALE
        try:
            self.idle_texture = arcade.load_texture(
                "images/characters/character_1.png")
        except:
            self.idle_texture = arcade.make_circle_texture(
                30, arcade.color.RED)

        self.texture = self.idle_texture
        self.face_direction = FaceDirection.RIGHT

    def update_animation(self, delta_time: float = 1/60):
        if self.change_x < 0 and self.face_direction == FaceDirection.RIGHT:
            self.face_direction = FaceDirection.LEFT
        elif self.change_x > 0 and self.face_direction == FaceDirection.LEFT:
            self.face_direction = FaceDirection.RIGHT

        if self.face_direction == FaceDirection.LEFT:
            self.texture = self.idle_texture.flip_horizontally()
        else:
            self.texture = self.idle_texture


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene = None
        self.player = None
        self.physics_engine = None
        self.camera = None
        self.tiles_texture_list = []

    def load_tile_textures(self):
        try:
            source_texture = arcade.load_texture(
                'images/map_textures/spritesheet-tiles-double.png')
            self.tiles_texture_list = []

            # tex_height нам нужен только для инверсии, но пока вернем обычный порядок
            # tex_height = source_texture.height

            for i in range(TILE_COUNT):
                row = i // TILE_COLUMNS
                col = i % TILE_COLUMNS

                x = col * (TILE_WIDTH + TILE_SPACING)
                # Возвращаем классический расчет "снизу-вверх"
                y = row * (TILE_HEIGHT + TILE_SPACING)

                try:
                    texture = source_texture.crop(
                        x, y, TILE_WIDTH, TILE_HEIGHT)
                except AttributeError:
                    texture = source_texture.create_child(
                        x, y, TILE_WIDTH, TILE_HEIGHT)

                self.tiles_texture_list.append(texture)

        except Exception as e:
            print(f"Ошибка загрузки тайлов: {e}")
            for i in range(200):
                self.tiles_texture_list.append(
                    arcade.make_circle_texture(30, arcade.color.GRAY))

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AZURE)
        self.setup()

    def setup(self):
        self.scene = arcade.Scene()

        try:
            self.camera = arcade.camera.Camera2D()
        except:
            self.camera = None

        self.load_tile_textures()

        if self.tiles_texture_list:
            map_height_tiles = len(LEVEL_MAP)
            for row_index, row_string in enumerate(LEVEL_MAP):
                for col_index, char in enumerate(row_string):

                    x = col_index * (TILE_WIDTH * TILE_SCALING) + \
                        (TILE_WIDTH * TILE_SCALING) / 2
                    y = (map_height_tiles - row_index) * (TILE_HEIGHT *
                                                          TILE_SCALING) - (TILE_HEIGHT * TILE_SCALING) / 2

                    if char == "#":
                        tex = self.tiles_texture_list[1] if len(
                            self.tiles_texture_list) > 1 else None
                        if tex:
                            tile = arcade.Sprite()
                            tile.texture = tex
                            tile.center_x = x
                            tile.center_y = y
                            tile.scale = TILE_SCALING
                            self.scene.add_sprite("Platforms", tile)

                    elif char == "B":
                        tex = self.tiles_texture_list[100] if len(
                            self.tiles_texture_list) > 100 else None
                        if tex:
                            tile = arcade.Sprite()
                            tile.texture = tex
                            tile.center_x = x
                            tile.center_y = y
                            tile.scale = TILE_SCALING
                            self.scene.add_sprite("Platforms", tile)

                    elif char == "P":
                        self.player = Player()
                        self.player.center_x = x
                        self.player.center_y = y + 64
                        self.scene.add_sprite("Player", self.player)

        if not self.player:
            self.player = Player()
            self.player.center_x = 100
            self.player.center_y = 300
            self.scene.add_sprite("Player", self.player)

        walls = self.scene["Platforms"] if "Platforms" in self.scene else arcade.SpriteList(
        )

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITY,
            walls=walls
        )

    def on_draw(self):
        self.clear()
        if self.camera:
            self.camera.use()
        self.scene.draw()

    def on_update(self, delta_time):
        if self.physics_engine:
            self.physics_engine.update()

        if self.player:
            self.player.update_animation()
            if self.camera:
                self.camera.position = (
                    self.player.center_x, self.player.center_y)

            if self.player.center_y < -300:
                self.setup()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine and self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            self.player.change_x = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = MyGame()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()
