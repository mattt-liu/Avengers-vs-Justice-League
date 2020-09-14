#Final Project

from pygame import*
from random import*
import os

###############################################################################
###WHERE THE WINDOW OPENS###
init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '25,100'

###############################################################################
###MUSIC###
init()
mixer.music.load("MainMusic.mp3")
mixer.music.play(-1) #loops the song

###############################################################################
def menu():
    screen=display.set_mode((1200,700))
    homescreen=image.load("homescreen.jpg")#uploading the homescreen
    display.set_caption('AVENGERS vs. JUSTICE LEAGUE')

    ###RECT###
    InstructionRect=Rect(450,200,300,50)
    AvengersRect=Rect(450,280,300,50)
    JusticeLeagueRect=Rect(450,360,300,50)
    HighScoreRect=Rect(450,440,300,50)
    backRect=Rect(15,585,100,100)
    ###FONT###
    font.init()
    TitleFont=font.SysFont("Ironman",85)
    Title=TitleFont.render("AVENGERS vs. JUSTICE LEAGUE", True, (240,240,0))#title button
    draw.line(homescreen,(240,240,0),(120,85),(1075,85),6)
    ###PICS###
    back=image.load("back.png") #back arrow 
    back=transform.scale(back,(90,90))
    how=image.load("how.jpg") #instructions pic
    how=transform.scale(how,(1200,700))

    mode="menu"

    running=True    
    while running:
        for evt in event.get():
            if evt.type==QUIT:
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

            if 450+300> mxmy[0]>450 and 440+50>mxmy[1]>440:
                draw.rect(screen,(0,0,0),HighScoreRect,3)
                draw.rect(screen,(255,255,0),HighScoreRect)
            else:
                draw.rect(screen,(0,0,0),HighScoreRect,3)
                draw.rect(screen,(200,200,0),HighScoreRect)
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

            HighScoreFont=font.SysFont("Times",45)
            HighScore=HighScoreFont.render("High Score", True, (0,0,0))#high score button
            screen.blit(HighScore,(500,435))
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
            play_avengers()
            init()
            mixer.music.stop("MainMusic.mp3") #doesn't play at the same time
            mixer.music.load("Avengers.mp3")
            mixer.music.play(-1) #loops the song
            mode="avengers"
        if JusticeLeagueRect.collidepoint(mx,my) and mb[0]==1:
            play_justice()
            init()
            mixer.music.stop("MainMusic.mp3") #doesn't play at the same time
            mixer.music.load("JL.mp3")
            mixer.music.play(-1) #loops the song
            mode="justice"
    ############################################################################
        display.flip()
        
test = True #you would have to click 'X' twice to exit out of program
while test: #fixes this 
    menu()
    test = False
        
quit()
