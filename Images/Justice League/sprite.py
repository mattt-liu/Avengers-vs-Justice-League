from pygame import *

init()
size = width, height = 800, 600
screen = display.set_mode(size)
running = True
myClock = time.Clock()

frameDelay = 8                              # only advance the frame
frame = 0                                   # every 6 loops
pics = []
for i in range(71):
    pics.append(image.load("batman/batman" + str(i) + ".png"))

while running:
    for evnt in event.get():                # checks all events that happen
        if evnt.type == QUIT:
            running = False

    screen.fill((150,220,150))
    screen.blit(pics[frame],(100,100))
    
    frameDelay -= 1                         # count down to zero
    if frameDelay == 0:                     # then advance frame like normal
        frameDelay = 8
        frame += 1
        if frame == 71: frame = 0
        
    display.flip()
    myClock.tick(50)
    
quit()
