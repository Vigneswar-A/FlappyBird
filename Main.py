import pygame as pg,random,sys,os
from pygame.constants import KEYDOWN, QUIT
from pygame.sprite import collide_mask

def R(RP):
    try:
        BP=sys._MEIPASS
    except:
        BP=os.path.abspath(".")
    return os.path.join(BP,RP)

icon=pg.transform.scale2x(pg.image.load(R("./Bird2.png")))

Loading=pg.transform.scale2x(pg.image.load(R("./Loading.png")))
pg.display.set_caption("Flappy Bird")
pg.display.set_icon(icon)
pg.init()

#Loading
bg=pg.transform.scale2x(pg.image.load(R("./Background.png")))
floor=pg.transform.scale2x(pg.image.load(R("./Floor.png")))
screen=pg.display.set_mode((bg.get_size()))
screen.blit(Loading,(0,0))
pg.display.flip()

#Clock
clock=pg.time.Clock()

#Assets
pipeb=pg.transform.flip(pg.transform.scale2x(pg.image.load(R("./Pipe.png")).convert_alpha()),False,True)
pipet=pg.transform.scale2x(pg.image.load(R("./Pipe.png")).convert_alpha())
bird1=pg.transform.scale2x(pg.image.load(R("./Bird1.png")).convert_alpha())
bird2=pg.transform.scale2x(pg.image.load(R("./Bird2.png")).convert_alpha())
bird3=pg.transform.scale2x(pg.image.load(R("./Bird3.png")).convert_alpha())
scoresound=pg.mixer.Sound(R("score.wav"))
losesound=pg.mixer.Sound(R("lose.wav"))
bgm=pg.mixer.Sound(R("BGM.wav"))
text=pg.font.Font(R("LTEnergy.ttf"),20)
lose=pg.transform.scale2x(pg.image.load(R("./lose.png")).convert_alpha())
score=0
speed=2
bgm.play(-1)


class Floor(pg.sprite.Sprite):
    def __init__(self):
        super(Floor,self).__init__()
        self.image=floor
        self.rect=self.image.get_rect()
        self.rect.bottomleft=bg.get_rect().bottomleft

    def update(self):
        self.rect.x-=speed
        if self.rect.left<-bg.get_width():
            self.rect.bottomleft=bg.get_rect().bottomleft

Floor_Sprite=Floor()



class PipeB(pg.sprite.Sprite):
    def __init__(self):
        super(PipeB,self).__init__()
        self.image=pipeb
        self.rect=self.image.get_rect()
        self.rect.left=screen.get_rect().right
        self.rect.top=random.choice((150,250,350))
    
    def update(self):
        self.rect.x-=speed
        if self.rect.right<0:
            self.rect.left=screen.get_rect().right
            self.rect.top=random.choice((150,250,350))

PipeB_Sprite=PipeB()
  
class PipeT(pg.sprite.Sprite):
    def __init__(self):
        super(PipeT,self).__init__()
        self.image=pipet
        self.rect=self.image.get_rect()
        self.rect.midbottom=(PipeB_Sprite.rect.centerx,PipeB_Sprite.rect.top-100)   
    
    def update(self):
        self.rect.midbottom=(PipeB_Sprite.rect.centerx,PipeB_Sprite.rect.top-100)      

PipeT_Sprite=PipeT()

Obstacle_Group=pg.sprite.Group()
Obstacle_Group.add(PipeB_Sprite)
Obstacle_Group.add(PipeT_Sprite)
Obstacle_Group.add(Floor_Sprite)

class Bird(pg.sprite.Sprite):
    def __init__(self):
        super(Bird,self).__init__()
        self.images=[bird1,bird2,bird3]
        self.index=0
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.x=50
        self.rect.y=bg.get_rect().centery
        self.vely=0
        self.accy=0
        self.angle=0
        self.counted=0

    def movements(self):
        self.accy=0.2
        if self.vely>6:
            self.accy=0

        for event in pg.event.get():
            if event.type==KEYDOWN:
                if event.key==pg.K_SPACE:
                    self.accy=-2
                    self.vely=-2
                elif event.key==pg.K_ESCAPE:
                    quit()
            elif event.type==SPEEDUP:
                global speed
                speed+=0.2
            elif event.type==QUIT:
                os.abort()

        self.vely+=self.accy
        self.rect.y+=self.vely

        if self.vely>3:
            if self.angle>-90:
                self.angle-=5
        elif self.vely<-2:
            if self.angle<45:
                self.angle+=5

    def update(self):
        self.index+=0.1
        if round(self.index)>2:
            self.index=0
        self.image=pg.transform.rotate(self.images[round(self.index)],self.angle)
        self.mask=pg.mask.from_surface(self.image)
      
Bird_Sprite=Bird()
Bird_Group=pg.sprite.Group(Bird_Sprite)

def Collision():
    if pg.sprite.groupcollide(Bird_Group,Obstacle_Group,False,False,collide_mask):
        bgm.stop()
        screen.blit(lose,(50,200))
        pg.display.flip()
        losesound.play()
        pg.time.wait(4000)
        os.abort()

def Score():
    if Bird_Sprite.rect.left>PipeB_Sprite.rect.right and Bird_Sprite.counted==False:
        global score
        score+=1
        bgm.set_volume(0.1)
        scoresound.play()
        Bird_Sprite.counted=True

    if Bird_Sprite.rect.right<PipeB_Sprite.rect.left:
        bgm.set_volume(1)
        Bird_Sprite.counted=False
    scoretext=text.render(str(score),False,(255,255,255))
    scorerect=scoretext.get_rect()
    scorerect.centerx=bg.get_width()/2
    scorerect.y=50
    screen.blit(scoretext,scorerect)

def Update():
    Bird_Sprite.update()
    Bird_Sprite.movements()
    PipeB_Sprite.update()
    PipeT_Sprite.update()
    Floor_Sprite.update()
    Score()

SPEEDUP=pg.USEREVENT

pg.time.set_timer(SPEEDUP,10000)

while 1:
    print(speed)
    clock.tick(60)
    screen.blit(bg,(0,0))
    Bird_Group.draw(screen)
    Obstacle_Group.draw(screen)
    Collision()
    Update()
    pg.display.update()