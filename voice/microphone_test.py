import sounddevice as sd
import numpy as np


sample_rate = 44100
duration = 5
device = 1


print("JARVIS Microphone Volume Test")
print("Speak normally for 5 seconds...")
print()

recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32",
    device=device
)

sd.wait()

volume = np.sqrt(np.mean(recording ** 2))
maximum = np.max(np.abs(recording))

print("Recording finished!")
print()
print("Average microphone volume:", volume)
print("Maximum microphone volume:", maximum)

if maximum < 0.005:
    print("WARNING: Microphone input is extremely low.")

elif maximum < 0.02:
    print("Microphone input is low.")

else:
    print("Microphone input looks active.")
