from time import *
import shutil
from os import path


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        elapsed_time = end_time - start_time
        print(f"\n{func.__name__} took {elapsed_time:.4f} seconds to complete.")
        with open(f"{func.__name__}.txt", "a") as f:
            t = (f"{elapsed_time: .4f}")
            f.write("\n" + t)
        with open(f"{func.__name__}.txt", "r") as f:
            numbers = []
            for line in f:
                try:
                    number = float(line.strip())
                    numbers.append(number)
                except ValueError:
                    pass
            try:
                average = sum(numbers) / len(numbers)
                print(f"\nThe average time for {func.__name__} is:", average)
            except ZeroDivisionError as z:
                pass
        with open(f"average_{func.__name__}.txt", "w") as f:
            average = str(average)
            f.write(average)
        return result
    return wrapper


def progress_bar(filename):
    progress = 0
    term_width, _ = shutil.get_terminal_size(fallback=(80, 24))
    bar_width = term_width - len(f"[ 100% ] ")
    with open(filename, "r") as f:
        file_content = f.read().strip()
        if path.getsize(filename) == 0:
            average_time = 10.0  # set a default value if the file is empty
        else:
            average_time = float(file_content)
        total_iterations = int(average_time * 10)  # Calculate total iterations
        sleep_time = int(average_time / (total_iterations / 2))
        if sleep_time < 0:
            return None
        while progress <= 100:
            bar = "[" + "=" * int(progress / (100 / (bar_width))) + " " * (bar_width - int(progress / (100 / (bar_width)))) + "]"
            print(f"\r{bar} {progress}%", end="", flush=True)
            progress += 2
            sleep(0.1)

progress_bar("time.txt")