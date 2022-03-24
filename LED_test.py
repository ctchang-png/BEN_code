import board
import neopixel
import numpy as np
import time



# Update to match the pin connected to your NeoPixels
pixel_pin = board.D18
# Update to match the number of NeoPixels you have connected
pixel_num = 300

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.1, auto_write=False)



def main():
    for i in range(pixel_num):
        pixels[i] = 0
        pixels.show()
        time.sleep(0.1)
        

if __name__ == "__main__":
    main()