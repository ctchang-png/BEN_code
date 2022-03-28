import time

from playsound import playsound
from pynput.keyboard import Key, Listener

# Library that maps effect names to relative paths
SOUND_EFFECTS = {"smp": "sample.wav"}


def play_sound(sound_effect_pth):
    """
    Given a path for an audio file, plays it

    :param sound_effect_pth: path of audio file
    """
    playsound(sound_effect_pth)


def do_sound_effect(sound_effect_key):
    """
    Plays a sound effect if it's in the library

    :param sound_effect_key: key of audio file
    """
    if sound_effect_key not in SOUND_EFFECTS:
        print(f"Sound effect with keyword '{sound_effect_key}' not in library")
    else:
        play_sound(SOUND_EFFECTS[sound_effect_key])


if __name__ == "__main__":
    ### Keypress driver for testing

    keys = set()
    KEYBOARD_EFFECT = {"1": "smp"}  # FILL ME

    def on_press(key):
        try:
            k = key.char
        except:
            k = key.name
        if k in KEYBOARD_EFFECT.keys():
            keys.add(k)

    def on_release(key):
        if key == Key.esc:
            # Stop listener
            return False
        try:
            k = key.char
        except:
            k = key.name
        if k in KEYBOARD_EFFECT.keys():
            keys.remove(k)

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:
        if len(keys) > 1:
            print(
                "Warning! Multiple keys activated. To avoid indeterminant behavior depress only 1 key at a time"
            )
        elif len(keys) == 0:
            continue
        do_sound_effect(KEYBOARD_EFFECT[list(keys)[0]])
        time.sleep(0.100)
