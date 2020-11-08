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


from Knuckle import Player
from skimage import transform 
from skimage.color import rgb2gray 
from collections import deque 
import tensorflow as tf 
from QLearning import QLearningNet
from Memory import Memory
import numpy as np 
from tensorflow.python.framework import ops


class QLearningPlayer(Player):
    #self.stacked_frames = deque([np.zeros((NEEDS TO BE THE DIM OF 1D array, dtype = np.int) for i in range(stack_size))],maxlen=stack_size)
    stacked_frames = 1 # This is just a place holder 
    stacked_state = 0  
    def __init__(self):
        """
        
        """

    def feedForward(self,inputVector):
        """
        Step : Action 
        --------------
        1: Preprocess frame, if the frame is not already grey scaled
        2: Append the frame to the deque that automtically, then remove the oldest frame 
        3: Then build the stacked state 
            More about the stack
            3.1: For the first frame, we feed 4 frames 
            3.2: For each timestep, we add the new frame to deque and then we stack them to form a new stacked frame 
            3.3: 

        """
        
        


    def preprocess(self,frame):
        '''
        Top-left is (0,0)
        1. Need to gray scale the frame if it is not already 
        3. Need to flatten the frame down to a 1D array 
        '''
        
        normalized = frame/255.0
        flattened_frame = normalized.flatten()
        print("FLATTENED FRAME SHAPE",flattened_frame.shape)
        print("FLATTENED FRAME SHAPE",flattened_frame.shape)
        return flattened_frame
    


    def stacked_frames(self,stacked_frames, state, is_new_episode): 
        #Preprocess frame 
        frame = preprocess_frame(state) 

        if is_new_episode:
            #Clear stacked_frames 
            self.stacked_frames  =  deque([np.zeros((500,700), dtype=np.int) for i in range(stack_size)], maxlen=4)

            #Add 4 new frames 
            for i in range(4):
                self.stacked_frames.append(frame)
            
            self.stacked_state = np.stack(stacked_frames,axis=2)
            
        else: 
            #Automatically removes the oldest frame so don't remove anything
            #This is because the maxlen is set to 
            self.stacked_frames.append(frame)

            #Build the stacked state 
            stacked_state = np.stack(self.stacked_frames,axis = 2 )
        return self.stacked_state, stacked_frames
    










def predict_action(explore_start, explore_stop, decay_rate, decay_step, state, actions):
    ## EPSILON GREEDY STRATEGY
    # Choose action a from state s using epsilon greedy.
    ## First we randomize a number
    exp_exp_tradeoff = np.random.rand()

    # Here we'll use an improved version of our epsilon greedy strategy used in Q-learning notebook
    explore_probability = explore_stop + (explore_start - explore_stop) * np.exp(-decay_rate * decay_step)
    
    if (explore_probability > exp_exp_tradeoff):
        # Make a random action (exploration)
        choice = random.randint(1,len(possible_actions))-1
        action = possible_actions[choice]
        
    else:
        # Get action from Q-network (exploitation)
        # Estimate the Qs values state
        Qs = sess.run(DQNetwork.output, feed_dict = {DQNetwork.inputs_: state.reshape((1, *state.shape))})
        
        # Take the biggest Q value (= the best action)
        choice = np.argmax(Qs)
        action = possible_actions[choice]
                
                
    return action, explore_probability


