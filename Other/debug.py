''' Avengers vs Justice League '''

# tasks

# [X] set escape as pause
# [ ] add 'x' button to pause menu
# [ ] add sound & music
# [ ] add info bar
# [ ] add sprites

######################## MODULES ########################
from glob import *
from math import *
from pprint import *
from pygame import *
from random import *
import os

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
os.environ['SDL_VIDEO_WINDOW_POS'] = '30, 50' # sets window location

screen_res = (1200, 700)
screen = display.set_mode(screen_res)
display.set_caption('Avengers vs Justice League')

running = True
clock = time.Clock()

######################## CLASSES ########################
class Tower:
    def __init__(self, cost, damage, reload):
        self.cost   = int(cost)
        self.dmg    = int(damage)
        self.reload = int(reload)
        self.time = 0
        
    def place(self, point):
        self.x, self.y = point
        self.bullet = Bullet((self.x, self.y))
        
    def __getitem__(self, i):
        self.feats = [self.cost, self.dmg, self.reload]
        return self.feats[i]
    
    def buy(self):
        return self.cost

    def fire(self):
        return self.reload * 60
            
    
class Npc:
    
    def __init__(self, health, damage, speed, place):
        self.hp    = int(health)
        self.speed = int(speed)
        self.dmg   = int(damage)
        self.x, self.y = place
        self.stop = False
        
    def __getitem__(self, i):
        # returns item in list that corresponds to entered index
        self.feats = [self.x, self.y, 25, 25]
        return self.feats[i]
    
    def stop(self, Bool):
        self.stop = Bool
        
    def move(self):
        if not self.stop:
            self.x -= self.speed // 12
        
    def hit(self, damage):
        # returns amount of health remaining if hit
        self.hp -= int(damage)
        if self.hp <= 0:
            return 0
        return self.hp

class Bullet:
    def __init__(self, point):
        self.v = 7
        self.x, self.y = point

    def __getitem__(self, i):
        self.points = [self.x, self.y]
        return self.points[i]
    
    def move(self):
        self.x += self.v
######################## GENERAL FUNCTIONS ########################
def check_x(List):
    ''' if all x values in a list are less than 100, returns true '''
    for i in range(len(List)):
        for j in range(len(List[i])):
            if List[i][j][0] > 100:
                return False
    return True

def confirm_sell():
    print('sell tower?')

def overlap(rect, rect1):
    ''' determines how much area a rect has on another '''

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
def game_over():
    print('game over')
    
def pause_menu():
    #### MENU OBJECTS ####
    ''' translucent background '''
    menu = Surface(screen_res)
    menu.set_alpha(150)
    menu.fill(WHITE)
    ''' rects '''
    pauseRect = Rect(300, 100, 500, 300)
    #### TEXT ####
    helFont1=font.SysFont("Helvetica",25)
    muteTXT=helFont1.render("Mute", True, BLACK)
    exitTXT=helFont1.render("Exit", True, BLACK)
    #### DRAW ####
    screen.blit(menu, (0, 0))
    draw.rect(screen, RED, pauseRect, 0)
    ########
    paused = True
    while paused:
        ########
        for evt in event.get():
            if evt.type == QUIT:
                paused = False
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    paused = False
        ########
        display.flip()
        clock.tick(60)
    
def pointer(x, y, size):
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
######################## GAME FUNCTIONS ########################

#### TEXT ####
font.init()
helFont=font.SysFont("Helvetica",30)
helFont1=font.SysFont("Helvetica",25)

