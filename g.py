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
thruster=pygame.image.load("ship_thruster.png")

bg=pygame.image.load("bg.png")
clock = pygame.time.Clock()
 
ship_x = 300
ship_y = 200

box_dir = 3

bg_x = 0
bg_y = 0
bg_w = 960
bg_h = 640

bg_speed_x = -0.15
bg_speed_y = 0
Frequency = 0
m = 0
smooth_m = 0
smooth_f = 0
frame = 0

e1 = [ pygame.image.load("e11.png"), pygame.image.load("e12.png"), pygame.image.load("e13.png"), pygame.image.load("e14.png"), pygame.image.load("e15.png") ]


enemies = []

enemies.append({ 'x' : 400, 'y' : 200, 't' : e1, 'c' : 32, 'f' : 3 , 'h' : 50, 's' : 0})

while True:
  clock.tick(100)
  keys=pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
 
  if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
    sys.exit()
  frame += 1
  screen.fill(BLACK)

  bg_x += bg_speed_x
  if bg_x > bg_w:
    bg_x -= bg_w
  if bg_x < 0:
    bg_x += bg_w

  bg_y += bg_speed_y
  if bg_y > bg_h:
    bg_y -= bg_h
  if bg_y < 0:
    bg_y += bg_h
    
  x = round(bg_x)
  y = round(bg_y)
  screen.blit(bg, (x, y))
  screen.blit(bg, (x - bg_w, y))
  screen.blit(bg, (x - bg_w, y - bg_h))
  screen.blit(bg, (x, y - bg_h))
 
 #ship
  t_shift = 0
  show_t = (frame % 20) > 5
  s = ship
  if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    ship_x -= 3
    show_t = False
  if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    ship_x += 3
    show_t = True
  if keys[pygame.K_UP] or keys[pygame.K_w]:
    ship_y -= 3
    s = ship_up
    t_shift = 3
  if keys[pygame.K_DOWN] or keys[pygame.K_s]:
    ship_y += 3
    s = ship_down
    t_shift = -3


  screen.blit(s, (ship_x, ship_y - 7 + t_shift))
  if show_t:
    screen.blit(thruster, (ship_x- 8, ship_y - 1))
 
 
#laser

  points = []
  
  
  h = smooth_m - 800
  
  h = max(0, min(h * 0.3, 100.0))
  f = smooth_f/450
  
  f = max(1.0, min(1.0 + (f - 1.0) * 5, 10.0))
  for i in xrange(100):
    x = i * 5 + ship_x
    points.append( (x, ship_y + math.sin(x * 0.01 * f) * h))
    
  
  pygame.draw.lines(screen, (255, 255, 255),  False, points, 3)
  pygame.draw.lines(screen, (0, 0, 255),  False, points, 1)
  
  
#enemies

  for e in enemies:
    fr = frame - e['s']
    x = e['x'] - fr * 0.5
    y = e['y']
    h = e['h']
    f = e['f']
    t = e['t']
    c = e['c']
    if x < -14 * c - 8:
        e['s'] = frame
    for i in xrange(c):
        m = len(t) * 2 - 2
        tf = int(fr * 0.07 + i * 0.4) % m
        if tf >= len(t):
            tf = len(t) * 2 - 2 - tf
        s = math.sin(x * 0.01 * f) 
        screen.blit(t[tf], (x,  y + s * h))
        x += (-abs(s) * 0.1 + 1.5) * 10
  
  pygame.display.flip()
  if stream.get_read_available() >= chunk:
    data = stream.read(chunk)
    Frequency, m=Pitch(data)
    n = 0.05
    smooth_m = smooth_m * (1.0 - n) + m * n
    smooth_f = smooth_f * (1.0 - n) + Frequency * n
    #print "freq %f vol %d " % (smooth_f, smooth_m)