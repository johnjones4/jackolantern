import enum
import numpy as np
from scipy.io import wavfile


samplerate, signal = wavfile.read("laugh1.wav")
signal_abs = np.abs(signal)
max = int(np.max(signal_abs))
mean = np.mean(signal_abs)
seconds = signal.shape[0] / samplerate

groups = np.array_split(signal_abs, len(signal)/5000)
print(len(groups))

group_seconds = seconds / len(groups)
print(group_seconds)

leds = []
ranges = [0, 1/3, 2/3, 1]
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
    leds.append(a)

with open("leds.h", "w") as file:
    file.write(f"#define SECONDS_PER_LED = {group_seconds}\n\n")
    file.write("int leds[" + str(len(leds)) + "][3] = {\n")
    for i, ledset in enumerate(leds):
        row = ",".join([str(l) for l in ledset])
        file.write("\t{" + row + "}")
        if i < len(leds) - 1:
            file.write(",")
        file.write("\n")
    file.write("};\n")
