import time

from playsound import playsound

# Library that maps effect names to relative paths
SOUND_EFFECTS = {"smp": "sample.wav"}

''''
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
'''

if __name__ == "__main__":
        playsound("sample.wav")
        time.sleep(0.100)
