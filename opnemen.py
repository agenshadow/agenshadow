# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 08:48:08 2024

@author: thijs
"""
import pyaudio
import wave
import time

# Audio file specifications
chunk = 1024
format = pyaudio.paInt16
rate = 44100
seconds = 5
channels = 1
pause = 3

#een loop van 3 omdat wij 3 keer willen opnemen op 1 punt
for i in range(3):
    # Start recording
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    print("Start recording")
    frames = []
    
    for j in range(0, int(rate / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
        
    print("Recording stopped")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert recording to WAV file
    wf = wave.open("meting{}_1.wav".format(i), 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    #pauze tussen de metingen
    print(pause, "s pauze")
    time.sleep(pause)
    print("volgende meting")
