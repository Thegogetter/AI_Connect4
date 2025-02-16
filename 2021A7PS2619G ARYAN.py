
from FourConnect import * # See the FourConnect.py file
import csv
import time #to check time differences on running code with and without move ordering heuristics 
import copy #to implement deep copy function 

class GameTreePlayer:
    
    def __init__(self):
        self.recursive_calls=0 #to check the number of recursive calls per move 
        pass

    def counter(self,window,player): #counts the number of player coins in a window 
        cnt=0
        for i in range(len(window)):
            if window[i]==player:
                cnt=cnt+1
        return cnt        
    
        
    def evaluate_func2(self,state,player): # A very medicore eval function which counts the number of consecutive 3 player coins 
        score=0
        #horizontal check 
        for row in range(6):
            for col in range(5):     
                flag=True   
                for iter in range(3):
                    if state[row][col+iter]!=player:
                        flag=False
                        break
                if flag==True:
                    score=score+1  
        #vertical check        
        for col in range(7):
            for row in range(4):        
                flag=True
                for iter in range(3):
                    if state[row+iter][col]!=player:
                        flag=False
                        break
                if flag==True:
                    score=score+1
        #positive diagonal check
        for row in range(4):
            for col in range(5):        
                flag=True
                for iter in range(3):
                    if state[row+iter][col+iter]!=player:
                        flag=False
                        break
                if flag==True:
                    score=score+1
        #negative diagonal check
        for row in range(4):
            for col in range(2,7):        
                flag=True
                for iter in range(3):
                    if state[row+iter][col-iter]!=player:
                        flag=False
                        break
                if flag==True:
                   score=score+1          
        return score

    def evaluate_state(self,state): #Checks every window of size 4 in the connect 4 system 
        score = 0
        # find all windows of size 4 horizontally
        for row in range(6):
            for col in range(4):
                window=list()
                for i in range(4):
                   window.append(state[row][col+i])
                score += self.windowscore(window)
        # find all windows of size 4 on vertical columns 
        for col in range(7):
            for row in range(3):
                window=list()
                for i in range(4):
                   window.append(state[row+i][col])
                score += self.windowscore(window)
        # find all windows of size 4 on positive diagonal 
        for row in range(3):
            for col in range(4):
                window=list()
                for i in range(4):
                   window.append(state[row+i][col+i])
                score += self.windowscore(window)
        # find all windows of size 4 on negative diagonal  
        for row in range(3):
            for col in range(3, 7):
                window=list()
                for i in range(4):
                   window.append(state[row+i][col-i])
                score += self.windowscore(window)

        return score

    def windowscore(self,window): 
        """
        reads the window and provides scores to those windows according to the number of player 2 coins 
        and player 1 coins , check the code for exact score i have provided , here i havent provided any significance to consecutive 3's 
        i just look at a bunch of 3 player 2 coins in a window , for example 2 2 2 0 and 2 2 0 2 have the same score 20 , similary for 2 player 2 
        2 player 1 coins 
        """ 
        score = 0
        if self.counter(window,2) == 4:
            score += 200
        elif self.counter(window,0) == 1 and self.counter(window,2) == 3 :
            score += 20
        elif self.counter(window,2) == 2 and self.counter(window,0) == 2:
            score += 4

        if self.counter(window,1) == 4:
            score -= 400
        elif self.counter(window,0) == 1 and self.counter(window,1) == 3 :
            score -= 40
        elif self.counter(window,1) == 2 and self.counter(window,0) == 2:
            score -= 8  
        return score


    def take_action(self,state,action,player): #performs the action of placing a coin at a given column (column is signified by action)
        new_state=copy.deepcopy(state) #imported the copy module for deep copying 
        for row in range(5,-1,-1):
            if new_state[row][action]==0:
               new_state[row][action]=player
               break
        return new_state


    def next_states(self,state,player):
        stater=list()
        act=[3,2,4,1,5,0,6] 
        """
        this I implemented for move ordering , here I prioritised the middle columns,
        The reason I prioritised the middle columns has been provided by me in the report Q.1)c) 
        """ 
        for i in act:
            if state[0][i]==0:  #means a valid move since topmost column isnt empty 
               next_state=self.take_action(state,i,player)
               stater.append((next_state,i)) #appending next state and the action it took to reach next_state
        return stater #set of next states and their corresponding actions
    
    
    
    
    def is_terminal(self,state): #to check if the current is terminal or not 
        """
        3 cases of terminal state 
        1. Player 2 (Game Tree Player) Wins
        2. Player 1 (Myopic Player) Wins
        3. Draw (This I have checked by checking if no player can make any move on the given state)
        """

        if self.Over(state,player=1) or self.Over(state,player=2):
            return True
        for i in range(6):
            for j in range(7):
                if state[i][j]==0:
                    return False       
        return True
    
    def Over(self,state,player):
        #checks if 4 consecutive coins of player found in horizontal
        for row in range(6):
            for col in range(4):        
                flag=True
                for iter in range(4):
                    if state[row][col+iter]!=player:
                        flag=False
                        break
                if flag==True:
                    return True  
        #checks if 4 consecutive coins of player found in vertical        
        for col in range(7):
            for row in range(3):        
                flag=True
                for iter in range(4):
                    if state[row+iter][col]!=player:
                        flag=False
                        break
                if flag==True:
                    return True 
        #checks if 4 consecutive coins of player found in positive diagonal
        for row in range(3):
            for col in range(4):        
                flag=True
                for iter in range(4):
                    if state[row+iter][col+iter]!=player:
                        flag=False
                        break
                if flag==True:
                    return True
        #checks if 4 consecutive coins of player found in negative diagonal  
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
        
    def minimax(self,state,depth,player,alpha,beta): #minimax with alpha beta pruning
        self.recursive_calls+=1
        if self.is_terminal(state) or depth==0: #eval function will come in handy when we reach a terminal state
            return self.evaluate_state(state),None
        if player==2: #game tree player is the max player in this case
            max_eval=float('-inf')
            best_move= None #initially no best move we have
            for next_possibilities in self.next_states(state,player):
                eval,_=self.minimax(next_possibilities[0],depth-1,player=1,alpha=alpha,beta=beta)
                if eval>max_eval:
                    max_eval=eval
                    best_move=next_possibilities[1]

                alpha=max(alpha,eval) #condition for pruning 
                if eval>=beta:
                    break
            return max_eval,best_move        
        
        else : #player 1 is the min player in this case
            min_eval=float('inf')
            best_move= None #initially no best move we have
            for next_possibilities in self.next_states(state,player):
                eval,_=self.minimax(next_possibilities[0],depth-1,player=2,alpha=alpha,beta=beta)
                if eval<min_eval:
                    min_eval=eval
                    best_move=next_possibilities[1]

                beta=min(beta,eval)
                if eval<=alpha: #condition for pruning 
                    break
            return min_eval,best_move   


    def FindBestAction(self,currentState): #finds the best action possible for the given state for player 2 
        """
        Modify this function to search the GameTree instead of getting input from the keyboard.
        The currentState of the game is passed to the function.
        currentState[0][0] refers to the top-left corner position.
        currentState[5][6] refers to the bottom-right corner position.
        Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
        Action 0 is refers to the left-most column and action 6 refers to the right-most column.
        """
        alpha, beta = float('-inf'), float('inf')
        result, bestAction = self.minimax(currentState,5,2,alpha,beta)
        bestAction = int(bestAction)
        return bestAction


