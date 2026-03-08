import random as r
import numpy as np

class CrosswarBase:
    def __init__(self, size = 9, pool = 27, board = [], score = np.array([0]*4), turn = 1, stage = "move", passedTurns = 0, avoid = -1):
        self.__size = size
        
        self.__pool = np.array([pool]*4)        
        
        self.__board = np.zeros(shape = (size+6,size+6))
        if len(board) == 0:        
            for i in range(3,size+3):
                self.__board[0,i] = 1
                self.__board[i,0] = 2
                self.__board[size+5,i] = 3
                self.__board[i,size+5] = 4
        else: self.__board = board

        self.__score = score
        self.__turn = turn
        self.__stage = stage
        self.__passedTurns = passedTurns
        self.__avoid = avoid

    def getSize(self):
        return self.__size
    def getPool(self):
        return self.__pool
    def getBoard(self):
        return self.__board
    def getScore(self):
        return self.__score
    def getTurn(self):
        return self.__turn
    def getStage(self):
        return self.__stage
    def getPassedTurns(self):
        return self.__passedTurns
    def getAvoid(self):
        return self.__avoid

    def move(self,action):
        player = self.__turn
        if self.__stage == "move":
            self.__board[action[0],action[1]] = 0
            if(action[2] == -1): self.__score[player] += 1
            else: self.__board[action[2],action[3]] = player
            self.__stage = "premove"
            self.__passedTurns = 0
            self.__avoid = -1
        elif self.__stage == "altpremove":
            if(action[2] == -1): 
                self.__passedTurns += 1
                self.__stage = "move"
                self.__turn = self.__turn%4 + 1
                self.__board = np.rot90(self.__board,-1)
            else:
                if action[0] == -1: self.__pool[player] -= 1
                else: self.__board[action[0],action[1]] = 0
                self.__board[action[2],action[3]] = player
                self.__passedTurns = 0
                self.__stage = "premove"
                self.avoid = action[3]
        else:
            if action[0] == -1: self.__pool[player] -= 1
            else: self.__board[action[0],action[1]] = 0
            self.__board[action[2],action[3]] = player
            self.__board = np.rot90(self.__board,-1)
            self.__stage = "move"
            self.__turn = self.__turn%4 + 1

    def checkJumps(self,pl,x,y):
        moves = []
        if y>=self.__size+3: return [(-1,-1)]
        for i in [-1,0,1]:
            if x+i>=self.__size+3 or x+i<3: continue
            if self.__board[y+1,x+i] == 0: continue
            if x+2*i>=self.__size+3 or x+2*i<3: continue
            if self.__board[y+2,x+2*i] != 0: continue
            
            moves.append((x+2*i,y+2))
            moves += self.checkJumps(pl,x+2*i,y+2)
        return moves
    
    def checkMovesAll(self,pl):
        moves = []
        if self.__stage == "premove":
            pos = np.zeros(self.__size)
            for y in range(3):
                for x in range(3,self.__size+3):
                    pos[y-3] = y
                    if self.__board[y,x] == 0 and x != self.__avoid:
                        moves.append((y,x,y+1,x))
            if self.__avoid == -1: pos[self.__avoid] = 4
            for i in range(self.__size):
                if pos[i]==0 and self.__pool[pl] != 0:
                     moves.append((-1,-1,0,i))
            moves = np.array(moves)
        elif self.__stage == "move":
            moves = []
            for y in range(3,self.__size+3):
                for x in range(3,self.__size+3):
                    if self.__board[y,x] != pl: continue
                    for i in [-1,0,1]:
                        if x+i>=self.__size+3 or x+i<3: continue
                        if y+1>=self.__size+3: moves.append((y,x,-1,-1))
                        else: moves.append((y,x,y+1,x+i))
                    jmoves = self.checkJumps(pl,x,y)
                    for jump in jmoves: moves.append((y,x,jump[0],jump[1]))
            if len(moves) == 0:
                self.__stage == "altpremove"
                pos = np.zeros(self.__size)
                moves = []
                for y in range(3):
                    for x in range(3,self.__size+3):
                        pos[y-3] = y
                        if self.__board[y,x] == 0 and x != self.__avoid:
                            moves.append((y,x,y+1,x))
                if self.__avoid == -1: pos[self.__avoid] = 4
                for i in range(self.__size):
                    if pos[i]==0 and self.__pool[pl] != 0:
                        moves.append((-1,-1,0,i))
        moves = np.array(list(set(moves)))
        if len(moves == 0): moves = np.array([(-1,-1,-1,-1)])
        return moves

    def to_pretty_string(self):
        s=[]
        for i in range(3):
            s.append([" "," "," "]+["." for i in range(self.__size)]+[" "," "," "])
        for i in range(self.__size):
            s.append(["." for i in range(self.__size+6)])
        for i in range(3):
            s.append([" "," "," "]+["." for i in range(self.__size)]+[" "," "," "])
        
        chars = ["$","&","#","@"]
        board = np.rot90(self.__board,-(self.__turn-1))
        for x in range(self.__size+6):
            for y in range(self.__size+6):
                if board[x][y]==0: continue
                s[x][y]=chars[board[x][y]-1]
        
        return '\n'.join([''.join(s[i]) for i in range(self.__size+6)]) + str(self.__turn)
