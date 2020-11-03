from Knuckle import Player
from skimage import transform 
from skimage.color import rgb2gray 
from collections import deque 




class QLearningPlayer(Player):
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
        # Dimensions 600, 500 

        stack_size = 4 #Change this number in order to stack a different number of frames 

        stacked_frames 

    


