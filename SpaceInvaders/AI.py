from Knuckle import Player
from skimage import transform 
from skimage.color import rgb2gray 
from collections import deque 




class QLearningPlayer(Player):
    self.stacked_frames = deque([np.zeros((NEEDS TO BE THE DIM OF 1D array, dtype = np.int) for i in range(stack_size))],maxlen=stack_size)
    self.stacked_state = 0  
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
        possible_actions = [[1,0,0],[0,1,0],[0,0,1]] #One-Hot encoded 
        # Dimensions 500, 668, 3 

        stack_size = 4 #Change this number in order to stack a different number of frames 

        self.stacked_frames = deque([np.zeros((NEEDS TO BE THE DIM OF 1D array, dtype = np.int) for i in range(stack_size))],maxlen=stack_size)


    def preprocess(self,frame):
        '''
        Top-left is (0,0)
        1. Need to gray scale the frame if it is not already 
        2. Need to remove the score from the scree: DONEZO
        3. Need to flatten the frame down to a 1D array 
        '''


        flattened_frame = frame.flatten()
        return flattened_frame
    


    def stacked_frames(self,stacked_frames, state, is_new_episode): 
        #Preprocess frame 
        frame = preprocess_frame(state) 

        if is_new_episode:
            #Clear stacked_frames 
            self.stacked_frames = deque([np.zeros((NEEDS TO BE THE DIM OF 1D array, dtype = np.int) for i in range(stack_size))],maxlen=stack_size)

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