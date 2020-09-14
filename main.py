''' Avengers vs Justice League '''

# main.py
# Owen Huang, Filip Vucak, Matthew Liu

######################## MODULES ########################
from glob import glob
from math import *
from pprint import pprint
from pygame import *
from pygame.locals import *
from random import *
import os
import threading
import sys

######################## COLOURS ########################
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
YELLOW = (255, 255,   0)
ORANGE = (255, 128,   0)
GREEN  = (  0, 255,   0)
BLUE   = (  0,   0, 255)
PURPLE = (128,   0, 128)
BROWN  = (100,  40,  40)
BLACK  = (  0,   0,   0)

######################## VARIABLES ########################
os.environ['SDL_VIDEO_WINDOW_POS'] = '50, 30' # window location

screen_res = (1200, 700)
screen = display.set_mode(screen_res, DOUBLEBUF)

running = True
clock = time.Clock()
gamemode = 'START'

display.set_caption('AVENGERS vs. JUSTICE LEAGUE')

######################## IMAGES ########################
fireballLogo  = image.load("Images\\Special\\fireball.png")
lightningLogo = image.load("Images\\Special\\lightning.png")
tornadoLogo   = image.load("Images\\Special\\tornado.png")
tornadoLogo   = transform.scale(tornadoLogo, (30, 40))

tornado   = []
lightning = []
fireball  = []

for i in range(10):
    tornado.append(image.load("Images\\Special\\tornado" + str(i) + ".png"))

for i in range(10):
    lightning.append(image.load("Images\\Special\\lightning" + str(i) + ".png"))

for i in range(16):
    fireball.append(image.load("Images\\Special\\fireball" + str(i) + ".png"))

######################## CLASSES ########################
class Tower:
    def __init__(self, cost, damage, reload):
        self.cost   = int(cost)
        self.dmg    = int(damage)
        self.reload = int(reload)
        self.time = 0
        
    def __getitem__(self, i):
        self.feats = [self.cost, self.dmg, self.reload]
        return self.feats[i]
    
    def buy(self):
        return self.cost
    
class Npc:
    
    def __init__(self, health, damage, place):
        self.hp     = int(health)
        self.health = int(health)
        self.speed  = -0.5
        self.dmg    = int(damage)
        
        self.x, self.y = place
        
    def move(self):
        self.x += self.speed
        
    def hit(self, damage):
        self.hp -= int(damage)
        if self.hp <= 0:
            self.hp = 0
    
    def __getitem__(self, i):
        # returns item in list that corresponds to entered index
        self.feats = [self.x, self.y]
        return self.feats[i]

    def get_health(self):
        return self.hp

    def original_hp(self):
        return self.health

class Bullet:
    def __init__(self, point, kind):
        self.kind = kind # tower index
        self.pos = point # original pos (static)
        self.v = 10
        self.x, self.y = point # actual pos (changing)

    def get_type(self):
        return self.kind

    def get_pos(self):
        return self.pos # original pos

    def __getitem__(self, i):
        self.rect = Rect(self.x, self.y, 5, 5)
        return self.rect[i]
    
    def move(self):
        self.x += self.v
        
######################## GENERAL FUNCTIONS ########################
def check_x(List):
    ''' if all x values in a list are less than 100, returns true '''
    for i in range(len(List)):
        if List[i][0] > 100:
            return False
    return True

def full(List, item):
    ''' checks if all item in a list are the same '''
    for i in List:
        try: # supports 2D lists
            for j in i:
                if j != item:
                    return False
        except IndexError:
            if i != item:
                return False
    return True

def game_over():
    ''' game over screen '''
    FONT  = font.Font('Fonts\\ubuntu.ttf', 70)
    text  = FONT.render('GAME OVER!!', True, WHITE)
    text2 = FONT.render('MENU', True, WHITE)

    backRect = Rect(300, 200, 500, 300)
    menuRect = Rect(400, 350, 300, 100)

    running = True
    click = False
    
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN and menuRect.collidepoint(mx, my):
                click = True
            if click is True and evt.type == MOUSEBUTTONUP:
                if menuRect.collidepoint(mx, my):
                    global gamemode
                    gamemode = 'START'
                    running = False
                else:
                    click = False
                
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        
        draw.rect(screen, BLACK, backRect, 0)
        draw.rect(screen, WHITE, backRect, 2)
        draw.rect(screen, BLUE, menuRect, 0)
        
        if menuRect.collidepoint(mx, my):
            draw.rect(screen, RED, menuRect, 0)
            
        screen.blit(text, (330, 200))
        screen.blit(text2, (450, 360))

        display.flip()
        
def loading(num):
    ''' draws the loading bar at different percent for num / 10 '''
    FONT = font.Font('Fonts\\ubuntu.ttf', 70)
    text = FONT.render('LOADING...', True, YELLOW)

    screen.fill(BLACK)
    screen.blit(text, (400, 150))

    rects = []
    for i in range(10):
        w = (i / 10) * 1000
        rects.append(Rect(100, 600, w, 5))
    
    draw.rect(screen, YELLOW, rects[num], 0)
    display.update()
    
def no_money():
    ''' message displayed when player has insufficient funds '''
    FONT = font.Font('Fonts\\ubuntu.ttf', 70)
    text = FONT.render('NOT ENOUGH MONEY!!', True, YELLOW)
    screen.blit(text, (250, 280))
    display.update()
    time.wait(1000)
    
def overlap(rect, rect1):
    ''' determines how much area of a rect is overlapping on another '''

    x,   y,  w,  h = rect
    x1, y1, w1, h1 = rect1

    if x1 <= x  and y1 <= y and (x + w) <= (x1 + w1) and (y + h) <= (y1 + h1):
        # rect is completely inside rect1
        return w * h
    if x <= x1  and y <= y1 and (x1 + w1) <= (x + w) and (y1 + h1) <= (y + h):
        # rect1 is completely inside rect
        return w1 * h1
    if x <= x1 <= x + w: # left side of rect1 is in rect
        if y <= y1 <= y + h: # top of rect1 is in rect
            area1 = (x + w - x1) * (y + h - y1)
            return area1
        if y1 <= y <= y1 + h: # top of rect is in rect1
            area1 = (x + w - x1) * (y1 + h1 - y)
            return area1
    if x1 <= x <= x1 + w1: # left side of rect is in rect1
        if y <= y1 <= y + h: # top of rect1 is in rect
            area1 = (x1 + w1 - x) * (y + h - y1)
            return area1
        if y1 <= y <= y1 + h: # top of rect is in rect1
            area1 = (x1 + w1 - x) * (y1 + h1 - y)
            return area1
    return 0
    
def pause_menu():
    clock = time.Clock()
    #### MENU OBJECTS ####
    ''' translucent background '''
    menu = Surface(screen_res)
    menu.set_alpha(150)
    menu.fill((255,255,255))
    ''' rects '''
    pauseRect = Rect(300, 200, 500, 300)
    
    homeRect = Rect(475,220,150,75)
    exitRect = Rect(475,370,150,75)
    Xrect    = Rect(750,200,50,25)
    #### TEXT ####
    helFont1=font.SysFont("Helvetica",35)
    exitTXT=helFont1.render("Exit", True, (0,0,0))
    homeTXT=helFont1.render("Menu", True, (0,0,0))
    
    FONT = font.Font('Fonts\\ubuntu.ttf', 25)
    text = FONT.render('X', True, WHITE)
        
    screen.blit(menu, (0, 0))
    ########
    click1 = False
    click2 = False
    click3 = False
    paused = True
    while paused:
        
        mx, my = mouse.get_pos()
        mb     = mouse.get_pressed()

        ########
        for evt in event.get():
            if evt.type == QUIT:
                paused = False
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    paused = False

            # user has to click and release while on exitRect
            if evt.type == MOUSEBUTTONDOWN and exitRect.collidepoint(mx, my):
                click1 = True
            if click1 is True and evt.type == MOUSEBUTTONUP:
                if exitRect.collidepoint(mx, my):
                    global gamemode
                    gamemode = 'QUIT'
                    paused = False
                else:
                    click1 = False
                    
            # click and release
            if evt.type == MOUSEBUTTONDOWN and homeRect.collidepoint(mx, my):
                click2 = True
            if click2 is True and evt.type == MOUSEBUTTONUP:
                if homeRect.collidepoint(mx, my):
                    paused = False
                    gamemode = 'START'
                else:
                    click2 = False

            # click and release
            if evt.type == MOUSEBUTTONDOWN and Xrect.collidepoint(mx, my):
                click3 = True
            if click3 is True and evt.type == MOUSEBUTTONUP:
                if Xrect.collidepoint(mx, my):
                    paused = False
                else:
                    click3 = False
                    
        #### DRAW ####
        draw.rect(screen, BLACK, pauseRect, 0)
        draw.rect(screen, BLUE, pauseRect, 2)
        ''' buttons '''
        draw.rect(screen, (250,250,210), exitRect, 0)
        draw.rect(screen, (250,250,210), homeRect, 0)
        draw.rect(screen, RED, Xrect, 0)
        
        if exitRect.collidepoint(mx,my):
            draw.rect(screen, BLUE, exitRect, 0)
        if homeRect.collidepoint(mx,my):
            draw.rect(screen, BLUE, homeRect, 0)
        if Xrect.collidepoint(mx,my):
            draw.rect(screen, (255, 128, 128), Xrect, 0)
            
        screen.blit(homeTXT, (515,240))
        screen.blit(exitTXT, (515,390))
        screen.blit(text, (765,198))

        display.flip()
        clock.tick(60)
    
def pointer(x, y, size):
    ''' draw crosshairs at a point '''
    draw.circle(screen, BLACK, (x, y), size, 1)
    draw.line(screen, BLACK, (x - size, y), (x + size, y), 1)
    draw.line(screen, BLACK, (x, y - size), (x, y + size), 1)
    
def rect_corner(x, y, rect):
    ''' determines how far x, y is
    from the top left of a rect '''

    w, h, a, b = rect
    out1 = x - w
    out2 = y - h

    return out1, out2
            
def return_mouse(rect, mouse):
    ''' if the mouse coordinates are outside
    the rect, move the mouse back to the nearest
    point inside the rect'''
    
    checkx = False
    checky = False
    x, y = mouse
    l, t, w, h = rect
    
    if x < l: # left of rect
        x = l
    elif x > l + w: # right of rect
        x = l + w
    
    if y < t: # above rect
        y = t
    elif y > t + h: # below rect
        y = t + h

    return x, y


