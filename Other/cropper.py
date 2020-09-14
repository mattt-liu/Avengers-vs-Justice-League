# Image Cropper

from glob import *
from pprint import *
from pygame import *

screen = display.set_mode((500, 500))

names = glob('*.png')
names.sort()
images = []

for i in range(9):
    images.append(image.load(names[i]))

for i in range(len(images)):
    image.save(transform.chop(images[i], (0, 0, 0, 20)), 'New folder//%s'%(names[i]))
    
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    screen.fill((0, 255, 255))
    draw.rect(screen, 0, (0, 0, images[0].get_width(), images[0].get_height()), 1)
    screen.blit(transform.chop(images[0], (0, 0, 0, 20)), (0, 0))
    screen.blit(images[0], (100, 100))
    display.flip()
quit()
