#main ben loop
from pynput.keyboard import Key, Listener
import time
import threading
from door_animation import do_door_animation
from sound_effects import do_sound_effect
import logging

keys = set()
VALID_KEYS = ['d', 'q', 'a']
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
        self.audio = False

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




thread_status = ThreadStatus()
simulated = True
threads = []
door_thread_old = False
audio_thread_old = False

while True:
    print("loop start")
    #animate eyes
    #play audio
    #scan for button press
    if 'd' in keys:
        if not thread_status.door:
            thread_status.door = True
            print("Main Thread:\t Creating Door Thread")
            door_thread = threading.Thread(target=door_thread_func, args=(thread_status, simulated), daemon=True)
            threads.append(door_thread)
            door_thread.start()
        else:
            print("Door animation attempted while already running. Please wait until current animation is completed")

    if 'a' in keys and not thread_status.audio:
        if not thread_status.audio:
            thread_status.audio = True
            print("Main Thread:\t Creating Audio Thread")
            sound_effect = input("Enter Sound Effect Name: ")
            audio_thread = threading.Thread(target=audio_thread_func, args=(thread_status, sound_effect), daemon=True)
            threads.append(audio_thread)
            audio_thread.start()
        else:
            print("Audio attempted while already running. Please wait until current sound effect is completed")


    #Join threads when function is completed
    door_thread_old = thread_status.door
    audio_thread_old = thread_status.audio


    if 'q' in keys:
        print("Main Thread:\t Joining Door Thread")
        door_thread.join()
        print("Main Thread:\t Joining Audio Thread")
        audio_thread.join()
        print("Main Thread:\t Program Terminated")
        break
        
    time.sleep(0.5)
    #Join threads on function completion
    print("Thread Count: {}".format(len(threads)))
    if door_thread_old and not thread_status.door:
        door_thread.join()
        threads.pop(threads.index(door_thread))
    if audio_thread_old and not thread_status.audio:
        audio_thread.join()
        threads.pop(threads.index(audio_thread))


    