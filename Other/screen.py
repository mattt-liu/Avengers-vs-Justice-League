from pygame import*
from random import*
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '50, 30' # window location
screen_res = 1200, 700
screen=display.set_mode((1200,700))

WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
YELLOW = (255, 255,   0)
ORANGE = (255, 128,   0)
GREEN  = (  0, 255,   0)
BLUE   = (  0,   0, 255)
PURPLE = (128,   0, 128)
BROWN  = (100,  40,  40)
BLACK  = (  0,   0,   0)

castleRect=Rect(40,120,100,470)
turretslot1=Rect(200,120,70,70)
turretslot2=Rect(200,200,70,70)
turretslot3=Rect(200,280,70,70)
turretslot4=Rect(200,360,70,70)
turretslot5=Rect(200,440,70,70)
turretslot6=Rect(200,520,70,70)
turretslot7=Rect(290,120,70,70)
turretslot8=Rect(290,200,70,70)
turretslot9=Rect(290,280,70,70)
turretslot10=Rect(290,360,70,70)
turretslot11=Rect(290,440,70,70)
turretslot12=Rect(290,520,70,70)
dividerRect=Rect(0,80,1200,10)
dividerRect2=Rect(0,630,1200,10)
exitRect=Rect(1070,30,100,30)
pauseRect=Rect(930,30,100,30)
muteRect=Rect(790,30,100,30)
skilltreeRect=Rect(650,30,100,30)
turret1=Rect(40,15,50,50)
turret2=Rect(120,15,50,50)
turret3=Rect(200,15,50,50)
turret4=Rect(280,15,50,50)
turret5=Rect(360,15,50,50)
turret6=Rect(440,15,50,50)
turret7=Rect(520,15,50,50)

draw.rect(screen, (255,255,255), castleRect)
draw.rect(screen, (255,0,0), dividerRect)
draw.rect(screen, (255,0,0), dividerRect2)
draw.rect(screen, (255,255,0), exitRect)
draw.rect(screen, (255,255,0), pauseRect)
draw.rect(screen, (255,255,0), muteRect)
draw.rect(screen, (255,255,255), skilltreeRect)
draw.rect(screen, (255,255,255), turretslot1)
draw.rect(screen, (255,255,255), turretslot2)
draw.rect(screen, (255,255,255), turretslot3)
draw.rect(screen, (255,255,255), turretslot4)
draw.rect(screen, (255,255,255), turretslot5)
draw.rect(screen, (255,255,255), turretslot6)
draw.rect(screen, (255,255,255), turretslot7)
draw.rect(screen, (255,255,255), turretslot8)
draw.rect(screen, (255,255,255), turretslot9)
draw.rect(screen, (255,255,255), turretslot10)
draw.rect(screen, (255,255,255), turretslot11)
draw.rect(screen, (255,255,255), turretslot12)
draw.circle(screen, (255,255,255), (1150,670), 25, 3)#special attack
draw.circle(screen, (255,255,255), (1070,670), 25, 3)#special attack 2
draw.circle(screen, (255,255,255), (990, 670), 25, 3)#special attack 3
draw.circle(screen, (255,255,255), (910, 670), 25, 3)#special attack 4
draw.rect(screen, (0,255,0), turret1)
draw.rect(screen, (0,255,0), turret2)
draw.rect(screen, (0,255,0), turret3)
draw.rect(screen, (0,255,0), turret4)
draw.rect(screen, (0,255,0), turret5)
draw.rect(screen, (0,255,0), turret6)
draw.rect(screen, (0,255,0), turret7)

font.init()
helFont=font.SysFont("Helvetica",30)
helFont1=font.SysFont("Helvetica",25)
moneyTXT=helFont.render("Money ", True, (255,255,255))
levelTXT=helFont.render("Level ", True, (255,255,255))
exitTXT=helFont.render("Exit", True, (0,0,0))
pauseTXT=helFont.render("Pause", True, (0,0,0))
muteTXT=helFont.render("Mute", True, (0,0,0))
skilltreeTXT=helFont1.render("Skill Tree", True, (0,0,0))

screen.blit(moneyTXT,(40,650))
screen.blit(levelTXT,(250,650))
screen.blit(exitTXT, (1100,25))
screen.blit(pauseTXT, (945,25))
screen.blit(muteTXT, (810,25))
screen.blit(skilltreeTXT, (660,30))



    
FONT  = font.Font('Fonts\\ubuntu.ttf', 70)
text  = FONT.render('GAME OVER!!', True, WHITE)
text2 = FONT.render('MENU', True, WHITE)

backRect = Rect(300, 200, 500, 300)
menuRect = Rect(400, 350, 300, 100)

running = True
click = False

count = 0

def loading(num):
    FONT = font.Font('Fonts\\ubuntu.ttf', 70)
    text = FONT.render('LOADING', True, YELLOW)

    screen.fill(BLACK)
    screen.blit(text, (420, 150))

    rects = []
    for i in range(10):
        w = (i / 10) * 1000
        rects.append(Rect(100, 600, w, 5))
    
    draw.rect(screen, YELLOW, rects[num], 0)
    
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
                    
            if evt.type == MOUSEBUTTONDOWN and exitRect.collidepoint(mx, my):
                click1 = True
            if click1 is True and evt.type == MOUSEBUTTONUP:
                if exitRect.collidepoint(mx, my):
                    global gamemode
                    gamemode = 'QUIT'
                    paused = False
                else:
                    click1 = False
                    
            if evt.type == MOUSEBUTTONDOWN and homeRect.collidepoint(mx, my):
                click2 = True
            if click2 is True and evt.type == MOUSEBUTTONUP:
                if homeRect.collidepoint(mx, my):
                    paused = False
                    global gamemode
                    gamemode = 'START'
                else:
                    click2 = False
                    
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
def win():
    
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
        
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    win()
    running = False
    display.flip()
quit()
