from random import randint

class Player():

    def __init__(self):
        """
        Abstract Class for Players
        """

    def feedForward(self,inputVector):
        return input()



class RandomPlayer(Player):

    def __init__(self):
        """
        Picks a random direction and plays
        """

    def feedForward(self,inputVector):
        return randint(1,3)




class QLearningPlayer(Player):
    def __init__(self):
        """
        
        """

    def feedForward(self,inputVector):
        """

        """
