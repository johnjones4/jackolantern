import enum
import numpy as np
from scipy.io import wavfile

CLIPS = [
    "laugh.wav",
    "tapping.wav",
    "weak.wav",
    "wine.wav"
]
SEGMENTS = 100

def encode_clip(clip):
    samplerate, signal = wavfile.read("laugh.wav")
    signal_abs = np.abs(signal)
    max = int(np.max(signal_abs))
    mean = np.mean(signal_abs)
    seconds = signal.shape[0] / samplerate

    groups = np.array_split(signal_abs, SEGMENTS)

    group_seconds = int(seconds / len(groups) * 1000)

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
    return leds, group_seconds

def save_header_info(clips, leds_settings, led_timings):
    with open("./jackolantern/leds.h", "w") as file:
        file.write(f"#define N_FILES {str(len(clips))}\n")
        file.write(f"#define N_SEGMENTS {SEGMENTS}\n")
        files_list = [f"\"{filename}\"" for filename in clips]
        file.write("char *filenames[] = {" + ",".join(files_list) + "};\n\n")

        timings_list = [f"{timing}" for timing in led_timings]
        file.write("int timings[] = {" + ",".join(timings_list) + "};\n\n")

        file.write("int leds[" + str(len(clips)) + "][" + str(SEGMENTS) + "][3] = {\n")
        for i, led_settings in enumerate(leds_settings):
            file.write("\t{\n")
            for j, ledset in enumerate(led_settings):
                row = ",".join([str(l) for l in ledset])
                file.write("\t\t{" + row + "}")
                if j < len(led_settings) - 1:
                    file.write(",")
                file.write("\n")
            file.write("\t}")
            if i < len(leds_settings) - 1:
                file.write(",")
            file.write("\n")
        file.write("};\n")

led_settings = list()
led_timings = list()
for clip in CLIPS:
    settings, timings = encode_clip(clip)
    led_settings.append(settings)
    led_timings.append(timings)
save_header_info(CLIPS, led_settings, led_timings)
