import tkinter as tk
from tkinter import *
from typing import Optional, Tuple
from PIL import Image, ImageTk

'''
MESSAGE_BOXES V.1.0.0
CURRENTLY IN DEVELOPMENT
CURRENTLY IN BETA TESTING
'''


class MessageBox(object):
    #use tkinter to create a window with a label and a button, that returns the text of the button pressed

    def __init__(self, text, title, button_options, win_background="white", Lbg="white", Lfg="black", justify=LEFT, font="consolas", btnfont="consolas"):
        self.value = None
        self.root = None
        self.text = text
        self.title = title
        self.button_options = button_options
        self.win_background = win_background
        self.Lbg = Lbg
        self.Lfg = Lfg
        self.justify = justify
        self.font = font
        self.btnfont = btnfont

    def center(self):
        self.root.update_idletasks()
        width, height = (self.root.winfo_width(), self.root.winfo_height())
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2) - 50 # 50 is for the awkwardness of the taskbar
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def message(self):
        self.root = tk.Tk()
        self.root['background'] = self.win_background
        self.root.attributes("-topmost", True)
        self.root.after(1, lambda: self.root.focus_force())
        self.root.title(self.title)
        Label(self.root, text=self.text, justify=self.justify, bg=self.Lbg, fg=self.Lfg, font=self.font).pack(padx=25, pady=10)
        tk.Button(self.root, text = self.button_options, font=self.btnfont, command = self.finish).pack(side=LEFT, padx=25, pady=10)
        self.root.bind("<Return>", lambda event: self.finish())
        tk.Button(self.root, text = "Cancel", font=self.btnfont, command = self.root.destroy).pack(side=RIGHT, padx=25, pady=10)
        self.center()
        self.root.mainloop()
        return self.value

    def finish(self):
        self.value = self.button_options
        self.root.destroy()

class ButtonBox(object):
    '''
    A message box that returns the text of the button pressed. Can have as many buttons as you want. 
    self, text, title, button_options, win_background="white", Lbg="white", Lfg="black", font="consolas", btnfont="consolas"
    '''
    def __init__(self, text, title, button_options, win_background="white", Lbg="white", Lfg="black", font="consolas", btnfont="consolas", highlight="light grey"):
        self.title = title
        self.text = text
        self.button_options = button_options
        self.font = font
        self.btnfont = btnfont
        self.win_background = win_background
        self.Lbg = Lbg
        self.Lfg = Lfg
        self.selected_button = None
        self.selected_button_index = 0
        self.highlight = highlight
    def center(self):
        self.root.update_idletasks()
        width, height = (self.root.winfo_width(), self.root.winfo_height())
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2) - 50 # 50 is for the awkwardness of the taskbar
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    def highlight_button(self, index):
        for i, button in enumerate(self.buttons):
            if i == index:
                button.config(bg=self.highlight)
            else:
                button.config(bg=self.Lbg, fg=self.Lfg)
    def move_highlighted_button_left(self):
        if self.selected_button_index > 0:
            self.selected_button_index -= 1
            self.highlight_button(self.selected_button_index)
    def move_highlighted_button_right(self):
        if self.selected_button_index < len(self.button_options) - 1:
            self.selected_button_index += 1
            self.highlight_button(self.selected_button_index)
    def options(self):
        self.root = tk.Tk()
        self.root['background'] = self.win_background
        self.root.attributes("-topmost", True)
        self.root.focus_force() # just in case
        self.root.title(self.title)
        Label(self.root, text=self.text, justify=CENTER, bg=self.Lbg, fg=self.Lfg, font=self.font).grid(columnspan=len(self.button_options), padx=25, pady=10)
        self.buttons = []
        if type(self.button_options) == str:
            self.button_options = [self.button_options]
        if type(self.button_options) == list or tuple:
            for index, text in enumerate(self.button_options):
                if index < 10:
                    button = tk.Button(self.root, text=text, font=self.btnfont, command=lambda index=index: self.finish(self.button_options[index]))
                    button.grid(row=3, column=index, padx=25, pady=10)
                    self.buttons.append(button)
                    self.root.bind(str(index + 1), lambda event, index=index: self.finish(self.button_options[index]))
            tk.Button(self.root, text="Cancel", font=self.btnfont, command=lambda: self.finish(None)).grid(row=4, columnspan=len(self.button_options), padx=25, pady=10)
            self.root.bind("<Escape>", lambda event: self.finish(None))
            self.root.bind("<Return>", lambda event: self.finish(self.button_options[self.selected_button_index]))

        # Bind arrow keys to move highlighted button and Enter key to select highlighted button
        self.root.bind("<Left>", lambda event: self.move_highlighted_button_left())
        self.root.bind("<Right>", lambda event: self.move_highlighted_button_right())

        self.highlight_button(0)   
        self.center()
        self.root.mainloop()
        return self.value

    def finish(self, value):
            self.value = value
            self.root.destroy()

