from pygame import*
from random import*
import os
os.environ['SDL_VIDEO_WINDOW_POS']='40,200'
screen=display.set_mode((1200,700))
screen_res=(1200,700)
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
turret1=Rect(40,15,50,50)
turret2=Rect(120,15,50,50)
turret3=Rect(200,15,50,50)
turret4=Rect(280,15,50,50)
turret5=Rect(360,15,50,50)
turret6=Rect(440,15,50,50)
turret7=Rect(520,15,50,50)

#NEW#
specialattack1rect=Rect(1125,645,50,50)
specialattack2rect=Rect(1045,645,50,50)
specialattack3rect=Rect(965,645,50,50)
#####

draw.rect(screen, (255,255,255), castleRect)
draw.rect(screen, (255,0,0), dividerRect)
draw.rect(screen, (255,0,0), dividerRect2)
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
#NEW#
draw.rect(screen, (255,255,255), specialattack1rect)
draw.rect(screen, (255,255,255), specialattack2rect)
draw.rect(screen, (255,255,255), specialattack3rect)
#####
#Changed#
draw.circle(screen, (255,0,0), (1150,670), 25, 3)#special attack
draw.circle(screen, (255,0,0), (1070,670), 25, 3)#special attack 2
draw.circle(screen, (255,0,0), (990, 670), 25, 3)#special attack 3
#########

draw.rect(screen, (0,255,0), turret1)
draw.rect(screen, (0,255,0), turret2)
draw.rect(screen, (0,255,0), turret3)
draw.rect(screen, (0,255,0), turret4)
draw.rect(screen, (0,255,0), turret5)
draw.rect(screen, (0,255,0), turret6)
draw.rect(screen, (0,255,0), turret7)

font.init()

running = True

###############################NEW############################
init()

####Change the variables####
##avengers1File=open("avengers1.txt").read().strip().split("\n")
##
##hawk=avengers1File[0]
##spider=avengers1File[1]
##hulk=avengers1File[2]
##silver=avengers1File[3]
##captain=avengers1File[4]
##iron=avengers1File[5]
##thor=avengers1File[6]
##
##justice1File=open("justice1.txt").read().strip().split("\n")
##cyborg1=justice1File[0]
##flash1=justice1File[1]
##lantern1=justice1File[2]
##aqua1=justice1File[3]
##woman1=justice1File[4]
##batman1=justice1File[5]
##superman1=justice1File[6]
##
##print(avengers1File)
##print(hawk)
##print(spider)
##print(hulk)
##print(silver)
##print(captain)
##print(iron)
##print(thor)

#########################
clock = time.Clock()
myClock = time.Clock()
myClock1 = time.Clock()
myClock2 = time.Clock()

tornado = []
lightning = []
fireball = []
for i in range(16):
    tornado.append(image.load("tornado" + str(i) + ".png"))

for i in range(10):
    lightning.append(image.load("lightning" + str(i) + ".png"))

for i in range(16):
    fireball.append(image.load("fireball" + str(i) + ".png"))

def pointer(x,y,size):
    draw.circle(screen ,(255,255,255) , (x,y) , size,1)
    draw.line(screen , (255,255,255) , (x-size,y) , (x+size,y),1)
    draw.line(screen , (255,255,255) , (x,y-size) , (x,y+size),1)

def special1():
    attack1 = False
    screenshot = screen.copy()
    frame1 = 0
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                x, y = evt.pos
                screenshot = screen.copy()
                attack1 = True
        mx,my = mouse.get_pos()
        mb    = mouse.get_pressed()
        if attack1:
            screen.blit(screenshot,(0,0))
            pointer(x,y,30)
            screen.blit(tornado[frame1] , (x-30,y-30)) 
            frame1 += 1
            if frame1 == 16:
                frame1 = 0
                running = False
        elif not attack1:
            screen.blit(screenshot , (0,0))
            pointer(mx,my,30)
        display.flip()
        myClock.tick(20)

def special2():
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
        myClock1.tick(10)


def special3():
    m = 120
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
            m += 30
            screen.blit(screenshot, (0,0))
            for i in range(5):
                if m-i*250 >= 150:
                    screen.blit(fireball[frame3] , (m-i*250,150)) 
                    screen.blit(fireball[frame3] , (m-i*250,230))
                    screen.blit(fireball[frame3] , (m-i*250,310))
                    screen.blit(fireball[frame3] , (m-i*250,390))
                    screen.blit(fireball[frame3] , (m-i*250,470))
                    screen.blit(fireball[frame3] , (m-i*250,550))
            frame3 +=1
            display.flip()
            if frame3 == 16:
                frame3 = 0
            if m-i*250>1100:
                running=False
        elif not attack3:
            screen.blit(screenshot , (0,0))
        display.flip()
        myClock2.tick(30)

