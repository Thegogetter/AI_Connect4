#!/usr/bin/env python3
from FourConnect import * # See the FourConnect.py file
import csv
import copy

class GameTreePlayer:
    
    def __init__(self):
        pass

    def counter(self,window,num):
        cnt=0
        for i in range(len(window)):
            if window[i]==num:
                cnt=cnt+1
        return cnt        
    
    def evaluate_func2(self,state):
        score=0
        for row in range(6):
            for col in range(5):     
                flag=True   
                for iter in range(3):
                    if state[row][col+iter]!=2:
                        flag=False
                        break
                if flag==True:
                    score=score+1  
                
        for col in range(7):
            for row in range(4):        
                flag=True
                for iter in range(3):
                    if state[row+iter][col]!=2:
                        flag=False
                        break
                if flag==True:
                    score=score+1
       
        for row in range(4):
            for col in range(5):        
                flag=True
                for iter in range(3):
                    if state[row+iter][col+iter]!=2:
                        flag=False
                        break
                if flag==True:
                    score=score+1

        for row in range(4):
            for col in range(2,7):        
                flag=True
                for iter in range(3):
                    if state[row+iter][col-iter]!=2:
                        flag=False
                        break
                if flag==True:
                   score=score+1          
        return score    
    
    def evaluate_state(self,board):
        """
        Evaluates the board state for the Connect 4 game.

        Parameters:
        board: A 2D array that represents the Connect 4 board.
        player_chip: The chip of the current player (usually 'X' or 'O').

        Returns:
        A score indicating the desirability of the position for the current player.
        """
        score = 0

        # Check horizontal spaces
        for row in range(6):
            for col in range(4):
                window=list()
                for i in range(4):
                   window.append(board[row][col+i])
                score += self.evaluate_window(window)

        # Check vertical spaces
        for col in range(7):
            for row in range(3):
                window=list()
                for i in range(4):
                   window.append(board[row+i][col])
                score += self.evaluate_window(window)

        # Check positive diagonal spaces
        for row in range(3):
            for col in range(4):
                window=list()
                for i in range(4):
                   window.append(board[row+i][col+i])
                score += self.evaluate_window(window)
        
        # Check negative diagonal spaces
        for row in range(3):
            for col in range(3, 7):
                window=list()
                for i in range(4):
                   window.append(board[row+i][col-i])
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self,window):
        """
        Evaluates a window of four board cells for Connect 4.

        Parameters:
        window: A list of 4 board cells.
        player_chip: The chip of the current player.
        opponent_chip: The chip of the opponent.

        Returns:
        A score for the window.
        """
        score = 0
        if self.counter(window,2) == 4:
            score += 100
        elif self.counter(window,2) == 3 and self.counter(window,0) == 1:
            score += 5
        elif self.counter(window,2) == 2 and self.counter(window,0) == 2:
            score += 2

        if self.counter(window,1) == 4:
            score -= 200
        elif self.counter(window,1) == 3 and self.counter(window,0) == 1:
            score -= 10
        elif self.counter(window,1) == 2 and self.counter(window,0) == 2:
            score -= 4    
        return score





    def get_next_states(self, state, player):
        next_states = []
        act=[3, 2, 4, 1, 5, 0, 6]
        # Prioritize the middle column
        for i in act:
            if self.is_valid_move(state, i):
                next_state = self.drop_coin(state, i, player)
                next_states.append((next_state, i))

        return next_states

    def is_valid_move(self,state, col):
        return state[0][col] == 0

    def drop_coin(self,state, col,player):
        new_state=copy.deepcopy(state)
        for row in range(5, -1, -1): #runs a for loop from 5 to 0 , since bottom most row has value 0
            if new_state[row][col] == 0:
                new_state[row][col] = player  # Assuming player n is putting value n into the row
                break
        return new_state
    
    
    
    
    def is_terminal(self,state):
        # Check if the current state is a terminal state or the maximum depth is reached
        if self.game_over(state,player=1) or self.game_over(state,player=2):
            return True
        for i in range(6):
            for j in range(7):
                if state[i][j]==0:
                    return False       
        return True
    
    def game_over(self,state,player):
        for row in range(6):
            for col in range(4):        
                flag=True
                for iter in range(4):
                    if state[row][col+iter]!=player:
                        flag=False
                        break
                if flag==True:
                    return True  
                
        for col in range(7):
            for row in range(3):        
                flag=True
                for iter in range(4):
                    if state[row+iter][col]!=player:
                        flag=False
                        break
                if flag==True:
                    return True 
       
        for row in range(3):
            for col in range(4):        
                flag=True
                for iter in range(4):
                    if state[row+iter][col+iter]!=player:
                        flag=False
                        break
                if flag==True:
                    return True

        for row in range(3):
            for col in range(3,7):        
                flag=True
                for iter in range(4):
                    if state[row+iter][col-iter]!=player:
                        flag=False
                        break
                if flag==True:
                    return True            
        return False
    def minimax(self, state, depth, player, alpha=float('-inf'), beta=float('inf')):
        if self.is_terminal(state) or depth == 0:
            return self.evaluate_state(state), None

        if player == 2:  # Maximizer (player 2)
            max_eval = float('-inf')
            best_move = None

            for next_state in self.get_next_states(state, player):
                eval, _ = self.minimax(next_state[0], depth - 1, player=1, alpha=alpha, beta=beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = next_state[1]

                alpha = max(alpha, eval)
                if alpha >= beta:
                    break  # Beta cutoff

            return max_eval, best_move
        else:  # Minimizer (player 1)
            min_eval = float('inf')
            best_move = None

            for next_state in self.get_next_states(state, player):
                eval, _ = self.minimax(next_state[0], depth - 1, player=2, alpha=alpha, beta=beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = next_state[1]

                beta = min(beta, eval)
                if alpha >= beta:
                    break  # Alpha cutoff

            return min_eval, best_move

     
    def FindBestAction(self,currentState):
        """
        Modify this function to search the GameTree instead of getting input from the keyboard.
        The currentState of the game is passed to the function.
        currentState[0][0] refers to the top-left corner position.
        currentState[5][6] refers to the bottom-right corner position.
        Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
        Action 0 is refers to the left-most column and action 6 refers to the right-most column.
        """
        alpha, beta = float('-inf'), float('inf')
        result, bestAction = self.minimax(currentState, 5, 2, alpha, beta)
        bestAction = int(bestAction)
        return bestAction


def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase.csv', 'r') as read_obj: 
        csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
        return testcaseState


def PlayGame():
    fourConnect = FourConnect()
    fourConnect.PrintGameState()
    gameTree = GameTreePlayer()
    
    move=0
    while move<42: #At most 42 moves are possible
        if move%2 == 0: #Myopic player always moves first
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    """
    You can add your code here to count the number of wins average number of moves etc.
    You can modify the PlayGame() function to play multiple games if required.
    """
    if fourConnect.winner==None:
       print("Game is drawn.")
    else:
        print("Winner : Player {0}\n".format(fourConnect.winner))
    print("Moves : {0}".format(move))
    return fourConnect.winner,move

def RunTestCase():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<5: #Player 2 must win in 5 moves
        if move%2 == 1: 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    print("Roll no : 2021A7PS2619G") #Put your roll number here
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))

