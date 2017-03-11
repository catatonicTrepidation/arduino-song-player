from mido import MidiFile
from mido import Message
import mido
import math

tempo = 0

songname = 'drwily_solo'

myhumps = MidiFile('music/'+songname+'.mid')

f = open('export/'+songname+'.txt','w')

alpha = ['A','AS','B','C','CS','D','DS','E','F','FS','G','GS']

newnotes = [0, ]
newlths = []

def trnsl(n):
    return 'NOTE_' + alpha[int(n)%12] + str(int(n)/12)

def lth(t):
    return round(10000*t,1)

def toArduinoArray(name, arr):
    ctr = 0
    out = "int " + name + "[] = {"
    for el in arr:
        out += str(el)
        out += ", "
        #if (ctr+1) % 10:
        #    out += "\n"
        ctr+=1
    out += "};"
    return out

for msg in myhumps:
    if not msg.is_meta:
	if msg.type == 'note_on':
    	    newnotes.append(trnsl(msg.note))
        elif msg.type == 'note_off':
            newnotes.append('0')

	if not msg.time == 0:
            noteLength = (mido.tick2second(msg.time,myhumps.ticks_per_beat,tempo)*100000)
            #print("%f " % noteLength)
	    newlths.append(int(noteLength))
	else:
	    newlths.append('0')
    elif msg.type == 'set_tempo':
        tempo = msg.tempo
    #else:
    print(msg)

#print(newnotes)
#print(newlths)

f.write(toArduinoArray("melody", newnotes))
f.write("\n\n")
f.write(toArduinoArray("tempo", newlths))


