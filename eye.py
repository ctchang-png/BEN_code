import numpy as np
import math
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pynput.keyboard import Key, Listener



 

class Eye:
    def __init__(self,):
        Window_Width = 320
        Window_Height = 240
        #Window/Canvas initialization
        self.window_width = Window_Width
        self.window_height = Window_Height
        self.window = self.create_animation_window()
        self.canvas = self.create_animation_canvas()
        self.refresh_rate = 0.010 # 10ms

        #Pupil
        self.xp = Window_Width/2            #pupil x pos
        self.yp = Window_Height/2           #pupil y pos
        self.rp = 30 #initial size          #pupil radius
        self.pupil = self.init_pupil()

        #Eyelids
        self.hu = Window_Height/8                   #upper eyelid height
        self.au = 0                                 #upper eyelid angle
        self.eyelid_u = self.init_eyelid_u()

        self.hl = Window_Height - Window_Height/8   #lower eyelid height      
        self.al = 0                                 #lower eyelid angle
        self.eyelid_l = self.init_eyelid_l()


    def create_animation_window(self):
        Window = tk.Tk()
        Window.title("Eye")
        Window.geometry(f'{self.window_width}x{self.window_height}')
        return Window

    def create_animation_canvas(self):
        canvas = tk.Canvas(self.window)
        canvas.configure(bg="Green")
        canvas.pack(fill="both", expand=True)
        return canvas

    def update_window(self):
        self.window.update()
        time.sleep(self.refresh_rate)


    def init_pupil(self):
        pupil = self.canvas.create_oval(self.xp-self.rp, self.yp-self.rp, 
            self.xp+self.rp, self.yp+self.rp,
            fill="Black", outline="Black", width=2)
        return pupil

    def move_pupil(self, xinc, yinc):
        self.canvas.move(self.pupil, xinc, yinc)


    def init_eyelid_u(self):
        #Initializes upper eyelid
        eyelid = self.canvas.create_polygon(0, 0, self.window_width, 0,
            self.window_width, self.hu, 0, self.hu,
            fill="Gray", outline="Gray", width=1)
        return eyelid

    def init_eyelid_l(self):
        #Initializes lower eyelid
        eyelid = self.canvas.create_polygon(0, self.window_height, 
            self.window_width, self.window_height,
            self.window_width, self.hl, 0, self.hl,
            fill="Gray", outline="Black", width=1)
        return eyelid

    def move_eyelids(self, hinc, ainc):
        #Moves both eyelids by a height increment and an angle increment
        #Will eventually want one for each eyelid, but this makes early testing easy with arrow keys
        self.hu += hinc
        self.hl -= hinc
        self.au += ainc
        self.al -= ainc

        #need to delete and redraw polygon to update
        self.canvas.delete(self.eyelid_u)
        self.eyelid_u = self.canvas.create_polygon(0, 0,
            self.window_width, 0,
            self.window_width, self.hu - (self.window_width/2)*math.tan(self.au*math.pi/180),
            0, self.hu + (self.window_width/2)*math.tan(self.au*math.pi/180),
            fill="Gray", outline="Black", width=1)

        self.canvas.delete(self.eyelid_l)
        self.eyelid_l = self.canvas.create_polygon(0, self.window_height,
            self.window_width, self.window_height,
            self.window_width, self.hl - (self.window_width/2)*math.tan(self.al*math.pi/180),
            0, self.hl + (self.window_width/2)*math.tan(self.al*math.pi/180),
            fill="Gray", outline="Black", width=1)

##################################




def get_keyboard_control(keys):
    xinc, yinc, hinc, ainc = 0, 0, 0, 0
    if "w" in keys:
        yinc -= 5
    if "s" in keys:
        yinc += 5
    if "a" in keys:
        xinc -= 5
    if "d" in keys:
        xinc += 5
    if "up" in keys:
        hinc += 5
    if "down" in keys:
        hinc -= 5
    if "left" in keys:
        ainc += 2
    if "right" in keys:
        ainc -= 2
    return xinc, yinc, hinc, ainc


def main():
    #Keypress driver stuff. keys keeps a set of held down keys so get_control
    #has a list to pull from
    keys = set()
    def on_press(key):
        try:
            k = key.char
        except:
            k = key.name
        if k in ['w','a','s','d','up','down','left','right']:
            keys.add(k)
    def on_release(key):
        if key == Key.esc:
            # Stop listener
            return False
        
        try:
            k = key.char
        except:
            k = key.name
        if k in ['w','a','s','d','up','down','left','right']:
            keys.remove(k)
        
    #Start non-blocking listener
    listener = Listener(
            on_press=on_press,
            on_release=on_release) 
    listener.start()

    #Create an instance of Eye
    eye = Eye()
    try:
        while True:
            xinc, yinc, hinc, ainc = get_keyboard_control(keys)
            eye.move_pupil(xinc, yinc)
            eye.move_eyelids(hinc, ainc)
            eye.update_window()
    except KeyboardInterrupt:
        eye.window.destroy()
        print("Program Terminated: Keyboard Interrupt")

if __name__ == "__main__":
    main()