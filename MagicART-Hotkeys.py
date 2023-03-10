# Imports:
import random
import threading
import shutil
from time import sleep, time
from os import startfile, system, path
from webbrowser import open as webopen
from global_hotkeys import register_hotkeys, start_checking_hotkeys
from bot import click_if_exists, search_and_click, found, find, bclick
from pyautogui import hotkey, moveTo
from pyperclip import copy
from subprocess import call
from input_boxes import message, buttons, double_input
from win32gui import MoveWindow, FindWindow, SetWindowPos
from win32con import HWND_TOPMOST, HWND_NOTOPMOST
from tendo.singleton import SingleInstance

# Startup Process:
'''Checks to make sure there is only one instance of the program. Then, resizes the window, and moves it to the bottom left corner.'''
only_one = SingleInstance()
try:
    hwnd = FindWindow(None, "MagicART-Hotkeys.py - Shortcut")
    MoveWindow(hwnd, -7, 750, 407, 300, True)
except Exception as e:
    message(f"Whoops: {e}")

# Global Variables:
is_alive = True
awake = True
keyboard_command = True
complete = False
admin = False
progress = 0
lock = threading.Lock()

# Login:
'''Asks the user to login. If the user does not have an account, it asks the user if they would like to create one. 
If the user is an admin, it sets the admin variable to True. Runs in response to the check_user() function.'''
def login():
    global admin
    result = double_input("Username", "Password", )
    if result == None:
        exit()
    file = open("TXT\\username_password.txt", "r")
    file2 = open("TXT\\admin_username_password.txt", "r")
    contents = file.read()
    contents2 = file2.read()
    if result not in contents and result not in contents2:
        b = buttons("Incorrect Username or Password. Would you like to create a new account?", button_options=["Yes", "No"])
        if b == None:
            exit()
        if b == "Yes":
            r = double_input("New Username", "New Password", "New User")
            file = open("TXT\\username_password.txt", "a")
            file.write('\n' + r)
            file.close()
        if b == "No":
            login()
    if result in contents:
        pass
    if result in contents2:
        admin = True
        pass
    file.close()

# Check for Users:
'''Checks to see if there are any users. If there are none, it asks the user to create a user account.'''
def check_user():
    if path.getsize("TXT\\username_password.txt") != 0 and path.getsize("TXT\\admin_username_password.txt") != 0:
        login()
    if path.getsize("TXT\\username_password.txt") == 0 and path.getsize("TXT\\admin_username_password.txt") != 0:
        login()
    if path.getsize("TXT\\username_password.txt") != 0 and path.getsize("TXT\\admin_username_password.txt") == 0:
        message("There are no Admin users. Please create an Admin user account.")
        r = double_input("New Admin Username", "New Admin Password", "New Admin Credentials")
        file = open("TXT\\admin_username_password.txt", "a")
        file.write('\n' + r)
        file.close()
    if path.getsize("TXT\\username_password.txt") == 0 and path.getsize("TXT\\admin_username_password.txt") == 0:
        message("There are no Admin users. Please create an Admin user account.")
        r = double_input("New Admin Username", "New Admin Password", "New Admin Credentials")
        file = open("TXT\\admin_username_password.txt", "a")
        file.write('\n' + r)
        file.close()
check_user()

# Commands List:
'''Prints a list of all the commands to the console.'''
print("F2: Go to 925 template")
print("F3: Go to 10K template")
print("F4: Go to 14K template")
print("F5: Go to Logos template")
print("F6: Open Toolbar")
print("F7: Hotkeys List")
print("F11: Close MagicART")
print("F12: Open MagicART")
print("Ctrl + Shift: Horizontal Alignment")
print("Ctrl + Alt: Center Alignment")
print("Alt + `: Toggle Keyboard Commands")
print(f"admin: {admin}")
print("----------------------------------------------")

# Lists:
template_list = [
    r"C:\Users\rcherveny\Desktop\MagicART saves\.925 Template.dgn",
    r"C:\Users\rcherveny\Desktop\MagicART saves\10K Template.dgn",
    r"C:\Users\rcherveny\Desktop\MagicART saves\14K Template.dgn",
    r"C:\Users\rcherveny\Desktop\MagicART saves\Logos Template.dgn"]

