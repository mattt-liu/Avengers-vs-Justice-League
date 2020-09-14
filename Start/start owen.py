#finalProject.py
from pygame import*
from random import*
screen=display.set_mode((1024,482))
homescreen=image.load("Pictures/homescreen.jpg")#uploading the homescreen
screen.blit(homescreen,(0,0))

InstructionRect=Rect(360,120,300,50)
AvengersRect=Rect(360,200,300,50)
JusticeLeagueRect=Rect(360,280,300,50)
HighScoreRect=Rect(360,360,300,50)

draw.rect(screen,(0,0,0),InstructionRect,3)
draw.rect(screen,(255,255,0),InstructionRect,0)

draw.rect(screen,(0,0,0),AvengersRect,3)
draw.rect(screen,(255,255,0),AvengersRect,0)

draw.rect(screen,(0,0,0),JusticeLeagueRect,3)
draw.rect(screen,(255,255,0),JusticeLeagueRect,0)

draw.rect(screen,(0,0,0),HighScoreRect,3)
draw.rect(screen,(255,255,0),HighScoreRect,0)

font.init()

TitleFont=font.SysFont("Ironman",85)
Title=TitleFont.render("Avengers vs. Justice League", True, (255,255,0))#title button

InstructionsFont=font.SysFont("Times",45)
Instructions=InstructionsFont.render("Instructions", True, (0,0,0))#instructions button

AvengersFont=font.SysFont("Times",45)
Avengers=AvengersFont.render("Avengers", True, (0,0,0))#avengers button

JusticeLeagueFont=font.SysFont("Times",45)
JusticeLeague=JusticeLeagueFont.render("Justice League", True, (0,0,0))#justiceleague button

HighScoreFont=font.SysFont("Times",45)
HighScore=HighScoreFont.render("High Score", True, (0,0,0))#high score button

screen.blit(Title, (112,30))#title position
screen.blit(Instructions, (400,120))
screen.blit(Avengers, (420,200))
screen.blit(JusticeLeague, (380,280))
screen.blit(HighScore,(400,360))

running=True

myClock = time.Clock()

frame = 0
tornado = []

    
while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
##############################################
    mx,my=mouse.get_pos()
    mb   =mouse.get_pressed()



##############################################
    display.flip()
quit()