def upgradebutton(x,y):
    draw.line(screen , (250,250,210) , (x,y-35), (x+70,y-35), 5)
    draw.line(screen , (250,250,210) , (x+35,y), (x+35,y-70), 5)
    
def upgradeAvengers1():
    if hawk.collidepoint(mx,my):#change the variable "hawk"
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            hawk.replace("50","60")
    if spider.collidepoint(mx,my):#change the variable "spider"
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            spider.replace("75","90")
    if hulk.collidepoint(mx,my):#change the variable "hulk"
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            hulk.replace("90","108")
    if silver.collidepoint(mx,my):#change the variable "silver"
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            silver.replace("120","144")
    if captain.collidepoint(mx,my):#change the variable "captain"
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            captain.replace("130","156")
    if iron.collidepoint(mx,my):#change the variable "iron"
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            iron.replace("220","264")
    if thor.collidepoint(mx,my):#change the variable "thor"
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            thor.replace("320","384")

def upgradeJustice1():
    if cyborg.collidepoint(mx,my):
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            cyborg.replace("50","60")
    if flash.collidepoint(mx,my):
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            flash.replace("70","84")
    if lantern.collidepoint(mx,my):
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            lantern.replace("95","114")
    if aqua.collidepoint(mx,my):
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            aqua.replace("120","144")
    if woman.collidepoint(mx,my):
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            woman.replace("175","210")
    if batman.collidepoint(mx,my):
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            batman.replace("220","264")
    if superman.collidepoint(mx,my):
        upgradebutton(mx,my)
        if mb[0]==1 and upgradebutton.collidepoint(mx,my):
            superman.replace("350","420")
    
def pause_menu():
    #### MENU OBJECTS ####
    ''' translucent background '''
    menu = Surface(screen_res)
    menu.set_alpha(150)
    menu.fill((255,255,255))
    ''' rects '''
    pauseRect = Rect(300, 100, 500, 300)
    muteRect = Rect(350,150,150,100)
    exitRect = Rect(600,150,150,100)
    homeRect = Rect(475,270,150,100)
    #### TEXT ####
    helFont1=font.SysFont("Helvetica",35)
    muteTXT=helFont1.render("Mute", True, (0,0,0))
    exitTXT=helFont1.render("Exit", True, (0,0,0))
    homeTXT=helFont1.render("Home", True, (0,0,0))
    #### DRAW ####
    screen.blit(menu, (0, 0))
    draw.rect(screen, (255,0,0), pauseRect, 0)
    draw.rect(screen, (250,250,210), muteRect, 0)
    draw.rect(screen, (250,250,210), exitRect, 0)
    draw.rect(screen, (250,250,210), homeRect, 0)
    screen.blit(muteTXT, (390,180))
    screen.blit(exitTXT, (650,180))
    screen.blit(homeTXT, (515,300))
    if muteRect.collidepoint(mx,my):
        if mb[0]==1:
            pass
    if exitRect.collidepoint(mx,my):
        if mb[0]==1:
            pass
    if homeRect.collidepoint(mx,my):
        if mb[0]==1:
            pass
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
    
            

###############################################################
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
            screenshot = screen.copy()
#############################################
    mx,my=mouse.get_pos()
    mb   =mouse.get_pressed()
    
    if mb[0]==1 and specialattack1rect.collidepoint(mx,my):
        special1()
        screen.blit(screenshot , (0,0))
    if mb[0]==1 and specialattack2rect.collidepoint(mx,my):
        special2()
        screen.blit(screenshot , (0,0))
    if mb[0]==1 and specialattack3rect.collidepoint(mx,my):
        special3()
        screen.blit(screenshot , (0,0))
    if hawk.collidepoint(mx,my) or spider.collidepoint(mx,my) or hulk.collidepoint(mx,my) or silver.collidepoint(mx,my)\
    or captain.collidepoint(mx,my) or iron.collidepoint(mx,my) or thor.collidepoint(mx,my):
        if mb[0]==1:
            upgradeAvengers1()
    if cyborg.collidepoint(mx,my) or flash.collidepoint(mx,my) or lantern.collidepoint(mx,my) or aqua.collidepoint(mx,my)\
    or  woman.collidepoint(mx,my) or batman.collidepoint(mx,my) or superman.collidepoint(mx,my):
        if mb[0]==1:
            upgradeJustice1()
    pause_menu()
        
#############################################
    display.flip()
quit()
