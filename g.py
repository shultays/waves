import sys, pygame
from matplotlib.mlab import find
import pyaudio
import numpy as np
import math
from random import randint
from random import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
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


infoObject = pygame.display.Info()
ww = infoObject.current_w / 2
wh = infoObject.current_h / 2
screen = pygame.display.set_mode((ww, wh), pygame.DOUBLEBUF | pygame.NOFRAME )

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

bg_speed_x = -6.15
bg_speed_y = 0

bg_2_x = 0
bg_2_y = 0
bg_2_w = 960 / 2
bg_2_h = 640 / 2

bg_2_speed_x = -4.05
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
pygame.mouse.set_visible(False)

etypes = [e1, e2, e3, e4]
rtypes = [True, False, False, True]

enemdata = []
z = 0
for e in etypes:
    enemy = {}
    enemy['img'] = e
    enemy['r'] = rtypes[z]
    
    red = []
    green = []
    blue = []
    for img in e:
        
        ri = img.copy()
        ar = pygame.PixelArray (ri)

        if ri.mustlock():
            self.assertTrue (ri.get_locked ())

            
        length = len(ar)
        length2 = len(ar[0])
        for i in xrange(length):
            for j in xrange(length2):
                ar[i][j] = ar[i][j] & 0xFF0000FF
        del ar

        if ri.mustlock():
            self.assertFalse (ri.get_locked ())

        red.append(ri)
        
        gi = img.copy()
        ar = pygame.PixelArray (gi)

        if gi.mustlock():
            self.assertTrue (gi.get_locked ())

            
        length = len(ar)
        length2 = len(ar[0])
        for i in xrange(length):
            for j in xrange(length2):
                ar[i][j] = ar[i][j] & 0xFF00FF00
        del ar

        if gi.mustlock():
            self.assertFalse (gi.get_locked ())

        green.append(gi)
        

        bi = img.copy()
        ar = pygame.PixelArray (bi)

        if bi.mustlock():
            self.assertTrue (bi.get_locked ())

            
        length = len(ar)
        length2 = len(ar[0])
        for i in xrange(length):
            for j in xrange(length2):
                ar[i][j] = ar[i][j] & 0xFFFF0000
        del ar

        if bi.mustlock():
            self.assertFalse (bi.get_locked ())

        blue.append(bi)
    z += 1
    
    
    enemy['red'] = red
    enemy['green'] = green
    enemy['blue'] = blue
    enemdata.append(enemy)


enemies = []

min_h = 20
max_h = 120

stars = []

for i in xrange(int(ww*wh/3000)):
    x = random() * (ww + 200) - 100
    y = random() * (wh + 100) - 50
    
    r = randint(100, 155)
    g = randint(100, 155)
    b = randint(100, 155)
    t = randint(0, 2)
    if t == 0:
        r = 155
    elif t == 1:
        g = 155
    else:
        b = 155
    stars.append([x, y, random() * 0.7 + 0.3, r, g, b])

r_spawn = random() * 100
while True:
  clock.tick(150)
  keys=pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
 
  if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
    sys.exit()
    
    
  if keys[pygame.K_z] == False:
    frame += 1
  screen.fill((0, 0, 0))

  
 #ship
  t_shift = 0
  show_t = (frame % 20) > 5
  img = ship
  if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    ship_x -= 4
    show_t = False
  if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    ship_x += 4
    show_t = True
  if keys[pygame.K_UP] or keys[pygame.K_w]:
    ship_y -= 3
    img = ship_up
    t_shift = 3
  if keys[pygame.K_DOWN] or keys[pygame.K_s]:
    ship_y += 3
    img = ship_down
    t_shift = -3

  if ship_x < 20:
    ship_x = 20
    
  if ship_x > max(200, ww/2):
    ship_x = max(200, ww/2)
  
  
  s_shift = 0
  if ship_y < 20:
    ship_y = 20
    s_shift = 3
  if ship_y > wh - 40:
    ship_y = wh - 40
    s_shift = -3
  
  
  for s in stars:
    s[0] -= 0.25 * s[2]
    if s[0] < -100:
        s[0] += ww + 200
        s[1] = random() * (wh + 100) - 50
        
    if s_shift != 0:
        s[1] += 0.05 * s[2] * s_shift
        if s[1] < -50:
            s[1] += wh + 100
            s[0] = random() * (ww + 200) - 100
        if s[1] > wh + 50:
            s[1] -= wh + 100
            s[0] = random() * (ww + 200) - 100
    pygame.draw.rect(screen, (s[3], s[4], s[5]), (s[0], s[1], 5 * s[2], 5 * s[2]))
  
  screen.blit(img, (ship_x, ship_y - 7 + t_shift))
  if show_t:
    screen.blit(thruster, (ship_x- 8, ship_y - 1))
 
 