zoom_list = [
    "PNG\\Silver Template.png",
    "PNG\\10K Template.png",
    "PNG\\14K Template.png",]

sleeplist = [
    "Don't fall asleep...",
    "Stay awake...",
    "Can't sleep yet...",
    "So tired..."]
progress = [
    1, 2, 3, 4, 5
]


# Wrappers:
'''Checks if keyboard commands are on or off. If they are off, it will not run the command.'''
def commands_on_off(input_function):
    def wrapper():
        global keyboard_command
        if not keyboard_command:
            print("Keyboard Commands OFF")
        if keyboard_command:
            input_function()

    return wrapper


'''Checks if the user is an admin. If they are not, it will ask them to sign in as an admin.'''
def admin_commands(input_function):
    def wrapper():
        global admin
        if admin:
            input_function()
        if not admin:
            r = buttons("You must have Administrator Privileges to use this command. \n \n Enter Admin credentials?",
                        button_options=["Yes", "No"])
            if r == "Yes":
                r = double_input("Admin Username", "Admin Password")
                if r == None:
                    pass
                file = open("TXT\\admin_username_password.txt")
                contents = file.read()
                if r in contents:
                    input_function()
                if r not in contents:
                    message("Incorrect username and password.")
                    wrapper()
            if r == "No":
                pass
    return wrapper


# Classes:
'''Gives multiple functions that deal with user accounts and privileges.'''
class Users(object):
    global admin
    def __init__(self):
        self.admin = admin

    '''Creates a new user account.'''
    def add_user(self):
        r = double_input("Enter New Username", "Enter New Password")
        if r == None:
            return
        else:
            file = open('TXT\\username_password.txt', "a")
            file.write('\n' + r)
            file.close()

    '''Checks if the user is an admin.'''
    def check_if_admin(self):
        r = double_input("Admin Username", "Admin Password")
        file = open('TXT\\admin_username_password.txt', "r")
        content = file.read()
        if r == None:
            return
        if r not in content:
            r = buttons("Username or Password is incorrect. Try again?",
                        button_options=["Yes", "No"])
            if r == "Yes":
                self.check_if_admin()
            if r == "No":
                return
            if r == None:
                return
        if r in content:
            self.admin = True
            return True

    '''Creates a new admin account.'''
    def make_admin(self):
        if self.check_if_admin():
            r = double_input("Enter New Admin Username", "Enter New Admin Password")
            file = open('TXT\\admin_username_password.txt', "a")
            file.write('\n' + r)
            file.close()
        else:
            return


# Functions:

def prog_bar(text=None):
    progress = 0
    print(text)
    term_width, _ = shutil.get_terminal_size(fallback=(80, 24))
    bar_width = term_width - len(f"[ 100% ] ")
    bar = "[" + "=" * int(progress / (100 / (bar_width - 2))) + " " * (bar_width - int(progress / (100 / (bar_width - 2))) - 2) + "]"
    print(f"\r{bar} {progress}%", end="", flush=True)

def update_prog_bar(start, stop):
    start = round(start)
    stop = round(stop)
    progress = start
    term_width, _ = shutil.get_terminal_size(fallback=(80, 24))
    bar_width = term_width - len(f"[ 100% ] ")
    while progress <= stop:
        bar = "[" + "=" * int(progress / (100 / (bar_width - 2))) + " " * (bar_width - int(progress / (100 / (bar_width - 2))) - 2) + "]"
        print(f"\r{bar} {progress}%", end="", flush=True)
        progress += 1
        sleep(0.15)


