#main ben loop
from pynput.keyboard import Key, Listener
import time
import threading
from door_animation import do_door_animation
from sound_effects import do_sound_effect
from pyduino_eyes import Eyes

#sshkeyboard for ssh control
from sshkeyboard import listen_keyboard
keys = set()
VALID_KEYS = ['0', '1', '2', 'q']
def press(key):
    if key in VALID_KEYS:
        keys.add(key)

def release(key):
    if key in VALID_KEYS:
        keys.remove(key)


#Keypress driver for testing

'''
def on_press(key):
    try:
        k = key.char
    except:
        k = key.name
    if k in VALID_KEYS:
        keys.add(k)
def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False
    try:
        k = key.char
    except:
        k = key.name
    if k in VALID_KEYS:
        keys.remove(k)
listener = Listener(
        on_press=on_press,
        on_release=on_release) 
listener.start()
'''
#Track running threads for joining & overload
class ThreadStatus():
    def __init__(self):
        #Mark as True if thread is running
        self.door = False
        self.audio = False
        self.keyboard = True

#Threading wrappers for clarity
def door_thread_func(thread_status, simulated):
    #for debugging
    print("Door Thread:\t Beginning Door Animation")
    do_door_animation(simulated=simulated)
    thread_status.door = False
    print("Door Thread:\t Door Animation Completed!")

def audio_thread_func(thread_status, sound_effect):
    print("Audio Thread:\t Beginning Sound Effect")
    do_sound_effect(sound_effect)
    thread_status.audio = False
    print("Audio Thread:\t Sound Effect Completed!")

def keyboard_thread_func(press, release):
    print("Keyboard Thread:\t Beginning Keyboard Thread")
    listen_keyboard(
        on_press=press,
        on_release=release,
        until='esc'
    )
    print("Keyboard Thread:\t \'Esc\' Pressed, Keyboard Thread Terminated")


def get_state():
    '''
    Scan for button inputs in order to decide if BEN should be in state:
    IDLE, ACTIVATED, PORTAL
    '''
    return "IDLE"

thread_status = ThreadStatus()
simulated = True
#threads = [] Debugging tool
door_thread_old = False
audio_thread_old = False
print("Main Thread:\t Creating Keyboard Thread")
keyboard_thread = threading.Thread(target=keyboard_thread_func, args=(press, release), daemon=True)
keyboard_thread.start()

BEN_state = "IDLE" #BEN_state: "IDLE", "ACTIVATED", "PORTAL"
eyes = Eyes()
prev_state = "IDLE"
while True:
    eyes.set_state(BEN_state)
    eyes.advance_animation()

    if 'q' in keys:
        eyes.shutdown()
        print('press \'esc\' to close keyboard listener')
        keyboard_thread.join()
        break

    if '0' in keys:
        eyes.set_animation("CENTER")

    if '1' in keys:
        #Trigger the transition into IDLE
        prev_state = BEN_state
        BEN_state = "IDLE"
        print(BEN_state)
        eyes.set_animation("IDLE1")
    
    if '2' in keys:
        #Trigger the transition into ACTIVATED
        prev_state = BEN_state
        BEN_state = "ACTIVATED"
        print(BEN_state)
        eyes.set_animation("ACTIVATED")
        None
    
    if '3' in keys:
        #Trigger the transition into PORTAL
        None
    time.sleep(0.050)
    '''
    #No inputs -> Idling auido/animations
    if len(keys) == 0:
        None
        

    #Trigger door animation on input. Some audio should be associated with this eventually
    if 'd' in keys:
        if not thread_status.door:
            thread_status.door = True
            print("Main Thread:\t Creating Door Thread")
            door_thread = threading.Thread(target=door_thread_func, args=(thread_status, simulated), daemon=True)
            #threads.append(door_thread)
            door_thread.start()
        else:
            print("Door animation attempted while already running. Please wait until current animation is completed")

    #Trigger audio 'animation' on some input --- Also need idling audio
    if 'a' in keys and not thread_status.audio:
        if not thread_status.audio:
            thread_status.audio = True
            print("Main Thread:\t Creating Audio Thread")
            sound_effect = "1" #Change me later
            audio_thread = threading.Thread(target=audio_thread_func, args=(thread_status, sound_effect), daemon=True)
            #threads.append(audio_thread)
            audio_thread.start()
        else:
            print("Audio attempted while already running. Please wait until current sound effect is completed")


    #Join threads when function is completed
    door_thread_old = thread_status.door
    audio_thread_old = thread_status.audio


    if 'q' in keys:
        #This is fuckin trash but need to press q to join keyboard thread then esc to release to join the rest
        print("Main Thread:\t Joining Keyboard Thread")
        keyboard_thread.join()
        print("Main Thread:\t Joining Door Thread")
        try:
            door_thread.join()
        except NameError:
            print("Main Thread:\t Door Thread not joined (did not exist)")
        print("Main Thread:\t Joining Audio Thread")
        try:
            audio_thread.join()
        except NameError:
            print("Main Thread:\t Audio Thread not joined (did not exist)")
        print("Main Thread:\t Program Terminated")
        break
    time.sleep(0.5)

    #Join threads on function completion
    #print("Thread Count: {}".format(len(threads)))
    if door_thread_old and not thread_status.door:
        door_thread.join()
        #threads.pop(threads.index(door_thread))
    if audio_thread_old and not thread_status.audio:
        audio_thread.join()
        #threads.pop(threads.index(audio_thread))
    '''

    