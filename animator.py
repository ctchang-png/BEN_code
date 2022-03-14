import numpy as np
import math
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
        try:
            control = self.control_array[:, self.frame]
        except:
            print("Control array empty! Automatically inputting zero control")
            control = np.zeros(12)
        self.frame += 1
        #Default to idling if end of animation is reached
        if self.frame >= np.shape(self.control_array,)[1]:
            self.idle = True
            self.frame = 0
            self.control_array = None
            print("Animation complete! Begin Idling")
        return control

    def get_idle_control(self):
        #While idling make small motions to seem 'alive'
        #There's definitely more believable idle motions to improve this fn
        control = self.idle_array[:, self.idle_frame]
        self.idle_frame = (self.idle_frame + 1) % np.shape(self.idle_array)[1]
        return control

    def do_animation(self, animation, name='unspecified animation'):
        if not self.idle:
            print("Animation already in progress...")
            return
        print("Beginning Animation: {}".format(name))
        self.idle = False
        self.frame = 0
        self.control_array = animation


def make_idle_array():
    #Seems like a solid start but pupil y and eyelid motion could use work
    #Maybe consider gazing at random locations rather than consistent motion
    n = 40
    xinc_max = 1
    xinc_vec = np.concatenate([np.linspace(0,xinc_max,int(n/4)), np.linspace(xinc_max,0,int(n/4)), 
                               np.linspace(0,-xinc_max,int(n/4)), np.linspace(-xinc_max,0,int(n/4))])
    yinc_max = .1
    yinc_vec = np.concatenate([np.linspace(0,yinc_max,int(n/4)), np.linspace(yinc_max,0,int(n/4)), 
                               np.linspace(0,-yinc_max,int(n/4)), np.linspace(-yinc_max,0,int(n/4))])
    hinc_max = .1
    hinc_vec = np.concatenate([np.linspace(0,hinc_max,int(n/4)), np.linspace(hinc_max,0,int(n/4)), 
        np.linspace(0,-hinc_max,int(n/4)), np.linspace(-hinc_max,0,int(n/4))])
    ainc_vec = np.zeros(n)
    idle_array = np.vstack((xinc_vec, yinc_vec, hinc_vec, hinc_vec, ainc_vec, ainc_vec,
                            xinc_vec, yinc_vec, hinc_vec, hinc_vec, ainc_vec, ainc_vec))
    return idle_array


def make_animation_random_x(n=200):
    xinc_vec = np.random.randint(-10, 11, n)
    yinc_vec = np.zeros(n)
    hinc_vec = np.zeros(n)
    ainc_vec = np.zeros(n)
    animation = np.vstack((xinc_vec, yinc_vec, hinc_vec, hinc_vec, ainc_vec, ainc_vec,
                           xinc_vec, yinc_vec, hinc_vec, hinc_vec, ainc_vec, ainc_vec))
    return animation

def make_animation_random_y(n=200):
    yinc_vec = np.random.randint(-10, 11, n)
    xinc_vec = np.zeros(n)
    hinc_vec = np.zeros(n)
    ainc_vec = np.zeros(n)
    animation = np.vstack((xinc_vec, yinc_vec, hinc_vec, hinc_vec, ainc_vec, ainc_vec,
                           xinc_vec, yinc_vec, hinc_vec, hinc_vec, ainc_vec, ainc_vec))
    return animation

