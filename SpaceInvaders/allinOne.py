import tensorflow as tf      # Deep Learning library
import numpy as np           # Handle matrices
from spaceinvaders import Game
from AI import QLearningPlayer
from skimage import transform # Help us to preprocess the frames
from skimage.color import rgb2gray # Help us to gray our frames
import matplotlib.pyplot as plt # Display graphs
from collections import deque# Ordered collection with ends
import random
import warnings # This ignore all the warning messages that are normally printed during the training because of skiimage
from QLearning import QLearningNet
from tensorflow.python.framework import ops
warnings.filterwarnings('ignore')


#Create Environment 
env = Game(QLearningPlayer)

# possible_actions = [[1,0,0],[0,1,0],[0,0,1]] #One-Hot encoded  



    
# stack_size = 4 # We stack 4 frames

# # Initialize deque with zero-images one array for each image
# stacked_frames  =  deque([np.zeros((500,700), dtype=np.int) for i in range(stack_size)], maxlen=4)




# ### MODEL HYPERPARAMETERS
# state_size = [500, 700, stack_size]      # Our input is a stack of 4 frames hence 110x84x4 (Width, height, channels) 
# action_size = 3
# learning_rate =  0.00025      # Alpha (aka learning rate)

# ### TRAINING HYPERPARAMETERS
# total_episodes = 50            # Total episodes for training
# max_steps = 50000              # Max possible steps in an episode
# batch_size = 64                # Batch size

# # Exploration parameters for epsilon greedy strategy
# explore_start = 1.0            # exploration probability at start
# explore_stop = 0.01            # minimum exploration probability 
# decay_rate = 0.00001           # exponential decay rate for exploration prob

# # Q learning hyperparameters
# gamma = 0.9                    # Discounting rate
# ### MEMORY HYPERPARAMETERS
# pretrain_length = batch_size   # Number of experiences stored in the Memory when initialized for the first time
# memory_size = 1000000          # Number of experiences the Memory can keep

# ### PREPROCESSING HYPERPARAMETERS
# stack_size = 4                 # Number of frames stacked

# ### MODIFY THIS TO FALSE IF YOU JUST WANT TO SEE THE TRAINED AGENT
# training = True

# ## TURN THIS TO TRUE IF YOU WANT TO RENDER THE ENVIRONMENT
# episode_render = False

# Reset The Graph 
ops.reset_default_graph()

# Instantiate the DQNetwork
DQNetwork = QLearningNet(state_size, action_size, learning_rate)

# Instantiate memory
memory = Memory(max_size = memory_size)
for i in range(pretrain_length):
    # If it's the first step
    if i == 0:
        state = Game(QLearningPlayer)

        previousFrame = state.memory[state.memoryCounter-1]
        state, stacked_frames = stack_frames(stacked_frames, previousFrame, True)
                
    # Get the next_state, the rewards, done by taking a random action
    choice = random.randint(1,len(possible_actions))-1
    action = possible_actions[choice]
    next_state, reward, done, _ = env.step(action)
            
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
        state = env.reset()
                
        # Stack the frames
        state, stacked_frames = stack_frames(stacked_frames, state, True)
                
    else:
        # Add experience to memory
        memory.add((state, action, reward, next_state, done))
                
        # Our new state is now the next_state
        state = next_state


# Setup TensorBoard Writer
writer = tf.summary.FileWriter("/tensorboard/dqn/1")

## Losses
tf.summary.scalar("Loss", DQNetwork.loss)

write_op = tf.summary.merge_all()

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
            state = env.reset()
                    
            # Remember that stack frame function also call our preprocess function.
            state, stacked_frames = stack_frames(stacked_frames, state, True)
                    
            while step < max_steps:
                step += 1
                        
                #Increase decay_step
                decay_step +=1
                        
                # Predict the action to take and take it
                action, explore_probability = predict_action(explore_start, explore_stop, decay_rate, decay_step, state, possible_actions)
                        
                #Perform the action and get the next_state, reward, and done information
                next_state, reward, done, _ = env.step(action)
                        
                if episode_render:
                    env.render()
                        
                # Add the reward to total reward
                episode_rewards.append(reward)
                        
                # If the game is finished
                if done:
                    # The episode ends so no next state
                    next_state = np.zeros((110,84), dtype=np.int)
                            
                    next_state, stacked_frames = stack_frames(stacked_frames, next_state, False)

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
                    next_state, stacked_frames = stack_frames(stacked_frames, next_state, False)
                        
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