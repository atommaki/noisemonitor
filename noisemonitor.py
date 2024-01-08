#!/usr/bin/env python3

import sounddevice as sd
import numpy as np
import time
import datetime

def audio_callback(indata, frames, time, status):
    if status:
        print(status)

    # Perform FFT on the audio data
    fft_result = np.fft.rfft(indata[:, 0])
    freqs = np.fft.rfftfreq(len(indata), 1 / sample_rate)

    # Divide the spectrum into 10 frequency bands
    band_limits = np.linspace(20, 20000, 11)
    band_levels = np.zeros(10)
    for i in range(10):
        # Find the indices of frequencies in this band
        indices = np.where((freqs >= band_limits[i]) & (freqs < band_limits[i + 1]))[0]
        # Calculate average power in this band
        band_levels[i] = np.sqrt(np.mean(np.abs(fft_result[indices])**2))

    # Check if any band level is higher than 1 and print the results
    if any(band_levels > 1):
        print(f"{datetime.datetime.now()}: Bands: " + " | ".join([f"{i+1}: {level:.2f}" for i, level in enumerate(band_levels)]))

# Set your microphone sensitivity here. The default is 1.
mic_sensitivity = 1

# Sample rate and duration for each audio capture.
sample_rate = 44100
duration = 2  # in seconds

try:
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, blocksize=int(sample_rate * duration)):
        while True:
            time.sleep(duration)
except KeyboardInterrupt:
    print("Monitoring stopped")

