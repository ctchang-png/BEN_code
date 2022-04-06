# main BEN loop
import time
import threading
from door_animation import do_door_animation
from sound_effects import do_sound_effect
from motors import Eyebrows
from pyduino_eyes import Eyes
#import RPi.GPIO as gpio

# sshkeyboard for ssh control
from sshkeyboard import listen_keyboard, stop_listening
keys = set()
VALID_KEYS = ['0', '1', '2', '3', 'q', 's']


def press(key):
    if key in VALID_KEYS:
        keys.add(key)


def release(key):
    if key in VALID_KEYS:
        keys.remove(key)


# Track running threads for joining & overload
class ThreadManager():
    def __init__(self):
        # Mark as True if thread is running
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
        # If no door animation is running, create a new thread and start it
        if self.door_running:
            print("Door thread already running")
            return
        self.door_thread = threading.Thread(
            target=door_thread_func, args=(self,), daemon=True)
        self.door_thread.start()

    def open_eyebrow_thread(self, eyebrows):
        if self.eyebrows_running:
            print("Eyebrow thread already running")
        self.eyebrows_thread = threading.Thread(
            target=eyebrow_thread_func, args=(self, eyebrows), daemon=True)
        self.eyebrows_thread.start()

    def close_eyebrow_thread(self):
        self.eyebrows_thread.join()
        self.eyebrows_thread = None
        self.eyebrows_running = False

    def open_keyboard_thread(self):
        #args: ()
        self.keyboard_thread = threading.Thread(
            target=keyboard_thread_func, args=(self, press, release), daemon=True)
        self.keyboard_thread.start()

    def clean_threads(self):
        # Threading wrappers should indicate when function is completed thorugh
        # flagging self.xxx_running = False
        if (self.door_thread != None) and (not self.door_running):
            self.door_thread.join()
        if (self.eyebrows_thread != None) and (not self.eyebrows_running):
            self.eyebrows_thread.join()

# Threading wrappers for clarity


def door_thread_func(thread_manager):
    # for debugging
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
    #print("Servo Thread:\t Beginning Servo Thread")
    thread_manager.eyebrows_running = True
    eyebrows.advance_animation()
    thread_manager.eyebrows_running = False
    #print("Servo Thread:\t Closing Servo Thread")


def surprise():
    eyes.set_animation("surprise")
    eyebrows.set_animation("surprise")


thread_manager = ThreadManager()
simulated = False
print("Main Thread:\t Creating Keyboard Thread")


BEN_state = "IDLE"  # BEN_state: "IDLE", "ACTIVATED", "PORTAL"
eyes = Eyes()
eyebrows = Eyebrows()
prev_state = "IDLE"
thread_manager.open_keyboard_thread()
while True:
    thread_manager.clean_threads()
    eyes.set_state(BEN_state)
    eyes.advance_animation()
    eyebrows.set_state(BEN_state)
    if not thread_manager.eyebrows_running:
        thread_manager.open_eyebrow_thread(eyebrows)

    if 'q' in keys:
        eyes.shutdown()
        thread_manager.close_keyboard_thread()
        break

    if '0' in keys:
        eyes.set_animation("CENTER")

    if '1' in keys:
        # Trigger the transition into IDLE
        prev_state = BEN_state
        BEN_state = "IDLE"
        print(BEN_state)
        eyes.set_animation("IDLE1")
        eyebrows.set_animation("IDLE1")

    if '2' in keys:
        # Trigger the transition into ACTIVATED
        prev_state = BEN_state
        BEN_state = "ACTIVATED"
        print(BEN_state)
        eyes.set_animation("ACTIVATED")
        None

    if '3' in keys:
        # Trigger the transition into PORTAL
        prev_state = BEN_state
        BEN_state = "PORTAL"
        print(BEN_state)
        eyes.set_animation("PORTAL")
        thread_manager.open_door_thread()
        None

    if 's' in keys:
        # Trigger the surprise emote
        surprise()

    time.sleep(0.050)
