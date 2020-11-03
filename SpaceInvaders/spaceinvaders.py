from ships import (Alien,None_Alien,
                    Defender,Bullet,None_Defender_Bullet)
from Knuckle import RandomPlayer,Player
import pygame
from pygame.locals import *
from random import randint
import numpy as np
from PIL import Image
from AI import QLearningPlayer
class Game:
    #Class variables that are consistent within all instances of games
    display_width = 500
    display_height = 700
    black = (0,0,0)
    white = (255,255,255)
    columns = range(88,413,27)
    rows = range(40,146,21)
    nAliens = 72
    alien_move_side = pygame.USEREVENT + 1
    alien_move_down = pygame.USEREVENT + 2
    defender_reload = pygame.USEREVENT + 3
    increase_velocity = pygame.USEREVENT + 4
    alien_fire_bullet = pygame.USEREVENT + 5
    player_move = pygame.USEREVENT + 6
    save_memory_slot = pygame.USEREVENT + 7
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

    def __init__(self,player,level = 1, score = 0,lives = 3):
        """
        Takes a player OBJECT as the argument. 
        """
        pygame.init()
        pygame.display.set_caption('Space Invaders')
        self.gameDisplay = pygame.display.set_mode((Game.display_width,Game.display_height))
        self.gameScore = score
        self.gameExit = False
        self.armada = []
        for c in Game.columns:
            for r in Game.rows:
                    self.armada.append(Alien(c,r,'red',self.gameDisplay))
        self.player = player
        self.defender = Defender(self.gameDisplay,Game.display_width,Game.display_height)
        self.lives = lives
        self.level = level
        self.kills = 0
        self.memory = [None] * 4
        self.memoryCounter = 0
        self.training = []
        self.font = pygame.font.SysFont("comicsansms", 20)
        self.nMemoryStored = 0
        self.previousAction = None

    def storeMemory(self,key):
        self.gameScore += key
        memKey = self.memoryCounter
        lastState = self.memory[memKey:] + self.memory[:memKey]
        self.training.append((key,self.previousAction,lastState))
        self.nMemoryStored += 1

    def soft_reset(self):
        self.player.x = Game.display_width // 2
        Alien.bullets = []
        self.defender.bullets = []
        self.gameDisplay.fill(Game.black)
        self.defender.draw()
        for alien in self.armada: alien.draw()

    def hard_reset(self):
        self.armada = []
        for c in Game.columns:
            for r in Game.rows:
                self.armada.append(Alien(c,r,'red',self.gameDisplay))
        self.kills = 0
        self.defender.bullets = []
        self.level += 1
        Alien.bullets = []
        Alien.xvelocity = 4 + self.level
        Alien.yvelocity = 9 + (self.level*2)
        self.player.x = Game.display_width // 2
        self.gameDisplay.fill(Game.black)
        self.defender.draw()
        for alien in self.armada: alien.draw()

    def playGame(self):
        pygame.time.set_timer(Game.alien_move_side,1000)
        pygame.time.set_timer(Game.alien_move_down,5000)
        pygame.time.set_timer(Game.defender_reload,1000)
        pygame.time.set_timer(Game.increase_velocity,10000)
        pygame.time.set_timer(Game.alien_fire_bullet,750)
        pygame.time.set_timer(Game.player_move,60)
        pygame.time.set_timer(Game.save_memory_slot,randint(0,30))
        while not self.gameExit:
            # game events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == Game.player_move:
                    curFrame = pygame.surfarray.array3d(self.gameDisplay)
                    move = self.player.feedForward(curFrame)
                    self.previousAction = move
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
                if event.type == Game.save_memory_slot:
                    self.memory[self.memoryCounter] = pygame.surfarray.array3d(self.gameDisplay)
                    self.memoryCounter = (self.memoryCounter + 1) % 4

            # displaying score
            text = self.font.render(f"Score: {self.gameScore}",True,Game.white)
            self.gameDisplay.fill(Game.black)
            self.gameDisplay.blit(text, ((self.display_width - text.get_width()) // 2, (self.display_height - (text.get_height())) // 70))

            self.defender.draw()
            for bullet in self.defender.bullets: bullet.tick()
            for bullet in Alien.bullets: bullet.tick()
            for alien in self.armada: alien.draw()
            # Colisions
            for bullet in self.defender.bullets:
                if bullet.y < 0:
                    self.defender.bullets.remove(bullet)
                    self.storeMemory(-1)
                for alien in self.armada:
                    if (bullet.x in range(alien.x,alien.x+alien.w) and
                        bullet.y in range(alien.y,alien.y+alien.h)):
                        self.defender.bullets.remove(bullet)
                        Game.listReplace(self.armada,
                                    alien,
                                    Game.NONE_ALIEN)
                        #REWARD
                        self.gameScore += 3 * (self.level)
                        self.kills += 1
                        self.storeMemory(3)
                    if alien.y >= self.defender.y:
                        self.gameExit = True

            for bullet in Alien.bullets:
                if bullet.y > Game.display_height:
                    Alien.bullets.remove(bullet)
                    self.gameScore += 1 * (self.level)
                    self.storeMemory(1)
                if (bullet.x in range(int(self.defender.x),int(self.defender.x+self.defender.w)+1) and
                    bullet.y in range(int(self.defender.y),int(self.defender.y+self.defender.h)+1)):
                    self.lives -= 1
                    if self.lives == 0:
                        self.gameExit = True
                    self.soft_reset()
                    pygame.time.wait(1000)
                    break
            if self.kills == Game.nAliens:
                self.hard_reset()
                pygame.time.wait(1000)
            if self.nMemoryStored == 64:
                counter = 0
                with open("SpaceInvaders/training.csv",'w') as data:
                    data.write("Reward,Action,state\n")
                    for point in self.training:
                        reward,action,lst2d = point
                        lst2d = [np.delete(i,slice(0,32),1) for i in lst2d]
                        np.savez(f"SpaceInvaders/savedStates/{counter}",*lst2d)
                        data.write(f"{reward}, {action}, SpaceInvaders/savedStates/{counter}.npz")
                        data.write("\n")
                        counter += 1
                self.gameExit = True
            pygame.display.update()
            Game.clock.tick(30)


    def endscreen(self):
        '''function to define the end screen'''
        pass

if __name__ == "__main__":
    game = Game(QLearningPlayer())
    game.playGame()

