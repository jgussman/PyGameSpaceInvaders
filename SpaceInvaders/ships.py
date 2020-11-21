import pygame

class Bullet():
    """
    Bullet class for defenders. Makes bullets for defenders 
    also serves as superclass for alien bullets.
    """

    color = (147,112,219)
    BulletSize = (2,2)

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
        self.y -= 4
        self.rect.move_ip(self.x,self.y)

    def draw(self):
        pygame.draw.rect(self.gameDisplay,Bullet.color,
                            [self.x,self.y,
                             self.h,self.w])

    def tick(self):
        self.update()
        self.draw()

class Alien_Bullet(Bullet):
    """
    Mostly the same as Bullet class but moves downwards as opposed to 
    upwards
    """

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
    xvelocity = 1
    yvelocity = 2
    AlienSize = (5,5)
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
    
    def draw(self):
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

    def draw(self):
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

    DefenderSize = (4,4)
    BulletSize = (1,2)
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