#main BEN loop
import time
import threading
from door_animation import do_door_animation
from sound_effects import do_sound_effect
from motors import Eyebrows
from pyduino_eyes import Eyes
#import RPi.GPIO as gpio

#sshkeyboard for ssh control
from sshkeyboard import listen_keyboard, stop_listening
keys = set()
VALID_KEYS = ['0', '1', '2', '3', 'q']
def press(key):
    if key in VALID_KEYS:
        keys.add(key)

def release(key):
    if key in VALID_KEYS:
        keys.remove(key)


#Track running threads for joining & overload
class ThreadManager():
    def __init__(self):
        #Mark as True if thread is running
        self.door_thread = None
        self.door_running = False
        self.eyebrows_thread = None
        self.eyebrows_running = False
        self.audio_thread = None
        self.keyboard_thread = None
    
    def close_keyboard_thread(self):
        stop_listening()
        self.keyboard_thread.join()
        self.keyboard_thread = None

    def open_door_thread(self):
        #If no door animation is running, create a new thread and start it
        if self.door_running:
            print("Door thread already running")
            return
        self.door_thread = threading.Thread(target=door_thread_func, args=(self,), daemon=True)
        self.door_thread.start()

    def open_eyebrow_thread(self, eyebrows):
        if self.eyebrows_running:
            print("Eyebrow thread already running")
        self.eyebrows_thread = threading.Thread(target=eyebrow_thread_func, args=(self, eyebrows),daemon=True)
        self.eyebrows_thread.start()


    def open_keyboard_thread(self):
        #args: ()
        self.keyboard_thread = threading.Thread(target=keyboard_thread_func, args=(self, press, release), daemon=True)
        self.keyboard_thread.start()

    def clean_threads(self):
        #Threading wrappers should indicate when function is completed thorugh
        # flagging self.xxx_running = False
        if (self.door_thread != None) and (not self.door_running):
            self.door_thread.join()
        if (self.eyebrows_thread != None) and (not self.eyebrows_running):
            self.eyebrows_thread.join()

#Threading wrappers for clarity
def door_thread_func(thread_manager):
    #for debugging
    print("Door Thread:\t Beginning Door Animation")
    thread_manager.door_running = True
    do_door_animation(simulated=False)
    thread_manager.door_running = False
    print("Door Thread:\t Door Animation Completed!")

def audio_thread_func(thread_manager, sound_effect):
    print("Audio Thread:\t Beginning Sound Effect")
    do_sound_effect(sound_effect)
    thread_manager.close_audio_thread()
    print("Audio Thread:\t Sound Effect Completed!")

def keyboard_thread_func(thread_manager, press, release):
    print("Keyboard Thread:\t Beginning Keyboard Thread")
    listen_keyboard(
        on_press=press,
        on_release=release,
    )
    print("Keyboard Thread:\t Closing Keybaord Thread")

def eyebrow_thread_func(thread_manager, eyebrows):
    print("Servo Thread:\t Beginning Servo Thread")
    thread_manager.eyebrows_running = True
    eyebrows.advance_animation()
    thread_manager.eyebrows_running = False
    print("Servo Thread:\t Closing Servo Thread")


thread_manager = ThreadManager()
simulated = False
print("Main Thread:\t Creating Keyboard Thread")


BEN_state = "IDLE" #BEN_state: "IDLE", "ACTIVATED", "PORTAL"
eyes = Eyes()
eyebrows = Eyebrows()
prev_state = "IDLE"
thread_manager.open_keyboard_thread()
while True:
    thread_manager.clean_threads()
    eyes.set_state(BEN_state)
    eyes.advance_animation()
    eyebrows.set_state(BEN_state)
    eyebrows.advance_animation()

    if 'q' in keys:
        eyes.shutdown()
        thread_manager.close_keyboard_thread()
        break

    if '0' in keys:
        eyes.set_animation("CENTER")

    if '1' in keys:
        #Trigger the transition into IDLE
        prev_state = BEN_state
        BEN_state = "IDLE"
        print(BEN_state)
        eyes.set_animation("IDLE1")
        motors.set_animation("IDLE1")
    
    if '2' in keys:
        #Trigger the transition into ACTIVATED
        prev_state = BEN_state
        BEN_state = "ACTIVATED"
        print(BEN_state)
        eyes.set_animation("ACTIVATED")
        None
    
    if '3' in keys:
        #Trigger the transition into PORTAL
        prev_state = BEN_state
        BEN_state = "PORTAL"
        print(BEN_state)
        eyes.set_animation("PORTAL")
        thread_manager.open_door_thread()
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

    