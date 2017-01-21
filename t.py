#Eng Eder de Souza 01/12/2011
#ederwander
from matplotlib.mlab import find
import pyaudio
import numpy as np
import math


chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 20


def Pitch(signal):
    signal = np.fromstring(signal, 'Int16');
    m = 0
    for s in signal:
        m = m + abs(s)
    m = m / len(signal)
    
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing));
    f0=round(len(index) *RATE /(2*np.prod(len(signal))))
    return f0, m;

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = chunk)

while 1:
    if stream.get_read_available() >= chunk:
        data = stream.read(chunk)
        Frequency, m=Pitch(data)
        
        
        print "%s %f %d Frequency" % (type(data), Frequency, m)