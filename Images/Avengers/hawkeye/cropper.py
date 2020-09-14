# Image Cropper

from glob import *
from pprint import *
from pygame import *

screen = display.set_mode((500, 500))

names = glob('*.png')
names.sort()
images = []

for i in range(20):
    images.append(image.load(names[i]))

for i in range(len(images)):
    image.save(transform.chop(images[i], (0, 0, 0, 30)), 'New folder//%s'%(names[i]))
    
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    screen.fill((0, 255, 255))
    draw.rect(screen, 0, (0, 0, images[18].get_width(), images[18].get_height()), 1)
    screen.blit(transform.chop(images[18], (0, 0, 0, 30)), (0, 0))
    screen.blit(images[18], (100, 100))
    display.flip()
quit()
