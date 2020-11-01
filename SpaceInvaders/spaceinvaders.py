import pygame
from pygame.locals import *

pygame.init()

display_width = 400
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
purple = (147,112,219)

AlienSize = (10,10)
BulletSize = (2,5)
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
    
    def update(self):
        '''
        to update the alien....going to need to have awareness of rows
        rows will also move down and repeatedly go left/right

        given the whole sprite list will find a range to conditonally check when to go up/down 
        will be based on a all_sprites_list

        will also be based on updating properties of self
        '''
        pass

class Bullet():

    def __init__(self,x,y =display_height * .95):
        h,w = BulletSize
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.rect = pygame.draw.rect(gameDisplay,purple,
                                    [x,y,h,w])
    
    def update(self):
        self.y -= 5
        self.rect.move_ip(self.x,self.y)

class Defender():

    def __init__(self,x = display_width * .5, y = display_height * .95):
        h,w = DefenderSize
        bullet_h,bullet_w = BulletSize
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.rect = pygame.draw.rect(gameDisplay,red,
                                    [x,y,h,w])
        self.bullet = None
        self.bullet_x = x
        self.bullet_y = y
        self.bullet_h = bullet_h
        self.bullet_w = bullet_w

        # dealings w/ ghosts
        self.width = 0
    
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
        if keys[pygame.K_SPACE]:
            ## add processing here to only trigger fire_bullet when there is non existant bullet here
            self.fire_bullet()
        if not (self.bullet is None):
            self.update_bullet()

        
    def fire_bullet(self):
        self.bullet_x = self.x + self.w//2
        self.bullet_y = self.y-5
        self.bullet = pygame.draw.rect(gameDisplay,purple,
                                        [self.bullet_x,self.bullet_y,
                                         self.bullet_h,self.bullet_w])
    
    def draw(self,surface):
        pygame.draw.rect(gameDisplay,red,
                         [self.x,self.y,self.h,self.w])
        if not (self.bullet is None):
            pygame.draw.rect(gameDisplay,purple,
                             [self.bullet_x,self.bullet_y,
                              self.bullet_h,self.bullet_w])

    def update_bullet(self):
        self.bullet_y -= 2
        self.bullet = pygame.draw.rect(gameDisplay,purple,
                                       [self.bullet_x,self.bullet_y,
                                       self.bullet_h,self.bullet_w])
        if self.bullet_y < 0:
            self.bullet = None
            self.bullet_y = self.y
        
    
    def get_x(self):
        return self.x

def game_loop():
    '''
    Main Loop of games
    Include:
    1.events
    2.collisions
    3.bullet system tracker
    4.clock
    5.sprites
    '''
    gameExit = False
    bullet = None
    while not gameExit:
        x_change = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black) 
        defender.draw(gameDisplay)
        alien.draw(gameDisplay)  
        print(defender.x)
        defender.update()
        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":
    defender = Defender()
    alien = Alien(100,300,'white')
    game_loop()