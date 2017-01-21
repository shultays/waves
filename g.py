import sys, pygame
from matplotlib.mlab import find
import pyaudio
import numpy as np
import math
from random import randint
from random import random

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

pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Waves")

ship=pygame.image.load("ship.png")
ship_up=pygame.image.load("ship_up.png")
ship_down=pygame.image.load("ship_down.png")
thruster=pygame.image.load("ship_thruster.png")

bg=pygame.image.load("bg.png")
bg_2=pygame.image.load("bg_2.png")
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

bg_2_x = 0
bg_2_y = 0
bg_2_w = 960 / 2
bg_2_h = 640 / 2

bg_2_speed_x = -0.05
bg_2_speed_y = 0


Frequency = 0
m = 0
smooth_m = 0
smooth_f = 0
frame = 0

e1 = [ pygame.image.load("e11.png"), pygame.image.load("e12.png"), pygame.image.load("e13.png"), pygame.image.load("e14.png"), pygame.image.load("e15.png") ]
e2 = [ pygame.image.load("e21.png"), pygame.image.load("e22.png"), pygame.image.load("e23.png"), pygame.image.load("e24.png"), pygame.image.load("e25.png"), pygame.image.load("e26.png"), pygame.image.load("e27.png"), pygame.image.load("e28.png"), pygame.image.load("e29.png") ]
e3 = [ pygame.image.load("e31.png"), pygame.image.load("e32.png"), pygame.image.load("e33.png"), pygame.image.load("e34.png"), pygame.image.load("e35.png"), pygame.image.load("e36.png") ]
e4 = [ pygame.image.load("e41.png"), pygame.image.load("e42.png"), pygame.image.load("e43.png"), pygame.image.load("e44.png") ]

etypes = [e1, e2, e3, e4]
rtypes = [True, False, False, True]

enemies = []

r_spawn = random() * 100
while True:
  clock.tick(100)
  keys=pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
 
  if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
    sys.exit()
    
    
  if keys[pygame.K_z] == False:
    frame += 1
  screen.fill((0, 0, 0))

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
  
  bg_2_x += bg_2_speed_x
  if bg_2_x > bg_2_w:
    bg_2_x -= bg_2_w
  if bg_2_x < 0:
    bg_2_x += bg_2_w

  bg_2_y += bg_2_speed_y
  if bg_2_y > bg_2_h:
    bg_2_y -= bg_2_h
  if bg_2_y < 0:
    bg_2_y += bg_2_h
    
  x = round(bg_2_x)
  y = round(bg_2_y)
  for i in xrange(4):
    for j in xrange(4):
        screen.blit(bg_2, (x - bg_2_w * (i - 1), y - bg_2_h * (j - 1)))
    
 
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
  
  
  h = smooth_m - 200
  h = max(0, min(h * 0.1, 100.0))
  f = smooth_f/450
  
  f = max(2.0, min(2.0 + (f - 1.0) * 5, 10.0))

  h = min(100.0, pygame.mouse.get_pos()[1])
  f = max(3.0, min(5.0 - (pygame.mouse.get_pos()[0]) * 0.01, 5.0))
  
  
  s_h = h
  s_f = f
  for i in xrange(200):
    
    sx = ship_x + 22
    x = i * 5 + sx
    
    
    points.append( (x, ship_y + math.sin(x * 0.01 * f) * h * min(1.0, i * 0.2)))
    
  
  pygame.draw.lines(screen, (255, 255, 255),  False, points, 3)
  pygame.draw.lines(screen, (0, 0, 255),  False, points, 1)
  
  
#enemies
  max_enemy = -100
  for e in enemies:
    fr = frame - e['s']
    x = e['x'] - fr * e['sp']
    y = e['y']
    h = e['h']
    f = e['f']
    t = e['t']
    c = e['c']
    r = e['r']
    
    
    if ship_x < x and abs(ship_y - y) < 10 and abs(h - s_h) < 10 and abs(f/s_f - 1.0) < 0.1:
        enemies.remove(e)
        
    for i in xrange(c):
        m = len(t) * 2 - 2

        
        if r:
            tf = int(fr * 0.07 + i * 0.4) % m
            if tf >= len(t):
                tf = len(t) * 2 - 2 - tf
        else:
            tf = int(fr * 0.07 + i * 0.4) % len(t)
        s = math.sin(x * 0.01 * f) 
        screen.blit(t[tf], (x - 8,  y + s * h - 8))
        x += (abs(s) * 0.5 + 1.5) * 12
    max_enemy = max(max_enemy, x)

    if x < -20:
        enemies.remove(e)
  
  if len(enemies) == 0 or frame > r_spawn:
    et = randint(0, len(etypes)-1)
    enemies.append({ 'x' : 700 + random() * 40, 'y' : random() * 280 + 100, 't' : etypes[et], 'r' : rtypes[et], 'c' : randint(8, 16), 'f' : 3 + random() * 2 , 'h' : 20 + random() * 40, 's' : frame, 'sp' : 0.3 + random() * 0.3})
    r_spawn = random() * 500 + 500 + frame

  pygame.display.flip()
  if stream.get_read_available() >= chunk:
    data = stream.read(chunk)
    Frequency, m=Pitch(data)
    n = 0.05
    smooth_m = smooth_m * (1.0 - n) + m * n
    smooth_f = smooth_f * (1.0 - n) + Frequency * n
    #print "freq %f vol %d " % (smooth_f, smooth_m)