def main():
    cnt=0
    avg=0
    avgvict=0
    for i in range(50):
        val,moves=PlayGame()
        if(val==2):
           cnt=cnt+1
           avgvict+=moves
        avg+=moves
    avg=avg/50      
    avgvict=avgvict/cnt 
    print("Number of times Player 2 wins out of 50 with depth 3 is ",cnt)
    print("Avg Number of Moves for Optimized eval function is ",avg)   
    print("Avg Number of Moves on victory for Optimized eval function is ",avgvict)           
    """
    You can modify PlayGame function for writing the report
    Modify the FindBestAction in GameTreePlayer class to implement Game tree search.
    You can add functions to GameTreePlayer class as required.
    """

    """
        The above code (PlayGame()) must be COMMENTED while submitting this program.
        The below code (RunTestCase()) must be UNCOMMENTED while submitting this program.
        Output should be your rollnumber and the bestAction.
        See the code for RunTestCase() to understand what is expected.
    """
    """
    fourier=FourConnect();
     
    stater=[
                    [0,0,0,0,0,0,0], #row 0 having columns 0 to 6 from left to right
                    [0,0,0,0,0,0,0], #row 1 having columns 0 to 6 from left to right
                    [0,0,0,0,2,0,0], #row 2 having columns 0 to 6 from left to right
                    [0,0,0,2,2,0,0], #row 3 having columns 0 to 6 from left to right
                    [0,0,2,2,2,0,0], #row 4 having columns 0 to 6 from left to right
                    [0,2,2,1,1,1,1]  #row 5 having columns 0 to 6 from left to right
                    ]
    gamer=GameTreePlayer();
    print(gamer.game_over(stater,player=1))
    """

if __name__=='__main__':
    main()
