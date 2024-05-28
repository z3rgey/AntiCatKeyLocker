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
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image

def run_icon(icon, stop_event):
    icon.run()

def on_clicked(icon, item):
    if item.text == "Exit":
        stop_event.set()

def on_key_press(event):
    global locker, unlocker
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "num lock" and keyboard.is_pressed('ctrl'):
            locker = False
            unlocker = True

def change_icon_color(icon, color):
    icon.icon = create_image(64, 64, 'black', color)

user32 = ctypes.windll.user32
locker = user32.GetKeyState(0x90) == 1
unlocker = False
keyboard.on_press(on_key_press)
icon = pystray.Icon("test_icon")
icon.icon = create_image(64, 64, 'black', 'red')
icon.title = "AntiCat"
icon.menu = pystray.Menu(item('Exit', on_clicked))
stop_event = threading.Event()

icon_thread = threading.Thread(target=run_icon, args=(icon, stop_event))
icon_thread.start()

try:
    while True:
        if stop_event.is_set():
            icon.stop()
            break

        if locker:
            change_icon_color(icon, 'green')
            user32.BlockInput(True)
        else:
            change_icon_color(icon, 'red')
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
