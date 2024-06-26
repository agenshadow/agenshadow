# -*- coding: utf-8 -*-
"""

@author: trash can monster
"""

import wave, struct
from scipy.io import wavfile
from math import log10

#de functie voor de nagalmtijd
def nagalmtijd_60db(file, dB_drop):
    #aanmaken van variabelen die nodig gaan zijn
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

        #dit verwerkt de lijst tot fatsoenlijke waardes en verwijderd telkens de laatste waarde van de lijst
        #hij doet dit om het een stuk sneller te maken
        if i >= 11025:
            gem += ydata[i]
            gem -= ydata[i-11025] 
            gemdata.append(gem/11025)
        else:
            gem += ydata[i]
            gemdata.append(gem/(i+1))
        
        te = round(i / sample_rate, 1)

        #progress bar
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

    #als je de "#" weghaalt bij de volgende twee lijnen dan print hij ook je db grafiek
    #x = np.linspace(0, len(gemdata)/sample_rate, len(gemdata))
    #plt.plot(x, gemdata)
    
    print("de nagalmtijd is:", t)
    #als je wil kan je hier ook gewoon return t van maken indien je het wil gebruiken voor in een lijst
