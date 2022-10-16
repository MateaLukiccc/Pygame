import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__),'img')
snd_dir = path.join(path.dirname(__file__),'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
 
#define colors
WHITE =(255,255,255)
BLACK =(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)

#initialize pygame and create window
pygame.init()
pygame.mixer.init()  #for sound and music
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shmup!")
clock =pygame.time.Clock()

font_name=pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):            #where,what,position on chosen surface
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
    
def draw_shield_bar(surf,x,y,pct):
    if pct < 0:
        pct =0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill=(pct/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)  #2-pixels wide

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
    
def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x= x+30*i
        img_rect.y=y
        surf.blit(img,img_rect)
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image,RED,self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100 #detoriates on hit
        self.shoot_delay = 250 #for auto shoot
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        
    def update(self):
        #timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() -self.power_time > POWERUP_TIME:
            self.power-=1
            self.power_time = pygame.time.get_ticks()
        #unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom= HEIGHT-10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        
        if self.rect.right >WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power ==1:
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.set_volume(0.1)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.set_volume(0.1)
                shoot_sound.play()
                
    
    def hide(self):
        #temp hide player
        self.hidden=True
        self.hide_timer=pygame.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT+200)
    
    def powerup(self):
        self.power+=1
        self.power_time = pygame.time.get_ticks() 
        
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        #for rotation
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85/ 2)
        #pygame.draw.circle(self.image,RED,self.rect.center, self.radius)        
        self.rect.x = random.randrange(0,WIDTH -self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.sppedy = random.randrange(1,8)
        self.sppedx = random.randrange(-3,3)
        #rotating meteors
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot +self.rot_speed) % 360  
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            new_image  .set_colorkey(BLACK)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
                       
    def update(self):
        self.rotate()
        self.rect.x +=self.sppedx
        self.rect.y += self.sppedy
        if self.rect.top > HEIGHT +60 or self.rect.left < -60 or self.rect.right > WIDTH +60:  #enemy respawn
            self.rect.x = random.randrange(0,WIDTH -self.rect.width)
            self.rect.y = random.randrange(-150,-100)
            self.sppedy = random.randrange(1,8)
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)   
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx= x
        self.speedy = -10
          
    def update(self):
        self.rect.y += self.speedy
        #kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()  #deletes the sprite

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)   
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
          
    def update(self):
        self.rect.y += self.speedy
        #kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()  #deletes the sprite

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=size
        self.image=explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame+=1
            if self.frame ==len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background,background_rect)
    draw_text(screen,"SHUMP!",64,WIDTH/2,HEIGHT/4)
    draw_text(screen,"Arrow keys move,Space to fire",22,WIDTH/2,HEIGHT/2)
    draw_text(screen,"Press a key to begin",18,WIDTH/2,HEIGHT*3/4)
    pygame.display.flip()
    waiting= True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting=False
  
#Load all game graphics
background = pygame.image.load(path.join(img_dir,"space.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,"playerShip.png"))
player_mini_img = pygame.transform.scale(player_img,(25,19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir,"laserRed15.png"))
meteor_images=[]
meteor_list =['meteor1.png','meteor2.png','meteor3.png','meteor4.png','meteor5.png','meteor6.png','meteor7.png','meteor8.png','meteor9.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())

explosion_anim = {}
explosion_anim['lg']=[]  #lg-large
explosion_anim['sm']=[]
explosion_anim['player']=[]
for i in range(9):
    filename='regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    filename='sonicExplosion0{}.png'.format(i)
    img=pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
    
powerup_images={}
powerup_images['shield']=pygame.image.load(path.join(img_dir,'shield_gold.png')).convert()
powerup_images['gun']=pygame.image.load(path.join(img_dir,'bolt_gold.png')).convert()


#Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser.wav'))
explosion_sounds=[]

for snd in ['explosion1.wav', 'explosion2.wav']:
    explosion_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    
player_die_sound = pygame.mixer.Sound(path.join(snd_dir,'rumble1.wav'))
pygame.mixer.music.load(path.join(snd_dir,'tgf.wav'))
pygame.mixer.music.set_volume(0.1)

pygame.mixer.music.play(loops=-1) 
#Game loop
game_over=True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over=False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()  
        player = Player()
        all_sprites.add(player)

        for i in range(15):
            newmob()
        
        score = 0
    #keep loop running at the right speed
    clock.tick(FPS)
    #Process input(events)
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT:
            running=False

    #Update
    all_sprites.update()
    
    #check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        a=random.choice(explosion_sounds)
        a.set_volume(0.1)
        a.play()
        score+= 50 -hit.radius
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()
    
    #check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)  #returns list true-disappear so that meteors only hit once
    for hit in hits:
        player.shield -= hit.radius *2
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center,'player')
            player_die_sound.play()
            all_sprites.add(death_explosion)
            player.hide()
            player.lives-=1
            player.shield=100
    #check if player hit powerup
    hits=pygame.sprite.spritecollide(player,powerups,True)
    for hit in hits:
      if hit.type == 'shield':
          player.shield += random.randrange(5,25)
          if player.shield >=100:
              player.shield=100  
      if hit.type=='gun':
          player.powerup()
          
            
    if player.lives == 0 and not death_explosion.alive():
        game_over=True
        
    #Render/Draw
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score),18,WIDTH/2,10)
    draw_shield_bar(screen,5,5,player.shield)
    draw_lives(screen,WIDTH-100,5,player.lives,player_mini_img)
    #after drawing everything
    pygame.display.flip()

pygame.quit()