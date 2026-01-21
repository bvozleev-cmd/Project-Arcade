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
MAP_PATH = "maps/map_2.tmx"


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
        self.idle_texture_right = self.idle_texture
        self.idle_texture_left = self.idle_texture.flip_horizontally()

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.face_direction == FaceDirection.RIGHT:
            self.face_direction = FaceDirection.LEFT
        elif self.change_x > 0 and self.face_direction == FaceDirection.LEFT:
            self.face_direction = FaceDirection.RIGHT

        if self.face_direction == FaceDirection.LEFT:
            self.texture = self.idle_texture_left
        else:
            self.texture = self.idle_texture_right


class MyGame(arcade.View):
    def __init__(self, level=1):
        super().__init__()
        self.level = level
        self.left_pressed = False
        self.right_pressed = False
        self.scene = None
        self.player = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None
        self.god_mode = False
        self.up_pressed = False
        self.down_pressed = False

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AZURE)
        self.setup()

    def setup(self):
        self.items_collected = 0
        map_name = f"maps/map_{self.level}.tmx"
        # If map doesn't exist, fallback to map_2.tmx or handle error
        if not os.path.exists(map_name):
            print(f"Warning: Map {map_name} not found, defaulting to maps/map_2.tmx")
            map_name = "maps/map_2.tmx"

        tile_map = arcade.load_tilemap(
            map_name,
            scaling=TILE_SCALING,
            layer_options={
                "Wall": {"use_spatial_hash": True},  # коллизии
                "Platforms": {"use_spatial_hash": True},  # видимые платформы
                "Items": {"use_spatial_hash": True},  # предметы
                "Door": {"use_spatial_hash": True},  # дверь выхода
            }
        )
        self.tile_map = tile_map
        self.scene = arcade.Scene()

        # Добавляем все слои, кроме Wall в сцену для отрисовки
        for layer_name, layer in tile_map.sprite_lists.items():
            if layer_name != "Wall":  # Wall не будет рисоваться
                self.scene.add_sprite_list(layer_name, sprite_list=layer)

        # Игрок
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

        # Камера
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        walls_for_physics = arcade.SpriteList()
        walls_for_physics.extend(tile_map.sprite_lists["Wall"])
        walls_for_physics.extend(tile_map.sprite_lists["Platforms"])

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITY,
            walls=walls_for_physics
        )

    def on_draw(self):
        self.clear()
        if self.camera:
            self.camera.use()
        self.scene.draw()
        if self.gui_camera:
            self.gui_camera.use()
        arcade.draw_text(
            f"Кристаллов собрано: {self.items_collected}",
            x=20,
            y=self.window.height - 40,
            color=arcade.color.YELLOW,
            font_size=24,
            bold=True
        )

        if self.god_mode:
            arcade.draw_text(
                "GOD MODE",
                x=20,
                y=self.window.height - 80,
                color=arcade.color.RED,
                font_size=20,
                bold=True
            )

    def on_update(self, delta_time):
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        else:
            self.player.change_x = 0

        if self.god_mode:
            if self.up_pressed and not self.down_pressed:
                self.player.change_y = PLAYER_MOVEMENT_SPEED
            elif self.down_pressed and not self.up_pressed:
                self.player.change_y = -PLAYER_MOVEMENT_SPEED
            else:
                self.player.change_y = 0
            
            self.player.center_x += self.player.change_x
            self.player.center_y += self.player.change_y
        else:
            if self.physics_engine:
                self.physics_engine.update()
            if self.player.center_y < -300:
                from death_view import DeathView
                from database import update_crystals
                update_crystals(self.level, self.items_collected)
                self.window.show_view(DeathView(self.level))

        if self.player:
            self.player.update_animation()
            if self.camera:
                self.camera.position = (
                    int(self.player.center_x),
                    self.window.height // 2
                )
        items_hit = arcade.check_for_collision_with_list(
            self.player,
            self.scene["Items"]
        )
        for item in items_hit:
            item.remove_from_sprite_lists()
            self.items_collected += 1

        # Check for door collision (victory)
        if "Door" in self.scene:
            if arcade.check_for_collision_with_list(self.player, self.scene["Door"]):
                from database import complete_level
                from win_view import WinView
                
                # Save progress
                complete_level(self.level, self.items_collected)
                
                # Show victory screen
                self.window.show_view(WinView(self.level, self.items_collected))

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            if self.god_mode:
                self.up_pressed = True
            elif self.physics_engine and self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
        elif key in (arcade.key.DOWN, arcade.key.S):
            if self.god_mode:
                self.down_pressed = True
        elif key == arcade.key.G:
            self.god_mode = not self.god_mode
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False
        elif key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            self.up_pressed = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = MyGame()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()
