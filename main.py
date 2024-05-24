import ctypes
import keyboard
import time


def on_key_press(event):
    global locker
    global unlocker
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "num lock" and keyboard.is_pressed('ctrl'):
            locker = False
            unlocker = True

user32 = ctypes.windll.user32
if user32.GetKeyState(0x90) == 1:
    locker = True
elif user32.GetKeyState(0x90) == 0:
    locker = False
unlocker = False
keyboard.on_press(on_key_press)
counter = 0

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
        elif (user32.GetKeyState(0x90)) == 0:
            locker = False
    time.sleep(0.1)

