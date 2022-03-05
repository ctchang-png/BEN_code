import numpy as np
from pynput.keyboard import Key, Listener
from eye import Eye

class Animator():
    def __init__(self):
        self.idle = True
        self.frame = 0
        self.idle_frame = 0
        self.idle_array = make_idle_array()
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
        control = self.idle_array[:, self.idle_frame]
        xinc, yinc, hinc, ainc = control[0], control[1], control[2], control[3]
        self.idle_frame = (self.idle_frame + 1) % np.shape(self.idle_array)[1]
        return xinc, yinc, hinc, ainc

    def do_animation(self, animation, name='unspecified'):
        if not self.idle:
            print("Animation already in progress...")
            return
        print("Beginning Animation: {}".format(name))
        self.idle = False
        self.frame = 0
        self.control_array = animation


def make_idle_array():
    n = 40
    xinc_max = 1
    xinc_vec = np.concatenate([np.linspace(0,xinc_max,int(n/4)), np.linspace(xinc_max,0,int(n/4)), np.linspace(0,-xinc_max,int(n/4)), np.linspace(-xinc_max,0,int(n/4))])
    yinc_vec = np.zeros(n)
    hinc_max = .1
    hinc_vec = np.concatenate([np.linspace(0,hinc_max,int(n/4)), np.linspace(hinc_max,0,int(n/4)), 
        np.linspace(0,-hinc_max,int(n/4)), np.linspace(-hinc_max,0,int(n/4))])
    ainc_vec = np.zeros(n)
    idle_array = np.vstack((xinc_vec, yinc_vec, hinc_vec, ainc_vec))
    return idle_array


def make_animation_random_x(n=200):
    xinc_vec = np.random.randint(-10, 11, n)
    yinc_vec = np.zeros(n)
    hinc_vec = np.zeros(n)
    ainc_vec = np.zeros(n)
    animation = np.vstack((xinc_vec, yinc_vec, hinc_vec, ainc_vec))
    return animation

def make_animation_random_y(n=200):
    yinc_vec = np.random.randint(-10, 11, n)
    xinc_vec = np.zeros(n)
    hinc_vec = np.zeros(n)
    ainc_vec = np.zeros(n)
    animation = np.vstack((xinc_vec, yinc_vec, hinc_vec, ainc_vec))
    return animation

def make_animation_blink(eye):
    move_frames = 5
    hold_frames = 2
    a0 = eye.au
    h0 = eye.hu
    hmax = Eye.Window_Height/2
    xinc_vec = np.zeros(2*move_frames + hold_frames)
    yinc_vec = np.zeros(2*move_frames + hold_frames)
    hinc_vec = np.concatenate([np.ones(move_frames)*(hmax-h0)/(move_frames),
                               np.zeros(hold_frames),
                               np.ones(move_frames)*(h0-hmax)/(move_frames)])
    ainc_vec = np.concatenate([-1*np.ones(move_frames)*a0/(move_frames),
                               np.zeros(hold_frames),
                               np.ones(move_frames)*a0*(move_frames)])
    animation = np.vstack((xinc_vec, yinc_vec, hinc_vec, ainc_vec))
    return animation

def key2animation(k, eye):
    if k == '1':
        animation = make_animation_random_x()
        name = 'random motion x'
    if k == '2':
        animation = make_animation_random_y()
        name = 'random motion y'
    if k == 'space':
        animation = make_animation_blink(eye)
        name = 'blink'
    return animation, name


def main():
    #############################################
    keys = set()
    def on_press(key):
        try:
            k = key.char
        except:
            k = key.name
        if k in ['1', '2', 'space']:
            keys.add(k)
    def on_release(key):
        if key == Key.esc:
            # Stop listener
            return False
        try:
            k = key.char
        except:
            k = key.name
        if k in ['1', '2', 'space']:
            keys.remove(k)
        
    #Start non-blocking listener
    listener = Listener(
            on_press=on_press,
            on_release=on_release) 
    listener.start()
    ##############################################
    #Create an instance of Eye
    eyeL = Eye("Left Eye")
    eyeR = Eye("Right Eye")
    #Create an instance of Animation
    animator = Animator()
    try:
        while True:
            if len(keys) != 0:
                k = list(keys)[0]
                animation, name = key2animation(k, eyeL)
                animator.do_animation(animation, name)
            xinc, yinc, hinc, ainc = animator.get_control()
            eyeL.move_pupil(xinc, yinc)
            eyeL.move_eyelids(hinc, ainc)
            eyeR.move_pupil(xinc, yinc)
            eyeR.move_eyelids(hinc, ainc)
            
            eyeL.update_window()
            eyeR.update_window()
    except KeyboardInterrupt:
        eyeL.window.destroy()
        eyeR.window.destroy()
        print("Program Terminated: Keyboard Interrupt")

if __name__ == "__main__":
    #example idea for creating/running animations
    #feel free to play around with the implementation
    main()