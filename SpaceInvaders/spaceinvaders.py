import pygame
from pygame.locals import *
from alien import Alien

pygame.init()

display_width = 400
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

AlienSize = (10,10)
DefenderSize = (20,20)


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

def alien(x,y,group):
    h,w = AlienSize
    pygame.draw.rect(gameDisplay,white,
                     [x,y,h,w])

class Defender():

    def __init__(self,x = display_width * .5, y = display_height * .95):
        h,w = DefenderSize
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        pygame.draw.rect(gameDisplay,red,
                        [x,y,h,w])
    
    def update(self,x_change):
        self.x += x_change
        pygame.draw.rect(gameDisplay,red,
                         [self.x,self.y,self.h,self.w])

def defender(x = 0,y = 0):
    h,w = DefenderSize
    pygame.draw.rect(gameDisplay,red,
                    [display_width*.5,display_height*.85,h,w])


def game_loop():
    gameExit = False
    
    while not gameExit:
        x_change = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[K_SPACE]:
                pass #shoot
            if keys_pressed[K_LEFT]:
                x_change = -5
            if keys_pressed[K_RIGHT]:
                x_change = 5

        gameDisplay.fill(black)        
        defender.update(x_change)
        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":
    defender = Defender()
    alien(300,300,'red')
    game_loop()