if __name__ == "__main__":
    game = Game(QLearningPlayer())
    ql = QLearningPlayer()

    possible_actions = [[1,0,0],[0,1,0],[0,0,1]] #One-Hot encoded 
    # Dimensions (500, 700, 3) 

    stack_size = 4 #Change this number in order to stack a different number of frames 

    stacked_frames  =  deque([np.zeros((500,700), dtype=np.int) for i in range(stack_size)], maxlen=4)


    ### MODEL HYPERPARAMETERS
    state_size = [500, 700, stack_size]      # Our input is a stack of 4 frames hence 110x84x4 (Width, height, channels) 
    action_size = 3
    learning_rate =  0.00025      # Alpha (aka learning rate)

    ### TRAINING HYPERPARAMETERS
    total_episodes = 50            # Total episodes for training
    max_steps = 50000              # Max possible steps in an episode
    batch_size = 64                # Batch size

    # Exploration parameters for epsilon greedy strategy
    explore_start = 1.0            # exploration probability at start
    explore_stop = 0.01            # minimum exploration probability 
    decay_rate = 0.00001           # exponential decay rate for exploration prob

    # Q learning hyperparameters
    gamma = 0.9                    # Discounting rate

    ### MEMORY HYPERPARAMETERS
    pretrain_length = batch_size   # Number of experiences stored in the Memory when initialized for the first time
    memory_size = 1000000          # Number of experiences the Memory can keep

    ### PREPROCESSING HYPERPARAMETERS
    stack_size = 4                 # Number of frames stacked

    ### MODIFY THIS TO FALSE IF YOU JUST WANT TO SEE THE TRAINED AGENT
    training = True

    ## TURN THIS TO TRUE IF YOU WANT TO RENDER THE ENVIRONMENT
    episode_render = False



    # Reset The Graph 
    ops.reset_default_graph()

    # Instantiate the Deep Learning 
    network = QLearningNet(state_size,action_size,learning_rate)

    # Setup TensorBoard Writer
    writer = tf.summary.create_file_writer("/tensorboard/dqn/1")

    # Instantiate memory
    memory = Memory(max_size = memory_size)
    for i in range(pretrain_length):
        # If it's the first step
        if i == 0:
            state = Game(QLearningPlayer())

                
            state, stacked_frames = ql.stack_frames(stacked_frames, state, True)
                
        # Get the next_state, the rewards, done by taking a random action
        choice = random.randint(1,len(possible_actions))-1
        action = possible_actions[choice]
        next_state, reward, done, _ = state, state.gameScore
            
        #env.render()
            
        # Stack the frames
        next_state, stacked_frames = stack_frames(stacked_frames, next_state, False)
            
            
        # If the episode is finished (we're dead 3x)
        if done:
            # We finished the episode
            next_state = np.zeros(state.shape)
                
            # Add experience to memory
            memory.add((state, action, reward, next_state, done))
                
            # Start a new episode
            state = Game(QLearningPlayer())
                
            # Stack the frames
            state, stacked_frames = ql.stack_frames(stacked_frames, state, True)
                
        else:
            # Add experience to memory
            memory.add((state, action, reward, next_state, done))
                
            # Our new state is now the next_state
            state = next_state

    # Setup TensorBoard Writer
    writer = tf.summary.create_file_writer("/tensorboard/dqn/1")

    ## Losses
    tf.summary.scalar("Loss", DQNetwork.loss)

    write_op = tf.summary.merge_all()



    # Saver will help us to save our model
    saver = tf.train.Saver()

    if training == True:
        with tf.Session() as sess:
            # Initialize the variables
            sess.run(tf.global_variables_initializer())

            # Initialize the decay rate (that will use to reduce epsilon) 
            decay_step = 0
                
            for episode in range(total_episodes):
                # Set step to 0
                step = 0
                    
                # Initialize the rewards of the episode
                episode_rewards = []
                    
                # Make a new episode and observe the first state
                state = Game(QLearningPlayer())
                    
                # Remember that stack frame function also call our preprocess function.
                state, stacked_frames = ql.stack_frames(stacked_frames, state, True)
                    
                while step < max_steps:
                    step += 1
                        
                    #Increase decay_step
                    decay_step +=1
                        
                    # Predict the action to take and take it
                    action, explore_probability = predict_action(explore_start, explore_stop, decay_rate, decay_step, state, possible_actions)
                        
                    #Perform the action and get the next_state, reward, and done information
                    next_state, reward, done, _ = game.step(action)
                        
                    #Not sure how to do render with pygames 
                    #if episode_render:
                    #    env.render()
                        
                    # Add the reward to total reward
                    episode_rewards.append(reward)
                        
                    # If the game is finished
                    if done:
                        # The episode ends so no next state
                        next_state = np.zeros((110,84), dtype=np.int)
                            
                        next_state, stacked_frames = ql.stack_frames(stacked_frames, next_state, False)

                        # Set step = max_steps to end the episode
                        step = max_steps

                        # Get the total reward of the episode
                        total_reward = np.sum(episode_rewards)

                        print('Episode: {}'.format(episode),
                                    'Total reward: {}'.format(total_reward),
                                    'Explore P: {:.4f}'.format(explore_probability),
                                    'Training Loss {:.4f}'.format(loss))

                        rewards_list.append((episode, total_reward))

                        # Store transition <st,at,rt+1,st+1> in memory D
                        memory.add((state, action, reward, next_state, done))

                    else:
                        # Stack the frame of the next_state
                        next_state, stacked_frames = ql.stack_frames(stacked_frames, next_state, False)
                        
                        # Add experience to memory
                        memory.add((state, action, reward, next_state, done))

                        # st+1 is now our current state
                        state = next_state
                            

                    ### LEARNING PART            
                    # Obtain random mini-batch from memory
                    batch = memory.sample(batch_size)
                    states_mb = np.array([each[0] for each in batch], ndmin=3)
                    actions_mb = np.array([each[1] for each in batch])
                    rewards_mb = np.array([each[2] for each in batch]) 
                    next_states_mb = np.array([each[3] for each in batch], ndmin=3)
                    dones_mb = np.array([each[4] for each in batch])

                    target_Qs_batch = []

                    # Get Q values for next_state 
                    Qs_next_state = sess.run(DQNetwork.output, feed_dict = {DQNetwork.inputs_: next_states_mb})
                        
                    # Set Q_target = r if the episode ends at s+1, otherwise set Q_target = r + gamma*maxQ(s', a')
                    for i in range(0, len(batch)):
                        terminal = dones_mb[i]

                        # If we are in a terminal state, only equals reward
                        if terminal:
                            target_Qs_batch.append(rewards_mb[i])
                                
                        else:
                            target = rewards_mb[i] + gamma * np.max(Qs_next_state[i])
                            target_Qs_batch.append(target)
                                

                    targets_mb = np.array([each for each in target_Qs_batch])

                    loss, _ = sess.run([DQNetwork.loss, DQNetwork.optimizer],
                                            feed_dict={DQNetwork.inputs_: states_mb,
                                                    DQNetwork.target_Q: targets_mb,
                                                    DQNetwork.actions_: actions_mb})

                    # Write TF Summaries
                    summary = sess.run(write_op, feed_dict={DQNetwork.inputs_: states_mb,
                                                        DQNetwork.target_Q: targets_mb,
                                                        DQNetwork.actions_: actions_mb})
                    writer.add_summary(summary, episode)
                    writer.flush()

                # Save model every 5 episodes
                if episode % 5 == 0:
                    save_path = saver.save(sess, "./models/model.ckpt")
                    print("Model Saved")