moneyTXT=helFont.render("Money:", True, WHITE)
levelTXT=helFont.render("Level:", True, WHITE)
pauseTXT=helFont.render("Pause", True, BLACK)
skilltreeTXT=helFont1.render("Skill Tree", True, BLACK)
#### IMAGES ####
justiceback1 = transform.scale(image.load('Backgrounds/Justice league background.jpg'), (1200, 700))
icon1 = transform.scale(image.load('Icons/JL/cyborg.png'), (50, 50))
icon2 = transform.scale(image.load('Icons/JL/flash.png'), (50, 50))
icon3 = transform.scale(image.load('Icons/JL/greenlantern.png'), (50, 50))
icon4 = transform.scale(image.load('Icons/JL/aquaman.png'), (50, 50))
icon5 = transform.scale(image.load('Icons/JL/wonderwomen.png'), (50, 50))
icon6 = transform.scale(image.load('Icons/JL/batman.png'), (50, 50))
icon7 = transform.scale(image.load('Icons/JL/superman.png'), (50, 50))
icons = [icon1, icon2, icon3, icon4,
         icon5, icon6, icon7]

cyborg_sprites = []
sprites1 = glob('Images//Justice League//cyborg//*.png')
sprites1.sort()
for pic in sprites1:
    cyborg_sprites.append(image.load(pic))
    
flash_sprites = []
sprites2 = glob('Images//Justice League//flash//*.png')
sprites2.sort()
for pic in sprites2:
    flash_sprites.append(image.load(pic))
    
green_sprites = []
sprites3 = glob('Images//Justice League//green_lantern//*.png')
sprites3.sort()
for pic in sprites3:
    p = image.load(pic)
    green_sprites.append(transform.scale(p, (int(p.get_width() * 1.5), int(p.get_height() * 1.5))))
    
aqua_sprites = []
sprites4 = glob('Images//Justice League//aquaman//*.png')
sprites4.sort()
for pic in sprites4:
    aqua_sprites.append(image.load(pic))
    
woman_sprites = []
sprites5 = glob('Images//Justice League//wonder_woman//*.png')
sprites5.sort()
for pic in sprites5:
    woman_sprites.append(image.load(pic))

batman_sprites = []
sprites6 = glob('Images//Justice League//batman//*.png')
sprites6.sort()
for pic in sprites6:
    batman_sprites.append(image.load(pic))
    
superman_sprites = []
sprites7 = glob('Images//Justice League//superman//*.png')
sprites7.sort()
for pic in sprites7:
    superman_sprites.append(image.load(pic))
#### RECTS ####
turretSlots = []
castleRect=Rect(40,120,100,470)
''' empty grid for turrets (2-D list) '''
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
enemy_count = open('Towers/npc.txt', 'r').read().split(' ') # creates list
for i in range(len(enemy_count)):
    enemy_count[i] = int(enemy_count[i]) # convert each item inside list to int
#### VARIABLES ####
''' bools '''
l_click = False
pause = False
playing = True
ready = False # tracks when to send the enemies
''' ints '''
money = 100000000
level = 1
''' lists '''
bullets = []
collideTurrets = [False, False, False, False, False, False, False]
colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]
distTurrets = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
turretEmpty = [[0] * 6 for i  in range(8)] # 0 represents the empty turret slots
turretEmpty = [[1, 0, 0, 0, 0, 0],
               [0, 2, 0, 0, 0, 0],
               [0, 0, 3, 0, 0, 0],
               [0, 0, 0, 4, 0, 0],
               [0, 0, 0, 0, 5, 0],
               [0, 0, 0, 0, 0, 6],
               [0, 0, 0, 0, 7, 0],
               [0, 0, 0, 0, 0, 0]]
''' other '''
mx, my = mouse.get_pos()
mb     = mouse.get_pressed()
preScreen = screen.copy()
''' sprites '''
frames = [0, 0, 0, 0, 0, 0, 0]
# Idling
sprite_max    = [6, 4, 5, 4, 4, 4, 4]
sprite_min    = [0, 1, 1, 1, 1, 1, 2]
sprite_speed  = [0.3, 0.2, 0.25, 0.2, 0.2, 0.2, 0.1]
# Attacking
fire_max    = [73, 55, 262, 56, 62, 47, 35]
fire_min    = [71, 51, 257, 54, 61, 42, 32]
fire_speed  = []
for i in range(len(towers)):
    fire_speed.append(towers[i].fire())