def special1():
    ''' special attack 1
    fire balls '''
    m = 120
    attack1 = True
    screenshot = screen.copy()
    frame1 = 0
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
        mx,my = mouse.get_pos()
        mb    = mouse.get_pressed()
        if attack1:
            m += 30
            screen.blit(screenshot, (0,0))
            for i in range(5):
                if m-i*250 >= 150:
                    screen.blit(fireball[frame1] , (m-i*250,150)) # lane 1
                    screen.blit(fireball[frame1] , (m-i*250,230)) # 2
                    screen.blit(fireball[frame1] , (m-i*250,310)) # 3
                    screen.blit(fireball[frame1] , (m-i*250,390)) # 4
                    screen.blit(fireball[frame1] , (m-i*250,470)) # 5
                    screen.blit(fireball[frame1] , (m-i*250,550)) # 6
            frame1 +=1
            display.flip()
            if frame1 == 16:
                frame1 = 0
            if m-i*250>1100:
                running=False
        elif not attack1:
            screen.blit(screenshot , (0,0))
        display.flip()
        clock.tick(30)

def special2():
    ''' special attack 2
    lightning '''
    d = 170
    attack2 = True
    screenshot = screen.copy()
    frame2 = 0
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
        mx,my = mouse.get_pos()
        mb    = mouse.get_pressed()
        if attack2:
            screen.blit(screenshot , (0,0))
            screen.blit(lightning[frame2] , (d,160))
            d = d + 100
            frame2 += 1
            if frame2 == 10:
                frame2 == 0
                running = False
        elif not attack2:
            screen.blit(screenshot , (0,0))
        display.flip()
        clock.tick(10)
        
def special3():
    ''' special attack 3
    tornado '''
    l = 120
    attack3 = True
    screenshot = screen.copy()
    frame3 = 0
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
        mx,my = mouse.get_pos()
        mb    = mouse.get_pressed()
        if attack3:
            l += 30
            screen.blit(screenshot,(0,0))
            for u in range(1):
                if l-u*250>=150:
                    screen.blit(tornado[frame3] , (l-u*250,150)) 
                    screen.blit(tornado[frame3] , (l-u*250,230))
                    screen.blit(tornado[frame3] , (l-u*250,310))
                    screen.blit(tornado[frame3] , (l-u*250,390))
                    screen.blit(tornado[frame3] , (l-u*250,470))
                    screen.blit(tornado[frame3] , (l-u*250,550))
            frame3 += 1
            display.flip()
            if frame3 == 10:
                frame3 = 0
            if l-u*250>=1100:
                running=False
            elif not attack3:
                screen.blit(screenshot , (0,0))
        display.flip()
        clock.tick(20)

def upgrade_msg(Bool):
    ''' False --> already
    True --> success '''
    
    FONT = font.Font('Fonts\\ubuntu.ttf', 70)
    
    if Bool is True:
        text1 = FONT.render('SUCCESSFULLY UPGRADED', True, YELLOW)
        screen.blit(text1, (200, 280))
        display.update()
        time.wait(1000)
        
    if Bool is False:
        text2 = FONT.render('ALREADY UPGRADED', True, YELLOW)
        screen.blit(text2, (250, 280))
        display.update()
        time.wait(1000)

def win():
    ''' win screen '''
    FONT  = font.Font('Fonts\\ubuntu.ttf', 70)
    text  = FONT.render('YOU WIN!!', True, WHITE)
    text2 = FONT.render('MENU', True, WHITE)

    backRect = Rect(300, 200, 500, 300)
    menuRect = Rect(400, 350, 300, 100)

    running = True
    click = False
    
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            # user has to click and release 
            if evt.type == MOUSEBUTTONDOWN and menuRect.collidepoint(mx, my):
                click = True
            if click is True and evt.type == MOUSEBUTTONUP:
                if menuRect.collidepoint(mx, my):
                    global gamemode
                    gamemode = 'START'
                    running = False
                else:
                    click = False
                
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        
        draw.rect(screen, BLACK, backRect, 0)
        draw.rect(screen, WHITE, backRect, 2)
        draw.rect(screen, BLUE, menuRect, 0)
        
        if menuRect.collidepoint(mx, my):
            draw.rect(screen, RED, menuRect, 0)
            
        screen.blit(text, (380, 200))
        screen.blit(text2, (450, 360))

        display.flip()
    
######################## GAME FUNCTIONS ########################
    
