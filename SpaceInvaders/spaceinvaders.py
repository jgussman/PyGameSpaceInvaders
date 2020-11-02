import pygame
from pygame.locals import *
from random import randint
from Knuckle import RandomPlayer,Player


class Bullet():

    color = (147,112,219)
    BulletSize = (2,5)

    def __init__(self,x,y,display):
        h,w = Bullet.BulletSize
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.gameDisplay = display
        self.rect = pygame.draw.rect(self.gameDisplay,Bullet.color,
                                    [x,y,h,w])
    
    def update(self):
        self.y -= 5
        self.rect.move_ip(self.x,self.y)

    def draw(self):
        pygame.draw.rect(self.gameDisplay,Bullet.color,
                            [self.x,self.y,
                             self.h,self.w])

    def tick(self):
        self.update()
        self.draw()

class Alien_Bullet(Bullet):

    color = (0,255,255)

    def __init__(self,x,y,display):
        h,w = Bullet.BulletSize
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.gameDisplay = display
        self.rect = pygame.draw.rect(self.gameDisplay,Alien_Bullet.color,
                                    [x,y,h,w])
    
    def update(self):
        self.y += 5
        self.rect.move_ip(self.x,self.y)

    def draw(self):
        pygame.draw.rect(self.gameDisplay,Alien_Bullet.color,
                            [self.x,self.y,
                            self.h,self.w])

    def tick(self):
        self.update()
        self.draw()

class None_Defender_Bullet(Bullet):

    def __init__(self):
        self.x = 0
        self.y = 0
    
    def update(self):
        pass

    def tick(self):
        pass

    def draw(self):
        pass

class Alien():

    bullets = []
    xvelocity = 5
    yvelocity = 10
    AlienSize = (10,10)
    white = (255,255,255)

    def __init__(self,x,y,group,display):
        h,w = Alien.AlienSize
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.group = group
        self.gameDisplay = display
        self.rect = pygame.draw.rect(self.gameDisplay,Alien.white,
                                     [x,y,h,w])
        self.direction = 0
    
    def draw(self,surface):
        pygame.draw.rect(self.gameDisplay,Alien.white,
                         [self.x,self.y,self.h,self.w])
        for bullet in Alien.bullets: bullet.draw()

    def move_side(self):
        if self.direction < 5:
            self.x -= Alien.xvelocity
        else:
            self.x += Alien.xvelocity
        self.direction = (self.direction + 1) % 10

    def move_down(self):
        self.y += Alien.yvelocity

    def increase_velocity():
        Alien.xvelocity += 1
        Alien.yvelocity += 2

    def fire_bullet(self):
        x = self.x + self.w//2
        y = self.y + self.h
        Alien.bullets.append(Alien_Bullet(x,y,self.gameDisplay)) 

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

class Defender():

    DefenderSize = (20,20)
    BulletSize = (2,5)
    red = (255,0,0)

    def __init__(self,display,display_width,display_height):
        h,w = Defender.DefenderSize
        bullet_h,bullet_w = Defender.BulletSize
        self.h = h
        self.w = w
        self.x = display_width * .5
        self.y = display_height * .95
        self.gameDisplay = display
        self.rect = pygame.draw.rect(display,Defender.red,
                                    [self.x,self.y,h,w])
        self.bullets = []
        self.loaded = False

    def move_left(self):
        self.x -= 2

    def move_right(self):
        self.x += 2

    def fire_bullet(self):
        if self.loaded:
            midShip = self.x + self.w//2
            self.bullets.append(Bullet(midShip,self.y,self.gameDisplay))
            self.loaded = False
    
    def draw(self):
        pygame.draw.rect(self.gameDisplay,Defender.red,
                         [self.x,self.y,self.h,self.w])
        for bullet in self.bullets: bullet.tick()

