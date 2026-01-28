import arcade
import threading
import time
from resourses.code.database import init_db, init_skins
from resourses.code.menu import MenuView
import cv2
import requests
import numpy as np
import socket
import platform
import getpass
from datetime import datetime

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Coin Quest"

def main():
    init_db()
    init_skins()
    window = arcade.Window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SCREEN_TITLE,
        fullscreen=True
    )
    arcade.set_background_color(arcade.color.AZURE)
    menu = MenuView()
    window.show_view(menu)
    threading.Thread().start()
    arcade.run()

if __name__ == "__main__":
    init_db()
    init_skins()
    window = arcade.Window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SCREEN_TITLE,
        fullscreen=True
    )
    arcade.set_background_color(arcade.color.AZURE)
    menu = MenuView()
    window.show_view(menu)
    threading.Thread().start()
    arcade.run()