def make_animation_blink(eyeL, eyeR):
    move_frames = 5
    hold_frames = 2
    a0_UL = eyeL.au
    a0_LL = eyeL.al
    a0_UR = eyeR.au
    a0_LR = eyeR.au
    h0_UL = eyeL.hu
    h0_LL = eyeL.hl
    h0_UR = eyeR.hu
    h0_LR = eyeR.hl

    hmax = Eye.Window_Height/2
    xinc_vec = np.zeros(2*move_frames + hold_frames)
    yinc_vec = np.zeros(2*move_frames + hold_frames)
    hinc_UL_vec = np.concatenate([np.ones(move_frames)*(hmax-h0_UL)/(move_frames),
                               np.zeros(hold_frames),
                               np.ones(move_frames)*(h0_UL-hmax)/(move_frames)])
    hinc_LL_vec = np.concatenate([-1*np.ones(move_frames)*(hmax-h0_LL)/(move_frames),
                               np.zeros(hold_frames),
                               -1*np.ones(move_frames)*(h0_LL-hmax)/(move_frames)])
    hinc_UR_vec = np.concatenate([np.ones(move_frames)*(hmax-h0_UR)/(move_frames),
                               np.zeros(hold_frames),
                               np.ones(move_frames)*(h0_UR-hmax)/(move_frames)])
    hinc_LR_vec = np.concatenate([-1*np.ones(move_frames)*(hmax-h0_LR)/(move_frames),
                               np.zeros(hold_frames),
                               -1*np.ones(move_frames)*(h0_LR-hmax)/(move_frames)])
    ainc_UL_vec = np.concatenate([-1*np.ones(move_frames)*a0_UL/(move_frames),
                               np.zeros(hold_frames),
                               np.ones(move_frames)*a0_UL*(move_frames)])
    ainc_LL_vec = np.concatenate([-1*np.ones(move_frames)*a0_LL/(move_frames),
                               np.zeros(hold_frames),
                               np.ones(move_frames)*a0_LL*(move_frames)])
    ainc_UR_vec = np.concatenate([-1*np.ones(move_frames)*a0_UR/(move_frames),
                               np.zeros(hold_frames),
                               np.ones(move_frames)*a0_UR*(move_frames)])
    ainc_LR_vec = np.concatenate([-1*np.ones(move_frames)*a0_LR/(move_frames),
                               np.zeros(hold_frames),
                               np.ones(move_frames)*a0_LR*(move_frames)])

    animation = np.vstack((xinc_vec, yinc_vec, hinc_UL_vec, hinc_LL_vec, ainc_UL_vec, ainc_LL_vec,
                           xinc_vec, yinc_vec, hinc_UR_vec, hinc_LR_vec, ainc_UR_vec, ainc_LR_vec))
    return animation

def make_animation_lookat(eyeL, eyeR, xf_L, yf_L, xf_R, yf_R):
    #Move pupils to deisgnated location/direction
    #May need to adjust eyelids to accomodate
    #Would be interesting to research how eyelids tend to follow eyes (beyond avoiding occlusion),
    #   might add a ton of fidelity to animation quality

    x0_L, y0_L = eyeL.xp, eyeL.yp
    x0_R, y0_R = eyeR.xp, eyeR.yp

    #set a max speed and determine frame count based on this speed/increment
    #not sure if this is better than setting a time to look (n) and determining speed from there
    max_dist = max(((xf_L-x0_L)**2 + (yf_L-y0_L)**2)**0.5, 
                   ((xf_R-x0_R)**2 + (yf_R-y0_R)**2)**0.5)
    max_inc = 5
    n = int(max_dist / max_inc)

    xinc_L_vec = np.ones(n) * (xf_L-x0_L)/n
    yinc_L_vec = np.ones(n) * (yf_L-y0_L)/n
    xinc_R_vec = np.ones(n) * (xf_R-x0_R)/n
    yinc_R_vec = np.ones(n) * (yf_R-y0_R)/n


    hinc_UL_vec = np.zeros(n)
    hinc_LL_vec = np.zeros(n)
    hinc_UR_vec = np.zeros(n)
    hinc_LR_vec = np.zeros(n)


    ainc_UL_vec = np.zeros(n)
    ainc_LL_vec = np.zeros(n)
    ainc_UR_vec = np.zeros(n)
    ainc_LR_vec = np.zeros(n)



    animation = np.vstack((xinc_L_vec, yinc_L_vec, hinc_UL_vec, hinc_LL_vec, ainc_UL_vec, ainc_LL_vec,
                           xinc_R_vec, yinc_R_vec, hinc_UR_vec, hinc_LR_vec, ainc_UR_vec, ainc_LR_vec))
    return animation

