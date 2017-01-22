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
pygame.mixer.init()
music = pygame.mixer.Sound("grad.ogg")
music.set_volume(0.35)
music.play(loops = -1)


exps = pygame.mixer.Sound("exp.wav")
exps.set_volume(0.65)

beep = pygame.mixer.Sound("beep.wav")
beep.set_volume(0.35)

point_lose = pygame.mixer.Sound("point_lose.wav")
point_lose.set_volume(0.15)

lost = pygame.mixer.Sound("lost.wav")
lost.set_volume(0.85)

infoObject = pygame.display.Info()

sc = 1
ww = infoObject.current_w / sc
wh = infoObject.current_h / sc
screen = pygame.display.set_mode((ww, wh), pygame.DOUBLEBUF | pygame.NOFRAME )

pygame.display.set_caption("Waves")

ship=pygame.image.load("ship.png")
ship_up=pygame.image.load("ship_up.png")
ship_down=pygame.image.load("ship_down.png")
thruster=pygame.image.load("ship_thruster.png")

clock = pygame.time.Clock()
 
ship_x = 50
ship_y = wh / 2

start_x = ship_x
start_y = ship_y

Frequency = 0
m = 0
smooth_m = 0
smooth_f = 0
frame = 0
frame_2 = 0
e1 = [ pygame.image.load("e11.png"), pygame.image.load("e12.png"), pygame.image.load("e13.png"), pygame.image.load("e14.png"), pygame.image.load("e15.png") ]
e2 = [ pygame.image.load("e21.png"), pygame.image.load("e22.png"), pygame.image.load("e23.png"), pygame.image.load("e24.png"), pygame.image.load("e25.png"), pygame.image.load("e26.png"), pygame.image.load("e27.png"), pygame.image.load("e28.png"), pygame.image.load("e29.png") ]
e3 = [ pygame.image.load("e31.png"), pygame.image.load("e32.png"), pygame.image.load("e33.png"), pygame.image.load("e34.png"), pygame.image.load("e35.png"), pygame.image.load("e36.png") ]
e4 = [ pygame.image.load("e41.png"), pygame.image.load("e42.png"), pygame.image.load("e43.png"), pygame.image.load("e44.png") ]
pygame.mouse.set_visible(False)

exp = [ pygame.image.load("big_exp_1.png"), pygame.image.load("big_exp_2.png"), pygame.image.load("big_exp_3.png"), pygame.image.load("big_exp_4.png"), pygame.image.load("big_exp_5.png"), pygame.image.load("big_exp_6.png"), pygame.image.load("big_exp_7.png") ]
etypes = [e1, e2, e3, e4]
rtypes = [True, False, False, True]
explosions = []

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
max_h = 90


m_t = 0

enemy_score = 0
hit_points = 100

stars = []
menu_bg = ""
bg_size = [750, 537]
def resize():
    global menu_bg
    global stars
    global bg_size
    global start_y
    start_y = wh / 2
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
    menu_bg = pygame.image.load("waveshift.jpg")
    bg_size = [750, 537]
    if bg_size[0] < ww:
        bg_size[1] = int(bg_size[1]  * float(ww) / bg_size[0])
        bg_size[0] = ww
    if bg_size[1] < wh:
        bg_size[0] = int(bg_size[0]  * float(wh) / bg_size[1])
        bg_size[1] = wh

    menu_bg = pygame.transform.scale(menu_bg, bg_size)
resize()
r_spawn = random() * 100

menu = 1
score = 0


play_c = 0

released = True
menu_sh = 30
basicfont = pygame.font.Font("game_over.ttf", 64)
option = 0

