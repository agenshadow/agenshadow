# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 11:41:56 2024

@author: merlijn
"""

import wave, struct
from scipy.io import wavfile
from math import log10

def nagalmtijd_60db(file, dB_drop):
    
    wavefile = wave.open(file)
    ydata = []
    gemdata = []
    length = wavefile.getnframes()
    sample_rate, data = wavfile.read(file)
    
    tstart = 0
    teind = 0
    td = -1
    gem = 0
    
    #dit is een gekozen start voor waar de code zijn dbstart vandaan haalt dit is gewoon een halve seconde
    start = 22050
    
    #variabele om te kijken of de dB daadwerkelijk gedaald is
    safety_variable = 3
    
    for i in range(length):
        filedata = wavefile.readframes(1)
        data = struct.unpack("<h", filedata)
        y = data[0]
         
        if y == 0:
            ydata.append(-60)
            continue
        
        y = abs(y)
        y = 20 * log10(y / 2**15)
        ydata.append(y)
        
        if i >= 11025:
            gem += ydata[i]
            gem -= ydata[i-11025] 
            gemdata.append(gem/11025)
        else:
            gem += ydata[i]
            gemdata.append(gem/(i+1))
        
        te = round(i / sample_rate, 1)
        
        if te != td:
            print(str(te) + "s verwerkt")
            td = te
    
    
    for i, waarde in enumerate(gemdata):
        if i >= start and tstart == 0:
            dBstart = gemdata[start]
            if gemdata[i] <= dBstart - safety_variable and gemdata[i] >= dBstart - (safety_variable + 0.1) :
                tstart = i
                
        if i >= start and teind == 0:
            if gemdata[i] <= dBstart - (dB_drop + safety_variable) and gemdata[i] >= dBstart - (dB_drop + safety_variable + 0.1) :
                teind = i
                break
    t = (teind - tstart) / sample_rate
    t = 60/dB_drop * t
    return t

file = r"C:\Users\User\OneDrive - HvA\project\project_3\opnames\metingen\1000hz\f1000meting2.0_vak6.wav"
dB_drop = 10

t = nagalmtijd_60db(file, dB_drop)
print("nagalmtijd is" , t, "s")
