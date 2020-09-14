from pygame import *
from random import *
from glob import *
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '50, 50'
screen = display.set_mode((1200, 700))
clock = time.Clock()

hawk_sprites = []
sprites1 = glob('Images\\Avengers\\hawkeye\\*.png')
sprites1.sort()
for pic in sprites1:
    hawk_sprites.append(transform.flip(image.load(pic), True, False).convert_alpha())

spider_sprites = []
sprites2 = glob('Images\\Avengers\\spiderman\\running\\*.png')
sprites2.sort()
for pic in sprites2:
    img1 = image.load(pic)
    img2 = transform.scale(img1, (int(img1.get_width() * 1.2), int(img1.get_height() * 1.2)))
    spider_sprites.append(transform.flip(img2, True, False).convert_alpha())

hulk_sprites = []
sprites3 = glob('Images\\Avengers\\hulk\\*.png')
sprites3.sort()
for pic in sprites3:
    hulk_sprites.append(transform.flip(image.load(pic), True, False).convert_alpha())

silver_sprites = []
sprites4 = glob('Images\\Avengers\\quick_silver\\*.png')
sprites4.sort()
for pic in sprites4:
    img1 = image.load(pic)
    img2 = transform.scale(img1, (int(img1.get_width() * 0.6), int(img1.get_height() * 0.6)))
    silver_sprites.append(transform.flip(img2, True, False).convert_alpha())

america_sprites = []
sprites5 = glob('Images\\Avengers\\cap_america\\*.png')
sprites5.sort()
for pic in sprites5:
    america_sprites.append(transform.flip(image.load(pic), True, False).convert_alpha())

iron_sprites = []
sprites6 = glob('Images\\Avengers\\iron_man\\running\\*.png')
sprites6.sort()
for pic in sprites6:
    img1 = image.load(pic)
    img2 = transform.scale(img1, (int(img1.get_width() * 1.5), int(img1.get_height() * 1.5)))
    iron_sprites.append(transform.flip(img2, True, False).convert_alpha())

thor_sprites = []
sprites7 = glob('Images\\Avengers\\thor\\running\\*.png')
sprites7.sort()
for pic in sprites7:
    thor_sprites.append(transform.flip(image.load(pic), True, False).convert_alpha())

tower_sprites = [hawk_sprites, spider_sprites, hulk_sprites, silver_sprites,
                 america_sprites, iron_sprites, thor_sprites]

##def draw_enemy(num, pos):

tower_sprites = [hawk_sprites, spider_sprites, hulk_sprites, silver_sprites,
                 america_sprites, iron_sprites, thor_sprites]
sprite_max   = [28, 11, 14, 128, 8, 9, 11]
sprite_min   = [23,  0,  9, 126, 3, 1,  0]
sprite_speed = [0.2, 0.2, 0.1, 0.15, 0.1, 0.15, 0.15]

frame = []
for i in range(7):
    frame.append(sprite_min[i])
dist = 1180
    
screen.fill((255, 255, 255))
tower = 6
running = True

while running:
    mx, my = mouse.get_pos()
    for evt in event.get():
        if evt.type==QUIT:
            running=False
            
    screen.fill((255, 255, 255))
               
    if dist < 20:
        dist = 1080
    else:
        dist -= 1

    for tower in range(7):
        
        frame[tower] += sprite_speed[tower]
        if int(frame[tower]) >= sprite_max[tower] + 1:
            frame[tower] = sprite_min[tower]
        screen.blit(tower_sprites[tower][int(frame[tower])], (50 + dist, 50 + tower * 100))
    
    display.flip()
    clock.tick(60)

quit()

##playing = True
##while playing:
##    draw_enemy(1, 1)
##    playing = False
##quit()
