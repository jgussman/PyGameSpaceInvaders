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


class Alien():
    
    def __init__(self,x,y,group):
        h,w = AlienSize
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.group = group
        self.rect = pygame.draw.rect(gameDisplay,white,
                                     [x,y,h,w])
    
    def draw(self,surface):
        pygame.draw.rect(gameDisplay,white,
                         [self.x,self.y,self.h,self.w])


class Defender():

    def __init__(self,x = display_width * .5, y = display_height * .95):
        h,w = DefenderSize
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.rect = pygame.draw.rect(gameDisplay,red,
                                    [x,y,h,w])
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x += -2
            if self.x < 1:
                self.x = 1
            self.rect.move_ip(self.x,self.y)
        if keys[pygame.K_RIGHT]:
            self.x += 2
            if self.x > display_width - self.w:
                self.x = display_width- self.w
            self.rect.move_ip(self.x,self.y)
    
    def draw(self,surface):
        pygame.draw.rect(gameDisplay,red,
                         [self.x,self.y,self.h,self.w])

def game_loop():
    gameExit = False
    movements = {pygame.K_LEFT: -5,
                 pygame.K_RIGHT: 5}
    while not gameExit:
        x_change = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black) 
        defender.draw(gameDisplay)
        alien.draw(gameDisplay)       
        defender.update()
        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":
    defender = Defender()
    alien = Alien(100,300,'white')
    game_loop()