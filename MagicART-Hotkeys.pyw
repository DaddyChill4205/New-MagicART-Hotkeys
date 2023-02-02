import sys
import random
from time import sleep, time
from os import startfile, system
from webbrowser import open as webopen
from tendo.singleton import SingleInstance
from global_hotkeys import register_hotkeys, start_checking_hotkeys
from bot import click_if_exists, search_and_click, found, find, bclick
from pyautogui import hotkey, moveTo
from pyperclip import copy
from subprocess import call
from input_boxes import message, buttons, double_input

# Global Variables
is_alive = True
awake = True
keyboard_command = True
complete = False
admin = False


# makes sure only one instance of the program is running
try:
    only_one = SingleInstance()
except Exception as e:
    message("Whoops:", e)


def check_user():
    global admin
    result = double_input("Username", "Password")
    if result == None:
        exit()
    input_user, input_password = result.split(' ')
    input_user = input_user
    with open("username_password.txt", "r") as file:
        username, password = file.read().split(" ")
        username = username
    with open("admin_username_password.txt") as file:
        admin_username, admin_password = file.read().split(" ")
        admin_username = admin_username
    if admin_username == input_user and admin_password == input_password:
        admin = True
        return
    elif username == input_user and password == input_password:
        admin = False
        return
    else:
        r = buttons("Username or Password is incorrect. Try again?",
                    button_options=["Yes", "No"])
        if r == "Yes":
            check_user()
        if r == "No":
            exit()
        if r == None:
            exit()


check_user()

# prints a list of all the hotkeys
#TODO: align text to the left side of window
message(" F2: Go to 925 template \n F3: Go to 10K template \n F4: Go to 14K template \n F5: Go to Logos template \n F6: Open Toolbar \n F7: Hotkeys List \n F11: Close MagicART \n F12: Open MagicART \n Ctrl + Shift: Horizontal Allignment \n Ctrl + Alt: Center Allignment \n Alt + `: Toggle Keyboard Commands", "Hotkeys")

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Lists
template_list = [
    r"C:\Users\rcherveny\Desktop\MagicART saves\.925 Template.dgn",
    r"C:\Users\rcherveny\Desktop\MagicART saves\10K Template.dgn",
    r"C:\Users\rcherveny\Desktop\MagicART saves\14K Template.dgn",
    r"C:\Users\rcherveny\Desktop\MagicART saves\Logos Template.dgn"]

zoom_list = [
    "images\\Silver Template.png",
    "images\\10K Template.png",
    "images\\14K Template.png",]

sleeplist = [
    "Don't fall asleep...",
    "Stay awake...",
    "Can't sleep yet...",
    "So tired..."]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Decorator to turn keyboard commands on and off


def commands_on_off(input_function):
    def wrapper():
        global keyboard_command
        if not keyboard_command:
            print("Keyboard Commands OFF")
        if keyboard_command:
            input_function()

    return wrapper


def admin_commands(input_function):
    def wrapper():
        global admin
        if admin:
            input_function()
        if not admin:
            r = buttons("You must have Administrator Privileges to use this command. \n \n Sign in as Admin?",
                        button_options=["Yes", "No"])
            if r == "Yes":
                r = double_input("Admin Username", "Admin Password")
                if r == None:
                    pass
                input_user, input_password = r.split(' ')
                input_user = input_user
                with open("admin_username_password.txt") as file:
                    admin_username, admin_password = file.read().split(" ")
                    admin_username = admin_username
                if admin_username == input_user and admin_password == input_password:
                    admin = True
                    input_function()
                if admin_username != input_user and admin_password != input_password:
                    message("Incorrect Admin Username or Password.")
            if r == "No":
                pass

    return wrapper

# Opens MagicART and opens all the templates


@commands_on_off
def open_MagicArt():
    # move mouse to bottom right corner
    moveTo(1260, 1079)
# open MagicART application
    startfile("C:\\Program Files (x86)\\MagicART 5\\MagicART.exe")
# make sure MagicART is full screen
    click_if_exists("images\\fullscreen.png")
