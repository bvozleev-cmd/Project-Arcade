import arcade
import enum
import os


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Coin Quest"
PLAYER_MOVEMENT_SPEED = 7
PLAYER_JUMP_SPEED = 25
GRAVITY = 1.2
TILE_SCALING = 0.5
PLAYER_SCALE = 0.2
MAP_PATH = "maps/map_1.tmx"


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

    def update_animation(self, delta_time: float = 1 / 60):
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

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AZURE)
        self.setup()


    def setup(self):
        self.items_collected = 0
        tile_map = arcade.load_tilemap(
            MAP_PATH,
            scaling=TILE_SCALING,
            layer_options={
                "Platforms": {"use_spatial_hash": True},
                "Items": {"use_spatial_hash": True},
            }
        )
        self.scene = arcade.Scene()
        for layer_name, layer in tile_map.sprite_lists.items():
            self.scene.add_sprite_list(layer_name, sprite_list=layer)
        self.player = Player()
        player_layer = tile_map.object_lists.get("Player")
        if player_layer:
            spawn = player_layer[0]
            self.player.center_x = spawn.shape[0] + self.player.width / 2
            self.player.center_y = spawn.shape[1] + self.player.height / 2
        else:
            self.player.center_x = self.player.width // 2
            self.player.center_y = self.player.height // 2
        self.scene.add_sprite("Player", self.player)
        try:
            self.camera = arcade.camera.Camera2D()
        except:
            self.camera = None
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITY,
            walls=self.scene["Platforms"]
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