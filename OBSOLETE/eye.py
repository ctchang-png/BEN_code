import numpy as np
import math
import time
import tkinter as tk
from pynput.keyboard import Key, Listener



 

class Eye:
    Window_Width = 320
    Window_Height = 240

    def __init__(self, name):
        #Window/Canvas initialization
        self.name = name
        self.window_width = Eye.Window_Width
        self.window_height = Eye.Window_Height
        self.window = self.create_animation_window()
        self.canvas = self.create_animation_canvas()
        self.refresh_rate = 0.010 # 10ms

        #Pupil
        self.xp = Eye.Window_Width/2            #pupil x pos
        self.yp = Eye.Window_Height/2           #pupil y pos
        self.rp = 30 #initial size          #pupil radius
        self.set_pupil(self.xp, self.yp)

        #Eyelids
        self.hu = Eye.Window_Height/8                   #upper eyelid height
        self.au = 0                                 #upper eyelid angle
        self.eyelid_u = None
        self.set_eyelid_u(self.hu, self.au)

        self.hl = Eye.Window_Height - Eye.Window_Height/8   #lower eyelid height      
        self.al = 0                                 #lower eyelid angle
        self.eyelid_l = None
        self.set_eyelid_l(self.hl, self.al)


    def create_animation_window(self):
        Window = tk.Tk()
        Window.title(self.name)
        Window.geometry(f'{self.window_width}x{self.window_height}')
        return Window

    def create_animation_canvas(self):
        canvas = tk.Canvas(self.window)
        canvas.configure(bg="Green")
        canvas.pack(fill="both", expand=True)
        return canvas

    def update_window(self):
        self.window.update()
        #overlay grid
        time.sleep(self.refresh_rate)


    def set_pupil(self, x, y):
        self.xp = x
        self.yp = y
        self.pupil = self.canvas.create_oval(x-self.rp, y-self.rp, 
            x+self.rp, y+self.rp,
            fill="Black", outline="Black", width=2)

    def move_pupil(self, xinc, yinc):
        self.xp += xinc
        self.yp += yinc
        self.canvas.move(self.pupil, xinc, yinc)


    def set_eyelid_u(self, hu, au):
        self.hu = hu
        self.au = au
        if self.eyelid_u != None:
            self.canvas.delete(self.eyelid_u)
        self.eyelid_u = self.canvas.create_polygon(0, 0,
            self.window_width, 0,
            self.window_width, self.hu - (self.window_width/2)*math.tan(self.au*math.pi/180),
            0, self.hu + (self.window_width/2)*math.tan(self.au*math.pi/180),
            fill="Gray", outline="Black", width=1)


    def set_eyelid_l(self, hl, al):
        self.hl = hl
        self.al = al
        if self.eyelid_l != None:
            self.canvas.delete(self.eyelid_l)
        self.eyelid_l = self.canvas.create_polygon(0, self.window_height,
            self.window_width, self.window_height,
            self.window_width, self.hl - (self.window_width/2)*math.tan(self.al*math.pi/180),
            0, self.hl + (self.window_width/2)*math.tan(self.al*math.pi/180),
            fill="Gray", outline="Black", width=1)

    def move_eyelids(self, hinc_u, hinc_l, ainc_u, ainc_l):
        #Moves both eyelids by a height increment and an angle increment
        #Will eventually want one for each eyelid, but this makes early testing easy with arrow keys
        self.hu += hinc_u
        self.hl -= hinc_l
        self.au += ainc_u
        self.al -= ainc_l

        self.set_eyelid_u(self.hu, self.au)
        self.set_eyelid_l(self.hl, self.al)



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
    eyeL = Eye("eyeL")
    eyeR = Eye("eyeR")
    try:
        while True:
            xinc, yinc, hinc, ainc = get_keyboard_control(keys)
            eyeL.move_pupil(xinc, yinc)
            eyeL.move_eyelids(hinc, ainc)
            eyeR.move_pupil(xinc, yinc)
            eyeR.move_eyelids(hinc, -ainc)
            eyeL.update_window()
            eyeR.update_window()
    except KeyboardInterrupt:
        eyeL.window.destroy()
        eyeR.window.destroy()
        print("Program Terminated: Keyboard Interrupt")

if __name__ == "__main__":
    main()