# find and click the object property pin
    found_pin = search_and_click(
        "images\\object property pin.png", region=(164, 46, 380, 213))
# if the object property pin is not found, click the fullscreen button
    if not found_pin:
        click_if_exists("images\\open magicart.png", region=(827, 971, 1005, 1079)) or click_if_exists(
            "images\\highlighted open magicart.png", region=(827, 971, 1005, 1079))
        click_if_exists("images\\object property pin.png")
        click_if_exists("images\\fullscreen.png")
# check that the engraver is connected
    found_connected = find("images\\engraver connected.png", region=(1717, 62, 1916, 242)) or find(
        "images\\engraver connected 2.png", region=(1717, 62, 1916, 242))
# if the engraver is not connected, close the application
    if not found_connected:
        call("taskkill /f /im MagicART.exe")
        r = buttons("Engraver not connected! \n Try again?", button_options=["Yes", "No"])
        if r == "Yes":
            open_MagicArt()
        if r == "No":
            return None
# if the engraver is connected, open all the templates
    for i in template_list:
        copy(i)
        hotkey("ctrl", "o")
        sleep(0.5)
        hotkey("ctrl", "v")
        hotkey("enter")
        sleep(0.7)
# size the logos template to 10%
    click_if_exists("images\\fit to page.png", region=(332, 927, 519, 1028))
    sleep(0.5)
    click_if_exists("images\\10%.png", region=(371, 802, 524, 998))
# size the rest of the templates to 15%
    for j in zoom_list:
        click_if_exists(j, region=(150, 64, 853, 128))
        click_if_exists("images\\fit to page.png",
                        region=(332, 927, 519, 1028))
        click_if_exists("images\\15%.png", region=(371, 802, 524, 998))

# opens Spotify and connects to Bluetooth


@commands_on_off
@admin_commands
def open_Spotify():
# open Spotify application
    startfile("C:\\Users\\rcherveny\\AppData\\Roaming\\Spotify\\Spotify.exe")
# open bluetooth options
    click_if_exists("images\\Bluetooth.png", region=(1657, 980, 1846, 1079))
    sleep(0.5)
# opens bluetooth and other devices page
    click_if_exists("images\\Show Bluetooth devices.png",
                    region=(1684, 856, 1904, 1044))
    sleep(1.5)\
        # check if joe's airpods are connected
    connected = found('images\\Bluetooth connected.png', region=(694, 6, 1878, 921)) or found(
        'images\\Bluetooth connected 2.png', region=(694, 6, 1878, 921))
# if not connected, gives the option to connect
    if not connected:
        r = buttons("No devices connected. Try connecting?",
                    button_options=['Yes', 'No'])
        if r == 'Yes':
            # tries to connect to joe's airpods, if not connected after 20 seconds, gives up
            search_and_click(
                'images\\Bluetooth not connected.png', region=(694, 6, 1878, 921))
            timeout = 20
            timeout_start = time()
            while time() < timeout_start + timeout:
                connected = found('images\\Bluetooth connected 2.png', region=(694, 6, 1878, 921)) or found(
                    'images\\Bluetooth connected.png', region=(694, 6, 1878, 921))
                click_if_exists('images\\connect bluetooth.png',
                                region=(694, 6, 1878, 921))
                if connected:
                    message("Bluetooth Connected")
                    click_if_exists('images\\exit bluetooth.png',
                                    region=(694, 6, 1878, 921))
                    return None
            if time() > timeout_start + timeout:
                message("Sorry, I couldn't connect any devices...")
                return None
# does not try to connect if the user says no
        if r == 'No':
            message("No devices connected")
# if connected, messages the status and exits the bluetooth page
    if connected:
        message("Bluetooth Connected")
        click_if_exists('images\\exit bluetooth.png',
                        region=(1724, 0, 1886, 86))


