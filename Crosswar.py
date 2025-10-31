import random as r

class Game:
    def __init__(self, size = 9, pool = 27):
        self.__size = size
        self.__board = [[-1 for _ in range(size)] for _ in range(size)]
        self.__preBoard = [[1 for _ in range(size)] for _ in range(4)]
        self.__pool = [pool]*4
        self.__moveList = [set(),set(),set(),set()]
        
        self.__score = [0]*4
        self.__turn = 0
        self.__passedTurns=0
    def exportGame(self):
        return {
            "size":self.__size,
            "board":self.__board,
            "preboard":self.__preBoard,
            "pool":self.__pool,
            "movelist":self.__moveList,
            "score":self.__score,
            "turn":self.__turn,
            "passedturn":self.__passedTurns
        }
    def importGame(self,settings):
        self.__size=settings["size"]
        self.__board=settings["board"]
        self.__preBoard=settings["preboard"]
        self.__pool=settings["pool"]
        self.__moveList=settings["movelist"]
        self.__score=settings["score"]
        self.__turn=settings["turn"]
        self.__passedTurns=settings["passedturns"]
    def importGameCopy(self,settings):
        self.__size=settings["size"]
        self.__board=settings["board"].copy()
        self.__preBoard=settings["preboard"].copy()
        self.__pool=settings["pool"].copy()
        self.__moveList=settings["movelist"].copy()
        self.__score=settings["score"].copy()
        self.__turn=settings["turn"]
        self.__passedTurns=settings["passedturns"]

    def relToAbs(self,pl,x,y):
        match pl:
            case 0:
                return (x,y)
            case 1:
                return (y,self.__size-1-x)
            case 2:
                return (self.__size-1-x,self.__size-1-y)
            case 3:
                return (self.__size-1-y,x)
    def absToRel(self,pl,x,y):
        match pl:
            case 0:
                return (x,y)
            case 1:
                return (self.__size-1-y,x)
            case 2:
                return (self.__size-1-x,self.__size-1-y)
            case 3:
                return (y,self.__size-1-x)
    
    def getSize(self):
        return self.__size
    def getBoard(self):
        return self.__board
    def getPreBoard(self):
        return self.__preBoard
    def getPool(self):
        return self.__pool
    def getScore(self):
        return self.__score
    def getMoveList(self):
        return self.__moveList
    def getTurn(self):
        return self.__turn
    
    def premove(self,pl,x):
        if self.__preBoard[pl][x] == 0:
            self.__pool[pl]-=1
        if self.__preBoard[pl][x] != 3:
            self.__preBoard[pl][x]+=1
            if self.__preBoard[pl][x] == 3:
                self.__moveList[pl].add((x,-1))
        else:
            return -1
        return 0
    def checkValidPremoves(self,pl,avoid=-1):
        # input: index of player to be move
        moves = []
        for x in range(9):
            if x==avoid:
                continue
            if self.__pool[pl]!=0 or self.__preBoard[pl][x] in [1,2]:
                moves.append(x)
        return moves
    
    def moveFromPreBoard(self,pl,x,y,dx,dy):
        self.__preBoard[pl][x]=0
        self.__moveList[pl].remove((x,y))
        absP = self.relToAbs(pl,x+dx,y+dy)
        self.__board[absP[0]][absP[1]]=pl
        self.__moveList[pl].add((x+dx,y+dy))
    def moveOnBoard(self,pl,x,y,dx,dy):
        abs1 = self.relToAbs(pl,x,y)
        self.__board[abs1[0]][abs1[1]]=-1
        self.__moveList[pl].remove((x,y))
        absP = self.relToAbs(pl,x+dx,y+dy)
        self.__board[absP[0]][absP[1]]=pl
        self.__moveList[pl].add((x+dx,y+dy))
    def checkMovesFromCoordinates(self,pl,x,y):
        moves = {"move":[],"capture":[],"jump":[]}
        for i in [-1,0,1]:
            abs1 = self.relToAbs(pl,x+i,y+1)
            if x+i>self.__size-1 or x+i<0:
                continue
            if y+1>self.__size-1 or self.__board[abs1[0]][abs1[1]] == -1:
                moves["move"].append((i,1))
            else:
                if self.__board[abs1[0]][abs1[1]] != pl:
                    moves["capture"].append((i,1))
                abs2 = self.relToAbs(pl,x+2*i,y+2)
                if x+2*i>self.__size-1 or x+2*i<self.__size-1:
                    continue
                if y+2>8 or self.__board[abs2[0]][abs2[1]]==-1:
                    moves["jump"].append((2*i,2))
                    nextJumps = self.checkMovesFromCoordinates(pl,x+2*i,y+2)["jump"]
                    for jump in nextJumps:
                        moves["jump"].append((jump[0]+2*i,jump[1]+2))
        return moves
    def checkMovesAll(self,pl):
        moves = []
        for piece in self.__moveList[pl]:
            moveDict = self.checkMovesFromCoordinates(pl,piece[0],piece[1])
            if moveDict["move"]==[] and moveDict["capture"]==[] and moveDict["jump"]==[]:
                continue
            moves.append((piece,moveDict))
        return moves
    
    def chooseMove(self,stage,pl,moves):
        if stage == "move":
            capture = 0
            chosenPiece = moves[r.randint(0,len(moves)-1)]
            chosenMoveType = []
            moveTypes = ["jump","capture","move"]
            while len(chosenMoveType) == 0:
                chosenMoveType = chosenPiece[1][moveTypes[r.randint(0,len(moveTypes)-1)]]
            if chosenMoveType == chosenPiece[1]["capture"]:
                capture = 1
            chosenElement = chosenMoveType[r.randint(0,len(chosenMoveType)-1)]
            return (capture,chosenPiece[0],chosenElement)
        elif stage == "altpremove" or stage == "premove":
            chosenMove = moves[r.randint(0,len(moves)-1)]
            return chosenMove
    
    def advanceGame(self):
        player = self.__turn%4
        if self.__passedTurns>=4:
            return 1        
        avoid = -1

        moves = self.checkMovesAll(player)
        if len(moves)==0:
            pmoves = self.checkValidPremoves(player)
            if len(pmoves)==0:
                self.__passedTurns+=1
                self.__turn+=1
                return -2
            move = self.chooseMove("altpremove",player,pmoves)
            self.premove(player,move)
            avoid = move
        else:
            move = self.chooseMove("move",player,moves)
            if move[0]==1:
                targetCell = self.relToAbs(player,move[1][0]+move[2][0],move[1][1]+move[2][1])
                targetpl = self.__board[targetCell[0]][targetCell[1]]
                self.__moveList[targetpl].remove(self.absToRel(targetpl,targetCell[0],targetCell[1]))
            
            if move[1][1]+move[2][1]>8:
                self.__moveList[player].remove(move[1])
                self.__board[move[1][0]][move[1][1]]=-1
                self.__score[player]+=1
            elif move[1][1]==-1:
                self.moveFromPreBoard(player,move[1][0],move[1][1],move[2][0],move[2][1])
            else:
                self.moveOnBoard(player,move[1][0],move[1][1],move[2][0],move[2][1])
        
        pmoves = self.checkValidPremoves(player,avoid)
        if len(pmoves)==0:
            self.__turn+=1
            return -1
        
        move = self.chooseMove("premove",player,pmoves)
        self.premove(player,move)
        self.__turn += 1
        return 0
    
    def write(self):
        s=[]
        for i in range(3):
            s.append([" "," "," "]+["." for i in range(self.__size)]+[" "," "," "])
        for i in range(self.__size):
            s.append(["." for i in range(self.__size+6)])
        for i in range(3):
            s.append([" "," "," "]+["." for i in range(self.__size)]+[" "," "," "])
        
        chars = ["$","&","#","@"]
        for pl in range(4):
            for i in range(self.__size):
                if self.__preBoard[pl][i]==0:
                    continue
                pos = self.relToAbs(pl,i,self.__preBoard[pl][i]-4)
                s[pos[0]+3][pos[1]+3]=chars[pl]
        
        for x in range(self.__size):
            for y in range(self.__size):
                if self.__board[x][y]==-1:
                    continue
                s[x+3][y+3]=chars[self.__board[x][y]]
        
        return '\n'.join([''.join(s[i]) for i in range(self.__size+6)])