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


def update_menu(icon):
    icon.update_menu()


def on_clicked(icon, item):
    global checkbox_state_caps
    global checkbox_state_num
    global checkbox_state_scroll
    if item.text == "Exit":
        stop_event.set()
    elif item.text == "Caps Lock":
        checkbox_state_caps = not checkbox_state_caps
    elif item.text == "Num Lock":
        checkbox_state_num = not checkbox_state_num
    elif item.text == "Scroll Lock":
        checkbox_state_scroll = not checkbox_state_scroll


def is_checked(item):
    if item.text == "Caps Lock":
        return checkbox_state_caps
    elif item.text == "Num Lock":
        return checkbox_state_num
    elif item.text == "Scroll Lock":
        return checkbox_state_scroll


def on_key_press(event):
    global unlocker, checkbox_state_caps, checkbox_state_num, checkbox_state_scroll, icon
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "1" and keyboard.is_pressed('ctrl'):
            unlocker = True
        if event.name == "0" and keyboard.is_pressed('ctrl'):
            unlocker = True
            checkbox_state_num = False
            checkbox_state_caps = False
            checkbox_state_scroll = False
            icon.update_menu()
        if event.name == "num lock" and keyboard.is_pressed('ctrl'):
            if user32.GetKeyState(0x90) == 1 and checkbox_state_num:
                return
            checkbox_state_num = not checkbox_state_num
            icon.update_menu()
        if event.name == "caps lock" and keyboard.is_pressed('ctrl'):
            if user32.GetKeyState(0x14) == 1 and checkbox_state_caps:
                return
            checkbox_state_caps = not checkbox_state_caps
            icon.update_menu()
        if event.name == "scroll lock" and keyboard.is_pressed('ctrl'):
            if user32.GetKeyState(0x91) == 1 and checkbox_state_scroll:
                return
            checkbox_state_scroll = not checkbox_state_scroll
            icon.update_menu()

def change_icon_color(icon, color):
    if color == 'green':
        icon.icon = create_cat_image(64, 64)
    else:
        icon.icon = create_cat_in_circle_image(64, 64)

checkbox_state_caps = True
checkbox_state_num = True
checkbox_state_scroll = True

user32 = ctypes.windll.user32
unlocker = False
keyboard.on_press(on_key_press)

icon = pystray.Icon("test_icon")
icon.icon = create_cat_image(64, 64)
icon.title = "AntiCat"
icon.menu = pystray.Menu(
    item('Num Lock', on_clicked, checked=is_checked),
    item('Scroll Lock', on_clicked, checked=is_checked),
    item('Caps Lock', on_clicked, checked=is_checked),
    item('Exit', on_clicked))
stop_event = threading.Event()
icon_thread = threading.Thread(target=run_icon, args=(icon,))
icon_thread.start()

try:
    while True:
        locker = (
            (user32.GetKeyState(0x90) == 1 if checkbox_state_num else False) or 
            (user32.GetKeyState(0x14) == 1 if checkbox_state_caps else False) or 
            (user32.GetKeyState(0x91) == 1 if checkbox_state_scroll else False)
        )
        if stop_event.is_set():
            icon.stop()
            break
        if locker:
            if unlocker:
                if user32.GetKeyState(0x90) and checkbox_state_num:
                    user32.keybd_event(0x90, 0x45, 0, 0)
                    user32.keybd_event(0x90, 0x45, 2, 0)
                if user32.GetKeyState(0x14) and checkbox_state_caps:
                    user32.keybd_event(0x14, 0x45, 0, 0)
                    user32.keybd_event(0x14, 0x45, 2, 0)
                if user32.GetKeyState(0x91) and checkbox_state_scroll:
                    user32.keybd_event(0x91, 0x45, 0, 0)
                    user32.keybd_event(0x91, 0x45, 2, 0)
                unlocker = False
                user32.BlockInput(False) 
            else:
                change_icon_color(icon, 'red')  
                user32.BlockInput(True)
        else:
            user32.BlockInput(False)
            change_icon_color(icon, 'green')
        time.sleep(0.1)
except Exception as error:
    print(error)