sprite_off    = [(10, -3), (3, -20), (12, 0), (-20, -35), (0, -25), (-5, -20), (-10, -22)]
tower_sprites = [cyborg_sprites, flash_sprites, green_sprites, aqua_sprites, woman_sprites, batman_sprites, superman_sprites]
#### LOCAL FUNCTIONS ####
def arrow():
    helFont = font.SysFont("Helvetica",30)
    start = Rect(1040, 300,  151, 100)
    startTXT = helFont.render('START', True, WHITE)
    points = [(1090, 325), (1090 + 100, 325), (1090 + 100, 325 + 50),
              (1090, 325 + 50), (1090, 325 + 75), (1040, 350), (1090, 325 - 25)]
    
    if start.collidepoint(mx, my):
        draw.polygon(screen, RED, points, 0)
        screen.blit(startTXT, (1085, 332))
        if l_click == True:
            draw.polygon(screen, BLUE, points, 0)
            screen.blit(startTXT, (1085, 332))
        if evt.type == MOUSEBUTTONUP:
            return True
    else:
        draw.polygon(screen, RED, points, 1)
        screen.blit(startTXT, (1085, 332))
    return False

def background():
    SLOT = (128, 128, 128) # gray
    moneyNUM = helFont.render(str(money), True, YELLOW)
    levelNUM = helFont.render(str(level), True, YELLOW)
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
    draw.rect(screen, SLOT, castleRect)
    draw.rect(screen, SLOT, dividerRect)
    draw.rect(screen, SLOT, dividerRect2)
    draw.rect(screen, YELLOW, pauseRect)
    draw.circle(screen, WHITE, (1150,670), 25, 3) # special attack
    draw.circle(screen, WHITE, (1070,670), 25, 3) # special attack 2
    draw.circle(screen, WHITE, (990, 670), 25, 3) # special attack 3
    draw.circle(screen, WHITE, (910, 670), 25, 3) # special attack 4
    ''' tower choices '''
    for x, y, w, h in turrets:
        rect = Rect(x, y, w, h)
        if collideTurrets[turrets.index(rect)] is True:
            continue
        screen.blit(icons[turrets.index(rect)], (x, y))
        if rect.collidepoint(mx, my):
            draw.rect(screen, WHITE, rect, 1)
    ''' text '''
    screen.blit(moneyTXT,(40,650))
    screen.blit(moneyNUM,(130,650))
    screen.blit(levelTXT,(250,650))
    screen.blit(levelNUM,(325,650))
    screen.blit(pauseTXT, (1085,25))
    screen.blit(skilltreeTXT, (660,30))
    
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

#### OTHER ####
background()

while playing:
    #### Interactions ####
    mx, my = mouse.get_pos()
    mb     = mouse.get_pressed()
    
    for evt in event.get():
        if evt.type == QUIT:
            playing = False
        ''' mouse events '''
        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                l_click = True
                preScreen = screen.copy()
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
                    distTurrets[i] = (0, 0)
                    collideTurrets[i] = False
                turrets = []
                for i in range(7):
                    x = 40 + (i * 80)
                    turrets.append(Rect(x, 15, 50, 50))
            if evt.button == 3:
                ''' clear slot '''
                for x in range(len(turretEmpty)):
                    for y in range(len(turretEmpty[x])):
                        if turretSlots[x][y].collidepoint(mx, my):
                            confirm_sell()
                            turretEmpty[x][y] = 0
        ''' keyboard events '''
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                pause_menu()
    ''' pause '''
    if pauseRect.collidepoint(mx, my):
        pause = True
    #### LEVELS ####
    if ready:
        ''' sprites '''
        for i in range(len(frames)):
            if int(frames[i]) >= fire_max[i] or int(frames[i]) <= fire_min[i]: # if that sprite exceeds its frames
                frames[i] = fire_min[i]
            frames[i] += fire_speed[i]