class Game:
    #Class variables that are consistent within all instances of games
    display_width = 500
    display_height = 600
    black = (0,0,0)
    white = (255,255,255)

    columns = range(88,413,27)
    rows = range(20,126,21)
    nAliens = 72
    alien_move_side = pygame.USEREVENT + 1
    alien_move_down = pygame.USEREVENT + 2
    defender_reload = pygame.USEREVENT + 3
    increase_velocity = pygame.USEREVENT + 4
    alien_fire_bullet = pygame.USEREVENT + 5
    player_move = pygame.USEREVENT + 6
    NONE_ALIEN = None_Alien()
    NONE_DEFENDER_BULLET = None_Defender_Bullet()

    font = None

    clock = pygame.time.Clock()

    def listReplace(lst,old,new):
        """
        assuming elemnts are uique
        so break after you find old
        """
        for index,item in enumerate(lst):
            if item == old:
                lst[index] = new
                break

    def __init__(self,player):
        """
        Takes a player OBJECT as the argument. 
        """
        pygame.init()
        pygame.display.set_caption('Space Invaders')
        self.gameDisplay = pygame.display.set_mode((Game.display_width,Game.display_height))
        self.gameScore = 0
        self.gameExit = False
        self.armada = []
        for c in Game.columns:
            for r in Game.rows:
                    self.armada.append(Alien(c,r,'red',self.gameDisplay))
        self.player = player
        self.defender = Defender(self.gameDisplay,Game.display_width,Game.display_height)

        self.font = pygame.font.SysFont("comicsansms", 20)


    def playGame(self):
        pygame.time.set_timer(Game.alien_move_side,1000)
        pygame.time.set_timer(Game.alien_move_down,5000)
        pygame.time.set_timer(Game.defender_reload,1000)
        pygame.time.set_timer(Game.increase_velocity,10000)
        pygame.time.set_timer(Game.alien_fire_bullet,750)
        pygame.time.set_timer(Game.player_move,60)
        while not self.gameExit:
            # game events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == Game.player_move:
                    inputVector = [
                        self.defender.h,
                        self.defender.w,
                        self.defender.x,
                        self.defender.y,
                        Alien.xvelocity,
                        Alien.yvelocity
                    ]
                    for alien in self.armada:
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
                    move = self.player.feedForward(inputVector)
                    if move == 1:
                        self.defender.move_left()
                    elif move == 2:
                        self.defender.move_right()
                    else:
                        self.defender.fire_bullet()
                if event.type == Game.alien_move_side:
                    for alien in self.armada: alien.move_side()
                if event.type == Game.alien_move_down:
                    for alien in self.armada: alien.move_down()
                if event.type == Game.defender_reload:
                    self.defender.loaded = True
                    pygame.time.set_timer(Game.defender_reload,1000)
                if event.type == Game.increase_velocity:
                    Alien.increase_velocity()
                if event.type == Game.alien_fire_bullet:
                    self.armada[randint(0,len(self.armada)-1)].fire_bullet()

            # displaying score
            text = self.font.render("Score: " + str(self.gameScore), True, Game.white)
            self.gameDisplay.fill(Game.black)
            self.gameDisplay.blit(text, ((self.display_width - text.get_width()) // 2, (self.display_height - (text.get_height())) // 70))

            self.defender.draw()
            for bullet in self.defender.bullets: bullet.tick()
            for bullet in Alien.bullets: bullet.tick()
            for alien in self.armada: alien.draw(self.gameDisplay)
            # Collisions
            for bullet in self.defender.bullets:
                for alien in self.armada:
                    if (bullet.x in range(alien.x,alien.x+alien.w) and
                        bullet.y in range(alien.y,alien.y+alien.h)):
                        self.defender.bullets.remove(bullet)
                        Game.listReplace(self.armada,
                                    alien,
                                    Game.NONE_ALIEN)
                        self.gameScore += 3
            for bullet in Alien.bullets:
                if bullet.y > Game.display_height:
                    Alien.bullets.remove(bullet)
                    self.gameScore += 1
                if (bullet.x in range(int(self.defender.x),int(self.defender.x+self.defender.w)+1) and
                    bullet.y in range(int(self.defender.y),int(self.defender.y+self.defender.h)+1)):
                    self.gameExit = True
            pygame.display.update()

            Game.clock.tick(60)


    def endscreen(self):
        '''function to define the end screen'''
        pass

if __name__ == "__main__":
    game = Game(RandomPlayer())
    game.playGame()