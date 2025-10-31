import random as r


def getPos(pl,x,y,dx,dy):
    match pl:
        case 0:
            return (x+dx,y+dy)
        case 1:
            return (y+dy,(8-x)-dx)
        case 2:
            return ((8-x)-dx,(8-y)-dy)
        case 3:
            return ((8-y)-dy,x+dx)

def getPosInverse(pl, pos):
    # Given board coordinates in pos tuple, returns player-relative coordinates
    # Assuming dx=0, dy=0
    match pl:
        case 0:
            return (pos[0], pos[1])  # No transformation needed for player 0
        case 1:
            return (8-pos[1], pos[0])  # Rotate 90° clockwise
        case 2:
            return (8-pos[0], 8-pos[1])  # Rotate 180°
        case 3:
            return (pos[1], 8-pos[0])  # Rotate 90° counterclockwise


def premove(pl,x):
    if p[pl][x] == 0:
        pool[pl]-=1
    if p[pl][x] != 3:
        p[pl][x]+=1
        if p[pl][x]==3:
            l[pl].add((x,-1))
    else:
        return -1
    return 0

def move(pl,x,y,dx,dy):
    t = getPos(pl,x,y,dx,dy)
    b[t[0]][t[1]]=pl
    l[pl].add((x+dx,y+dy))

def moveFromPre(pl,x,y,dx,dy):
    p[pl][x]=0
    l[pl].remove((x,y))
    move(pl,x,y,dx,dy)

def moveOnBoard(pl,x,y,dx,dy):
    t = getPos(pl,x,y,0,0)
    l[pl].remove((x,y))
    b[t[0]][t[1]]=-1
    move(pl,x,y,dx,dy)

def checkMovesSingle(pl,x,y):
    m = [[],[],[]]
    for i in [-1,0,1]:
        t = getPos(pl,x,y,i,1)   
        if x+i>8 or x+i<0:
            continue
        if y+1>8 or b[t[0]][t[1]]==-1:
            m[0].append((i,1))
        else:
            if b[t[0]][t[1]]!=pl:
                m[1].append((i,1))
            t1=getPos(pl,x,y,2*i,2)
            if x+2*i>8 or x+2*i<0:
                continue
            if y+2>8 or b[t1[0]][t1[1]]==-1:
                m[2].append((2*i,2))
                liss = checkMovesSingle(pl,x+2*i,y+2)[2]
                for ee in liss:
                    m[2].append((ee[0]+2*i,ee[1]+2))
    return m

def checkMovesAll(pl):
    m = []
    for pos in l[pl]:
        el = checkMovesSingle(pl,pos[0],pos[1])
        if el != [[],[],[]]:
            m.append((pos,el))
    return m

def checkPremoves(pl):
    m = []
    for x in range(9):
        if pool[pl]!=0 or (p[pl][x] in [1,2]):
            m.append(x)
    return m

def choosemove(pl,m):
    el = m[r.randint(0,len(m)-1)]
    ln = 0
    delet = 0
    tp = []
    while ln==0:
        tp = el[1][r.randint(0,len(el[1])-1)]
        ln = len(tp)
    if tp == el[1][1]:
        delet = 1
    elm = tp[r.randint(0,len(tp)-1)]
    return (delet,(el[0],elm))

def choosepremove(pl,m,avoid):
    res = avoid
    while res==avoid:
        res = m[r.randint(0,len(m)-1)]
    return res

def game():
    global b 
    b = [[-1 for _ in range(9)] for _ in range(9)]
    global p 
    p = [[1 for _ in range(9)] for _ in range(4)]
    global l
    l = [set(),set(),set(),set()]
    global pool
    pool= [27]*4
    global score
    score = [0]*4
    turn = 0
    passedTurns=0


    while passedTurns<4:
        moves = checkMovesAll(turn%4)
        avoid = -1
        if len(moves)==0:
            pmoves = checkPremoves(turn%4)
            if len(pmoves)==0:
                passedTurns+=1
                turn+=1
                continue
            avoid = choosepremove(turn%4,pmoves,avoid)
            premove(turn%4,avoid)
        else:
            mm = choosemove(turn%4,moves)
            if mm[0]==1:
                for ll in range(4):
                    l[ll].discard(getPosInverse(ll,getPos(turn%4,mm[1][0][0],mm[1][0][1],mm[1][1][0],mm[1][1][1])))
            if mm[1][0][1]+mm[1][1][1]>8:
                l[turn%4].remove((mm[1][0][0],mm[1][0][1]))
                b[mm[1][0][0]][mm[1][0][1]]=-1
                score[turn%4]+=1
            elif mm[1][0][1]==-1:
                moveFromPre(turn%4,mm[1][0][0],mm[1][0][1],mm[1][1][0],mm[1][1][1])
            else:
                moveOnBoard(turn%4,mm[1][0][0],mm[1][0][1],mm[1][1][0],mm[1][1][1])
        pmoves = checkPremoves(turn%4)
        if len(pmoves)==0:
            turn+=1
            continue
        avoid = choosepremove(turn%4,pmoves,avoid)
        premove(turn%4,avoid)
        turn+=1
        #print(score,end='\r')
    #print()
    return score

s = [0,0,0,0]
for i in range(10000):
    a = game()
    s[0]+=a[0]
    s[1]+=a[1]
    s[2]+=a[2]
    s[3]+=a[3]
print(s)