from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import keyboard
import pystray
import ctypes
import time
import os


def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    return image


def run_icon():
    def on_clicked(icon, item):
        if item.text == "Exit":
            icon.stop()
            os._exit(0)
    icon = pystray.Icon("test_icon")
    icon.icon = create_image(64, 64, 'black', 'red')
    icon.title = "AntiCat"
    icon.menu = pystray.Menu(
        item('Exit', on_clicked)
    )
    icon.run()


def on_key_press(event):
    global locker
    global unlocker
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "num lock" and keyboard.is_pressed('ctrl'):
            locker = False
            unlocker = True


user32 = ctypes.windll.user32
locker = user32.GetKeyState(0x90) == 1
unlocker = False
keyboard.on_press(on_key_press)
icon_thread = threading.Thread(target=run_icon)
icon_thread.start()

try:
    while True:
        if locker:
            user32.BlockInput(True)
        else:
            if user32.GetKeyState(0x90) == 1:
                if unlocker:
                    user32.BlockInput(False)
                    user32.keybd_event(0x90, 0x45, 0, 0)
                    user32.keybd_event(0x90, 0x45, 2, 0)
                    unlocker = False
                else:
                    locker = True
            elif user32.GetKeyState(0x90) == 0:
                locker = False
        time.sleep(0.1)
except Exception as error:
    print(error)