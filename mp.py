import numpy as np
import argparse
from scipy.io import wavfile
import json

SPEED_OF_SOUND = 340  # meters/sec

parser = argparse.ArgumentParser(description="""Obtain the distance between a
                                 receiver and a reflector based on the channel
                                 impulse response""")
parser.add_argument("-r", metavar="--received-audio", type=str,
                    help="name of audio singal/file at the receiver")
parser.add_argument("-c", metavar="--distance", type=str,
                    help="name of configuration file")
parser.add_argument("-o", metavar="--output", type=str,
                    help="name of output file")
args = parser.parse_args()

received_audio = args.r or "received_audio.wav"
config_file = args.c or "signal_config.json"
output_file = args.o or "distance.txt"

# read the configuration generated from gen_
with open(config_file, 'r') as file:
    data = file.read()

config = json.loads(data)

xt = np.array(config["training data"])

samplerate, data = wavfile.read(received_audio)

if (samplerate != config["samplerate"]):
    print(f"""Inconsistent samplerates\n
    received samplerate: {samplerate}\n
    transmitted samplerate: {config['samplerate']}""")

# grab data size equal to the transmitted data size
mid = int(len(data) / 2)
yr = data[mid: mid + config["window size"]]

# convert time domain signals into frequency domain
fxt = np.fft.fft(xt)
fyr = np.fft.fft(yr)

# channel impulse response
cir = np.fft.ifft(np.divide(fyr, fxt))

# line of sight response
los = np.argmax(np.absolute(cir))

# Index gap computed for 1 foot distance between receiver and reflective surface
index_padding = 45

# reflected response
reflected = np.argmax(np.absolute(cir[(los + index_padding): -1])) + index_padding + los

change_in_samples = reflected - los
change_in_time = change_in_samples * (1 / samplerate)

distance = SPEED_OF_SOUND * (change_in_time / 2)

output_file = open(output_file, "w")
output_file.write(f"Distance from receiver and reflector: {distance} meters")
