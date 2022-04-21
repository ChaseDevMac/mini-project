import numpy as np
import argparse
import soundfile as sf
import json

SPEED_OF_SOUND = 343  # meters/sec

parser = argparse.ArgumentParser(description="""Obtain the distance between a
                                 receiver and a reflector based on the channel
                                 impulse response""")
parser.add_argument("-d", metavar="--distance", type=float,
                    help="measured distance from Rx to reflector in meters")
parser.add_argument("-r", metavar="--received-audio", type=str,
                    help="name of audio singal/file at the receiver")
parser.add_argument("-c", metavar="--config", type=str,
                    help="name of configuration file")
parser.add_argument("-o", metavar="--output", type=str,
                    help="name of output file")
args = parser.parse_args()

measured_dist = args.d or 0.5  # default to 0.5 meters
received_audio = args.r or "received_audio.wav"
config_file = args.c or "signal_config.json"

# read the configuration generated from gen_transmit_signal()
with open(config_file, 'r') as file:
    data = file.read()

config = json.loads(data)

# Obtain training data (transmitted data)
xt = np.array(config['training data'])

data, samplerate = sf.read(received_audio)

if (samplerate != config["samplerate"]):
    print(f"""Inconsistent samplerates\n
    received samplerate: {samplerate}\n
    transmitted samplerate: {config['samplerate']}""")

# grab data size equal to the transmitted data size
mid = int(len(data) / 1.5)
yr = data[mid: mid + config['window size']]

# convert time domain signals into frequency domain
fxt = np.fft.fft(xt)
fyr = np.fft.fft(yr)

# channel impulse response
cir = np.fft.ifft(np.divide(fyr, fxt))

# line of sight response
los = np.argmax(np.absolute(cir))

# margin for potential measuring error
measure_err = 0.90

# padding in samples to reduce error in finding reflected response peak
padding = int((measured_dist / SPEED_OF_SOUND) * samplerate * 2 * measure_err)

# reflected response
reflected = np.argmax(np.absolute(cir[(los + padding): -1])) + padding + los

change_in_samples = reflected - los
change_in_time = change_in_samples * (1 / samplerate)

distance = SPEED_OF_SOUND * (change_in_time / 2)

if (args.o):
    output_file = open(args.o, "w")
    output_file.write(f"Distance from receiver and reflector: {distance} m")

print(distance, "meters")
