from Knuckle import Player
from skimage import transform 
from skimage.color import rgb2gray 
from collections import deque 




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
        print("INPUT VECTORR HEERE",inputVector)
        possible_actions = [[1,0,0],[0,1,0],[0,0,1]] #One-Hot encoded 
        # Dimensions 500, 668, 3 

        stack_size = 4 #Change this number in order to stack a different number of frames 

        #self.stacked_frames = deque([np.zeros((NEEDS TO BE THE DIM OF 1D array, dtype = np.int) for i in range(stack_size))],maxlen=stack_size)


        ### MODEL HYPERPARAMETERS
        state_size = [110, 84, 4]      # Our input is a stack of 4 frames hence 110x84x4 (Width, height, channels) 
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
        training = False

        ## TURN THIS TO TRUE IF YOU WANT TO RENDER THE ENVIRONMENT
        episode_render = False


        self.preprocess(inputVector)


    def preprocess(self,frame):
        '''
        Top-left is (0,0)
        1. Need to gray scale the frame if it is not already 
        3. Need to flatten the frame down to a 1D array 
        '''
        print("This is the type of the frame ",type(frame))
        print(frame)
        normalized = frame/255.0

        flattened_frame = normalized.flatten()
        print(flattened_frame.shape)
        return flattened_frame
    


    def stacked_frames(self,stacked_frames, state, is_new_episode): 
        #Preprocess frame 
        frame = preprocess_frame(state) 

        if is_new_episode:
            #Clear stacked_frames 
            #self.stacked_frames = deque([np.zeros((NEEDS TO BE THE DIM OF 1D array, dtype = np.int) for i in range(stack_size))],maxlen=stack_size)

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