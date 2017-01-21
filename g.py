import sys, pygame
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

BLACK = 0, 0, 0
WHITE = 255, 255, 255
 
pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Waves")

ship=pygame.image.load("ship.png")
ship_up=pygame.image.load("ship_up.png")
ship_down=pygame.image.load("ship_down.png")
clock = pygame.time.Clock()
 
ship_x = 300
ship_y = 200

box_dir = 3

Frequency = 0
m = 0
smooth_m = 0
smooth_f = 0
while True:
  clock.tick(50)
  keys=pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
 
  screen.fill(BLACK)

  points = []
  
  
  h = smooth_m - 800
  
  h = max(0, min(h * 0.5, 320.0))
  f = smooth_f/450
  
  f = max(1.0, min(1.0 + (f - 1.0) * 5, 10.0))
  for i in xrange(100):
    points.append( (i * 5, 240 + math.sin(i * 0.1 * f) * h))
    
  
  pygame.draw.lines(screen, WHITE,  False, points, 2)
  
  s = ship
  if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    ship_x -= 3
  if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    ship_x += 3
  if keys[pygame.K_UP] or keys[pygame.K_w]:
    ship_y -= 3
    s = ship_up
  if keys[pygame.K_DOWN] or keys[pygame.K_s]:
    ship_y += 3
    s = ship_down


  screen.blit(s, (ship_x, ship_y))
 
  pygame.display.flip()
  if stream.get_read_available() >= chunk:
    data = stream.read(chunk)
    Frequency, m=Pitch(data)
    n = 0.05
    smooth_m = smooth_m * (1.0 - n) + m * n
    smooth_f = smooth_f * (1.0 - n) + Frequency * n
    print "freq %f vol %d " % (smooth_f, smooth_m)