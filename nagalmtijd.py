# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 11:41:56 2024

@author: Merlijn
@sub author: Mike
"""

import wave, struct
from scipy.io import wavfile
from math import log10

#de functie voor de nagalmtijd
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
        #dit eerste deel rekent alle waardes om naar dB
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
        #het bepalen van het begin punt
        if i >= start and tstart == 0:
            dBstart = gemdata[start]
            if gemdata[i] <= dBstart - safety_variable and gemdata[i] >= dBstart - (safety_variable + 0.1) :
                tstart = i
                
       #het bepalen van het eind punt
        if i >= start and teind == 0:
            if gemdata[i] <= dBstart - (dB_drop + safety_variable) and gemdata[i] >= dBstart - (dB_drop + safety_variable + 0.1) :
                teind = i
                break
        
    #het bereken van de nagalmtijd
    t = (teind - tstart) / sample_rate
    t = 60/dB_drop * t
    print("de nagalmtijd is:", t)
