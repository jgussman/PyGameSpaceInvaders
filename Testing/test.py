class Players():

    def __init__(self):
        self.score = 0
    
    def player_score(self):
        self.score += 1


class SomeGame():


    def __init__(self,player1,player2):
        self.turn = 0
        self.score = 1
        self.player1 = player1
        self.player2 = player2
    
    def playGame(self):
        turn = input("What do you wanna do")
        while turn != "N":
            if turn == "1":
                self.player1.player_score()
            if turn == "2":
                self.player2.player_score()
            turn = input("What's next")
        

if __name__ == "__main__":
    p1 = Players()
    p2 = Players()
    game = SomeGame(p1,p2)
    i = 0
    while True:
         game.playGame()
         game = SomeGame(p1,p2)
         if i == 2:
             print(p1.score)
             print(p2.score)
         i += 1
            