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
TILE_SPACING = 0
PLAYER_SCALE = 0.2
ITEM_TILE_INDEX = 57

LEVEL_MAP = [
    "........................................",
    "........................................",
    "........................................",
    "...................BBB..................",
    "..................#####.................",
    ".......BBB....####......................",
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
        self.left_pressed = False
        self.right_pressed = False
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
                x = col * (TILE_WIDTH + TILE_SPACING) + 2
                y = row * (TILE_HEIGHT + TILE_SPACING) + 2
                width = TILE_WIDTH - 4
                height = TILE_HEIGHT - 4
                try:
                    texture = source_texture.crop(x, y, width, height)
                except AttributeError:
                    texture = source_texture.create_child(x, y, width, height)
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
        self.items_collected = 0
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Items")
        try:
            self.camera = arcade.camera.Camera2D()
        except:
            self.camera = None
        self.load_tile_textures()
        self.items_text = arcade.Text(
            "Items: 0",  # text
            20,  # x
            SCREEN_HEIGHT - 40,  # y
            arcade.color.YELLOW,  # color
            24,  # font_size
            bold=True
        )
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
                            tex = self.tiles_texture_list[ITEM_TILE_INDEX]
                            item = arcade.Sprite(
                                scale=TILE_SCALING,
                                hit_box_points=[(-32, -32), (32, -32), (32, 32), (-32, 32)]
                            )
                            item.texture = tex
                            item.center_x = x
                            item.center_y = y

                            self.scene.add_sprite("Items", item)
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
        arcade.draw_text(
            f"Items: {self.items_collected}",
            x=20,
            y=self.window.height - 40,
            color=arcade.color.YELLOW,
            font_size=24,
            bold=True
        )

    def on_update(self, delta_time):
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        else:
            self.player.change_x = 0
        if self.physics_engine:
            self.physics_engine.update()
        if self.player:
            self.player.update_animation()
            if self.camera:
                self.camera.position = (
                    self.player.center_x,
                    SCREEN_HEIGHT // 2
                )
            if self.player.center_y < -300:
                self.setup()
        items_hit = arcade.check_for_collision_with_list(
            self.player,
            self.scene["Items"]
        )

        for item in items_hit:
            item.remove_from_sprite_lists()
            self.items_collected += 1
        self.items_text.text = f"Items: {self.items_collected}"

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            if self.physics_engine and self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = MyGame()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()
