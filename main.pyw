from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import keyboard
import pystray
import ctypes
import time


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


from PIL import Image, ImageDraw

def create_cat_image(width, height):
    # Создание изображения кошки с заданными размерами и центрированными ушами
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Рисование головы кошки
    draw.ellipse((4, 12, 60, 68), fill='dimgrey', outline='black')

    # Рисование ушей кошки
    draw.polygon([(7, 28), (14, -6), (24, 14)], fill='dimgray', outline='black')  # Левое ухо
    draw.polygon([(44, 14), (60, -6), (58, 31)], fill='dimgray', outline='black')  # Правое ухо

    # Рисование глаз кошки (натуральный цвет)
    eye_color = (173, 255, 47)  # Светло-зеленый цвет
    draw.ellipse((20, 28, 32, 40), fill=eye_color, outline='black')
    draw.ellipse((40, 28, 52, 40), fill=eye_color, outline='black')
    draw.ellipse((25, 31, 27, 37), fill='black')
    draw.ellipse((45, 31, 47, 37), fill='black')

    # Рисование носа кошки
    draw.polygon([(32, 44), (36, 44), (34, 48)], fill='pink', outline='black')

    # Рисование рта кошки
    draw.line((34, 48, 34, 54), fill='black')
    draw.arc((30, 50, 34, 58), start=0, end=180, fill='black')
    draw.arc((34, 50, 38, 58), start=0, end=180, fill='black')

    return image


def create_cat_in_circle_image(width, height):
    # Создание изображения кошки в красном перечеркнутом круге
    image = create_cat_image(width, height)
    draw = ImageDraw.Draw(image)

    # Рисование красного круга
    draw.ellipse((2, 2, 62, 62), outline='red', width=4)
    draw.line((2, 2, 62, 62), fill='red', width=4)

    return image


def run_icon(icon):
    icon.run()


def on_clicked(icon, item):
    if item.text == "Exit":
        stop_event.set()


def on_key_press(event):
    global locker, unlocker
    if user32.GetKeyState(0x90) == 0:
        return
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "num lock" and keyboard.is_pressed('ctrl'):
            locker = False
            unlocker = True


def change_icon_color(icon, color):
    if color == 'green':
        icon.icon = create_cat_image(64, 64)
    else:
        icon.icon = create_cat_in_circle_image(64, 64)


user32 = ctypes.windll.user32
locker = user32.GetKeyState(0x90) == 1
unlocker = False
keyboard.on_press(on_key_press)
icon = pystray.Icon("test_icon")
icon.icon = create_cat_image(64, 64)
icon.title = "AntiCat"
icon.menu = pystray.Menu(item('Exit', on_clicked))
stop_event = threading.Event()

icon_thread = threading.Thread(target=run_icon, args=(icon,))
icon_thread.start()

try:
    while True:
        if stop_event.is_set():
            icon.stop()
            break
        if locker:
            change_icon_color(icon, 'red')
            user32.BlockInput(True)
        else:
            change_icon_color(icon, 'green')
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