'''Opens MagicART and all the necessary templates.'''
@commands_on_off
def open_MagicArt():
    hwnd = FindWindow(None, "MagicART-Hotkeys.py - Shortcut")
    SetWindowPos(hwnd, HWND_TOPMOST, -7, 750, 407, 300, 0)
    prog_bar("Opening MagicART\nDO NOT MOVE THE MOUSE")
    threading.Thread(target=update_prog_bar, args=(0, 2.13)).start()
    moveTo(1300, 1079) 

    threading.Thread(target=update_prog_bar, args=(2.13, 4.26)).start()
    startfile(r"C:\Program Files (x86)\MagicART 5\MagicART.exe") 

    threading.Thread(target=update_prog_bar, args=(4.26, 12.78)).start()
    found_pin = search_and_click("PNG\\object property pin.png", timeout=6, region=(164, 46, 380, 213)) 
    if not found_pin:
        click_if_exists("PNG\\open magicart.png", region=(827, 971, 1005, 1079)) or click_if_exists("PNG\\highlighted open magicart.png", region=(827, 971, 1005, 1079)) 
        search_and_click("PNG\\object property pin.png", region=(164, 46, 380, 213)) 
        click_if_exists("PNG\\fullscreen.png") 

    threading.Thread(target=update_prog_bar, args=(12.78, 14.91)).start()
    found_connected = find("PNG\\engraver connected.png", timeout=3, region=(1717, 62, 1916, 242)) or find(
        "PNG\\engraver connected 2.png", region=(1717, 62, 1916, 242)) 
    

    if not found_connected:
        call("taskkill /f /im MagicART.exe")
        r = buttons("Engraver not connected! \n Try again?", button_options=["Yes", "No"])
        if r == "Yes":
            open_MagicArt()
        if r == "No":
            return None
        
    threading.Thread(target=update_prog_bar, args=(14.91, 63.9)).start()
    for i in template_list: 
        copy(i) 
        hotkey("ctrl", "o")
        sleep(0.5)
        hotkey("ctrl", "v")
        hotkey("enter")
        sleep(0.7)
    with lock:
        progress = 63.9

    threading.Thread(target=update_prog_bar, args=(63.9, 66)).start()
    click_if_exists("PNG\\fit to page.png", region=(332, 927, 519, 1028))
    sleep(0.5)
    click_if_exists("PNG\\10%.png", region=(371, 802, 524, 998))

    threading.Thread(target=update_prog_bar, args=(66, 100)).start()
    for j in zoom_list:
        click_if_exists(j, region=(150, 64, 853, 128))
        click_if_exists("PNG\\fit to page.png",
                        region=(332, 927, 519, 1028))
        click_if_exists("PNG\\15%.png", region=(371, 802, 524, 998))
    click_if_exists("PNG\\object property pin.png", region=(164, 46, 380, 213))
    hwnd = FindWindow(None, "MagicART-Hotkeys.py - Shortcut")
    SetWindowPos(hwnd, HWND_NOTOPMOST, -7, 750, 407, 300, 0)
    click_if_exists("PNG\\Terminal window.png")
    bclick(1300, 0)

'''Opens Spotify and connects to Joe's Airpods.'''
@commands_on_off
@admin_commands
def open_Spotify():
    startfile(r"C:\Users\rcherveny\AppData\Roaming\Spotify\Spotify.exe")
    click_if_exists("PNG\\Bluetooth.png", region=(1657, 980, 1846, 1079))
    sleep(0.5)
    click_if_exists("PNG\\Show Bluetooth devices.png",
                    region=(1684, 856, 1904, 1044))
    sleep(1.5)
    connected = found('PNG\\Bluetooth connected.png', region=(694, 6, 1878, 921)) or found(
        'PNG\\Bluetooth connected 2.png', region=(694, 6, 1878, 921))
    if not connected:
        r = buttons("No devices connected. Try connecting?",
                    button_options=['Yes', 'No'])
        if r == 'Yes':
            search_and_click(
                'PNG\\Bluetooth not connected.png', region=(694, 6, 1878, 921))
            timeout = 20
            timeout_start = time()
            while time() < timeout_start + timeout:
                connected = found('PNG\\Bluetooth connected 2.png', region=(694, 6, 1878, 921)) or found(
                    'PNG\\Bluetooth connected.png', region=(694, 6, 1878, 921))
                click_if_exists('PNG\\connect bluetooth.png',
                                region=(694, 6, 1878, 921))
                if connected:
                    message("Bluetooth Connected")
                    click_if_exists('PNG\\exit bluetooth.png',
                                    region=(694, 6, 1878, 921))
                    return None
            if time() > timeout_start + timeout:
                message("Sorry, I couldn't connect any devices...")
                return None
        if r == 'No':
            message("No devices connected")
    if connected:
        message("Bluetooth Connected")
        click_if_exists('PNG\\exit bluetooth.png',
                        region=(1724, 0, 1886, 86))


