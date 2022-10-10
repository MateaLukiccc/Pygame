# Pygame template - skeleton for a new pygame project
import pygame
import random
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

#define colors
WHITE =(255,255,255)
BLACK =(0,0,0)
RED=(255,0,0)
GREEN=(0,0,255)
BLUE=(0,0,255)

#set up assets folders
game_folder = os.path.dirname(__file__)  #gives us current file directory
img_folder = os.path.join(game_folder, "img")  #adds img in currect directory

class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"p1_jump.png")).convert()  #convert in usable data
        self.image.set_colorkey(BLACK)  #doesnt load rect so we cant see black rectangle
        self.rect = self.image.get_rect()    #hitbox
        self.rect.center = (WIDTH/2, HEIGHT/2)  #will put player in center of screen
        self.y_speed = 5
        
    def update(self):
        self.rect.x += 5  #moves by 5 pixels to the right
        self.rect.y += self.y_speed
        
        if self.rect.y > HEIGHT-200:
            self.y_speed =-5
        if self.rect.top < 200:
            self.y_speed = 5
        if self.rect.left>WIDTH:
            self.rect.right = 0
        
          
#initialize pygame and create window
pygame.init()
pygame.mixer.init()  #for sound and music
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("My Game")
clock =pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
#Game loop
running = True
while running:
    #keep loop running at the right speed
    clock.tick(FPS)
    #Process input(events)
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT:
            running=False
    #Update
    all_sprites.update()
    
    #Render/Draw
    screen.fill(BLUE)
    all_sprites.draw(screen)   #will draw all sprites
    #after drawing everything
    pygame.display.flip()

pygame.quit()
