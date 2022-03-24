#main ben loop
from pynput.keyboard import Key, Listener
import time
import threading
from door_animation import do_door_animation
import logging

keys = set()
VALID_KEYS = ['d', 'q']
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

class ThreadStatus():
    def __init__(self):
        #Mark as True if thread is running
        self.door = False

thread_status = ThreadStatus()
simulated = False
door_animation = False #True if animation already occurring

def door_thread_func(thread_status, simulated):
    #for debugging
    print("Door Thread:\t Beginning Door Animation")
    do_door_animation(simulated=simulated)
    thread_status.door = False
    print("Door Thread:\t Door Animation Completed!")

while True:
    print("loop start")
    #animate eyes
    #play audio
    #scan for button press
    if 'd' in keys:
        if not thread_status.door:
            thread_status.door = True
            print("Main Thread:\t Creating Door Thread")
            door_thread = threading.Thread(target=door_thread_func, args=(thread_status, simulated,), daemon=True)
            door_thread.start()
        else:
            print("Door animation attempted while already running. Please wait until animation is completed")

    if 'q' in keys:
        print("Main Thread:\t Joining Door Thread")
        door_thread.join()
        
    time.sleep(0.5)


    