'''Checks if the user is an admin and alerts them if they are not.'''
def admin_login():
    global admin
    chadmin = Users().check_if_admin()
    if chadmin:
        admin = True
        message("Login Successful")
    else:
        message("Login Failed")
        

def change_username_password():
    r = double_input("Please enter your current username and password.\n\nUsername", "Password")
    if r == None:
        user_settings()
    n = double_input("Please enter your new username and password.\n(Note: these credentials will need to be\nelevated to gain admin privileges)\n\nNew Username", "New Password")
    if n == None:
        user_settings()
    with open("TXT\\username_password.txt", "r") as file1, open("TXT\\admin_username_password.txt", "r") as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    with open("TXT\\username_password.txt", "w") as new_file, open("TXT\\admin_username_password.txt", "w") as new_file2:
        for line in lines1:
            if line.strip("\n") != r:
                new_file.write(line)
        for line in lines2:
            if line.strip("\n") != r:
                new_file2.write(line)


'''Gives multiple functions that deal with user accounts and privileges.'''
@commands_on_off
def user_settings():
    selection = buttons('', 'User Settings', button_options=[
                        'Add User', 'Make Admin', 'Admin Login', 'Change Username and Password'])
    selection_to_function = {
        'Add User': lambda: Users().add_user(),
        'Make Admin': admin_commands(lambda: Users().make_admin()),
        'Admin Login': admin_login,
        'Change Username and Password': change_username_password
    }
    if selection in selection_to_function:
        selection_to_function[selection]()


'''Gives access to the Engraving Guide and the BB5-S User Manual.'''
def engraving_documents():
    selection = buttons('', 'Engraving Documents', button_options=['Engraving Guide', 'BB-5S Manual'])
    selection_to_function = {
        'Engraving Guide': lambda: startfile(r'C:\Users\rcherveny\Documents\Code\MagicART-Hotkeys\PDF\Engraving Guide.pdf'),
        'BB-5S Manual': lambda: startfile(r'C:\Users\rcherveny\Documents\Code\MagicART-Hotkeys\PDF\magic-5s.pdf')
    }
    if selection in selection_to_function:
        selection_to_function[selection]()


'''Opens a toolbar with common automated tasks.'''
@commands_on_off
def open_toolbar():
    selection = buttons('', 'Toolbar', button_options=[
                        'Workday', 'ChatGPT', 'SKU Search', 'Engraving Documents', 'Spotify', 'Calculator', 'User Settings', 'Shutdown'])
    selection_to_function = {
        'Workday': lambda: webopen(f"https://www.myworkday.com/wday/authgwy/signetjewelers/login.htmld"),
        'ChatGPT': lambda: webopen(f"https://chat.openai.com/chat"),
        'SKU Search': lambda: startfile('sku_search.py'),
        'Engraving Documents': engraving_documents,
        'Spotify': open_Spotify,
        'Calculator': lambda: system("calc"),
        'User Settings': user_settings,
        'Shutdown': shut_down_computer
    }
    if selection in selection_to_function:
        selection_to_function[selection]()
    if selection == None:
        return


'''Toggles the keyboard commands on and off.'''
def toggle_keyboard_commands():
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


'''Terminates this program.'''
@commands_on_off
def end_program():
    r = buttons("Are you sure you want to end the program?", button_options=[
                'Yes', 'No'])
    if r == 'Yes':
        # end the program
        call(["taskkill", "/F", "/IM", "python.exe"])


'''Shuts down the computer.'''
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


# Key Bindings for Commands:
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


# Always Running Code:
start_checking_hotkeys()
register_hotkeys(bindings)
while awake:
    # pick a random phrase from the sleeplist to print, then sleep for 5 minutes and press f15
    sleep(60 * 5)
    print("\n" + random.choice(sleeplist) + "\n")
    hotkey("F15")


