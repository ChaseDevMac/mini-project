import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

SPEED_OF_SOUND = 340  # meters/sec

samplerate, data = wavfile.read("white_noise.wav")
print(samplerate)
new_data = data[4410:8820]
repeat_data = new_data
for i in range(100):
    repeat_data = np.concatenate((repeat_data, new_data), axis=0)

full_data = np.concatenate((new_data, new_data), axis=0)
full_data = np.concatenate((full_data, new_data), axis=0)

plt.plot(repeat_data)
plt.legend()
plt.show()

wavfile.write("new_white_noise.wav", samplerate, repeat_data)
