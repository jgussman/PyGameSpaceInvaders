from ships import (Alien,None_Alien,
                    Defender,Bullet,None_Defender_Bullet)
import pygame
from pygame.locals import *
from random import randint
import numpy as np
from QLearning import QLearningNet,RandomPlayer
import time




class Game:
    """
    Base Class for Space Invaders Game that accepts human input
    """
    #Class variables that are consistent within all instances of games
    display_width = 100
    display_height = 100
    black = (0,0,0)
    white = (255,255,255)
    columns = range(40,80,5)
    rows = range(8,30,3)
    nAliens = 108
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
    def grayScaleConvert(mem):
        r, g, b = mem[:,:,0], mem[:,:,1], mem[:,:,2]
        return 0.2989 * r + 0.5870 * g + 0.1140 * b

    def __init__(self,player,level = 1, score = 0,lives = 3,train = False):
        """
        Takes a player OBJECT as the argument. 
        """
        pygame.init()
        pygame.display.set_caption('Space Invaders')
        self.gameDisplay = pygame.display.set_mode((Game.display_width,Game.display_height))
        self.gameScore = score
        self.gameExit = False
        self.train = train
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
        self.font = pygame.font.SysFont("comicsansms", 4)
        self.nMemoryStored = 0
        self.previousAction = None

    def storeMemory(self,key):
        if any([i is None for i in self.memory]):
            return
        if any([i.shape == (100,140,3) for i in self.memory]):
            return
        self.gameScore += key
        memKey = self.memoryCounter
        lastState = self.memory[memKey:] + self.memory[:memKey]
        lastState = map(lambda x: x/255,lastState)
        lastState = map(Game.grayScaleConvert,lastState)
        lastState = np.stack(lastState)
        lastState = np.reshape(lastState,(4,120,140,1))
        self.training.append((key,self.previousAction,lastState))
        self.nMemoryStored += 1

    def soft_reset(self):
        self.defender.x = Game.display_width // 2
        Alien.bullets = []
        self.defender.bullets = []
        self.gameDisplay.fill(Game.black)
        self.defender.draw()
        for alien in self.armada: alien.draw()

    def hard_reset(self):
        self.armada = []
        if isinstance(self,Game):
            cols,rows = Game.columns,Game.rows
        if isinstance(self,SimpleGame):
            cols,rows = SimpleGame.columns,SimpleGame.rows
        for c in cols:
            for r in rows:
                self.armada.append(Alien(c,r,'red',self.gameDisplay))
        self.kills = 0
        self.defender.bullets = []
        self.level += 1
        Alien.bullets = []
        Alien.xvelocity = 1 
        Alien.yvelocity = 1 
        self.defender.x = Game.display_width//2
        self.player.x = Game.display_width // 2
        self.gameDisplay.fill(Game.black)
        self.defender.draw()
        for alien in self.armada: alien.draw()
        self.gameExit = False
        self.memory = [None] * 4
        self.memoryCounter = 0
        self.training = []
        self.nMemoryStored = 0
        self.previousAction = None

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
                    if any([i is None for i in self.memory]):
                        break
                    if any([i.shape == (100,140,3) for i in self.memory]):
                        break
                    lastMemory = (self.memory[self.memoryCounter:] + 
                                  self.memory[:self.memoryCounter])
                    move = self.player.feedForward(lastMemory)
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
                # if event.type == Game.increase_velocity:
                #     Alien.increase_velocity()
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
            if self.defender.x < 0:
                self.defender.x = 95
            if self.defender.x > 100:
                self.defender.x = 0
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
            pygame.display.update()
            Game.clock.tick(30)


    def endscreen(self):
        '''function to define the end screen'''
        pass



class GameTrainer(Game):
    """
    Sub Class of Original Space Invaders Game
    Used to train QLearner object
    """
    batch_size = 64

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
                    if any([i is None for i in self.memory]):
                        break
                    if any([i.shape == (100,140,3) for i in self.memory]):
                        print('fuck')
                        break
                    lastMemory = (self.memory[self.memoryCounter:] + 
                                  self.memory[:self.memoryCounter])
                    lastMemory = map(lambda x: x/255,lastMemory)
                    lastMemory = map(Game.grayScaleConvert,lastMemory)
                    lastMemory = np.stack(lastMemory)
                    lastMemory = np.reshape(lastMemory,(4,120,140,1))
                    move = self.player.feedForward(lastMemory)
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
                # if event.type == Game.increase_velocity:
                #     Alien.increase_velocity()
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
            if self.defender.x < 0:
                self.defender.x = 1
                self.storeMemory(-3)
            if self.defender.x > Game.display_width:
                self.defender.x = 95
            for bullet in self.defender.bullets:
                if bullet.y < 0:
                    self.defender.bullets.remove(bullet)
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
            if self.nMemoryStored == GameTrainer.batch_size:
                print("TRAINING")
                self.player.train(self.training)
                self.gameExit = True
                # Change to reset quickly at first 
                # then let it play longer as it gets better
            pygame.display.update()
            Game.clock.tick(30)