class InputBox(object):
    '''
    A message box that returns the text of the entry.
    
    '''
    def __init__(self, text, title = '', show = None, win_background="white", Lbg="white", Ebg="white", Lfg="black", font="consolas", entfont="consolas", btnfont="consolas"):
        self.value = None
        self.root = None
        self.text = text
        self.title = title
        self.show = show
        self.result = None
        self.Lbg = Lbg
        self.win_background = win_background
        self.Ebg = Ebg
        self.Lfg = Lfg
        self.font = font
        self.entfont = entfont
        self.btnfont = btnfont

    def center(self):
        self.root.update_idletasks()
        width, height = (self.root.winfo_width(), self.root.winfo_height())
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2) - 50 # 50 is for the awkwardness of the taskbar
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def return_entry(self):
        self.result = self.entry.get()
        self.root.destroy()

    def input(self):
        self.root = tk.Tk()
        self.root['background'] = self.win_background
        self.root.attributes("-topmost", True)
        self.root.focus_force() # just in case
        self.root.title(self.title)
        Label(self.root, text=self.text, bg=self.Lbg, fg=self.Lfg, font=self.font).grid(columnspan = 2)
        self.entry = Entry(self.root, show=self.show, bg=self.Ebg, font=self.entfont)
        self.entry.focus_force()
        self.entry.grid(columnspan = 2)
        self.ok_button = Button(self.root, text = "OK", font=self.btnfont, command = self.return_entry)
        self.ok_button.grid(row=3, column=0, padx=25, pady=10)
        Button(self.root, text = "Cancel", font=self.btnfont, command = lambda: self.root.destroy()).grid(row=3, column=1, padx=25, pady=10)
        self.center()
        self.root.bind("<Return>", lambda e = None: self.return_entry())
        self.root.bind("<Escape>", lambda e = None: self.root.destroy())
        self.root.mainloop()