h_minus = 15
h_mult = 5
sc_pressed = False
music_pressed = False
while True:
  clock.tick(150)
  play_c -= 1
  keys=pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
 
  if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
    sys.exit()
  frame_2 += 1
    
  if keys[pygame.K_F2]:
    if music_pressed == False:
        music_pressed = True
        music.stop()
        music.play(loops = -1)
  else:
    music_pressed = False
  if keys[pygame.K_F5]:
    hit_points = -1
  if keys[pygame.K_F10]:
    if sc_pressed == False:
        sc_pressed = True
        sc = 3 - sc
        ww = infoObject.current_w / sc
        wh = infoObject.current_h / sc
        screen = pygame.display.set_mode((ww, wh), pygame.DOUBLEBUF | pygame.NOFRAME )
        resize()
  else:
    sc_pressed = False
  if keys[pygame.K_KP_PLUS]:
    h_minus += 1
    print(h_minus)
  if keys[pygame.K_KP_MINUS]:
    h_minus -= 1
    print(h_minus)
  h_minus = max(1, min(1000, h_minus))

  if keys[pygame.K_KP_DIVIDE]:
    h_mult /= 1.001
    print(h_mult)
  if keys[pygame.K_KP_MULTIPLY]:
    h_mult *= 1.001
    print(h_mult)
  h_mult = max(0.1, min(10.0, h_mult))
  
  if keys[pygame.K_z] == False and menu == 0:
    frame += 1
  screen.fill((0, 0, 0))
  ss = 0
  if wh > 650:
    ss = (wh - 650) * 0.1
  if menu == 1:
    screen.blit(menu_bg, ((bg_size[0] - ww) * -0.5, (bg_size[1] - wh) * -0.3))

    pygame.draw.rect(screen, (0, 0, 0), (screen.get_rect().w * 0.5 - 100, screen.get_rect().h - 93 - ss, 200, 85))
    
    text = basicfont.render('Start Game', True, (200, 200, 200))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.y = screen.get_rect().h - 90.0 - ss
    oldrect = textrect
    screen.blit(text, textrect)

    text = basicfont.render('Tutorial', True, (200, 200, 200))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.y = screen.get_rect().h - 60.0 - ss
    screen.blit(text, textrect)
    
    
    screen.blit(ship, (screen.get_rect().w * 0.5 - 90 + option * 20, screen.get_rect().h - 75 - ss + option * 30))
    pygame.display.flip()

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if released:
            released = False
            option -= 1
            if option < 0:
                option = 0
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if released:
            released = False
            option += 1
            if option > 1:
                option = 1
    elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
  
        if released:
            ship_x = start_x
            ship_y = start_y
            if option == 0:
                menu = 0
                enemy_score = 0
                hit_points = 100
                enemies = []
                explosions = []
                frame = 0
            else:
                menu = 2
            released = False
            m_t = 0.0
    else:
        released = True
    continue
    
  elif menu == 2 or menu == 3 or menu == 4 or menu == 5:
    m_t += 0.004
    max_t = 2.0
    if menu < 4:
        max_t = 1.4
    if menu == 4:
        max_t = 4.0
        
    if menu == 5:
        max_t = 3.2
        
    if m_t > max_t:
        m_t = 0.0
        if menu != 2:
            enemies = [{ 'shift' : -70, 'hp' : 1.0, 'x' : 400 + ss * 10, 'y' : wh / 2, 'et' : 0, 'c' : 20, 'f' : 3, 'h' : 50, 's' : frame, 'sp' : 0.0}]
            explosions = []

    move_t = max(0.0, 0.5 - m_t)
    
    if menu == 4:
        move_t = max(move_t, m_t - 1.4)
        move_t = min(move_t, 1.0)
    
    if menu == 2:
        ship_x = start_x + 100 * move_t + ss * 5
    else:
        ship_x = start_x + ss * 5
        
    ship_y = start_y + 150 * move_t
    if menu == 5:
        ship_x = start_x + 200 * 0.4  + ss * 5
        ship_y = start_y + 50 * 0.4
        menu_sh = 20
        if m_t > 0.2:
            ship_y = start_y + 50 * min(1.0, max(0.0, 0.6 - m_t))
        if m_t > 0.8:
            ship_x = start_x + 200 * max(0.0, 1.2 - m_t) + ss * 5
        if m_t > 1.8:
            menu_sh = 50 - 30 * max(0.0, 2.6 - m_t) / 0.8
    if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
        if released:
            enemies = []
            explosions = []
            menu += 1
            m_t = 5.0
            released = False
                    
            ship_x = start_x  + ss * 5
            ship_y = start_y
    else:
        released = True
        
  elif menu == 6:
    if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
        if released:
            menu = 0
            enemy_score = 0
            hit_points = 100
            frame = 0
            released = False
    else:
        released = True
  elif menu == 7:
    text = basicfont.render('Final Score : ' + str(score), True, (200, 200, 200))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery
    screen.blit(text, textrect)
    if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
        if released:
            menu = 1
            released = False
            music.play(loops = -1)
    else:
        released = True
    pygame.display.flip()
    continue
 #ship
  t_shift = 0
  show_t = (frame % 20) > 5
  img = ship
  if menu == 0 or menu == 6:
      if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ship_x -= 3
        show_t = False
      if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ship_x += 3
        show_t = True
      if keys[pygame.K_UP] or keys[pygame.K_w]:
        ship_y -= 2
        img = ship_up
        t_shift = 3
      if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        ship_y += 2
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
  
  diff = frame / 12000.0
  
  if diff > 1.0:
    diff = 1.0
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

  if menu == 2:
      text = basicfont.render('Use WASD to move around', True, (200, 200, 200))
      textrect = text.get_rect()
      textrect.centerx = screen.get_rect().centerx
      textrect.centery = screen.get_rect().centery - 150 - ss * 5
      screen.blit(text, textrect)

  elif menu == 3:
      text = basicfont.render('Keep your "Sonic Wave Gun" on your enemies', True, (200, 200, 200))
      textrect = text.get_rect()
      textrect.centerx = screen.get_rect().centerx
      textrect.centery = screen.get_rect().centery - 150 - ss * 5
      screen.blit(text, textrect)
      
  elif menu == 4:
      text = basicfont.render('If your gun is not synced with enemy wave, you deal minimum damage', True, (200, 200, 200))
      textrect = text.get_rect()
      textrect.centerx = screen.get_rect().centerx
      textrect.centery = screen.get_rect().centery - 150 - ss * 5
      screen.blit(text, textrect)

      text = basicfont.render('And enemy ship can repair themselves', True, (200, 200, 200))
      textrect = text.get_rect()
      textrect.centerx = screen.get_rect().centerx
      textrect.centery = screen.get_rect().centery - 120 - ss * 4
      screen.blit(text, textrect)
  
  elif menu == 5:
    text = basicfont.render('Move vertically to center the enemy wave', True, (200, 50, 50))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery - 200 - ss * 5
    screen.blit(text, textrect)
  
    text = basicfont.render('Move horizontally to overlap your wavelength with enemy wave', True, (50, 200, 50))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery - 160 - ss * 4
    screen.blit(text, textrect)
    
    text = basicfont.render('Use your microphone to align your wave amplitude with enemies', True, (50, 50, 200))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery - 120 - ss * 3
    screen.blit(text, textrect)
    
    text = basicfont.render('If you properly align your gun, you kill entire wave instantly!', True, (200, 200, 200))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery + 160 + ss * 5
    screen.blit(text, textrect)
    
    
  elif menu == 6:
  
    text = basicfont.render('Test your skills!', True, (200, 200, 200))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery - 200 - ss * 5
    screen.blit(text, textrect)
  
    text = basicfont.render('Hit SPACE to start game', True, (50, 200, 50))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery - 160 - ss * 5
    screen.blit(text, textrect)
    
  elif menu == 0:
    score = int(frame/400) * 10 + enemy_score * 20
    text = basicfont.render('Score: ' + str(score), True, (200, 200, 200))
    textrect = text.get_rect()
    textrect.x = 14.0
    textrect.y = 14.0
    screen.blit(text, textrect)
    text = basicfont.render('Hitpoints: ' + str(hit_points), True, (200, 200, 200))
    textrect = text.get_rect()
    textrect.x = 14.0
    textrect.y = 44.0
    screen.blit(text, textrect)
  
  if menu > 0 and menu < 6:
        text = basicfont.render('Press SPACE to continue', True, (200, 200, 200))
        textrect = text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery + 200 + ss * 5
        screen.blit(text, textrect)
