import pyautogui
import time
import keyboard
from os import listdir, path, get_terminal_size


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        global dont_move
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        elapsed_time = end_time - start_time
        with open(f"TXT\\{func.__name__}.txt", "a") as f:
            t = (f"{elapsed_time: .4f}")
            f.write(t + "\n")
        with open(f"TXT\\{func.__name__}.txt", "r") as f:
            numbers = []
            for line in f:
                try:
                    number = float(line.strip())
                    numbers.append(number)
                except ValueError:
                    pass
            while dont_move:
                time.sleep(0.1)
            if not dont_move:
                try:
                    average = sum(numbers) / len(numbers)
                    print(
                        f"\n{func.__name__} took {elapsed_time:.4f} sec to complete.")
                    print(
                        f"The average time for {func.__name__} is:{average}\n")
                except ZeroDivisionError as z:
                    pass
        with open(f"TXT\\average_{func.__name__}.txt", "w") as f:
            average = str(average)
            f.write(average)
        return result
    return wrapper


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
        found_it = pyautogui.locateOnScreen(image_name, region=region, confidence=confidence)
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
    x, y = found_it[0], found_it[1]
    return True
    return x, y

def found(image_name, confidence = .8, region = (0, 0, 1920, 1080)):
    result = bool(pyautogui.locateOnScreen(image_name, region=region, confidence=confidence))
    if result:
        return bool(pyautogui.locateOnScreen(image_name, region=region, confidence=confidence))

def progress_bar(text, average_time):
    global dont_move
    start_time = time()
    progress = 0
    term_width, _ = get_terminal_size(fallback=(80, 24))
    bar_width = term_width - len(f"[ 100% ] ")
    print(text)
    while progress <= 100:
        dont_move = True
        bar = "[" + "=" * int(progress / (100 / (bar_width))) + " " * \
            (bar_width - int(progress / (100 / (bar_width)))) + "]"
        print(f"\r{bar} {progress}%", end="", flush=True)
        progress += 1
        elapsed_time = time() - start_time
        remaining_time = average_time - elapsed_time
        if remaining_time > 0 and progress < 100:
            sleep_time = remaining_time / (100 - progress)
            time.sleep(sleep_time)
    dont_move = False

def get_average_time(filename):
    with open(filename, "r") as f:
        file_content = f.read().strip()
        if path.getsize(filename) == 0:
            return
        else:
            return float(file_content)

if __name__ == "__main__":
    # test some stuff
    center_mouse()

#did it work?