class DoubleInputBox(object):
    '''
    A message box that allows for two seperate text entries, with two different labels. Wil return ("text_input1", "text_input2").
    
    '''
    def __init__(self, label1: str, label2: str, title: Optional[str] = None, mask1: Optional[str] = None,
                 mask2: Optional[str] = None, win_background: str = "white", label_background1: str = "white",
                 label_forground1: str = "black", label_background2: str = "white", label_forground2: str = "black",
                 entry_background1: str = "white", entry_background2: str = "white", font1: str = "consolas",
                 font2: str = "consolas", entfont1: str = "consolas", entfont2: str = "consolas", btnfont: str = "consolas"):
        '''
        Parameters:
        - label1: string label for the first text entry box
        - label2: string label for the second text entry box
        - title: optional string for the window title
        - mask1: optional string to control whether characters in the first text entry box are shown as they are typed
        - mask2: optional string to control whether characters in the second text entry box are shown as they are typed
        - win_background: string color code for the window background
        - label_background1: string color code for the background of the first label
        - label_forground1: string color code for the foreground (text) of the first label
        - label_background2: string color code for the background of the second label
        - label_forground2: string color code for the foreground (text) of the second label
        - entry_background1: string color code for the background of the first text entry box
        - entry_background2: string color code for the background of the second text entry box
        - font1: string specifying the font for the first label and first text entry box
        - font2: string specifying the font for the second label and second text entry box
        - entfont1: string specifying the font for the text in the first text entry box
        - entfont2: string specifying the font for the text in the second text entry box
        - btnfont: string specifying the font for the OK and Cancel buttons
        '''        
        self.value = None
        self.root = None
        self.label1 = label1
        self.label2 = label2
        self.title = title
        self.mask1 = mask1
        self.mask2 = mask2
        self.result = None
        self.label_background1 = label_background1
        self.label_background2 = label_background2
        self.win_background = win_background
        self.entry_background1 = entry_background1
        self.entry_background2 = entry_background2
        self.label_forground1 = label_forground1
        self.label_forground2 = label_forground2
        self.font1 = font1
        self.font2 = font2
        self.btnfont = btnfont
        self.entfont1 = entfont1
        self.entfont2 = entfont2

    def center(self) -> None:
        self.root.update_idletasks()
        width, height = (self.root.winfo_width(), self.root.winfo_height())
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2) - 50 # 50 is for the awkwardness of the taskbar
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def return_entry(self) -> None:
        self.result = self.entry1.get()
        self.result2 = self.entry2.get()
        self.root.destroy()

    def input(self) -> Tuple[str, str]:
        self.root = tk.Tk()
        self.root['background'] = self.win_background
        self.root.attributes("-topmost", True)
        self.root.focus_force() # just in case
        self.root.title(self.title)
        Label(self.root, text=self.label1, bg=self.label_background1, fg=self.label_forground1, font=self.font1).grid(columnspan = 2)
        self.entry1 = Entry(self.root, show=self.mask1, bg=self.entry_background1, font=self.entfont1)
        self.entry1.focus_force()
        self.entry1.grid(columnspan = 2)
        Label(self.root, text=self.label2, bg=self.label_background2, fg=self.label_forground2, font=self.font2).grid(columnspan = 2)
        self.entry2 = Entry(self.root, show=self.mask2, bg=self.entry_background2, font=self.entfont2)
        self.entry2.grid(columnspan = 2)
        self.ok_button = Button(self.root, text = "OK", font=self.btnfont, command = self.return_entry)
        self.ok_button.grid(row=4, column=0, padx=25, pady=10)
        Button(self.root, text = "Cancel", font=self.btnfont, command = lambda: self.root.destroy()).grid(row=4, column=1, padx=25, pady=10)
        self.center()
        self.root.bind("<Return>", lambda e = None: self.return_entry())
        self.root.bind("<Escape>", lambda e = None: self.root.destroy())
        self.root.mainloop()

loading_permissions = False

