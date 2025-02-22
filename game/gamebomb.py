import pygame
import os
import random


#setค่า
# WIDTH = 800
# HIGH = 600
FPS = 30
#color 
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()
pygame.mixer.init()

# screen set
screen = pygame.display.set_mode((800 , 600))

# ชื่อเกม
pygame.display.set_caption("bomb throwing game")

#เวลา
clock = pygame.time.Clock()

# Background+กำหนดภาพให้ตรงกับหน้าจอ
background = pygame.image.load("bg.jpg")
background_new = pygame.transform.scale(background,(800 , 600))

#folderimg + chackfolder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder , 'img')

# score
score = 0
font_name = pygame.font.match_font("comicsansms")


#sound
music = pygame.mixer.music.load('bgsong.mp3')
pop_sound = pygame.mixer.Sound('eff.mp3')
pygame.mixer.music.play(-1)


#player
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        kon_img = os.path.join(img_folder,'kon1.PNG')

        self.image = pygame.image.load(kon_img).convert()
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.centery = 500  

        self.speedx = 0 
    
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -15
        if keystate[pygame.K_RIGHT]:
            self.speedx = 15

        self.rect.x += self.speedx    #อัพเดตเมื่อกดkey

        if self.rect.right >= 800:    #ไม่ให้เกินกรอบ
            self.rect.right = 800

        if self.rect.left <= 0:
            self.rect.left = 0 

    def shoot(self):
        bullet = Bullet(self.rect.centerx , self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


#ตู่
class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        em = os.path.join(img_folder,'tu2.PNG')
        self.image = pygame.image.load(em).convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20,700)
        self.rect.y = random.randint(10, 200)
        self.speedx = random.randint(1,1)

    def update(self):
        
        self.rect.x += self.speedx
        if self.rect.top > 610:
            self.rect.x = random.randint(20,700)
            self.rect.y = random.randint(10, 200)
            self.speedx = random.randint(1,1)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        bullets = os.path.join(img_folder,'bomb2.PNG')
        self.image = pygame.image.load(bullets).convert()
        self.image.set_colorkey(BLACK)
    
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

def message_to_screen(message , color , font_size ,x ,y ):
    font = pygame.font.SysFont( font_name,font_size)
    text = font.render( message , True ,color)
    text_rect = text.get_rect()
    text_rect.center = (x,y)
    screen.blit( text,text_rect)



#sprites คือ player(kon)
all_sprites = pygame.sprite.Group()
kon = Player()
all_sprites.add(kon)

# enemy
enemy = pygame.sprite.Group()

#bullet
bullets = pygame.sprite.Group() 

for i in range(20):
    em = Enemy()
    all_sprites.add(em)
    enemy.add(em)


running = True 
while running:
    clock.tick(FPS)

        # check exit event(กดปิดสีแดงแล้วปิดเกม)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                kon.shoot()
               

    all_sprites.update()

    hits = pygame.sprite.groupcollide(enemy, bullets,True ,True)
    
    if hits:
        em = Enemy()
        all_sprites.add(em)
        enemy.add(em)
        # print ("Score: " +str(score))
        score += 1
        pop_sound.play()
    

    screen.blit(background_new ,(0,0) )
    all_sprites.draw(screen)
    message_to_screen("Score: " +str(score) , BLACK , 40 ,70 ,50 )
    pygame.display.flip()
    pygame.display.update()


with open("Game Score.csv" , "w") as f:
    f.write("Score update: " +str(score))


pygame.quit()