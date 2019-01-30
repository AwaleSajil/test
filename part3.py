import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time


# constants
CHUNK = 1024             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

freqRange = np.array([500,2000])
freqBlock = freqRange*(2*CHUNK)/(RATE)


#for discrete counting
globvar = 0
count = 0

def incORnot():
    global globvar
    if ((globvar) == 0):
        (globvar) = 1
        return 1
    return 0

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)


xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)


print('stream started')


while True:
    # binary data
    data = stream.read(CHUNK)  
    
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    
    avgData = np.sum(data_int)/(len(data_int))
    avgPower = 20*np.log10(avgData/255)

    print(avgPower)
    # compute FFT and update line
    yf = fft(data_int)
    yf_data = (np.abs(yf[int(freqBlock[0]):int(freqBlock[1])])  / (128 * CHUNK))
    
    power = 20*np.log10(yf_data)



#     print(np.max(power))
    
#     if((np.max(power)) > -12):
#         if (incORnot() == 1):
#             count = count + 1
#             print("HI")
#     elif ((np.max(power)) < -30):
#         globvar = 0
        
#     if(np.max(power) > -15):
#         print(np.max(power), count)


