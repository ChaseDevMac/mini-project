from random import sample
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

SPEED_OF_SOUND = 340  # meters/sec

#Code to create 10 second long white noise wav file (Tx / x_t)
"""
samplerate, data = wavfile.read("white_noise.wav")
print(samplerate)
new_data = data[4410:8820]
repeat_data = new_data
for i in range(100):
    repeat_data = np.concatenate((repeat_data, new_data), axis=0)

plt.plot(repeat_data)
plt.legend()
plt.show()

wavfile.write("new_white_noise.wav", samplerate, repeat_data)
"""

samplerate, data = wavfile.read("white_noise.wav")
xt = data[4410:8820]

samplerate, data = wavfile.read("CybertoriumMono.wav")
#print(samplerate)
mid = int(len(data) / 1.5)
yr = data[mid: mid + (samplerate // 10)]
#print(len(yr))

fxt = np.fft.fft(xt)
fyr = np.fft.fft(yr)

hrt = np.fft.ifft(np.divide(fyr, fxt))

#plt.plot(hrt)
#plt.show()

hrtmax = np.argmax(np.absolute(hrt))
print(hrtmax)

#Index gap computed for 1 foot distance between receiver and reflective surface
indexDist = 45

hrt2ndmax = np.argmax(np.absolute(hrt[hrtmax + indexDist : -1])) + indexDist + hrtmax
print(hrt2ndmax)

gap = hrt2ndmax - hrtmax
time = gap * (1 / samplerate)

distance = SPEED_OF_SOUND * time / 2
print(distance)




