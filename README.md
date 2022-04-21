# Mini-Project (Final)

Find the distance from a receiver and a reflecting object (wall) using audio signals

## Getting Started
1) run ``` python gen_transmit_signal -tx <wav_audio_file>``` passing in the name of a wav file
2) record the received signal and put use it for step 3
3) run ```python mp.py -r <rec_audio_file>```

### Need help or need more command line arguments?


* run
  ```sh
  python gen_transmit_signal -h #and/or
  python mp.py -h
  ```

## Usage Example
1) run ```python gen_transmit_signal -tx white_noise.wav```
2) run ```python mp.py -r demo.wav```