##            for i in range(len(bullets)):
##                draw.rect(screen, WHITE, (i[0], i[1], 5, 5), 0)
##                bullets[i].move()
##                if reload[i] == 0:
##                    bullets[i] = Bullet(
##                else:
##                    reload[i] -= 1
##                if bullets[i][0] > screen_res[0]: # if past the right side of screen
##                    bullets[i] = -1
##                    reload[i] = -1
##            for i in range(len(npcs)):
##                for j in range(len(npcs[i])):
##                    if collide_turrets((npcs[i][j][0], npcs[i][j][1])):
##                        npcs[i][j].stop(True)
    if not ready:
        ''' sprites '''
        for i in range(len(frames)):
            if int(frames[i]) >= sprite_max[i]: # if that sprite exceeds its frames
                frames[i] = sprite_min[i]
            frames[i] += sprite_speed[i]
        ''' set enemies for the level '''
        npcs = []
        for i in range(enemy_count[level]): # sets all enemies for the level
            enemy_place = (screen_res[0], choice((120, 200, 280, 360, 440, 520)) + 22) # (past right of screen, random lane)
            hp = 1.25 ** (level - 1) * 50
            enemy = Npc(hp, 25, 0.5, enemy_place) # health, dmg, speed, (x, y)
            npcs.append(enemy)
        ''' bullets '''
##            bullets = []
##            reload = []
##            for x in range(len(turretEmpty)):
##                for y in range(len(turretEmpty[x])):
##                    tower_type = turretEmpty[x][y]
##                    if tower_type != 0:
##                        bullet = Bullet((turretSlots[x][y][0] + 70, turretSlots[x][y][1] + 35)) # set bullet x, y
##                        bullets.append(bullet)
##                        reload.append(towers[tower_type].reloading()) # set reload time
    #### DRAW ####
    background()
    ''' drag and snap '''
    for i in range(len(turrets)):
        if collideTurrets[i] is True and l_click is True:
            dx, dy = distTurrets[i]
            turrets[i] = Rect(mx - dx, my - dy, turrets[i][2], turrets[i][3])
            img = tower_sprites[i][0] # tower type corresponds to sprite
            w, h = img.get_width(), img.get_width()
            screen.blit(img, (mx - w//2, my - h//2))
    ''' pause '''
    if pause:
        draw.rect(screen, RED, pauseRect, 0)
        screen.blit(pauseTXT, (1085,25))
        if l_click is True:
            display.flip()
            pause_menu()
        pause = False
    ''' entities '''
    if ready:
        for x in range(len(turretEmpty)):
            for y in range(len(turretEmpty[x])):
                if turretEmpty[x][y] != 0 :
                    num = turretEmpty[x][y] - 1 # index is one less than real number
                    px, py = sprite_off[num] # offset for sprite (sizes vary)
                    pos = turretSlots[x][y][0] + px, turretSlots[x][y][1] + py
                    screen.blit(tower_sprites[num][int(frames[num])], pos)
##            ''' bullets '''
##            for i in range(len(bullets)):
##                draw.rect(screen, WHITE, (i[0], i[1], 5, 5), 0)
##            ''' npcs '''
##            for i in range(len(npcs)):
##                if not ready:
##                    break
##                for j in range(len(npcs[i])):
##                    if check_x(npcs):
##                        ready = False
##                        level += 1
##                        print(level)
##                    if not ready:
##                        break
##                    enemy = npcs[i][j]
##                    enemy.move()
##                    draw.rect(screen, BLUE, (enemy[0], enemy[1], 20, 20), 0)
    if not ready:
        ready = arrow()
        for x in range(len(turretEmpty)):
            for y in range(len(turretEmpty[x])):
                if turretEmpty[x][y] != 0 :
                    num = turretEmpty[x][y] - 1 # index is one less than real number
                    px, py = sprite_off[num] # offset for sprite (sizes vary)
                    pos = turretSlots[x][y][0] + px, turretSlots[x][y][1] + py
                    screen.blit(tower_sprites[num][int(frames[num])], pos)
    ########
    clock.tick(60)
    display.flip()
quit()