#laser

  points = []
  
  
  h = smooth_m - 100
  h = max(0, min(h * 0.15, max_h + 50))
  f = smooth_f/450
  
  f = max(3.0, min(3.0 + (f - 1.0) * 2, 50.0))

  #h = min(100.0, pygame.mouse.get_pos()[1])
  #f = max(3.0, min(5.0 - (pygame.mouse.get_pos()[0]) * 0.01, 5.0))
  f = 3
  s_h = h
  s_f = f
  
  for i in xrange(550):
    
    sx = ship_x + 22
    x = i * 3 + sx
    
    
    points.append( (x, ship_y + math.sin(i * 3 * 0.01 * f) * s_h * min(1.0, i * 0.1)))
    
  
  pygame.draw.lines(screen, (155, 155, 155),  False, points, 3)
  pygame.draw.lines(screen, (0, 0, 200),  False, points, 1)
  
  
#enemies
  max_enemy = -100
  for e in enemies:
    fr = frame - e['s']
    sx = x = e['x'] - fr * e['sp']
    y = e['y']
    h = e['h']
    f = e['f']
    sh = e['shift']
    t = enemdata[e['et']]['img']
    red = enemdata[e['et']]['red']
    green = enemdata[e['et']]['green']
    blue = enemdata[e['et']]['blue']
    r = enemdata[e['et']]['r']
    c = e['c']
    
    hits = False

    red_shift = max(0.0, min(1.0, (abs(ship_y - y) - 7) / 100.0))
    blue_shift =  max(0.0, min(1.0, (abs(s_h - h) - 10) / 10.0))
    n = (sh + ship_x + 22) * 0.01 * f * 0.5 / math.pi
    n = abs(n - round(n))
    green_shift = max(0.0, min(1.0, n * 2.0 - 0.4))
    
    
    if green_shift + red_shift + blue_shift < 0.01:
        e['hp'] -= 0.15
        if e['hp'] <= 0:
            e['hp'] = 0.0
            hits = True
    else:
        e['hp'] += 0.02
        if e['hp'] >= 1.0:
            e['hp'] = 1.0
            
            
    for i in xrange(c):
        m = len(t) * 2 - 2

        if x > ship_x + 20 and hits:
            e['c'] = i
            break
        
        if r:
            tf = int(fr * 0.07 + i * 0.4) % m
            if tf >= len(t):
                tf = len(t) * 2 - 2 - tf
        else:
            tf = int(fr * 0.07 + i * 0.4) % len(t)
        s = math.sin((x + sh) * 0.01 * f) 
        
        a = frame / 30.0
        d = 10
        screen.blit(red[tf], (x - 8 + math.sin(a) * red_shift * d,  y + s * h - 8 + math.cos(a) * red_shift * d), None, pygame.BLEND_RGB_MAX )
        a += math.pi * 0.66
        screen.blit(blue[tf], (x - 8 + math.sin(a) * blue_shift * d,  y + s * h - 8 + math.cos(a) * blue_shift * d), None, pygame.BLEND_RGB_MAX )
        a += math.pi * 0.66
        screen.blit(green[tf], (x - 8 + math.sin(a) * green_shift * d,  y + s * h - 8 + math.cos(a) * green_shift * d), None, pygame.BLEND_RGB_MAX )
        
        
        screen.blit(t[tf], (x - 8,  y + s * h - 8) ) 
        
        x += (abs(s) * 0.5 + 1.5) * 12
    max_enemy = max(max_enemy, x)

    if x < -20 or e['c'] == 0:
        enemies.remove(e)
  
  if len(enemies) == 0 or frame > r_spawn:
    et = randint(0, len(etypes)-1)
    
    enemies.append({ 'shift' : random() * 100, 'hp' : 1.0, 'x' : ww + 20 + random() * 40, 'y' : random() * (wh - 300) + 150, 'et' : et, 'c' : randint(8, 16), 'f' : 3 + random() * 0 , 'h' : min_h + random() * (max_h - min_h), 's' : frame, 'sp' : 0.7 + random() * 0.7})
    r_spawn = random() * 300 + 400 + frame

  pygame.display.flip()
  if stream.get_read_available() >= chunk:
    data = stream.read(chunk)
    Frequency, m=Pitch(data)
    n = 0.05
    smooth_m = smooth_m * (1.0 - n) + m * n
    smooth_f = smooth_f * (1.0 - n) + Frequency * n
    #print "freq %f vol %d " % (smooth_f, smooth_m)