@commands_on_off
@admin_commands
def add_user():
    r = double_input("Admin Username", "Admin Password")
    file = open('admin_username_password.txt', "r")
    content = file.read()

    if r not in content:
        r = buttons("Username or Password is incorrect. Try again?",
                    button_options=["Yes", "No"])
        if r == "Yes":
            add_user()
        if r == "No":
            exit()
        if r == None:
            exit()
    if r == None:
        return
    if r in content:
        r = double_input("Enter New Username", "Enter New Password")
        users = [r]
        file = open('username_password.txt', "a")
        for user in users:
            file.write('\n' + user)
        file.close()


@commands_on_off
def open_toolbar():
    '''
    Opens the toolbar to give the user some options
    '''
    selection = buttons('', 'Toolbar', button_options=[
                        'Google', 'Workday', 'SKU Search', 'Spotify', 'Calculator', 'Add User', 'Shutdown'])
    selection_to_function = {
        'Google': lambda: webopen(f"https://www.google.com/"),
        'Workday': lambda: webopen(f"https://www.myworkday.com/wday/authgwy/signetjewelers/login.htmld"),
        'SKU Search': lambda: startfile('sku_search.py'),
        'Spotify': open_Spotify,
        'Calculator': lambda: system("calc"),
        'Add User': add_user,
        'Shutdown': shut_down_computer
    }
    if selection in selection_to_function:
        selection_to_function[selection]()


def toggle_keyboard_commands():
    '''
    Enables or disables keyboard commands
    '''
    global keyboard_command
    enable_disable = 'DISABLE' if keyboard_command else 'ENABLE'
    on_off = 'OFF' if keyboard_command else 'ON'
    r = buttons(f"Do you want to {enable_disable} Joe's Keyboard Commands?", button_options=[
                'Yes', 'No'])
    if r == 'Yes':
        keyboard_command = not keyboard_command
        message(f"Keyboard Commands {on_off}")
    elif r == 'No':
        message("Well then why did you click the button?")


@commands_on_off
def end_program():
    r = buttons("Are you sure you want to end the program?", button_options=[
                'Yes', 'No'])
    if r == 'Yes':
        call(["taskkill", "/F", "/IM", "pythonw.exe"])


@commands_on_off
def shut_down_computer():
    '''
    Shuts down the computer
    '''
    # shut down the computer
    r = buttons("Are you sure you want to shut down the computer?",
                button_options=['Yes', 'No'])
    if r == 'Yes':
        system("shutdown /s /t 1")


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Key Bindings for Commands
bindings = [
    # go to 925 template
    [["F2"], None, commands_on_off(lambda: bclick(240, 95))],
    # go to 10K template
    [["F3"], None, commands_on_off(lambda: bclick(400, 95))],
    # go to 14K template
    [["F4"], None, commands_on_off(lambda: bclick(565, 95))],
    # go to Logos template
    [["F5"], None, commands_on_off(lambda: bclick(720, 95))],
    [["F6"], None, open_toolbar],
    [["F7"], None, commands_on_off(lambda: message(
        " F2: Go to 925 template \n F3: Go to 10K template \n F4: Go to 14K template \n F5: Go to Logos template \n F6: Open Toolbar \n F7: Hotkeys List \n F11: Close MagicART \n F12: Open MagicART \n Alt + `: Toggle Keyboard Commands \n Ctrl + Shift: Horizontal Allignment \n Ctrl + Alt: Center Allignment", "Hotkeys"))],
    [["F10"], None, end_program],
    [["F11"], None, commands_on_off(lambda: call(
        ["taskkill", "/F", "/IM", "MagicART.exe"]))],
    [["F12"], None, open_MagicArt],
    [["alt", "`"], None, toggle_keyboard_commands],
    [["control", "shift"], None, commands_on_off(
        lambda: bclick(400, 65))],  # horizontal allignment
    [["control", "alt"], None, lambda: commands_on_off(
        bclick(475, 65))],  # center allignment
]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

start_checking_hotkeys()

register_hotkeys(bindings)

while awake:
    # pick a random phrase from the sleeplist to print, then sleep for 5 minutes and press f15
    print(random.choice(sleeplist))
    hotkey("F15")
    sleep(60 * 5)