def make_animation_zero(eyeL, eyeR):
    xf_L, xf_R = Eye.Window_Width/2, Eye.Window_Width/2
    yf_L, yf_R = Eye.Window_Height/2, Eye.Window_Height/2
    #Lazy and doesn't reset eyelids, change later
    return make_animation_lookat(eyeL, eyeR, xf_L, yf_L, xf_R, yf_R)

def make_animation_freeze(n=20):
    #Freeze all motion for n frames
    xinc_L_vec = np.zeros(n)
    yinc_L_vec = np.zeros(n)
    hinc_UL_vec = np.zeros(n)
    hinc_LL_vec = np.zeros(n)
    ainc_UL_vec = np.zeros(n)
    ainc_LL_vec = np.zeros(n)

    xinc_R_vec = np.zeros(n)
    yinc_R_vec = np.zeros(n)
    hinc_UR_vec = np.zeros(n)
    hinc_LR_vec = np.zeros(n)
    ainc_UR_vec = np.zeros(n)
    ainc_LR_vec = np.zeros(n)


    animation = np.vstack((xinc_L_vec, yinc_L_vec, hinc_UL_vec, hinc_LL_vec, ainc_UL_vec, ainc_LL_vec,
                           xinc_R_vec, yinc_R_vec, hinc_UR_vec, hinc_LR_vec, ainc_UR_vec, ainc_LR_vec))
    return animation 

def main():
    #############################################
    keys = set()
    active_keys = ['1', '2', '3', '0', 'f', 'space']
    def on_press(key):
        try:
            k = key.char
        except:
            k = key.name
        if k in active_keys:
            keys.add(k)
    def on_release(key):
        if key == Key.esc:
            # Stop listener
            return False
        try:
            k = key.char
        except:
            k = key.name
        if k in active_keys:
            keys.remove(k)
        
    #Start non-blocking listener
    listener = Listener(
            on_press=on_press,
            on_release=on_release) 
    listener.start()
    ##############################################
    #For manual testing
    def key2animation(k, eyeL, eyeR):
        if k == '1':
            animation = make_animation_random_x()
            name = 'random motion x'
        if k == '2':
            animation = make_animation_random_y()
            name = 'random motion y'
        if k == 'space':
            animation = make_animation_blink(eyeL, eyeR)
            name = 'blink'
        if k == '3':
            loc_LX = int(input("Input left eye location x: "))
            loc_LY = int(input("Input left eye location y: "))
            loc_RX = int(input("Input right eye location x: "))
            loc_RY = int(input("Input right eye location y: "))
            animation = make_animation_lookat(eyeL, eyeR, loc_LX, loc_LY, loc_RX, loc_RY)
            name = 'lookat (manual input)'
        if k == '0':
            animation = make_animation_zero(eyeL, eyeR)
            name = 'zero eyes'
        if k == 'f':
            n = int(input("Input freeze frames: "))
            animation = make_animation_freeze(n=n)
            name = 'freeze'
        return animation, name
    #############################################

    #Create an instance of Eye
    eyeL = Eye("Left Eye")
    eyeR = Eye("Right Eye")
    #Create an instance of Animation
    animator = Animator()
    try:
        while True:
            if len(keys) != 0:
                k = list(keys)[0]
                animation, name = key2animation(k, eyeL, eyeR)
                animator.do_animation(animation, name=name)
            c = animator.get_control()
            #controls: (xL,yL,hUL,hLL,aUL,aLL, xR,yR,hUR,hLR,aUR,aLR)
            #           0  1   2   3   4   5   6  7   8   9   10  11
            eyeL.move_pupil(c[0], c[1])
            eyeL.move_eyelids(c[2], c[3], c[4], c[5])
            eyeR.move_pupil(c[6], c[7])
            eyeR.move_eyelids(c[8], c[9], c[10], c[11])
            
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