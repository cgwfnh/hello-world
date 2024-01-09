'''Use python code to detect whether the PPT is playing in full screen. If it is playing in full screen, use the countdown program to time the playback.﻿ ```python

'''
import win32con
import win32gui
import time
import keyboard

# Check if PowerPoint is running
def is_powerpoint_running():
    hwnd = win32gui.FindWindow(None, "永中简报")
    if hwnd:
        return True
    else:
        return False

# Check if PowerPoint is playing in full screen
def is_powerpoint_in_full_screen():
    # hwnd = win32gui.FindWindow(None, "Microsoft PowerPoint")
    # hwnd = win32gui.FindWindow(None, "WPS 演示")
    hwnd = win32gui.FindWindow(None, "永中简报")
    if hwnd:
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        if style & win32con.WS_MAXIMIZE == win32con.WS_MAXIMIZE:
            return True
    return False

# Start countdown timer
def start_countdown_timer():
    print("Countdown timer started.")
    seconds = 0
    minutes = 0
    while True:
        if keyboard.is_pressed('q'):
            break
        time.sleep(1)
        seconds += 1
        if seconds == 60:
            minutes += 1
            seconds = 0
        print(f"{minutes}:{seconds}")

# Main program
if is_powerpoint_running():
    if is_powerpoint_in_full_screen():
        start_countdown_timer()
    else:
        print("PowerPoint is not playing in full screen.")
else:
    print("PowerPoint is not running.")

# generate add tow integer function