def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase_easy1.csv', 'r') as read_obj: 
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
    I have added the code for counting number of avg wins and playing multiple game of PlayGame() in the main function , i have commented it for ease 
    """
    """
    You can add your code here to count the number of wins average number of moves etc.
    You can modify the PlayGame() function to play multiple games if required.
    """
    if fourConnect.winner==None:
       print("Game is drawn.")
    else:
        print("Winner : Player {0}\n".format(fourConnect.winner))
    print("Moves : {0}".format(move))
    return fourConnect.winner,move,gameTree.recursive_calls/(move/2) #here i divided by move/2 for recursive calls since player 2 makes move/2 
                                                                     #moves , hence for avg of recursive calls per we divide by move/2
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
    PlayGame()
    """
    start=time.time()
    cnt=0
    avg=0
    avgvict=0
    recurser=0
    for i in range(50):
        val,moves,re_calls=PlayGame()
        if(val==2):
           cnt=cnt+1
           avgvict+=moves
        avg+=moves
        recurser+=re_calls
    avg=avg/50 
    recurser=recurser/50
    if cnt!=0:  
       avgvict=avgvict/cnt 
    else:
        avgvict=0
    end=time.time()

    print("Time in case of Move Ordering and depth 5 is ",end-start)    
        
    print("Number of times Player 2 wins out of 50 with depth 5 and alpha beta pruning + move ordering is ",cnt)
    print("Avg Number of Moves for Optimized eval function is ",avg)   
    print("Avg Number of Moves on victory for Optimized eval function is ",avgvict)
    print("Avg number of recursive calls is ",recurser)
    """
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
    # RunTestCase()

if __name__=='__main__':
    main()
