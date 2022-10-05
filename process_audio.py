import enum
import numpy as np
from scipy.io import wavfile


_, signal = wavfile.read("laugh1.wav")
signal_abs = np.abs(signal)
max = int(np.max(signal_abs))
mean = np.mean(signal_abs)

groups = np.array_split(signal_abs, len(signal)/5000)
print(len(groups))

leds = []
ranges = [0, 1/3, 2/3, 1]
print(ranges)
for g in groups:
    group_mean = np.mean(g)
    distance_from_total_mean = abs(mean - group_mean)
    pcnt = min(1, distance_from_total_mean / mean)
    a = []
    for i, _ in enumerate(ranges[1:]):
        if pcnt > ranges[i] and pcnt <= ranges[i+1]:
            a.append(1)
        else:
            a.append(0)
    print(a)
