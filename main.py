import arcade
from database import init_db, init_skins
from menu import MenuView

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Coin Quest"

if __name__ == "__main__":
    init_db()
    init_skins()
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
    arcade.set_background_color(arcade.color.AZURE)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()
