import board
import neopixel
import numpy as np
import time
from math import sqrt, exp, pi



# Update to match the pin connected to your NeoPixels
pixel_pin = board.D18
# Update to match the number of NeoPixels you have connected
pixel_num = 300

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.1, auto_write=False)

def make_line(n, i):
    #generates a binary line from P[0] to P[i]
    if i >= n:
        return np.ones(n)
    P = np.concatenate((np.ones(i), np.zeros(n-i)))
    return P

def make_green_line(n, i):
    # 0 0 0
    # 1 1 0
    # 0 0 0
    # - i n
    P = np.vstack((np.zeros(n), 
                   make_line(n,i),
                   np.zeros(n)))
    return P

def make_yellow_gauss(n):
    sigma = 1
    num_filts = 10
    k = int(n/num_filts) #10 humps along the line
    r = range(-int(k/2),int(k/2)+1)
    filt = [1 / (sigma * sqrt(2*pi)) * exp(-float(x)**2/(2*sigma**2)) for x in r]
    P = np.concatenate([filt for _ in range(num_filts)])
    return P

def add_noise(P, scale):
    P = P + np.random.normal(scale=scale, size=P.size())
    return P

def normalize(P):
    lo = np.min(P)
    hi = np.max(P)
    return (P + lo) / (hi-lo)




def main():
    i = 0
    yellow_mask = make_yellow_gauss(pixel_num)
    yellow_bias = 1.0
    while True():
        P = make_green_line(pixel_num, i)
        P = P + yellow_bias*yellow_mask
        P = P + np.random.normal(scale=1.0, size=pixel_num)
        P = normalize(P)
        P = int(np.floor(P*255))
        for i, pi in enumerate(P):
            pixels[i] = pi
        yellow_mask = np.roll(yellow_mask, scroll_rate=-5)
        
        pixels.show()
        time.sleep(0.1)

        

main()