class SimpleGame(Game):
    """
    Same as GameTrainer but the simplified version
    of Space Invaders
    """

    batch_size = 64
    columns = range(15,105,10)
    rows = range(14,82,6)
    endGame = USEREVENT + 8

    def set_player(self,newPlayer):
        self.player = newPlayer

    def __init__(self,player,level = 1, score = 0,lives = 3,train = False):
        """
        Takes a player OBJECT as the argument. 
        """
        pygame.init()
        pygame.display.set_caption('Space Invaders')
        self.gameDisplay = pygame.display.set_mode((Game.display_width,Game.display_height))
        self.gameScore = score
        self.gameExit = False
        self.train = train
        self.armada = []
        for c in SimpleGame.columns:
            for r in SimpleGame.rows:
                    self.armada.append(Alien(c,r,'red',self.gameDisplay))
        self.player = player
        self.defender = Defender(self.gameDisplay,Game.display_width,Game.display_height)
        self.lives = lives
        self.level = level
        self.kills = 0
        self.memory = [None] * 4
        self.memoryCounter = 0
        self.training = []
        self.font = pygame.font.SysFont("comicsansms", 4)
        self.nMemoryStored = 0
        self.previousAction = None

    def simpleStore(self,key,frame):
        frame = Game.grayScaleConvert(frame)
        frame = np.reshape(frame,(1,120,100,1))
        self.training.append((key,frame))
        self.nMemoryStored += 1

    def playGame(self):
        pygame.time.set_timer(Game.defender_reload,600)
        pygame.time.set_timer(Game.player_move,150)
        pygame.time.set_timer(Game.save_memory_slot,randint(0,30))
        self.frameAtFire = pygame.surfarray.array3d(self.gameDisplay)
        while not self.gameExit:
            # game events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == SimpleGame.endGame:
                    print(Game.nAliens - len(self.armada))
                    self.gameExit = True
                if event.type == Game.player_move:
                    curFrame = pygame.surfarray.array3d(self.gameDisplay)
                    curFrame = Game.grayScaleConvert(curFrame)
                    curFrame = np.reshape(curFrame,(1,120,100,1))
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

            # displaying score
            text = self.font.render(f"Score: {self.gameScore}",True,Game.white)
            self.gameDisplay.fill(Game.black)
            self.gameDisplay.blit(text, ((self.display_width - text.get_width()) // 2, (self.display_height - (text.get_height())) // 70))

            self.defender.draw()
            for bullet in self.defender.bullets: bullet.tick()
            for alien in self.armada: alien.draw()
            # Colisions
            if self.defender.x < 0:
                self.defender.x = 95
            if self.defender.x > Game.display_width:
                self.defender.x = 1
            for bullet in self.defender.bullets:
                if bullet.y < 0:
                    self.defender.bullets.remove(bullet)
                    self.simpleStore(-1,self.frameAtFire)
                for alien in self.armada:
                    if (alien.x-1 <= bullet.x <= alien.x+alien.w+1 and
                        alien.y-1 <= bullet.y <= alien.y+alien.h+1):
                        self.defender.bullets.remove(bullet)
                        self.armada.remove(alien)
                        #REWARD
                        self.kills += 1
                        self.simpleStore(3,self.frameAtFire)
            if self.kills == int(Game.nAliens * .75):
                self.gameExit = True
            # if self.nMemoryStored == SimpleGame.batch_size and self.train:
            #     print("TRAINING")
            #     self.player.train(self.training,False)
            #     self.gameExit = True
            pygame.display.update()
            Game.clock.tick(30)



if __name__ == "__main__":
    baseModel = "Models/results_i.h5"
    allModels = [f"Models/results_{i}.h5" for i in range(4)]
    allModels.append("Models/model.h5")
    game = SimpleGame("None_Player")
    for model in allModels:
        newPlayer = QLearningNet(previousModel = True,
                                 randomActions = False,
                                 filepath = model)
        game.set_player(newPlayer)
        begin = time.perf_counter_ns()
        game.playGame()
        game.hard_reset()
        end = time.perf_counter_ns()
        print(model)
        print(abs(begin - end))
    ## TO SEE RESULTS
    # player = QLearningNet(previousModel = True,
    #                       randomActions = False)
    # game = SimpleGame(player)
    # game.playGame()
    # TO TRAIN THE MODEL FURTHER
    # for totalLoop in range(3,100):
    #     player = QLearningNet(previousModel = True,
    #                           randomActions = False,
    #                           filepath = f"Models/results_{totalLoop-1}.h5")
    #     game = SimpleGame(player,train = True)
    #     n = 25
    #     game.playGame()
    #     for i in range(n): 
    #         game.playGame()
    #         if game.nMemoryStored < game.batch_size:
    #             player.train(game.training,False)
    #             print("training")
    #         game.hard_reset()
    #         print(f'new game {i} of {n}')
    #     player.train(game.training,True)
    #     player.store_weights(filepath = f"Models/results_{totalLoop}.h5")
    #     print(f"Target Update {totalLoop} of 100")

