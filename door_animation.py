import numpy as np
import time
from math import sqrt, exp, pi
import board
import neopixel


def make_line(n, i, j):
    #generates a binary line from P[i] to P[j]
    '''
    if i >= n:
        return np.ones(n)
    '''
    P = np.concatenate((np.zeros(i), np.ones(j-i), np.zeros(n-j)))
    return P

def make_green_line(n, i, j):
    # 0 0 0
    # 1 1 0
    # 0 0 0
    # - i n
    P = np.vstack((np.zeros(n),
                   make_line(n,i, j),
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

def set_pixels(pix, pix_arr, n, simulated, fig=None, axim=None):
    pix_arr = np.clip(pix_arr, 0, 255).astype(int)
    if not simulated:
        #pix is adafruit object
        for i in range(n):
            pix[i] = pix_arr[:,i]
        pix.show()
    else:
        #pix is plt ax image handle
        #make pix_arr (1xnx3)
        pix_im = np.expand_dims(pix_arr.transpose(), 0)
        pix_im = np.reshape(pix_im, (10, 30, 3))
        axim.set_data(pix_im)
        fig.canvas.flush_events()

def make_ignite_array(pixel_num):
    red_mask = make_red_gauss(pixel_num) #R + G = Y
    red_bias = 7.0
    scroll_rate = -5
    animation = np.zeros((pixel_num, 3, pixel_num))
    for k in range(1, (pixel_num - 0)//2):
        i = int(pixel_num//2 - k) + 10
        j = int(pixel_num//2 + k) + 10
        if i < 20:
            i = 20
        if j > 300:
            j = 300
        print("i: {}, j: {} ".format(i,j))
        P = make_green_line(pixel_num, i, j)
        #P = P + red_bias*red_mask*make_line(pixel_num, i, j)
        #P = P + np.random.normal(scale=0.01, size=pixel_num)*make_line(pixel_num, i, j)
        P = normalize(P)
        P = np.floor(P*160).astype(int) #Max Brightness of 128 to allow for yellow flash effect
        animation[i,:] = P
        red_mask = np.roll(red_mask, scroll_rate, axis=1)
    return animation

def do_door_animation(simulated=False):

    pixel_num = 300
    refresh_rate = 0.050 #50ms

    if not simulated:
        # Update to match the pin connected to your NeoPixels
        pixel_pin = board.D18
        # Update to match the number of NeoPixels you have connected
        pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.2, auto_write=False)
        fig, axim = None, None
    else:
        from matplotlib import pyplot as plt
        from matplotlib import animation
        plt.ion()
        fig, ax = plt.subplots()
        axim = ax.imshow(np.zeros((10,30, 3)))
        pixels = None

    #Pre-compute animations
    start = time.time()
    ignite_array = make_ignite_array(pixel_num)
    #print(time.time() - start) Takes the pi 0.13s to compute these frames
    try:
        for frame in range(0, ignite_array.shape[0], 5): #Play with speed
            P = ignite_array[frame,:]
            set_pixels(pixels, P, pixel_num, simulated, fig, axim)
            time.sleep(refresh_rate)
        #last idx
        P = ignite_array[ignite_array.shape[0]-1, :]
        set_pixels(pixels, P, pixel_num, simulated, fig, axim)
        time.sleep(refresh_rate)
        
        #Flash Yellow
        Y = np.vstack([255*np.ones(pixel_num),
                       255*np.ones(pixel_num),
                       np.zeros(pixel_num)])
        diff = Y - P
        n = 10
        inc = diff / n
        #to yellow
        for _ in range(n):
            P = P + inc
            set_pixels(pixels, P, pixel_num, simulated, fig, axim)
            time.sleep(refresh_rate)
        #to original
        for _ in range(n):
            P = P - inc
            set_pixels(pixels, P, pixel_num, simulated, fig, axim)
            time.sleep(refresh_rate)
        
        #Idle after animation complete
        red_mask = make_red_gauss(pixel_num) #R + G = Y
        red_bias = 7.0
        scroll_rate = -5
        tic = time.time()
        while time.time() < tic + 10: #remain active for 10seconds
            P = make_green_line(pixel_num, pixel_num)
            P = P + red_bias*red_mask
            P = P + np.random.normal(scale=0.01, size=pixel_num)
            P = normalize(P)
            P = np.floor(P*128).astype(int) #Max Brightness of 128 to allow for yellow flash effect
            set_pixels(pixels, P, pixel_num, simulated, fig, axim)
            red_mask = np.roll(red_mask, scroll_rate, axis=1)
            time.sleep(refresh_rate)
        Z = np.zeros((3, pixel_num))
        set_pixels(pixels, Z, pixel_num, simulated, fig, axim)
    except KeyboardInterrupt:
        print("Program Terminated, shutting off pixels")
        Z = np.zeros((3, pixel_num))
        set_pixels(pixels, Z, pixel_num, simulated, fig, axim)
    return True

if __name__ == "__main__":
    do_door_animation()
