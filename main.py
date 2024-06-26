import pygame
pygame.init()
win=pygame.display.set_mode((500,500))

pygame.display.set_caption("mariogame")

# Thesepicturesmustbepartofworkingdirectory theyarelocatedin"pygame_imagesfolderincodefold"
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock=pygame.time.Clock()
scr=0
hitsound=pygame.mixer.Sound('goblinhit.mp3')
bulletsound=pygame.mixer.Sound('shot.mp3')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

class player(object):
    def __init__(self,x,y,width,height) :
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.isJump=False
        self.jumpCount=10
        self.left=False
        self.right=False
        self.walkCt=0
        self.standing=True
        self.hitbox=(self.x + 20,self.y+10,28,52)
        self.health=50

    def draw (self,win):
        if(self.walkCt+1 >=27):
            self.walkCt=0
        if not (self.standing):
            if self.left :
                win.blit(walkLeft[self.walkCt//3],(self.x,self.y))
                self.walkCt+=1
            elif self.right :
                win.blit(walkRight[self.walkCt//3],(self.x,self.y))
                self.walkCt+=1
        else :
            if self.left :
                win.blit(walkLeft[0],(self.x,self.y))
            else :
                win.blit(walkRight[0],(self.x,self.y))
        self.hitbox=(self.x +20,self.y+10,28,52)
        pygame.draw.rect(win,"red",(self.hitbox[0],self.hitbox[1]-20,50,10))
        pygame.draw.rect(win,"green",(self.hitbox[0],self.hitbox[1]-20,self.health,10))
        # pygame.draw.rect(win,"red",self.hitbox,2)
    def hit(self):
        self.health-=10
        self.x=20
        self.walkCt=0
        text=font.render('-10 Health',1,'black')
        win.blit(text,(250-text.get_width()/2 , 200))
        pygame.display.update()
        pygame.time.delay(1000)
        self.y=420
        self.isJump=False
        self.jumpCount=10


class  projectile (object):
    def __init__(self,x,y,radius,color,direction) :
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.direction=direction
        self.vel=10*direction

    def draw (self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

class goblin (object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png')]

    def __init__(self,x,y,width,height,end ):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path=[self.x,self.end]
        self.walkCt=0
        self.vel=4
        self.hitbox=(self.x +20,self.y,28,60)
        self.health=50
        self.visible=True

    def draw(self,win):
        self.move()
        if (self.visible):
            if(self.walkCt+1 >=27):
                self.walkCt=0
            if self.vel >0 :
                win.blit(self.walkRight[ self.walkCt//3 ],(self.x , self.y))
                self.walkCt+=1
            else :
                win.blit(self.walkLeft[self.walkCt//3],(self.x,self.y))
                self.walkCt+=1
            self.hitbox=(self.x +20,self.y,28,60)
            
            pygame.draw.rect(win,"red",(self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(win,"dark green",(self.hitbox[0],self.hitbox[1]-20,self.health,10))
        # pygame.draw.rect(win,"red",self.hitbox,2)
    
    def hit(self):
        if self.health==0:
            self.visible =False
            text=font.render('goblin is now invisible;>',1,'black')
            win.blit(text,(250-text.get_width()/2 , 200))
            pygame.display.update()
            pygame.time.delay(1000)
        elif self.health>0 :
            self.health-=5
        print("hit")
        

    def move(self):
        if(self.vel >0):
            if(self.x + self.vel <self.path[1] ):
                self.x+=self.vel
            else:
                self.vel=self.vel *-1
                self.walkCt=0
        else:
            if self.x - self.vel >self.path[0]:
                self.x+=self.vel
            else:
                self.vel=self.vel *-1
                self.walkCt=0
        
def drawGamewindow():
    
    win.blit(bg,(0,0))
    text=font.render('Score:'+ str(scr),1,'red')
    win.blit(text,(390,10))
    man.draw(win)
    gob.draw(win)
    for bullet in bullets :
        bullet.draw(win)
    pygame.display.update()

#main loop
font=pygame.font.SysFont('calibri',25)
man=player(0,420,64,64)
gob=goblin(120,425,64,64,440)
bullets=[]
bulletchek=0
run =True
while run:
    clock.tick(27)
    if man.health ==0:
        text=font.render('you died!',1,'black')
        win.blit(text,(250-text.get_width()/2 , 200))
        pygame.display.update()
        pygame.time.delay(1000)
        pygame.QUIT()
    if(man.hitbox[1] <gob.hitbox[1] + gob.hitbox[3] and man.hitbox[1] +man.hitbox[3] >gob.hitbox[1]):
        if(man.hitbox[0]+man.hitbox[2]>gob.hitbox[0] and man.hitbox[0]<gob.hitbox[0]+gob.hitbox[2]):
            hitsound.play()
            man.hit()

    if bulletchek>0 :
        bulletchek+=1
    if bulletchek>3:
       bulletchek=0 

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run=False
    
    for bullet in bullets:
        if(bullet.y <gob.hitbox[1] + gob.hitbox[3] and bullet.y >gob.hitbox[1]):
            if(bullet.x>gob.hitbox[0] and bullet.x<gob.hitbox[0]+gob.hitbox[2]):
                if gob.health>=0:
                    hitsound.play()
                    scr+=10
                gob.hit()
                bullets.pop(bullets.index(bullet))
        if bullet.x <500 and bullet.x>0:
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    
    keys =pygame.key.get_pressed()

    if keys[ pygame.K_SPACE] and bulletchek==0:
        bulletchek+=1
        bulletsound.play()
        if man.left :
            side=-1
        else:
            side=1
        if len(bullets)<5 :
            bullets.append(projectile(round(man.x + man.width //2),round(man.y + man.height//2),5,"red", side ))

    if keys[pygame.K_LEFT] and man.x > 0:
        man.x-=man.vel
        man.left=True
        man.right=False
        man.standing=False
    elif keys[pygame.K_RIGHT] and man.x <460:
        man.x+=man.vel
        man.left=False
        man.right=True
        man.standing=False
    else:
        man.standing=True
        man.walkCt=0    
    if not (man.isJump):
        # if keys[pygame.K_UP] and y > 0:
        #     y-=vel
        # if keys[pygame.K_DOWN] and y<440:
        #     y+=vel
        if keys[pygame.K_UP] :
            man.isJump =True
            man.left=False
            man.right=False
            man.walkCt=0
    else :
        if(man.jumpCount >= -10):
            neg=1
            if(man.jumpCount<0):
                neg=-1
            man.y-= ((man.jumpCount ** 2)  *neg)*0.2
            man.jumpCount -= 1
            if man.jumpCount==-11 :
                man.isJump=False
                man.jumpCount=10
        else: 
            man.isJump=False
            man.jumpCount =10
    
    drawGamewindow()

pygame.quit()