#laser

  points = []
  
  
  h = smooth_m - h_minus
  h = max(0, min(h * h_mult, max_h + 50))
  f = smooth_f/450
  
  f = max(3.0, min(3.0 + (f - 1.0) * 2, 50.0))

  #h = min(100.0, pygame.mouse.get_pos()[1])
  #f = max(3.0, min(5.0 - (pygame.mouse.get_pos()[0]) * 0.01, 5.0))
  f = 3
  s_h = h
  s_f = f

  if menu == 2 or menu == 3:
    s_h = 50
  if menu == 4:
    s_h = 33
  if menu == 5:
    s_h = menu_sh
  for i in xrange(650):
    sx = ship_x + 22
    x = i * 3 + sx
    points.append( (x, ship_y + math.sin(i * 3 * 0.01 * f) * s_h * min(1.0, i * 0.1)))
    
  pygame.draw.lines(screen, (155, 155, 155),  False, points, 3)
  pygame.draw.lines(screen, (0, 0, 200),  False, points, 1)
  
  
#enemies
  max_enemy = -100
  for e in enemies:
    fr = frame - e['s']
    fr2 = frame_2 - e['s']
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

    red_shift = max(0.0, min(1.0, (abs(ship_y - y) - 7) / 30.0))
    blue_shift =  max(0.0, min(1.0, (abs(s_h - h) - 15) / 10.0))
    n = (sh + ship_x + 22) * 0.01 * f * 0.5 / math.pi
    n = abs(n - round(n))
    green_shift = max(0.0, min(1.0, n * 2.0 - 0.15))
    
    if ('hpm' in e) == False:
        e['hpm'] = []
            
        for i in xrange(c):
            e['hpm'].append(1.0)
        
    hpm = e['hpm']
    if green_shift + red_shift + blue_shift < 0.01:
        hits = True
    else:
        e['hp'] += 0.02
        if e['hp'] >= 1.0:
            e['hp'] = 1.0
            
    playedbeep = False
    for i in xrange(c):
    
        if hpm[i] > 0.0:
            if i > 0:
                alive2 =  hpm[i-1] > 0
                hpm[i-1] += 0.002
                if alive2 == False and hpm[i-1] > 0 and playedbeep == False:
                    beep.stop()
                    beep.play()
                    playedbeep = True
                    hpm[i-1] = 1.0
            if i < c-1:
                alive2 =  hpm[i+1] > 0
                hpm[i+1] += 0.002
                if alive2 == False and hpm[i+1] > 0 and playedbeep == False:
                    beep.stop()
                    beep.play()
                    playedbeep = True
                    hpm[i+1] = 1.0
    all_dead = True
    
    for i in xrange(c):
        m = len(t) * 2 - 2

            
        if r:
            tf = int(fr2 * 0.07 + i * 0.4) % m
            if tf >= len(t):
                tf = len(t) * 2 - 2 - tf
        else:
            tf = int(fr2 * 0.07 + i * 0.4) % len(t)
        s = math.sin((x + sh) * 0.01 * f) 
        alive = hpm[i] > 0.0
        if hpm[i] > 1.0:
            hpm[i] = 1.0
            
        if x > ship_x + 20 and hits:
            hpm[i] -= 0.3
            if hpm[i] < 0.0:
                hpm[i] = -100000.0
                if play_c < 0 and alive:
                    play_c = 20
                    exps.play()
                if alive:
                    enemy_score += 4
                    explosions.append([x,  y + s * h, frame_2])
        elif x > ship_x + 40 and x < ww + 10:
            laser_y =  math.sin((x - ship_x - 22) * 0.01 * f) * s_h + ship_y
            if abs(laser_y - (y + s * h)) < 6:
                hpm[i] -= 0.02 + (1.0 - diff) * 0.01
                if hpm[i] < 0.0:
                    hpm[i] = -1.0
                    if play_c < 0 and alive:
                        play_c = 20
                        exps.play()
                    if alive:
                        enemy_score += 1
                        explosions.append([x,  y + s * h, frame_2])
        
    
        if hpm[i] < -1.0 and hpm[i] > -1000.0:
            hpm[i] = -1.0
        if hpm[i] > 0.0:

            all_dead = False
            a = frame_2 / 50.0
            d = 10
            screen.blit(red[tf], (x - 8 + math.sin(a) * red_shift * d,  y + s * h - 8 + math.cos(a) * red_shift * d), None, pygame.BLEND_RGB_MAX )
            a += math.pi * 0.66
            screen.blit(blue[tf], (x - 8 + math.sin(a) * blue_shift * d,  y + s * h - 8 + math.cos(a) * blue_shift * d), None, pygame.BLEND_RGB_MAX )
            a += math.pi * 0.66
            screen.blit(green[tf], (x - 8 + math.sin(a) * green_shift * d,  y + s * h - 8 + math.cos(a) * green_shift * d), None, pygame.BLEND_RGB_MAX )
            
            
            screen.blit(t[tf], (x - 8,  y + s * h - 8) ) 
        if x < -10 and hpm[i] > -1000.0:
            if hpm[i] > 0.0:
                hit_points -= 5
                point_lose.stop()
                point_lose.play()
            hpm[i] = -100000.0
        x += (abs(s) * 0.5 + 1.5) * 12
    max_enemy = max(max_enemy, x)

    if all_dead or x < -20 or e['c'] == 0 and menu == 0:
        enemies.remove(e)
 
  for e in explosions:
    t = int((frame_2 - e[2]) / 12)
    if t >= len(exp):
        explosions.remove(e)
    else:
        screen.blit(exp[t], (e[0] - 8, e[1] - 8) ) 
    
  if menu == 0 and (len(enemies) == 0 or frame > r_spawn):
    et = randint(0, len(etypes)-1)
    
    enemies.append({ 'shift' : random() * 100, 'hp' : 1.0, 'x' : ww + 20 + random() * 40, 'y' : random() * (wh - 300) + 150, 'et' : et, 'c' : randint(8, 16), 'f' : 3 + random() * 0 , 'h' : min_h + random() * (max_h - min_h), 's' : frame, 'sp' : (0.5 + random() * 1.0) * (diff * 0.6 + 0.4) })
    r_spawn = random() * 150 + 150 + frame + (1.0 - diff) * 600
  
  if menu == 0 and hit_points <= 0:
    menu = 7
    enemies = []
    explosions = []
    option = 0
    
    music.stop()
    exps.stop()
    beep.stop()
    point_lose.stop()
    lost.play()
    
  pygame.display.flip()
  if stream.get_read_available() >= chunk:
    data = stream.read(chunk)
    Frequency, m=Pitch(data)
    n = 0.05
    smooth_m = smooth_m * (1.0 - n) + m * n
    smooth_f = smooth_f * (1.0 - n) + Frequency * n
    #print "freq %f vol %d " % (smooth_f, smooth_m)