class LoadingBar(object):
    global loading_permissions
    def __init__(self, text="DO NOT MOVE MOUSE", gif_path="C:\\Program Files\\Python\\Lib\\bot_and_boxes\\loading wheel.gif", speed=50, xscale=1, yscale=1, xpos=0, ypos=-50):
            self.root = None
            self.text = text
            self.gif_path = gif_path
            self.speed = speed
            self.xscale = xscale
            self.yscale = yscale
            self.xpos = xpos
            self.ypos = ypos
            
            

    def center(self):
        self.root.update_idletasks()
        width, height = (self.root.winfo_width(), self.root.winfo_height())
        x = (self.root.winfo_screenwidth() // 2) - (width // 2) + self.xpos
        y = (self.root.winfo_screenheight() // 2) - (height // 2) + self.ypos
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def update_frame(self, frame_number):
        global loading_permissions
        if self.root and self.loading_label:
            self.loading_label.config(image=self.frames[frame_number])
            if loading_permissions:
                self.root.after(self.speed, self.update_frame, (frame_number + 1) % len(self.frames))
            else:
                self.loading_label.destroy()
                self.root.destroy()

    
    def loading_screen(self):
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root['bg'] = '#FAF3F2'
        self.root.overrideredirect(1)
        self.image = Image.open(self.gif_path)
        self.frames = []
        for frame in range(0, self.image.n_frames):
            self.image.seek(frame)
            resized_image = self.image.resize((int(self.image.size[0] * self.xscale), int(self.image.size[1] * self.yscale)))
            self.frames.append(ImageTk.PhotoImage(resized_image))
        self.information_label = Label(self.root, text=self.text, font=("Arial", 15), bg="#FAF3F2")
        self.information_label.grid(row=0, column=0, padx=10, pady=10)
        self.loading_label = Label(self.root, border=0, highlightthickness=0, bg="#FAF3F2")
        self.loading_label.grid(row=3, column=0, padx=10, pady=10)
        self.update_frame(0)
        self.center()
        self.root.mainloop()


def message(text=None, title=None, button_options="Ok", win_background="white", Lbg="white", Lfg="black"):
    # text: the text to be displayed, title: the title of the window, button_options: the text displayed on the buttons, 
    # win_background: the background color of the window (name of color or HEX), Lbg: the background color of the text (name of color or HEX),
    # Lfg: the foreground color of the text (name of color or HEX)
    msg = MessageBox(text=text, title=title, button_options=button_options, win_background=win_background, Lbg=Lbg, Lfg=Lfg).message()
    return msg

def buttons(text=None, title=None, button_options=["Ok"], win_background="white", Lbg="white", Lfg="black"):
    # text: the text to be displayed, title: the title of the window, button_options: the text displayed on the buttons, 
    # win_background: the background color of the window (name of color or HEX), Lbg: the background color of the text (name of color or HEX),
    # Lfg: the foreground color of the text (name of color or HEX)
    bttn = ButtonBox(text=text, title=title, button_options=button_options, win_background=win_background, Lbg=Lbg, Lfg=Lfg).options()
    return bttn

def input(text=None, title=None, show=None, win_background="white", Lbg="white", Ebg="white", Lfg="black"):
    # text: the text to be displayed, title: the title of the window, show: what other character the text should be displayed 
    # as(*, #, etc), win_background: the background color of the window (name of color or HEX), Lbg: the background color of the text 
    # (name of color or HEX),Lfg: the foreground color of the text (name of color or HEX)
    box = InputBox(text=text, title=title, show=show, win_background=win_background, Lbg=Lbg, Lfg=Lfg)
    box.input()
    return box.result

def double_input(label1=None, label2=None, title=None, mask1=None, mask2="*",
                 win_background="white", label_background1="white", label_forground1="black",
                 label_background2="white", label_forground2="black", entry_background1="white",
                 entry_background2="white"):
    # text: the text to be displayed, title: the title of the window, show: what other character the text should be displayed 
    # as(*, #, etc), win_background: the background color of the window (name of color or HEX), Lbg: the background color of the text 
    # (name of color or HEX),Lfg: the foreground color of the text (name of color or HEX)
    box = DoubleInputBox(label1=label1, label2=label2, title=title, mask1=mask1,
                         mask2=mask2, win_background=win_background,
                         label_background1=label_background1, label_forground1=label_forground1,
                         label_background2=label_background2, label_forground2=label_forground2,
                         entry_background1=entry_background1, entry_background2=entry_background2)
    box.input()
    try:
        final_result = box.result + " " + box.result2
    except TypeError as e:
        print(e)
        final_result = None
    return final_result

def loading_bar(text="DO NOT MOVE MOUSE", gif_path="C:\\Program Files\\Python\\Lib\\bot_and_boxes\\loading wheel.gif", speed=50, xscale=1, yscale=1, xpos=0, ypos=-50):
    global loading_permissions
    loading_permissions = True
    try:
        LoadingBar(text=text, gif_path=gif_path, speed=speed, xscale=xscale, yscale=yscale, xpos=xpos, ypos=ypos).loading_screen()
    except tk.TclError:
        pass

def loading_bar_done():
    global loading_permissions
    loading_permissions = False
