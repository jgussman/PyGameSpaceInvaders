import pygame
from pygame.locals import *
from random import randint
from Knuckle import Player
pygame.init()

display_width = 400
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
purple = (147,112,219)
blue = (0,255,255)
AlienSize = (10,10)
BulletSize = (2,5)
DefenderSize = (20,20)


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

class Alien_Bullet():

    def __init__(self,x,y):
        h,w = BulletSize
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.rect = pygame.draw.rect(gameDisplay,blue,
                                    [x,y,h,w])
    
    def update(self):
        self.y += 5
        self.rect.move_ip(self.x,self.y)

    def tick(self):
        self.y += 5
        self.rect.move_ip(self.x,self.y)
        pygame.draw.rect(gameDisplay,blue,
                            [self.x,self.y,
                            self.h,self.w])

    def draw(self):
        pygame.draw.rect(gameDisplay,blue,
                            [self.x,self.y,
                            self.h,self.w])

class Alien():

    bullets = []
    xvelocity = 5
    yvelocity = 10

    def __init__(self,x,y,group):
        h,w = AlienSize
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.group = group
        self.rect = pygame.draw.rect(gameDisplay,white,
                                     [x,y,h,w])
        self.direction = 0
    
    def draw(self,surface):
        pygame.draw.rect(gameDisplay,white,
                         [self.x,self.y,self.h,self.w])
        for bullet in Alien.bullets: bullet.draw()

    def move_side(self):
        if self.direction < 5:
            self.x -= Alien.xvelocity
        else:
            self.x += Alien.xvelocity
        self.direction = (self.direction + 1) % 11

    def move_down(self):
        self.y += Alien.yvelocity

    def increase_velocity():
        Alien.xvelocity += 1
        Alien.yvelocity += 2

    def fire_bullet(self):
        x = self.x + self.w//2
        y = self.y + self.h
        Alien.bullets.append(Alien_Bullet(x,y)) 

class None_Alien(Alien):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.h = 0
        self.w = 0
    def draw(self,surface):
        pass

    def move_side(self):
        pass

    def move_down(self):
        pass

    def increase_velocity(self):
        pass

    def fire_bullet(self):
        pass


class Defender_Bullet():

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

    def tick(self):
        self.y -= 5
        self.rect.move_ip(self.x,self.y)
        pygame.draw.rect(gameDisplay,purple,
                            [self.x,self.y,
                            self.h,self.w])

    def draw(self):
        pygame.draw.rect(gameDisplay,purple,
                            [self.x,self.y,
                            self.h,self.w])

class None_Defender_Bullet(Defender_Bullet):

    def __init__(self):
        self.x = 0
        self.y = 0
    
    def update(self):
        pass

    def tick(self):
        pass

    def draw(self):
        pass

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
        self.bullets = []
        self.loaded = False

        # dealings w/ ghosts
        self.width = 0

    def move_left(self):
        self.x -= 2

    def move_right(self):
        self.x += 2

    def fire_bullet(self):
        if self.loaded:
            midShip = self.x + self.w//2
            self.bullets.append(Defender_Bullet(midShip))
            self.loaded = False
    
    def draw(self,surface):
        pygame.draw.rect(gameDisplay,red,
                         [self.x,self.y,self.h,self.w])
        for bullet in self.bullets: bullet.tick()
        
    def get_x(self):
        return self.x

def game_loop():
    GAME_SCORE = 0
    def listReplace(lst,old,new):
        """
        assuming elements are unique
        So break after you find old
        """
        for index,item in enumerate(lst):
            if item == old:
                lst[index] = new
                break

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
    while not gameExit:
        x_change = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == player_move:
                inputVector = [
                    defender.h,
                    defender.w,
                    defender.x,
                    defender.y,
                    Alien.xvelocity,
                    Alien.yvelocity
                ]
                for alien in armada:
                    inputVector.extend(
                        [alien.x,
                        alien.y]
                    )
                for i in range(3):
                    try:
                        inputVector.extend(
                            [Alien.bullets[i].x,
                            Alien.bullets[i].y]
                        )
                    except:
                        inputVector.extend([0,0])
                move = player.feedForward(inputVector)
                if move == 1:
                    defender.move_left()
                elif move == 2:
                    defender.move_right()
                else:
                    defender.fire_bullet()
            if event.type == alien_move_side:
                for alien in armada: alien.move_side()
            if event.type == alien_move_down:
                for alien in armada: alien.move_down()
            if event.type == defender_reload:
                defender.loaded = True
                pygame.time.set_timer(defender_reload,1000)
            if event.type == increase_velocity:
                Alien.increase_velocity()
            if event.type == alien_fire_bullet:
                armada[randint(0,len(armada)-1)].fire_bullet()

        gameDisplay.fill(black) 
        defender.draw(gameDisplay)
        for bullet in defender.bullets: bullet.tick()
        for bullet in Alien.bullets: bullet.tick()
        for alien in armada: alien.draw(gameDisplay)
        # Collisions
        for bullet in defender.bullets:
            for alien in armada:
                if (bullet.x in range(alien.x,alien.x+alien.w) and
                    bullet.y in range(alien.y,alien.y+alien.h)):
                    defender.bullets.remove(bullet)
                    listReplace(armada,
                                alien,
                                NONE_ALIEN)
                    GAME_SCORE += 3
        for bullet in Alien.bullets:
            if bullet.y > display_height:
                Alien.bullets.remove(bullet)
                GAME_SCORE += 1
            if (bullet.x in range(int(defender.x),int(defender.x+defender.w)+1) and
                bullet.y in range(int(defender.y),int(defender.y+defender.h)+1)):
                gameExit = True
        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":
    defender = Defender()
    armada = []
    columns = range(50,351,27)
    rows = range(20,126,21)
    for c in columns:
        for r in rows:
            armada.append(Alien(c,r,'red'))
    nAliens = 72
    alien_move_side = pygame.USEREVENT + 1
    alien_move_down = pygame.USEREVENT + 2
    defender_reload = pygame.USEREVENT + 3
    increase_velocity = pygame.USEREVENT + 4
    alien_fire_bullet = pygame.USEREVENT + 5
    player_move = pygame.USEREVENT + 6
    pygame.time.set_timer(alien_move_side,1000)
    pygame.time.set_timer(alien_move_down,5000)
    pygame.time.set_timer(defender_reload,1000)
    pygame.time.set_timer(increase_velocity,10000)
    pygame.time.set_timer(alien_fire_bullet,1500)
    pygame.time.set_timer(player_move,60)
    player = Player()
    NONE_ALIEN = None_Alien()
    NONE_DEFENDER_BULLET = None_Defender_Bullet()
    game_loop()