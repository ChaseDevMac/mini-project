import argparse
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import json

parser = argparse.ArgumentParser(description="Generate a repeated signal")
parser.add_argument("-s", metavar="--start", type=float,
                    help="start of repeated signal in seconds")
parser.add_argument("-int", metavar="--interval", type=float,
                    help="length of repeated part of signal in seconds")
parser.add_argument("-d", metavar="--duration", type=float,
                    help="length of audio singal/file in seconds")
parser.add_argument("-p", metavar="--plot", type=bool,
                    help="whether a plot should be made for singal (bool)")
parser.add_argument("-i", metavar="--input-signal", type=str,
                    help="name of audio file in wav format")
parser.add_argument("-tx", metavar="--transmit-signal", type=str,
                    help="name of audio signal/file to be transmitted")
parser.add_argument("-td", metavar="--training-data", type=str,
                    help="name of text file to save training data")
parser.add_argument("-c", metavar="--config", type=str,
                    help="name of configuration file")
args = parser.parse_args()

duration = args.d or 10     # seconds
interval = args.int or 0.1    # seconds
input_audio = args.i or "white_noise.wav"
transmit_audio = args.tx or "transmit.wav"
training_file = args.td or "training_data.txt"
config_file = args.c or "signal_config.json"

# import white noise file
samplerate, data = wavfile.read(input_audio)

# determine starting index of audio singal
start = int(args.s * samplerate if args.s else (len(data) / 2))
window_size = int(interval * samplerate)
training_data = data[start: start + window_size]

repeat_amt = int(duration / interval)
output_data = data[0:0]
for _ in range(repeat_amt):
    output_data = np.concatenate((output_data, training_data), axis=0)

if (args.p):
    plt.plot(output_data)
    plt.legend()
    plt.show()

# output the audio to be transmitted
wavfile.write(transmit_audio, samplerate, output_data)

# write the configuration of the signal
config_file = open(config_file, "w")

config = {
    "start index": start,
    "interval": interval,
    "duration": duration,
    "window size": window_size,
    "input audio": input_audio,
    "transmit audio": transmit_audio,
    "samplerate": samplerate,
    "training data": training_data.tolist(),
}
config_file.write(json.dumps(config, indent=4))
