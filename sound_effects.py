import time

SOUND_EFFECTS = dict() 
#key: "str"
#val: TBD, could be a str path to sounds folder, could be mp4, could be others...

def play_sound(SOUND_EFFECTS_VAL):
    raise NotImplementedError("Write me!")

def do_sound_effect(sound_effect):
    #Consult Chris before changing this fucntion
    if sound_effect not in SOUND_EFFECTS:
        print("Sound effect with keyword \"{}\" not in library".format(sound_effect))
        return
    play_sound(SOUND_EFFECTS[sound_effect])


if __name__ == "__main__":
    ### Keypress driver for testing
    from pynput.keyboard import Key, Listener
    keys = set()
    VALID_KEYS = ["1"]                                  #FILL ME
    KEYBOARD_2_EFFECT = {"1": "test_audio"}             #FILL ME
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

    while True:
        if len(keys) > 1:
            print("Warning! Multiple keys activated. To avoid indeterminant behavior depress only 1 key at a time")
        if len(keys) == 0:
            continue
        sound_effect = KEYBOARD_2_EFFECT[keys[0]] #Take first active key if any
        do_sound_effect(sound_effect)
        time.sleep(0.100)
