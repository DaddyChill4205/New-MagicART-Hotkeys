import pyautogui
import time
import keyboard
from os import listdir

# pyautogui.displayMousePosition()

def bclick(x, y):
    original_position = pyautogui.position()
    pyautogui.click(x=x, y=y)
    pyautogui.moveTo(*original_position)
    
def center_mouse():
    x, y = pyautogui.size()
    pyautogui.moveTo(int(x / 2), int(y / 2))

def show_desktop():
    # TODO: update this, will not work across different computers
    x, y = 1918, 1079
    bclick(x=x, y=y)

# keyboard.is_pressed('q') # returns True is q is pressed
# pyautogui.locateOnScreen(image_name) # returns position of the image
# if it's not there then just return false

def hold_key(key, hold_time):
    start = time.time()
    while time.time() - start < hold_time:
        pyautogui.keyDown(key)

def hover_over(image_name, confidence = .8, region = (0, 0, 1920, 1080)):
    '''
    Moves the mouse over the specified image without clicking.
    '''
    found_it = pyautogui.locateOnScreen(image_name, region=region, confidence=confidence)
    if found_it:
        x, y = found_it[0], found_it[1]
        pyautogui.moveTo(x, y)
    else:
        print("Couldn't find anything to hover over.")

def search_and_click(image_name, double = False, go_back = True, below = 0, timeout=3, confidence = .8, region = (0, 0, 1920, 1080)):
    original_position = pyautogui.position()
    found_it = pyautogui.locateOnScreen(image_name, region=region, confidence=confidence)
    start = time.time()
    while found_it == None:
        if time.time() - start >= timeout:
            return False
        print("looking for", image_name)
        found_it = pyautogui.locateOnScreen(image_name, region=region, confidence=confidence)
    print("found", image_name)
    x, y = found_it[0], found_it[1]
    pyautogui.moveTo(x, y + below)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    if double:
        pyautogui.click(x=x, y=y + below)
    if go_back:
        pyautogui.moveTo(*original_position)
    return True

def click_if_exists(image_name, double = False, go_back = True, below = 0, confidence = .8, region = (0, 0, 1920, 1080)):
    original_position = pyautogui.position()
    found_it = pyautogui.locateOnScreen(image_name, region=region, confidence=confidence)
    if found_it != None:
        print("found", image_name)
        x, y = found_it[0], found_it[1]
        pyautogui.moveTo(x, y + below)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.1)
        if double:
            pyautogui.click(x=x, y=y + below)
        if go_back:
            pyautogui.moveTo(*original_position)
        return True
    return False

def find(image_name, confidence = .8, timeout = 10, region = (0, 0, 1920, 1080)):
    found_it = pyautogui.locateOnScreen(image_name, region=region, confidence=confidence)
    start = time.time()
    while found_it == None:
        if time.time() - start > timeout:
            return False
            print(f"Timed out, spend too much time looking for {image_name}.")
        found_it = pyautogui.locateOnScreen(image_name, region=region, confidence=confidence)
        print("looking for {0}...".format(image_name))
    x, y = found_it[0], found_it[1]
    print("found", image_name)
    return True
    return x, y

def found(image_name, confidence = .8, region = (0, 0, 1920, 1080)):
    result = bool(pyautogui.locateOnScreen(image_name, region=region, confidence=confidence))
    if result:
        print("found {0}".format(image_name))
    else:
        print("didn't find {0}".format(image_name))
    return bool(pyautogui.locateOnScreen(image_name, region=region, confidence=confidence))

if __name__ == "__main__":
    # test some stuff
    center_mouse()
