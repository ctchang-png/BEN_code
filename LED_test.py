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

def make_red_gauss(n):
    sigma = 5
    num_filts = 12
    k = int(n/num_filts) #12 humps along the line
    r = range(-int(k/2),int(k/2)+1)
    filt = [1 / (sigma * sqrt(2*pi)) * exp(-float(x)**2/(2*sigma**2)) for x in r]
    wave = np.concatenate([filt for _ in range(num_filts)])
    P = np.vstack([ wave, np.zeros(n), np.zeros(n)])
    return P

def add_noise(P, scale):
    P = P + np.random.normal(scale=scale, size=P.size())
    return P

def normalize(P):
    lo = np.min(P)
    hi = np.max(P)
    if hi == lo:
      return np.zeros_like(P)
    return (P - lo) / (hi-lo)




def main():
    i = 0
    yellow_mask = make_red_gauss(pixel_num)
    yellow_bias = 6.0
    scroll_rate = -5
    try:
      #Ignite Portal
      for i in range(pixel_num):
          #P = np.zeros((3,pixel_num))
          P = make_green_line(pixel_num, i)
          P = P + yellow_bias*yellow_mask*make_line(pixel_num, i)
          P = P + np.random.normal(scale=0.01, size=pixel_num)*make_line(pixel_num, i)
          P = normalize(P)
          P = np.floor(P*128).astype(int) #Max Brightness of 128 to allow for yellow flash effect
          for j in range(pixel_num):
              pixels[j] = P[:,j]
          yellow_mask = np.roll(yellow_mask, scroll_rate, axis=1)
          pixels.show()
          time.sleep(0.005)
      #Idle after animation complete
      while True:
         time.sleep(0.005)
    except KeyboardInterrupt:
      print("Program Terminated, shutting off pixels")
      for j in range(pixel_num):
        pixels[j] = (0,0,0)
      pixels.show()

main()
