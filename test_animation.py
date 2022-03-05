import numpy as np
from pynput.keyboard import Key, Listener
from eye import Eye

class Animator():
    def __init__(self):
        self.idle = True
        self.frame = 0
        self.control_array = None #4xn np array

    def get_control(self):
        if self.idle == True:
            return self.get_idle_control()
        control = self.control_array[:, self.frame]
        xinc, yinc, hinc, ainc = control[0], control[1], control[2], control[3]
        self.frame += 1
        #Default to idling if end of animation is reached
        if self.frame >= np.shape(self.control_array,)[1]:
            self.idle = True
            self.frame = 0
            self.control_array = None
            print("Animation complete! Begin Idling")
        return xinc, yinc, hinc, ainc

    def get_idle_control(self):
        #While idling make small motions to seem 'alive'
        #There's definitely more believable idle motions to improve this fn
        xinc = np.random.randint(-2, 3)
        yinc = np.random.randint(-2, 3)
        hinc = np.random.randint(-4, 5)
        ainc = np.random.randint(-1, 2)
        return xinc, yinc, hinc, ainc

    def do_animation(self, animation, name='unspecified'):
        if not self.idle:
            print("Animation already in progress...")
            return
        print("Beginning Animation: {}".format(name))
        self.idle = False
        self.frame = 0
        self.control_array = animation


def make_animation_random_x(n=500):
    xinc_vec = np.random.randint(-10, 10, n)
    yinc_vec = np.zeros(n)
    hinc_vec = np.zeros(n)
    ainc_vec = np.zeros(n)
    animation = np.vstack((xinc_vec, yinc_vec, hinc_vec, ainc_vec))
    return animation

def make_animation_random_y(n=500):
    yinc_vec = np.random.randint(-10, 10, n)
    xinc_vec = np.zeros(n)
    hinc_vec = np.zeros(n)
    ainc_vec = np.zeros(n)
    animation = np.vstack((xinc_vec, yinc_vec, hinc_vec, ainc_vec))
    return animation

def key2animation(k):
    if k == '1':
        animation = make_animation_random_x()
        name = 'random motion x'
    if k == '2':
        animation = make_animation_random_y()
        name = 'random motion y'
    return animation, name


def main():
    #############################################
    keys = set()
    def on_press(key):
        try:
            k = key.char
        except:
            k = key.name
        if k in ['1', '2']:
            keys.add(k)
    def on_release(key):
        if key == Key.esc:
            # Stop listener
            return False
        try:
            k = key.char
        except:
            k = key.name
        if k in ['1', '2']:
            keys.remove(k)
        
    #Start non-blocking listener
    listener = Listener(
            on_press=on_press,
            on_release=on_release) 
    listener.start()
    ##############################################
    #Create an instance of Eye
    eye = Eye()
    #Create an instance of Animation
    animator = Animator()
    try:
        while True:
            if len(keys) != 0:
                for k in keys:
                    animation, name = key2animation(k)
                    animator.do_animation(animation, name)
            xinc, yinc, hinc, ainc = animator.get_control()
            eye.move_pupil(xinc, yinc)
            eye.move_eyelids(hinc, ainc)
            eye.update_window()
    except KeyboardInterrupt:
        eye.window.destroy()
        print("Program Terminated: Keyboard Interrupt")

if __name__ == "__main__":
    #example idea for creating/running animations
    #feel free to play around with the implementation
    main()