def play_avengers():    
    #### TEXT ####
    font.init()
    helFont=font.SysFont("Helvetica",30)
    helFont1=font.SysFont("Helvetica",25)
    smallFont=font.SysFont("Helvetica",20)
    
    moneyTXT=helFont.render("Money:", True, WHITE)
    levelTXT=helFont.render("Level:", True, WHITE)
    pauseTXT=helFont.render("Pause", True, BLACK)
    startTXT = helFont.render('START', True, WHITE)
    upgradeTXT=helFont.render("Upgrades", True, BLACK)

    loading(0)
    #### IMAGES ####
    avengersback1 = transform.flip(transform.scale(image.load('Images\\avengers base 2.png'), (1200, 700)), True, False).convert_alpha()
    
    icon1 = transform.scale(image.load('Icons\\Avengers\\hawkeye.png'), (50, 50))
    icon2 = transform.scale(image.load('Icons\\Avengers\\spiderman.png'), (50, 50))
    icon3 = transform.scale(image.load('Icons\\Avengers\\hulk.png'), (50, 50))
    icon4 = transform.scale(image.load('Icons\\Avengers\\quicks.png'), (50, 50))
    icon5 = transform.scale(image.load('Icons\\Avengers\\capamerica.png'), (50, 50))
    icon6 = transform.scale(image.load('Icons\\Avengers\\ironman.png'), (50, 50))
    icon7 = transform.scale(image.load('Icons\\Avengers\\thor.png'), (50, 50))
    icons = [icon1, icon2, icon3, icon4,
             icon5, icon6, icon7]
    
    # towers
    
    loading(1)
    
    hawk_sprites = []
    esprites1 = glob('Images\\Avengers\\hawkeye\\*.png')
    esprites1.sort()
    for pic in esprites1:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 1.1), int(img1.get_height() * 1.1)))
        hawk_sprites.append(transform.flip(img2, False, False).convert_alpha())

    spider_sprites = []
    esprites2 = glob('Images\\Avengers\\spiderman\\attacking\\*.png')
    esprites2.sort()
    for pic in esprites2:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 0.6), int(img1.get_height() * 0.6)))
        spider_sprites.append(transform.flip(img2, False, False).convert_alpha())
                              
    loading(2)
    
    hulk_sprites = []
    esprites3 = glob('Images\\Avengers\\hulk\\*.png')
    esprites3.sort()
    for pic in esprites3:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 0.9), int(img1.get_height() * 0.9)))
        hulk_sprites.append(transform.flip(img2, False, False).convert_alpha())

    silver_sprites = []
    esprites4 = glob('Images\\Avengers\\quick_silver\\*.png')
    esprites4.sort()
    for pic in esprites4:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 0.65), int(img1.get_height() * 0.65)))
        silver_sprites.append(transform.flip(img2, False, False).convert_alpha())

    loading(3)
                              
    america_sprites = []
    esprites5 = glob('Images\\Avengers\\cap_america\\*.png')
    esprites5.sort()
    for pic in esprites5:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 1.1), int(img1.get_height() * 1.1)))
        america_sprites.append(transform.flip(img2, False, False).convert_alpha())

    iron_sprites = []
    esprites6 = glob('Images\\Avengers\\iron_man\\*.png')
    esprites6.sort()
    for pic in esprites6:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 1.6), int(img1.get_height() * 1.6)))
        iron_sprites.append(transform.flip(img2, False, False).convert_alpha())

    loading(4)
    
    thor_sprites = []
    esprites7 = glob('Images\\Avengers\\thor\\*.png')
    esprites7.sort()
    for pic in esprites7:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 1.3), int(img1.get_height() * 1.3)))
        thor_sprites.append(transform.flip(img2, False, False).convert_alpha())
    
    ########
    
    cyborg_sprites = []
    sprites1 = glob('Images\\Justice League\\cyborg\\*.png')
    sprites1.sort()
    for pic in sprites1:
        cyborg_sprites.append(transform.flip(image.load(pic), True, False).convert_alpha())
        
    loading(5)
    
    flash_sprites = []
    sprites2 = glob('Images\\Justice League\\flash\\*.png')
    sprites2.sort()
    for pic in sprites2:
        flash_sprites.append(transform.flip(image.load(pic), True, False).convert_alpha())
        
    green_sprites = []
    sprites3 = glob('Images\\Justice League\\green_lantern\\*.png')
    sprites3.sort()
    for pic in sprites3:
        p = image.load(pic).convert_alpha()
        p2 = transform.scale(p, (int(p.get_width() * 1.5), int(p.get_height() * 1.5)))
        green_sprites.append(transform.flip(p2, True, False).convert_alpha())
        
    loading(6)
    
    aqua_sprites = []
    sprites4 = glob('Images\\Justice League\\aquaman\\*.png')
    sprites4.sort()
    for pic in sprites4:
        p = image.load(pic).convert_alpha()
        p2 = transform.scale(p, (int(p.get_width() * 0.85), int(p.get_height() * 0.85)))
        aqua_sprites.append(transform.flip(p2, True, False).convert_alpha())
        
    woman_sprites = []
    sprites5 = glob('Images\\Justice League\\wonder_woman\\*.png')
    sprites5.sort()
    for pic in sprites5:
        woman_sprites.append(transform.flip(image.load(pic), True, False).convert_alpha())

    loading(7)
    
    batman_sprites = []
    sprites6 = glob('Images\\Justice League\\batman\\running\\*.png')
    sprites6.sort()
    for pic in sprites6:
        batman_sprites.append(transform.flip(image.load(pic), True, False).convert_alpha())
        
    superman_sprites = []
    sprites7 = glob('Images\\Justice League\\superman\\*.png')
    sprites7.sort()
    for pic in sprites7:
        superman_sprites.append(transform.flip(image.load(pic), True, False).convert_alpha())

    loading(8)
    #### RECTS ####
    startRect   = Rect(1040, 300, 151, 100)
    upgradeRect = Rect( 900,  30, 130,  30)
    
    ''' empty grid for turrets (2-D list) '''
    turretSlots = []
    for x in range(8):
        turretx = x * (70 + 20) # x * (width + space b/w boxes)
        turretColumn = []
        for y in range(6):
            turrety = y * (70 + 10) # y * (height + space b/w boxes)
            turretColumn.append(Rect(200 + turretx, 120 + turrety, 70, 70))
        turretSlots.append(turretColumn)
        
    ''' aesthetics '''
    turretField   = Rect( 200, 120,  700, 470)
    dividerRect   = Rect(   0,  80, 1200,  10)
    dividerRect2  = Rect(   0, 630, 1200,  10)
    pauseRect     = Rect(1070,  30,  100,  30)
    
    ''' turret buttons '''
    turrets = []
    for i in range(7):
        x = 40 + (i * 80)
        turrets.append(Rect(x, 15, 50, 50))

    ''' special attacks '''
    specialattack1rect=Rect(965,645,50,50)
    specialattack2rect=Rect(1045,645,50,50)
    specialattack3rect=Rect(1125,645,50,50)
    
    loading(9)
    #### TOWER CLASSES ####
    towers = open('Towers/avengers1.txt', 'r').readlines()
    for i in towers:
        towers[towers.index(i)] = i.strip('\n').split(' ')
    hawk    = Tower(towers[0][1], towers[0][2], towers[0][3]) # sets as Tower class
    spider  = Tower(towers[1][1], towers[1][2], towers[2][3]) # cost, damage, reload
    hulk    = Tower(towers[2][1], towers[2][2], towers[2][3])
    silver  = Tower(towers[3][1], towers[3][2], towers[3][3])
    captain = Tower(towers[4][1], towers[4][2], towers[4][3])
    iron    = Tower(towers[5][1], towers[5][2], towers[5][3])
    thor    = Tower(towers[6][1], towers[6][2], towers[6][3])
    
    towers = [hawk, spider, hulk, silver, captain, iron, thor]
    
    #### NPC CLASSES ####
    enemy_stats = open('Towers/justice1.txt', 'r').read().split('\n')
    
    ''' strip extra text ''' 
    for i in range(len(enemy_stats)):
        enemy_stats[i] = enemy_stats[i][enemy_stats[i].find(' ') + 1 : enemy_stats[i].rfind(' ')]

    ''' convert to 2D list '''
    for i in range(len(enemy_stats)):
        enemy_stats[i] = enemy_stats[i].split(' ') 

    ''' convert str to int '''
    for i in range(len(enemy_stats)):
        for j in range(len(enemy_stats[i])):
            enemy_stats[i][j] = int(enemy_stats[i][j])
    
    enemy_count = open('Towers/npc.txt', 'r').read().split(' ') # creates list
    for i in range(len(enemy_count)):
        enemy_count[i] = int(enemy_count[i]) # convert each item inside list to int

    #### VARIABLES ####
    ''' bools '''
    check       = False
    l_click     = False
    r_click     = False
    pause       = False
    playing     = True
    ready       = False # when to send the enemies
    set_bullets = False
    set_npcs    = False
    start_hover = False
    specattack1 = True
    specattack2 = True
    specattack3 = True
    upgrade     = False
    
    ''' ints '''
    castle = 500 # castle hp
    money = 700
    level = 1
    
    ''' lists '''
    arrow_points = [(1090, 325), (1090 + 100, 325), (1090 + 100, 325 + 50),
                    (1090, 325 + 50), (1090, 325 + 75), (1040, 350), (1090, 325 - 25)]
    bullets = []
    collideTurrets = [False, False, False, False, False, False, False]
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]
    distTurrets = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    turretEmpty = [[0] * 6 for i  in range(8)] # 0 represents the empty turret slots
    upgraded    = [False, False, False, False, False, False, False]
    
    ''' other '''
    mx, my = mouse.get_pos()
    mb     = mouse.get_pressed()
    
    ''' sprites '''
    frames = [13, 89, 0, 0, 0,  4, 1]

    # Idling
    sprite_max    = [14, 93, 2, 2, 2, 12, 8]
    sprite_min    = [13, 89, 0, 0, 0,  4, 1]
    sprite_speed  = [0.02, 0.12, 0.1, 0.1, 0.1, 0.25, 0.2]
    sprite_off    = [(5, -15), (10, -10), (10, -5), (15, 0), (5, -20), (15, -15), (5, 0)] # x, y offset
    
    # Attacking
    fire_max    = [28, 62, 7, 41, 25, 86, 16]
    fire_min    = [23, 56, 4, 36, 22, 77,  9]
    fire_speed  = [0.3, 0.2, 0.25, 0.15, 0.2, 0.1, 0.2]
    fire_off    = [(5, -25), (10, 20), (12, -10), (15, -5), (5, -20), (15, -50), (5, -10)] # x, y offset
    sprite_reload = 40
    reload_time = 0
    sprite_fire = [False, False, False, False, False, False, False]
    
    tower_sprites = [hawk_sprites, spider_sprites, hulk_sprites, silver_sprites, america_sprites, iron_sprites, thor_sprites]

    # Bullets
    bullet_max   = [19, 65, 48, 163, 26, 104, 18]
    bullet_min   = [18, 70, 47, 163, 26, 103, 17]
    bullet_off   = [(-25, -27), (-15, -17), (-40, 25), (-5, -25), (-10, -30), (-5, -30), (0, -50)]
    bullet_speed = [0.1, 0.1, 0.1, 0.1, 0.3, 0.2, 0.1]
    bullet_frame = []
    for i in range(7):
        bullet_frame.append(bullet_min[i])

    # Enemy
    walk_sprites = [cyborg_sprites, flash_sprites, green_sprites, aqua_sprites, woman_sprites, batman_sprites, superman_sprites]
    walk_max   = [19, 14, 21, 25, 14, 5, 40]
    walk_min   = [12,  9,  6, 21,  9, 0, 40]
    walk_off   = [(0, -23), (0, -40), (0, -28), (-10, -35), (0, -50), (0, -40), (0, -60)]
    walk_speed = [0.25, 0.17, 0.22, 0.15, 0.15, 0.15, 0.15]
    walk_frame = []
    for i in range(7):
        walk_frame.append(walk_min[i])
    
    #### LOCAL FUNCTIONS ####    
    def background1():
        SLOT = (128, 128, 128) # gray
        
        #### DRAW ####
        screen.blit(avengersback1, (0, 0)) # background

        ''' grid '''
        if l_click is True and turretField.collidepoint(mx, my):
            for i in collideTurrets:
                if i is True: # if clicking on turrets
                    for x in turretSlots: # then draw the grid
                        for y in x:
                            draw.rect(screen, WHITE, y, 1)
                    break # grid was drawn, so break
                
        ''' aesthetics '''
        draw.rect(screen, SLOT, dividerRect)
        draw.rect(screen, SLOT, dividerRect2)
        draw.rect(screen, YELLOW, pauseRect)
        draw.rect(screen, YELLOW, upgradeRect)
        
        ''' tower choices '''
        for x, y, w, h in turrets:
            rect = Rect(x, y, w, h)
            if collideTurrets[turrets.index(rect)] is True:
                continue
            screen.blit(icons[turrets.index(rect)], (x, y))
            if rect.collidepoint(mx, my):
                draw.rect(screen, WHITE, rect, 1)
        
        ''' text '''
        screen.blit(pauseTXT, (1085,25))
        screen.blit(moneyTXT,(40,650))
        screen.blit(levelTXT,(250,650))
        screen.blit(upgradeTXT, (910,25))
        
    def check_slots(rect):
        ''' checks which turret slots are colliding and returns index'''
        out = []
        for i in range(len(turretSlots)):
            for j in range(len(turretSlots[i])):
                if rect.colliderect(turretSlots[i][j]):
                    out.append((i,j))
        return out
    
    def collide_turrets(point):
        ''' checks which turret is colliding with a point '''
        x, y = point
        for i in range(len(turretEmpty)):
            for j in range(len(turretEmpty[i])):
                if turretEmpty[i][j] != 0:
                    if turretSlots[i][j].collidepoint(x, y):
                        return True
        return False

    def confirm_sell(kind):
        return towers[kind][0]

    def create_bullets():
        out = []
        for x in range(len(turretEmpty)):
            for y in range(len(turretEmpty[x])):
                tower_type = turretEmpty[x][y]
                if tower_type != 0:
                    bullet = Bullet((turretSlots[x][y][0] + 70, turretSlots[x][y][1] + 35), tower_type - 1) # (bullet x, y), tower index
                    out.append(bullet)
        return out

    def info(team, num):
        ''' 0 --> avengers
        1 --> justice league '''
        
        avengers1 = ['Hawkeye', 'Spiderman', 'Hulk', 'Quicksilver',
                     'Captain America', 'Ironman', 'Thor']
        avengers2 = towers
            
        justice1 = ['Cyborg', 'The Flash', 'Green Lantern', 'Aquaman',
                     'Wonder Woman', 'Batman', 'Superman']
        justice2 = open('Towers/justice1.txt', 'r').readlines()
        for i in justice2:
            justice2[justice2.index(i)] = i.strip('\n').split(' ')

        cost = 'Cost: '
        dmg  = 'Damage: '

        if team == 0:
            return avengers1[num], cost + str(avengers2[num][0]), dmg + str(avengers2[num][1])

        if team == 1:
            return justice1[num], cost + str(justice2[num][0]), dmg + str(justice2[num][1])
    
    def snap(rect):
        ''' determines which turret slot has the most overlapping
        area with rect and returns the index of that slot '''
        x, y, w, h = rect
        areas = [] # holds the areas
        points = [] # holds the point 
        
        for point in check_slots(rect): # (x, y) in list of points
            areas.append(overlap(rect, turretSlots[point[0]][point[1]])) # add the area of the overlapped rects
            points.append(point) # add some (x, y)

        if len(areas) == 0: # if no slots are colliding
            return (-1, -1)
        
        largest = areas.index(max(areas)) # index of the biggest area
        return points[largest]

    def upgrade_tower(kind, upgraded):
        if upgraded[kind] is False: # if not upgraded
            oldTower = towers[kind]
            newTower = Tower(oldTower[0], oldTower[1] * 1.25, oldTower[2])
            towers[kind] = newTower
            upgraded[kind] = True
            upgrade_msg(True)
            return True, upgraded
        upgrade_msg(False)
        return False, upgraded

    def upgrade_menu(money, upgraded):
        choosing = True
        click = False

        buttonRect = Rect(40, 15, 530, 50)
        choices = []
        for i in range(7):
            x = 40 + (i * 80)
            choices.append(Rect(x, 15, 50, 50)) # 7 towers

        screenshot = screen.copy()

        while choosing:
            # mouse interactions
            mx, my = mouse.get_pos()
            mb     = mouse.get_pressed()
            
            for evt in event.get():
                if evt.type == QUIT:
                    choosing = False
                if evt.type == MOUSEBUTTONDOWN and evt.button == 1:                
                    if not buttonRect.collidepoint(mx, my):
                        click = True
                if click is True and evt.type == MOUSEBUTTONUP and evt.button == 1:
                    if not buttonRect.collidepoint(mx, my):
                        choosing = False
                    else:
                        click = False
                        
            if buttonRect.collidepoint(mx, my):
                click = False

            # drawing
            
            screen.blit(screenshot, (0, 0))
            
            for i in range(7):
                if choices[i].collidepoint(mx, my):
                    draw.rect(screen, GREEN, choices[i], 1)
                    if mb[0] == 1:
                        if money >= towers[i][0]: # if enough money
                            
                            if upgrade_tower(i, upgraded)[0] is True: # if successfully upgraded
                                money -= towers[i][0]
                                display.update()
                                choosing = False
                                
                            else:
                                break
            
            display.update()
        return money, upgraded
    
    ################
    background1()

    preScreen = screen.copy()
    
    def background2():
        
        screen.blit(preScreen, (0, 0))
        
        for x, y, w, h in turrets:
            rect = Rect(x, y, w, h)
            if collideTurrets[turrets.index(rect)] is True:
                continue
            screen.blit(icons[turrets.index(rect)], (x, y))
            if rect.collidepoint(mx, my):
                draw.rect(screen, WHITE, rect, 1)

                ''' tower info '''
                stats = info(0, turrets.index(rect))
                FONT  = font.Font('Fonts\\ubuntu.ttf', 25)
                text1 = FONT.render(str(stats[0]), True, WHITE) # name
                text2 = FONT.render(str(stats[1]), True, WHITE) # cost
                text3 = FONT.render(str(stats[2]), True, WHITE) # damage
                
                screen.blit(text1, (400, 650))
                screen.blit(text2, (text1.get_width() + 400 + 50, 650))
                screen.blit(text3, (text1.get_width() + text2.get_width() + 400 + 100, 650))
                
        if l_click is True and turretField.collidepoint(mx, my):
            for i in collideTurrets:
                if i is True: # if clicking on turrets
                    for x in turretSlots: # then draw the grid
                        for y in x:
                            draw.rect(screen, WHITE, y, 1)
                    break # grid was drawn, so break
        
        moneyNUM  = helFont.render(str(money), True, YELLOW)
        levelNUM  = helFont.render(str(level), True, YELLOW)
        screen.blit(moneyNUM,(130,650))
        screen.blit(levelNUM,(330,650))

                    
    while playing:
        
        ################
        mx, my = mouse.get_pos()
        mb     = mouse.get_pressed()
        
        for evt in event.get():
            if evt.type == QUIT:
                
                playing = False
                global gamemode
                gamemode = 'START'
                
            ''' mouse events '''
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button == 1: # left click
                    l_click = True
                    
                    ''' drag and snap '''
                    for i in range(len(turrets)):
                        if turrets[i].collidepoint(mx, my):
                            distTurrets[i] = rect_corner(mx, my, turrets[i])
                            collideTurrets[i] = True
                            
            if evt.type == MOUSEBUTTONUP:
                
                if evt.button == 1: # left click
                    
                    l_click = False
                    
                    ''' drag and snap '''
                    for i in range(len(turrets)):
                        if collideTurrets[i] is True:
                            if turrets[i].colliderect(turretField):
                                large_x, large_y = snap(turrets[i]) # snap() returns which the slot index in 2d list
                                if (large_x, large_y) == (-1, -1): # if no collisions occur (x, y) = (-1, -1)
                                    continue
                                if turretEmpty[large_x][large_y] == 0: # if that slot is empty
                                    if towers[i].buy() <= money: # if enough money
                                        money -= towers[i].buy()
                                        turretEmpty[large_x][large_y] = i + 1 # slot is now occupied
                                    else:
                                        no_money()
                        distTurrets[i] = (0, 0)
                        collideTurrets[i] = False
                    turrets = []
                    for i in range(7):
                        x = 40 + (i * 80)
                        turrets.append(Rect(x, 15, 50, 50))
                        
                if evt.button == 3: #right click
                    r_click = False
                    
                    ''' clear slot '''
                    for x in range(len(turretEmpty)):
                        for y in range(len(turretEmpty[x])):
                            if turretSlots[x][y].collidepoint(mx, my):
                                if turretEmpty[x][y] != 0:
                                    money += confirm_sell(turretEmpty[x][y] - 1)
                                    turretEmpty[x][y] = 0
                                
            ''' keyboard events '''
            if evt.type == KEYDOWN:
                
                if evt.key == K_ESCAPE:
                    pause_menu()
                    if gamemode != 'PLAY AVENGERS':
                        playing = False
                    
        ################
        ''' upgrades '''
        if upgradeRect.collidepoint(mx, my):
            upgrade = True
        
        ''' pause '''
        if pauseRect.collidepoint(mx, my):
            pause = True

        ######## DRAW ########    
        background2()
        
        ''' health '''
        healthNUM  = smallFont.render('Health', True, RED)
        
        redRect    = Rect(25, 130, 150, 3)
        healthRect = Rect(25, 130, int((castle / 500) * 150), 3)

        draw.rect(screen, RED, redRect, 0)
        draw.rect(screen, GREEN, healthRect, 0)
        
        screen.blit(healthNUM,(25,100))
        
        ''' drag and snap '''
        for i in range(len(turrets)):
            if collideTurrets[i] is True and l_click is True:
                dx, dy = distTurrets[i]
                turrets[i] = Rect(mx - dx, my - dy, turrets[i][2], turrets[i][3])
                img = tower_sprites[i][0] # tower type corresponds to sprite
                w, h = img.get_width(), img.get_width()
                if i ==0 or i == 3 or i == 4:
                    screen.blit(img, (mx - w//2, my - h//2 - 20))
                else:
                    screen.blit(img, (mx - w//2, my - h//2))

        ################        
        if not ready:

            if level > 20:
                win()
                playing = False

            bullets     = []
            set_bullets = False
            set_npcs    = False
            reload_time = 0
            
            ''' sprites '''
            for i in range(len(frames)):
                if int(frames[i]) >= sprite_max[i]: # if that sprite exceeds its frames
                    frames[i] = sprite_min[i]
                frames[i] += sprite_speed[i]

            # DRAW

            ''' arrow '''
            if startRect.collidepoint(mx, my):
                draw.polygon(screen, RED, arrow_points, 0)
                screen.blit(startTXT, (1085, 332))
                    
                if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                    start_hover = True
                
                if l_click == True:
                    draw.polygon(screen, BLUE, arrow_points, 0)
                    screen.blit(startTXT, (1085, 332))
                    
                if start_hover is True and evt.type == MOUSEBUTTONUP and evt.button == 1:
                    ready = True
                    start_hover = False
                    
            else:
                start_hover = False
                draw.polygon(screen, RED, arrow_points, 1)
                screen.blit(startTXT, (1085, 332))

            ''' towers '''
            for x in range(len(turretEmpty)):
                for y in range(len(turretEmpty[x])):
                    
                    if turretEmpty[x][y] != 0 :
                        num    = turretEmpty[x][y] - 1 # index is one less than real number
                        px, py = sprite_off[num] # offset for sprite (sizes vary)
                        pos    = turretSlots[x][y][0] + px, turretSlots[x][y][1] + py
                        
                        screen.blit(tower_sprites[num][int(frames[num])], pos)
        
        #################
        if ready:
            
            ''' sprites '''
            for i in range(len(towers)):
                if sprite_fire[i] is True:
                    frames[i] += fire_speed[i]
                    
                    if int(frames[i]) >= fire_max[i] + 1:
                        frames[i] = fire_min[i]
                        sprite_fire[i] = False

            ''' npc sprites '''
            for i in range(7):
                walk_frame[i] += walk_speed[i]
                
                if int(walk_frame[i]) >= walk_max[i] + 1:
                    walk_frame[i] = walk_min[i]


            ''' bullet sprites '''
            for i in range(7):
                bullet_frame[i] += bullet_speed[i]
                
                if int(bullet_frame[i]) >= bullet_max[i] + 1:
                    bullet_frame[i] = bullet_min[i]

            ''' reloading '''
            if reload_time <= 0:
                sprite_fire = [True, True, True, True, True, True, True]
                reload_time = sprite_reload
                for i in range(len(towers)):
                    frames[i] = fire_min[i] # set all towers to first frame
                set_bullets = False
                    
            ''' set bullets '''
            if set_bullets is False:
                bullets += create_bullets()
                set_bullets = True # bullets were set

            ''' fire bullets '''
            if reload_time <= 0:
                for i in range(len(bullets)):
                    if bullets[i] == None:
                        continue
                    else:
                        bullets[i].move()
                        bullet_type = bullets[i].get_type()
                        bullet_next = Bullet(bullets[i].get_pos(), bullets[i].get_type())
                        bullets.append(bullet_next)
                reload_time = sprite_reload
            else:
                for i in range(len(bullets)):
                    if bullets[i] == None:
                        continue
                    else:
                        bullets[i].move()
                reload_time -= 1

            ''' check bullets '''
            for i in range(len(bullets)):
                if bullets[i] == None:
                    continue
                if bullets[i][0] > screen_res[0] - 100: # if past the max range                    
                    bullets[i] = None

            ''' set npcs '''
            if set_npcs is False:
                npcs = []
                column_count = int(enemy_count[level - 1] / 6)
                lanes = [[0, 0, 0, 0, 0, 0] for i in range(column_count)]
                for x in range(len(lanes)):
                    npcs1 = []
                    
                    for y in range(len(lanes[x])):
                        z       = randint(0, 6)
                        
                        enemy_x = []
                        for i in range(20):
                            enemy_x.append(i * 100 + 10)
                        enemy_y = (120, 200, 280, 360, 440, 520)
                            
                        enemy_place = (screen_res[0] + enemy_x[x], enemy_y[y] + 22)          # (past right of screen, random lane)
                        enemy       = Npc(enemy_stats[z][0], enemy_stats[z][1], enemy_place) # health, dmg, (x, y)
                        npcs1.append(enemy)
                        
                        lanes[x][y] = z # stores npc type
                        
                    npcs.append(npcs1) # appends to 2D list
                    
                set_npcs = True
                
            ''' move npcs '''
            for enemies in npcs:
                for enemy in enemies:
                    if enemy != None: # if not dead
                        enemy.move()
            
            ''' check npcs'''
            if set_npcs is True:
                for x in range(len(turretEmpty)):
                    for y in range(len(turretEmpty[x])):
                        for enemies in npcs:
                            for enemy in enemies:
                                if enemy != None: # if not dead
                                    if turretSlots[x][y].collidepoint(enemy[0], enemy[1]):
                                        turretEmpty[x][y] = 0

            ''' check bullets '''
            for i in range(len(bullets)):
                if bullets[i] == None:
                    continue
                
                else:
                    if 120 <= bullets[i][1] < 200:   # lane 1
                        lane = 0
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears                            
                        
                    elif 200 <= bullets[i][1] < 280: # lane 2
                        lane = 1 
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears
                                
                    elif 280 <= bullets[i][1] < 360: # lane 3
                        lane = 2
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears
                                
                    elif 360 <= bullets[i][1] < 440: # lane 4
                        lane = 3
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears
                                
                    elif 440 <= bullets[i][1] < 520: # lane 5
                        lane = 4
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears
                                
                    elif 520 <= bullets[i][1] < 600: # lane 6
                        lane = 5
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears

            ''' check npc health '''
            for i in range(len(npcs)):
                for j in range(len(npcs[i])):
                    if npcs[i][j] != None:               # if not dead
                        if npcs[i][j].get_health() <= 0: # if dead
                            money += int(npcs[i][j].original_hp() // 6)   # award money
                            npcs[i][j] = None        # npc is dead
                        else:
                            if npcs[i][j][0] <= 190:
                                castle -= npcs[i][j].get_health()
                                npcs[i][j] = None
                        
            
            ''' npcs '''
            if full(npcs, None) is True: # if all the npcs are dead
                ready = False     # round is over
                level += 1        # advance to next level

            # DRAW
            
            ''' sprites '''
            for x in range(len(turretEmpty)):
                for y in range(len(turretEmpty[x])):
                    if turretEmpty[x][y] != 0 :
                        num = turretEmpty[x][y] - 1
                        if sprite_fire[num] is True:
                            px, py = fire_off[num] # offset for sprite
                            pos = turretSlots[x][y][0] + px, turretSlots[x][y][1] + py
                            screen.blit(tower_sprites[num][int(frames[num])], pos)
                        elif sprite_fire[num] is False:
                            px, py = fire_off[num] # offset for sprite
                            pos = turretSlots[x][y][0] + px, turretSlots[x][y][1] + py
                            screen.blit(tower_sprites[num][fire_min[num]], pos)
            
            ''' bullets '''
            for i in range(len(bullets)):
                
                if bullets[i] != None:
                    bullettype = bullets[i].get_type()
                    sprite        = tower_sprites[bullettype] [int(bullet_frame[bullettype])] # [sprite type] [sprite frame]
                    
                    screen.blit(sprite, (bullets[i][0] + bullet_off[bullettype][0], bullets[i][1] + bullet_off[bullettype][1])) # frame, (x offset, y offset)
                    
            ''' npcs '''
            for i in range(len(npcs)):
                for j in range(len(npcs[i])):
                    if npcs[i][j] != None:

                        sprite = walk_sprites[lanes[i][j]] [int(walk_frame[lanes[i][j]])] # [sprite type] [sprite frame]
                        
                        screen.blit(sprite, (npcs[i][j][0] + walk_off[ lanes[i][j] ] [0], npcs[i][j][1] + walk_off[ lanes[i][j] ][1])) # frame, (x offset, y offset)
            
            ''' special attacks '''
            screen.blit(fireballLogo,(965,650))
            screen.blit(lightningLogo,(1060,645))
            screen.blit(tornadoLogo,(1135,650))
            
            draw.circle(screen, (255,0,0), (990, 670), 25, 3)
            draw.circle(screen, (255,0,0), (1070,670), 25, 3)
            draw.circle(screen, (255,0,0), (1150,670), 25, 3)
            
            if specialattack1rect.collidepoint(mx,my):
                if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                    specattack1 = True
                if l_click == True:
                    screen.blit(fireballLogo,(965,650))
                    draw.circle(screen, WHITE, (990, 670), 25, 3)
                if specattack1 == True and evt.type == MOUSEBUTTONUP and evt.button == 1:
                    if money >= 500:
                        money -= 500
                        special1()
                        specattack1 = False
                        for enemies in npcs:
                            for enemy in enemies:
                                if enemy != None:
                                    enemy.hit(100)
                    else:
                        no_money()
                        specattack1 = False
                    
            elif specialattack2rect.collidepoint(mx,my):
                if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                    specattack2 = True
                if l_click == True:
                    screen.blit(lightningLogo,(1060,645))
                    draw.circle(screen, WHITE, (1070,670), 25, 3)
                if specattack2 == True and evt.type == MOUSEBUTTONUP and evt.button == 1:
                    if money >= 500:
                        money -= 500
                        special2()
                        specattack2 = False
                        for enemies in npcs:
                            for enemy in enemies:
                                if enemy != None:
                                    enemy.hit(100)
                    else:
                        no_money()
                        specattack2 = False
                
            elif specialattack3rect.collidepoint(mx,my):
                if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                    specattack3 = True
                if l_click == True:
                    screen.blit(tornadoLogo,(1135,650))
                    draw.circle(screen, WHITE, (1150,670), 25, 3)
                if specattack3 == True and evt.type == MOUSEBUTTONUP and evt.button == 1:
                    if money >= 500:
                        money -= 500
                        special3()
                        specattack3 = False
                        for enemies in npcs:
                            for enemy in enemies:
                                if enemy != None:
                                    enemy.hit(100)
                    else:
                        no_money()
                        specattack3 = False
                        
        #### DRAW ####        
        if castle <= 0:
            game_over()
            gamemode = 'START'
            playing = False

        ''' upgrades '''
        if upgrade:
            draw.rect(screen, RED, upgradeRect, 0)
            screen.blit(upgradeTXT, (910, 25))
            if l_click is True:
                display.flip()
                money, upgraded = upgrade_menu(money, upgraded)
                l_click = False
            upgrade = False
        
        ''' pause '''
        if pause:
            draw.rect(screen, RED, pauseRect, 0)
            screen.blit(pauseTXT, (1085,25))
            if l_click is True:
                pause_menu()
                if gamemode != 'PLAY AVENGERS':
                    playing = False
                l_click = False
            pause = False

        ################        
        clock.tick(60)
        display.update()

#############################################################################################################

def play_justice():

    loading(0)
    #### TEXT ####
    font.init()
    helFont=font.SysFont("Helvetica",30)
    helFont1=font.SysFont("Helvetica",25)
    smallFont=font.SysFont("Helvetica",20)
    
    moneyTXT=helFont.render("Money:", True, WHITE)
    levelTXT=helFont.render("Level:", True, WHITE)
    pauseTXT=helFont.render("Pause", True, BLACK)
    startTXT = helFont.render('START', True, WHITE)
    upgradeTXT=helFont.render("Upgrades", True, BLACK)
    
    #### IMAGES ####
    base_original = image.load('Images\\justice base 2.png')
    base2 = transform.scale(base_original, (int(base_original.get_width() * 0.8), int(base_original.get_height() * 0.8)))
    base = transform.rotate(base2, 50)
    justiceback1 = transform.scale(image.load('Backgrounds\\Justice league background.jpg'), (1200, 700))
    icon1 = transform.scale(image.load('Icons\\JL\\cyborg.png'), (50, 50))
    icon2 = transform.scale(image.load('Icons\\JL\\flash.png'), (50, 50))
    icon3 = transform.scale(image.load('Icons\\JL\\greenlantern.png'), (50, 50))
    icon4 = transform.scale(image.load('Icons\\JL\\aquaman.png'), (50, 50))
    icon5 = transform.scale(image.load('Icons\\JL\\wonderwomen.png'), (50, 50))
    icon6 = transform.scale(image.load('Icons\\JL\\batman.png'), (50, 50))
    icon7 = transform.scale(image.load('Icons\\JL\\superman.png'), (50, 50))
    icons = [icon1, icon2, icon3, icon4,
             icon5, icon6, icon7]
    
    loading(1)
    # towers
    cyborg_sprites = []
    sprites1 = glob('Images\\Justice League\\cyborg\\*.png')
    sprites1.sort()
    for pic in sprites1:
        cyborg_sprites.append(image.load(pic).convert_alpha())
        
    flash_sprites = []
    sprites2 = glob('Images\\Justice League\\flash\\*.png')
    sprites2.sort()
    for pic in sprites2:
        flash_sprites.append(image.load(pic).convert_alpha())
        
    loading(2)
    
    green_sprites = []
    sprites3 = glob('Images\\Justice League\\green_lantern\\*.png')
    sprites3.sort()
    for pic in sprites3:
        p = image.load(pic).convert_alpha()
        green_sprites.append(transform.scale(p, (int(p.get_width() * 1.5), int(p.get_height() * 1.5))))
        
    aqua_sprites = []
    sprites4 = glob('Images\\Justice League\\aquaman\\*.png')
    sprites4.sort()
    for pic in sprites4:
        p = image.load(pic).convert_alpha()
        aqua_sprites.append(transform.scale(p, (int(p.get_width() * 0.85), int(p.get_height() * 0.85))))
        
    loading(3)
    
    woman_sprites = []
    sprites5 = glob('Images\\Justice League\\wonder_woman\\*.png')
    sprites5.sort()
    for pic in sprites5:
        woman_sprites.append(image.load(pic).convert_alpha())

    batman_sprites = []
    sprites6 = glob('Images\\Justice League\\batman\\*.png')
    sprites6.sort()
    for pic in sprites6:
        batman_sprites.append(image.load(pic).convert_alpha())
        
    loading(4)
    
    superman_sprites = []
    sprites7 = glob('Images\\Justice League\\superman\\*.png')
    sprites7.sort()
    for pic in sprites7:
        superman_sprites.append(image.load(pic).convert_alpha())
    
    ########
    
    hawk_sprites = []
    esprites1 = glob('Images\\Avengers\\hawkeye\\*.png')
    esprites1.sort()
    for pic in esprites1:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 0.8), int(img1.get_height() * 0.8)))
        hawk_sprites.append(transform.flip(img2, True, False).convert_alpha())

    loading(5)
    
    spider_sprites = []
    esprites2 = glob('Images\\Avengers\\spiderman\\running\\*.png')
    esprites2.sort()
    for pic in esprites2:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 1.2), int(img1.get_height() * 1.2)))
        spider_sprites.append(transform.flip(img2, True, False).convert_alpha())

    hulk_sprites = []
    esprites3 = glob('Images\\Avengers\\hulk\\*.png')
    esprites3.sort()
    for pic in esprites3:
        hulk_sprites.append(transform.flip(image.load(pic), True, False).convert_alpha())

    loading(6)
    
    silver_sprites = []
    esprites4 = glob('Images\\Avengers\\quick_silver\\*.png')
    esprites4.sort()
    for pic in esprites4:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 0.65), int(img1.get_height() * 0.65)))
        silver_sprites.append(transform.flip(img2, True, False).convert_alpha())

    america_sprites = []
    esprites5 = glob('Images\\Avengers\\cap_america\\*.png')
    esprites5.sort()
    for pic in esprites5:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 0.8), int(img1.get_height() * 0.8)))
        america_sprites.append(transform.flip(img2, True, False).convert_alpha())

    loading(7)
    
    iron_sprites = []
    esprites6 = glob('Images\\Avengers\\iron_man\\running\\*.png')
    esprites6.sort()
    for pic in esprites6:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 1.5), int(img1.get_height() * 1.5)))
        iron_sprites.append(transform.flip(img2, True, False).convert_alpha())

    thor_sprites = []
    esprites7 = glob('Images\\Avengers\\thor\\running\\*.png')
    esprites7.sort()
    for pic in esprites7:
        img1 = image.load(pic)
        img2 = transform.scale(img1, (int(img1.get_width() * 1.3), int(img1.get_height() * 1.3)))
        thor_sprites.append(transform.flip(img2, True, False).convert_alpha())
    
    loading(8)
    
    #### RECTS ####
    startRect   = Rect(1040, 300, 151, 100)
    upgradeRect = Rect( 900,  30, 130,  30)
    
    ''' empty grid for turrets (2-D list) '''
    turretSlots = []
    for x in range(8):
        turretx = x * (70 + 20) # x * (width + space b/w boxes)
        turretColumn = []
        for y in range(6):
            turrety = y * (70 + 10) # y * (height + space b/w boxes)
            turretColumn.append(Rect(200 + turretx, 120 + turrety, 70, 70))
        turretSlots.append(turretColumn)
        
    ''' aesthetics '''
    turretField   = Rect( 200, 120,  700, 470)
    dividerRect   = Rect(   0,  80, 1200,  10)
    dividerRect2  = Rect(   0, 630, 1200,  10)
    pauseRect     = Rect(1070,  30,  100,  30)
    
    ''' turret buttons '''
    turrets = []
    for i in range(7):
        x = 40 + (i * 80)
        turrets.append(Rect(x, 15, 50, 50))

    ''' special attacks '''
    specialattack1rect=Rect(965,645,50,50)
    specialattack2rect=Rect(1045,645,50,50)
    specialattack3rect=Rect(1125,645,50,50)

    #### TOWER CLASSES ####
    towers = open('Towers/justice1.txt', 'r').readlines()
    for i in towers:
        towers[towers.index(i)] = i.strip('\n').split(' ')
    cyborg   = Tower(towers[0][1], towers[0][2], towers[0][3]) # sets as Tower class
    flash    = Tower(towers[1][1], towers[1][2], towers[2][3]) # cost, damage, reload
    green    = Tower(towers[2][1], towers[2][2], towers[2][3])
    aqua     = Tower(towers[3][1], towers[3][2], towers[3][3])
    woman    = Tower(towers[4][1], towers[4][2], towers[4][3])
    batman   = Tower(towers[5][1], towers[5][2], towers[5][3])
    superman = Tower(towers[6][1], towers[6][2], towers[6][3])
    
    towers = [cyborg, flash, green, aqua, woman, batman, superman]
    
    #### NPC CLASSES ####
    enemy_stats = open('Towers/avengers1.txt', 'r').read().split('\n')
    
    ''' strip extra text ''' 
    for i in range(len(enemy_stats)):
        enemy_stats[i] = enemy_stats[i][enemy_stats[i].find(' ') + 1 : enemy_stats[i].rfind(' ')]

    ''' convert to 2D list '''
    for i in range(len(enemy_stats)):
        enemy_stats[i] = enemy_stats[i].split(' ') 

    ''' convert str to int '''
    for i in range(len(enemy_stats)):
        for j in range(len(enemy_stats[i])):
            enemy_stats[i][j] = int(enemy_stats[i][j])
    
    enemy_count = open('Towers/npc.txt', 'r').read().split(' ') # creates list
    for i in range(len(enemy_count)):
        enemy_count[i] = int(enemy_count[i]) # convert each item inside list to int
        
    #### VARIABLES ####
    ''' bools '''
    check       = False
    l_click     = False
    r_click     = False
    pause       = False
    playing     = True
    ready       = False # when to send the enemies
    set_bullets = False
    set_npcs    = False
    start_hover = False
    specattack1 = True
    specattack2 = True
    specattack3 = True
    upgrade     = False
    
    ''' ints '''
    castle = 500 # castle hp
    money = 700
    level = 1
    
    ''' lists '''
    arrow_points = [(1090, 325), (1090 + 100, 325), (1090 + 100, 325 + 50),
                    (1090, 325 + 50), (1090, 325 + 75), (1040, 350), (1090, 325 - 25)]
    bullets = []
    collideTurrets = [False, False, False, False, False, False, False]
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]
    distTurrets = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    turretEmpty = [[0] * 6 for i  in range(8)] # 0 represents the empty turret slots
    upgraded    = [False, False, False, False, False, False, False]
    
    ''' other '''
    mx, my = mouse.get_pos()
    mb     = mouse.get_pressed()
    
    ''' sprites '''
    frames = [0, 0, 0, 0, 0, 0, 0]
    
    # Idling
    sprite_max    = [6, 4, 5, 4, 4, 4, 4]
    sprite_min    = [0, 1, 1, 1, 1, 1, 2]
    sprite_speed  = [0.2, 0.2, 0.2, 0.15, 0.1, 0.12, 0.12]
    sprite_off    = [(10, -3), (3, -20), (12, 0), (-20, -35), (0, -25), (-5, -20), (-10, -22)] # x, y offset
    
    # Attacking
    fire_max    = [73, 55, 171, 56, 62, 46, 35]
    fire_min    = [69, 51, 166, 54, 57, 41, 32]
    fire_speed  = [0.3, 0.2, 0.25, 0.15, 0.15, 0.2, 0.1]
    fire_off    = [(10, -3), (3, -20), (12, -10), (-40, -15), (0, -25), (-5, -50), (-15, -32)] # x, y offset
    sprite_reload = 40
    reload_time = 0
    sprite_fire = [False, False, False, False, False, False, False]
    
    tower_sprites = [cyborg_sprites, flash_sprites, green_sprites, aqua_sprites, woman_sprites, batman_sprites, superman_sprites]

    # Bullets
    bullet_max   = [107, 59, 87, 74, 81, 67, 52]
    bullet_min   = [107, 56, 87, 74, 78, 64, 52]
    bullet_off   = [(0, -60), (0, -77), (0, -45), (-80, -40), (0, -30), (0, -20), (0, -15)]
    bullet_speed = [0.1, 0.1, 0.1, 0.1, 0.3, 0.2, 0.1]
    bullet_frame = []
    for i in range(7):
        bullet_frame.append(bullet_min[i])

    # Enemy
    walk_sprites = [hawk_sprites, spider_sprites, hulk_sprites, silver_sprites, america_sprites, iron_sprites, thor_sprites]
    walk_max   = [28, 11, 14, 128, 8, 9, 11]
    walk_min   = [23,  0,  9, 126, 3, 1,  0]
    walk_off   = [(0, -35), (0, -20), (0, -35), (0, -35), (0, -25), (0, -15), (0, -25)]
    walk_speed = [0.2, 0.2, 0.1, 0.15, 0.1, 0.15, 0.15]
    walk_frame = []
    for i in range(7):
        walk_frame.append(walk_min[i])
    
    loading(9)
    
    #### LOCAL FUNCTIONS ####    
    def background1():
        SLOT = (128, 128, 128) # gray
        
        #### DRAW ####
        screen.blit(justiceback1, (0, 0)) # background

        ''' grid '''
        if l_click is True and turretField.collidepoint(mx, my):
            for i in collideTurrets:
                if i is True: # if clicking on turrets
                    for x in turretSlots: # then draw the grid
                        for y in x:
                            draw.rect(screen, WHITE, y, 1)
                    break # grid was drawn, so break
                
        ''' aesthetics '''
        draw.rect(screen, SLOT, dividerRect)
        draw.rect(screen, SLOT, dividerRect2)
        draw.rect(screen, YELLOW, pauseRect)
        draw.rect(screen, YELLOW, upgradeRect)
        
        ''' tower choices '''
        for x, y, w, h in turrets:
            rect = Rect(x, y, w, h)
            if collideTurrets[turrets.index(rect)] is True:
                continue
            screen.blit(icons[turrets.index(rect)], (x, y))
            if rect.collidepoint(mx, my):
                draw.rect(screen, WHITE, rect, 1)
        
        ''' text '''
        screen.blit(base, (-230, 70))
        screen.blit(pauseTXT, (1085,25))
        screen.blit(moneyTXT,(40,650))
        screen.blit(levelTXT,(250,650))
        screen.blit(upgradeTXT, (910,25))
        
    def check_slots(rect):
        ''' checks which turret slots are colliding and returns index'''
        out = []
        for i in range(len(turretSlots)):
            for j in range(len(turretSlots[i])):
                if rect.colliderect(turretSlots[i][j]):
                    out.append((i,j))
        return out
    
    def collide_turrets(point):
        ''' checks which turret is colliding with a point '''
        x, y = point
        for i in range(len(turretEmpty)):
            for j in range(len(turretEmpty[i])):
                if turretEmpty[i][j] != 0:
                    if turretSlots[i][j].collidepoint(x, y):
                        return True
        return False

    def confirm_sell(kind):
        return towers[kind][0]

    def create_bullets():
        out = []
        for x in range(len(turretEmpty)):
            for y in range(len(turretEmpty[x])):
                tower_type = turretEmpty[x][y]
                if tower_type != 0:
                    bullet = Bullet((turretSlots[x][y][0] + 70, turretSlots[x][y][1] + 35), tower_type - 1) # (bullet x, y), tower index
                    out.append(bullet)
        return out

    def info(team, num):
        ''' 0 --> avengers
        1 --> justice league '''
            
        justice1 = ['Cyborg', 'The Flash', 'Green Lantern', 'Aquaman',
                     'Wonder Woman', 'Batman', 'Superman']
        justice2 = towers

        cost = 'Cost: '
        dmg  = 'Damage: '

        if team == 0:
            return avengers1[num], cost + str(avengers2[num][0]), dmg + str(avengers2[num][1])

        if team == 1:
            return justice1[num], cost + str(justice2[num][0]), dmg + str(justice2[num][1])
    
    def snap(rect):
        ''' determines which turret slot has the most overlapping
        area with rect and returns the index of that slot '''
        x, y, w, h = rect
        areas = [] # holds the areas
        points = [] # holds the point 
        
        for point in check_slots(rect): # (x, y) in list of points
            areas.append(overlap(rect, turretSlots[point[0]][point[1]])) # add the area of the overlapped rects
            points.append(point) # add some (x, y)

        if len(areas) == 0: # if no slots are colliding
            return (-1, -1)
        
        largest = areas.index(max(areas)) # index of the biggest area
        return points[largest]

    def upgrade_tower(kind, upgraded):
        
        if upgraded[kind] is False: # if not upgraded
            oldTower = towers[kind]
            newTower = Tower(oldTower[0], oldTower[1] * 1.25, oldTower[2])
            towers[kind] = newTower
            upgraded[kind] = True
            upgrade_msg(True)
            return True, upgraded
        upgrade_msg(False)        
        return False, upgraded        

    def upgrade_menu(money, upgraded):
        choosing = True
        click = False

        buttonRect = Rect(40, 15, 530, 50)
        choices = []
        for i in range(7):
            x = 40 + (i * 80)
            choices.append(Rect(x, 15, 50, 50))

        screenshot = screen.copy()

        while choosing:
            # mouse interactions
            mx, my = mouse.get_pos()
            mb     = mouse.get_pressed()
            
            for evt in event.get():
                if evt.type == QUIT:
                    choosing = False
                if evt.type == MOUSEBUTTONDOWN and evt.button == 1:                
                    if not buttonRect.collidepoint(mx, my):
                        click = True
                if click is True and evt.type == MOUSEBUTTONUP and evt.button == 1:
                    if not buttonRect.collidepoint(mx, my):
                        choosing = False
                    else:
                        click = False
                        
            if buttonRect.collidepoint(mx, my):
                click = False

            # drawing
            
            screen.blit(screenshot, (0, 0))
            
            for i in range(7):
                if choices[i].collidepoint(mx, my):
                    draw.rect(screen, GREEN, choices[i], 1)
                    if mb[0] == 1:
                        if money >= towers[i][0]: # if enough money
                            
                            if upgrade_tower(i, upgraded)[0] is True: # if successfully upgraded
                                money -= towers[i][0]
                                display.update()
                                choosing = False
                                
                            else:
                                break
                
            display.update()
        return money, upgraded
    
    ################
    background1()

    preScreen = screen.copy()
    
    def background2():
        
        screen.blit(preScreen, (0, 0))
        
        for x, y, w, h in turrets:
            rect = Rect(x, y, w, h)
            if collideTurrets[turrets.index(rect)] is True:
                continue
            screen.blit(icons[turrets.index(rect)], (x, y))
            if rect.collidepoint(mx, my):
                draw.rect(screen, WHITE, rect, 1)

                ''' tower info '''
                stats = info(1, turrets.index(rect))
                FONT  = font.Font('Fonts\\ubuntu.ttf', 25)
                text1 = FONT.render(str(stats[0]), True, WHITE) # name
                text2 = FONT.render(str(stats[1]), True, WHITE) # cost
                text3 = FONT.render(str(stats[2]), True, WHITE) # damage
                
                screen.blit(text1, (400, 650))
                screen.blit(text2, (text1.get_width() + 400 + 50, 650))
                screen.blit(text3, (text1.get_width() + text2.get_width() + 400 + 100, 650))
                
        if l_click is True and turretField.collidepoint(mx, my):
            for i in collideTurrets:
                if i is True: # if clicking on turrets
                    for x in turretSlots: # then draw the grid
                        for y in x:
                            draw.rect(screen, WHITE, y, 1)
                    break # grid was drawn, so break
        
        moneyNUM  = helFont.render(str(money), True, YELLOW)
        levelNUM  = helFont.render(str(level), True, YELLOW)
        screen.blit(moneyNUM,(130,650))
        screen.blit(levelNUM,(330,650))

                    
    while playing:
        
        ################
        mx, my = mouse.get_pos()
        mb     = mouse.get_pressed()
        
        for evt in event.get():
            if evt.type == QUIT:
                
                playing = False
                global gamemode
                gamemode = 'START'
                
            ''' mouse events '''
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button == 1:
                    l_click = True
                    
                    ''' drag and snap '''
                    for i in range(len(turrets)):
                        if turrets[i].collidepoint(mx, my):
                            distTurrets[i] = rect_corner(mx, my, turrets[i])
                            collideTurrets[i] = True
                            
            if evt.type == MOUSEBUTTONUP:
                
                if evt.button == 1:
                    
                    l_click = False
                    
                    ''' drag and snap '''
                    for i in range(len(turrets)):
                        if collideTurrets[i] is True:
                            if turrets[i].colliderect(turretField):
                                large_x, large_y = snap(turrets[i]) # snap() returns which the slot index in 2d list
                                if (large_x, large_y) == (-1, -1): # if no collisions occur (x, y) = (-1, -1)
                                    continue
                                if turretEmpty[large_x][large_y] == 0: # if that slot is empty
                                    if towers[i].buy() <= money: # if enough money
                                        money -= towers[i].buy()
                                        turretEmpty[large_x][large_y] = i + 1 # slot is now occupied
                                    else:
                                        no_money()
                        distTurrets[i] = (0, 0)
                        collideTurrets[i] = False
                    turrets = []
                    for i in range(7):
                        x = 40 + (i * 80)
                        turrets.append(Rect(x, 15, 50, 50))
                        
                if evt.button == 3:
                    r_click = False
                    
                    ''' clear slot '''
                    for x in range(len(turretEmpty)):
                        for y in range(len(turretEmpty[x])):
                            if turretSlots[x][y].collidepoint(mx, my):
                                if turretEmpty[x][y] != 0:
                                    money += confirm_sell(turretEmpty[x][y] - 1)
                                    turretEmpty[x][y] = 0
                                
            ''' keyboard events '''
            if evt.type == KEYDOWN:
                
                if evt.key == K_ESCAPE:
                    pause_menu()
                    if gamemode != 'PLAY JUSTICE':
                        playing = False
                    
        ################
        ''' upgrades '''
        if upgradeRect.collidepoint(mx, my):
            upgrade = True
        
        ''' pause '''
        if pauseRect.collidepoint(mx, my):
            pause = True

        ######## DRAW ########    
        background2()
        
        ''' health '''
        healthNUM  = smallFont.render('Health', True, RED)
        
        redRect    = Rect(25, 130, 150, 3)
        healthRect = Rect(25, 130, int((castle / 500) * 150), 3)

        draw.rect(screen, RED, redRect, 0)
        draw.rect(screen, GREEN, healthRect, 0)
        
        screen.blit(healthNUM,(25,100))
        
        ''' drag and snap '''
        for i in range(len(turrets)):
            if collideTurrets[i] is True and l_click is True:
                dx, dy = distTurrets[i]
                turrets[i] = Rect(mx - dx, my - dy, turrets[i][2], turrets[i][3])
                img = tower_sprites[i][0] # tower type corresponds to sprite
                w, h = img.get_width(), img.get_width()
                if i == 3 or i == 4:
                    screen.blit(img, (mx - w//2, my - h//2 - 20))
                else:
                    screen.blit(img, (mx - w//2, my - h//2))

        ################        
        if not ready:

            if level > 20:
                win()
                playing = False

            bullets     = []
            set_bullets = False
            set_npcs    = False
            reload_time = 0
            
            ''' sprites '''
            for i in range(len(frames)):
                if int(frames[i]) >= sprite_max[i]: # if that sprite exceeds its frames
                    frames[i] = sprite_min[i]
                frames[i] += sprite_speed[i]

            # DRAW

            ''' arrow '''
            if startRect.collidepoint(mx, my):
                draw.polygon(screen, RED, arrow_points, 0)
                screen.blit(startTXT, (1085, 332))
                    
                if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                    start_hover = True
                
                if l_click == True:
                    draw.polygon(screen, BLUE, arrow_points, 0)
                    screen.blit(startTXT, (1085, 332))
                    
                if start_hover is True and evt.type == MOUSEBUTTONUP and evt.button == 1:
                    ready = True
                    start_hover = False
                    
            else:
                start_hover = False
                draw.polygon(screen, RED, arrow_points, 1)
                screen.blit(startTXT, (1085, 332))

            ''' towers '''
            for x in range(len(turretEmpty)):
                for y in range(len(turretEmpty[x])):
                    
                    if turretEmpty[x][y] != 0 :
                        num    = turretEmpty[x][y] - 1 # index is one less than real number
                        px, py = sprite_off[num] # offset for sprite (sizes vary)
                        pos    = turretSlots[x][y][0] + px, turretSlots[x][y][1] + py
                        
                        screen.blit(tower_sprites[num][int(frames[num])], pos)
        
        #################
        if ready:
            
            ''' sprites '''
            for i in range(len(towers)):
                if sprite_fire[i] is True:
                    frames[i] += fire_speed[i]
                    
                    if int(frames[i]) >= fire_max[i] + 1:
                        frames[i] = fire_min[i]
                        sprite_fire[i] = False

            ''' npc sprites '''
            for i in range(7):
                walk_frame[i] += walk_speed[i]
                
                if int(walk_frame[i]) >= walk_max[i] + 1:
                    walk_frame[i] = walk_min[i]


            ''' bullet sprites '''
            for i in range(7):
                bullet_frame[i] += bullet_speed[i]
                
                if int(bullet_frame[i]) >= bullet_max[i] + 1:
                    bullet_frame[i] = bullet_min[i]

            ''' reloading '''
            if reload_time <= 0:
                sprite_fire = [True, True, True, True, True, True, True]
                reload_time = sprite_reload
                for i in range(len(towers)):
                    frames[i] = fire_min[i] # set all towers to first frame
                set_bullets = False
                    
            ''' set bullets '''
            if set_bullets is False:
                bullets += create_bullets()
                set_bullets = True # bullets were set

            ''' fire bullets '''
            if reload_time <= 0:
                for i in range(len(bullets)):
                    if bullets[i] == None:
                        continue
                    else:
                        bullets[i].move()
                        bullet_type = bullets[i].get_type()
                        bullet_next = Bullet(bullets[i].get_pos(), bullets[i].get_type())
                        bullets.append(bullet_next)
                reload_time = sprite_reload
            else:
                for i in range(len(bullets)):
                    if bullets[i] == None:
                        continue
                    else:
                        bullets[i].move()
                reload_time -= 1

            ''' check bullets '''
            for i in range(len(bullets)):
                if bullets[i] == None:
                    continue
                if bullets[i][0] > screen_res[0] - 100: # if past the max range                    
                    bullets[i] = None

            ''' set npcs '''
            if set_npcs is False:
                npcs = []
                column_count = int(enemy_count[level - 1] / 6)
                lanes = [[0, 0, 0, 0, 0, 0] for i in range(column_count)]
                for x in range(len(lanes)):
                    npcs1 = []
                    
                    for y in range(len(lanes[x])):
                        z       = randint(0, 6)
                        
                        enemy_x = []
                        for i in range(20):
                            enemy_x.append(i * 100 + 10)
                        enemy_y = (120, 200, 280, 360, 440, 520)
                            
                        enemy_place = (screen_res[0] + enemy_x[x], enemy_y[y] + 22)          # (past right of screen, random lane)
                        enemy       = Npc(enemy_stats[z][0], enemy_stats[z][1], enemy_place) # health, dmg, (x, y)
                        npcs1.append(enemy)
                        
                        lanes[x][y] = z # stores npc type
                        
                    npcs.append(npcs1) # appends to 2D list
                    
                set_npcs = True
                
            ''' move npcs '''
            for enemies in npcs:
                for enemy in enemies:
                    if enemy != None: # if not dead
                        enemy.move()
            
            ''' check npcs'''
            if set_npcs is True:
                for x in range(len(turretEmpty)):
                    for y in range(len(turretEmpty[x])):
                        for enemies in npcs:
                            for enemy in enemies:
                                if enemy != None: # if not dead
                                    if turretSlots[x][y].collidepoint(enemy[0], enemy[1]):
                                        turretEmpty[x][y] = 0

            ''' check bullets '''
            for i in range(len(bullets)):
                if bullets[i] == None:
                    continue
                
                else:
                    if 120 <= bullets[i][1] < 200:   # lane 1
                        lane = 0
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears                            
                        
                    elif 200 <= bullets[i][1] < 280: # lane 2
                        lane = 1 
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears
                                
                    elif 280 <= bullets[i][1] < 360: # lane 3
                        lane = 2
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears
                                
                    elif 360 <= bullets[i][1] < 440: # lane 4
                        lane = 3
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears
                                
                    elif 440 <= bullets[i][1] < 520: # lane 5
                        lane = 4
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears
                                
                    elif 520 <= bullets[i][1] < 600: # lane 6
                        lane = 5
                        
                        x = bullets[i][0]
                        y = bullets[i][1]
                        
                        for j in range(len(npcs)):
                            if npcs[j][lane] != None:
                                lane_pos = j
                                break
                            else:
                                lane_pos = None
                                
                        if lane_pos != None:
                            npcRect = Rect(npcs[lane_pos][lane][0], npcs[lane_pos][lane][1], 40, 40)
                            
                            if npcRect.collidepoint(x, y):
                                bullet_kind = bullets[i].get_type()
                                tower_dmg   = towers[bullet_kind][1]
                                
                                npcs[lane_pos][lane].hit(tower_dmg)
                                
                                bullets[i] = None # npc is hit so bullet disappears

            ''' check npc health '''
            for i in range(len(npcs)):
                for j in range(len(npcs[i])):
                    if npcs[i][j] != None:               # if not dead
                        if npcs[i][j].get_health() <= 0: # if dead
                            money += int(npcs[i][j].original_hp() // 6)   # award money
                            npcs[i][j] = None        # npc is dead
                        else:
                            if npcs[i][j][0] <= 190:
                                castle -= npcs[i][j].get_health()
                                npcs[i][j] = None
                        
            
            ''' npcs '''
            if full(npcs, None) is True: # if all the npcs are dead
                ready = False     # round is over
                level += 1        # advance to next level

            # DRAW
            
            ''' sprites '''
            for x in range(len(turretEmpty)):
                for y in range(len(turretEmpty[x])):
                    if turretEmpty[x][y] != 0 :
                        num = turretEmpty[x][y] - 1
                        if sprite_fire[num] is True:
                            px, py = fire_off[num] # offset for sprite
                            pos = turretSlots[x][y][0] + px, turretSlots[x][y][1] + py
                            screen.blit(tower_sprites[num][int(frames[num])], pos)
                        elif sprite_fire[num] is False:
                            px, py = fire_off[num] # offset for sprite
                            pos = turretSlots[x][y][0] + px, turretSlots[x][y][1] + py
                            screen.blit(tower_sprites[num][fire_min[num]], pos)
            
            ''' bullets '''
            for i in range(len(bullets)):
                
                if bullets[i] != None:
                    bullettype = bullets[i].get_type()
                    sprite        = tower_sprites[bullettype] [int(bullet_frame[bullettype])] # [sprite type] [sprite frame]
                    
                    globals().update(locals())
                    
                    screen.blit(sprite, (bullets[i][0] + bullet_off[bullettype][0], bullets[i][1] + bullet_off[bullettype][1])) # frame, (x offset, y offset)
                    
            ''' npcs '''
            for i in range(len(npcs)):
                for j in range(len(npcs[i])):
                    if npcs[i][j] != None:
                        
                        sprite = walk_sprites[lanes[i][j]] [int(walk_frame[lanes[i][j]])] # [sprite type] [sprite frame]
                        
                        screen.blit(sprite, (npcs[i][j][0] + walk_off[ lanes[i][j] ] [0], npcs[i][j][1] + walk_off[ lanes[i][j] ][1])) # frame, (x offset, y offset)
            
            ''' special attacks '''
            screen.blit(fireballLogo,(965,650))
            screen.blit(lightningLogo,(1060,645))
            screen.blit(tornadoLogo,(1135,650))
            
            draw.circle(screen, (255,0,0), (990, 670), 25, 3)
            draw.circle(screen, (255,0,0), (1070,670), 25, 3)
            draw.circle(screen, (255,0,0), (1150,670), 25, 3)
            
            if specialattack1rect.collidepoint(mx,my):
                if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                    specattack1 = True
                if l_click == True:
                    screen.blit(fireballLogo,(965,650))
                    draw.circle(screen, WHITE, (990, 670), 25, 3)
                if specattack1 == True and evt.type == MOUSEBUTTONUP and evt.button == 1:
                    if money >= 500:
                        money -= 500
                        special1()
                        specattack1 = False
                        for enemies in npcs:
                            for enemy in enemies:
                                if enemy != None:
                                    enemy.hit(100)
                    else:
                        no_money()
                        specattack1 = False
                    
            elif specialattack2rect.collidepoint(mx,my):
                if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                    specattack2 = True
                if l_click == True:
                    screen.blit(lightningLogo,(1060,645))
                    draw.circle(screen, WHITE, (1070,670), 25, 3)
                if specattack2 == True and evt.type == MOUSEBUTTONUP and evt.button == 1:
                    if money >= 500:
                        money -= 500
                        special2()
                        specattack2 = False
                        for enemies in npcs:
                            for enemy in enemies:
                                if enemy != None:
                                    enemy.hit(100)
                    else:
                        no_money()
                        specattack2 = False
                
            elif specialattack3rect.collidepoint(mx,my):
                if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                    specattack3 = True
                if l_click == True:
                    screen.blit(tornadoLogo,(1135,650))
                    draw.circle(screen, WHITE, (1150,670), 25, 3)
                if specattack3 == True and evt.type == MOUSEBUTTONUP and evt.button == 1:
                    if money >= 500:
                        money -= 500
                        special3()
                        specattack3 = False
                        for enemies in npcs:
                            for enemy in enemies:
                                if enemy != None:
                                    enemy.hit(100)
                    else:
                        no_money()
                        specattack3 = False
                        
        #### DRAW ####        
        if castle <= 0:
            game_over()
            gamemode = 'START'
            playing = False

        ''' upgrades '''
        if upgrade:
            draw.rect(screen, RED, upgradeRect, 0)
            screen.blit(upgradeTXT, (910, 25))
            if l_click is True:
                display.flip()
                money, upgraded = upgrade_menu(money, upgraded)
                l_click = False
            upgrade = False
        
        ''' pause '''
        if pause:
            draw.rect(screen, RED, pauseRect, 0)
            screen.blit(pauseTXT, (1085,25))
            if l_click is True:
                pause_menu()
                if gamemode != 'PLAY JUSTICE':
                    playing = False
                l_click = False
            pause = False

        ################        
        clock.tick(60)
        display.update()

############ MENU ############
def menu():
    init()
    mixer.music.load("Music\\MainMusic.mp3")
    mixer.music.play(-1) #loops the song
    homescreen=image.load("Images\\homescreen.jpg")#uploading the homescreen

    ###RECT###
    InstructionRect=Rect(450,200,300,50)
    AvengersRect=Rect(450,280,300,50)
    JusticeLeagueRect=Rect(450,360,300,50)
##    HighScoreRect=Rect(450,440,300,50)
    backRect=Rect(15,585,100,100)
    ###FONT###
    font.init()
    TitleFont=font.SysFont("Ironman",85)
    Title=TitleFont.render("AVENGERS vs. JUSTICE LEAGUE", True, (240,240,0))#title button
    draw.line(homescreen,(240,240,0),(120,85),(1075,85),6)
    ###PICS###
    back=image.load("Images\\back.png") #back arrow 
    back=transform.scale(back,(90,90))
    how=image.load("Images\\how.jpg") #instructions pic
    how=transform.scale(how,(1200,700))

    mode="menu"

    running=True    
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                if mode == "how":
                    mode = "menu"
                else:
                    global gamemode
                    gamemode = 'QUIT'
                    running=False
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    click=True
    ############################################################################
        mx,my=mouse.get_pos()
        mb   =mouse.get_pressed()
        mxmy=mouse.get_pos()
    ############################################################################
    ###BUTTON HIGHLIGHTS###
        if mode == "menu":
            screen.blit(homescreen,(0,0))
            screen.blit(Title, (120,30))#title position
            if 450+300> mxmy[0]>450 and 200+50>mxmy[1]>200: #if the position of the mouse is not in these coordinates
                draw.rect(screen,(0,0,0),InstructionRect,3) #then draws the box darker
                draw.rect(screen,(255,255,0),InstructionRect)
            else:
                draw.rect(screen,(0,0,0),InstructionRect,3) #else, draws the box lighter to create highlight effect
                draw.rect(screen,(200,200,0),InstructionRect)

            if 450+300> mxmy[0]>450 and 280+50>mxmy[1]>280:
                draw.rect(screen,(0,0,0),AvengersRect,3)
                draw.rect(screen,(255,255,0),AvengersRect)
            else:
                draw.rect(screen,(0,0,0),AvengersRect,3)
                draw.rect(screen,(200,200,0),AvengersRect)

            if 450+300> mxmy[0]>450 and 360+50>mxmy[1]>360:
                draw.rect(screen,(0,0,0),JusticeLeagueRect,3)
                draw.rect(screen,(255,255,0),JusticeLeagueRect)
            else:
                draw.rect(screen,(0,0,0),JusticeLeagueRect,3)
                draw.rect(screen,(200,200,0),JusticeLeagueRect)

##            if 450+300> mxmy[0]>450 and 440+50>mxmy[1]>440:
##                draw.rect(screen,(0,0,0),HighScoreRect,3)
##                draw.rect(screen,(255,255,0),HighScoreRect)
##            else:
##                draw.rect(screen,(0,0,0),HighScoreRect,3)
##                draw.rect(screen,(200,200,0),HighScoreRect)
            ###FONTS###
            InstructionsFont=font.SysFont("Times",45)
            Instructions=InstructionsFont.render("Instructions", True, (0,0,0))#instructions button
            screen.blit(Instructions, (500,200))

            AvengersFont=font.SysFont("Times",45)
            Avengers=AvengersFont.render("Avengers", True, (0,0,0))#avengers button
            screen.blit(Avengers, (515,275))

            JusticeLeagueFont=font.SysFont("Times",45)
            JusticeLeague=JusticeLeagueFont.render("Justice League", True, (0,0,0))#justiceleague button
            screen.blit(JusticeLeague, (470,355))

##            HighScoreFont=font.SysFont("Times",45)
##            HighScore=HighScoreFont.render("High Score", True, (0,0,0))#high score button
##            screen.blit(HighScore,(500,435))
        ###FUNCTIONS###
        if InstructionRect.collidepoint(mx,my) and mb[0]==1:
            mode="how"
        if backRect.collidepoint (mx,my) and mb[0]==1:
            mode="menu"
        if mode == "how":
            screen.blit(how,(0,0))
            draw.rect(screen,(0,0,0),backRect,3)
            draw.rect(screen,(0,0,220),backRect)
            screen.blit(back,(20,590))
        if AvengersRect.collidepoint(mx,my) and mb[0]==1:
            init()
            mixer.music.stop() #doesn't play at the same time
            mixer.music.load("Music\\Avengers.mp3")
            mixer.music.play(-1) #loops the song
            
            gamemode="PLAY AVENGERS"
            running = False
        if JusticeLeagueRect.collidepoint(mx,my) and mb[0]==1:
            init()
            mixer.music.stop() #doesn't play at the same time
            mixer.music.load("Music\\JL.mp3")
            mixer.music.play(-1) #loops the song
            gamemode="PLAY JUSTICE"
            running = False
        
        display.flip()

############ MAIN LOOP ############

while running:
    if gamemode == 'START':
        menu()
        
    if gamemode == 'PLAY JUSTICE':
        play_justice()
        
    if gamemode == 'PLAY AVENGERS':
        play_avengers()
        
    if gamemode == 'QUIT':
        running = False

quit()
