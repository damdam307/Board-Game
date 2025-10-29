b = [[-1]*9]*9
p = [[1]*9]*4
l = [{}*4]
pool = [27]*4
score = [0]*4

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

def premove(pl,x):
    if p[pl][x] == 0:
        pool[pl]-=1
    if p[pl][x] != 3:
        p[pl][x]+=1
        l.add((x,-1))
    else:
        return -1
    return 0

def move(pl,x,y,dx,dy):
    t = getPos(pl,x,y,dx,dy)
    b[t[0]][t[1]]=pl
    l.add((x+dx,y+dy))

def moveFromPre(pl,x,y,dx,dy):
    p[pl][x]=0
    move(pl,x,y,dx,dy)

def moveOnBoard(pl,x,y,dx,dy):
    t = getPos(pl,x,y,dx,dy)
    l[pl].remove((x,y))
    b[t[0]][t[1]]=-1
    move(pl,x,y,dx,dy)

def checkMovesSingle(pl,x,y):
    m = [[]]*3
    for i in [-1,0,1]:
        t = getPos(pl,x,y,2*i,2)   
        if t[0]>8 or t[0]<0:
            continue
        if y+1>8 or b[t[0]][t[1]]==-1:
            m[0].append((i,1))
        else:
            if b[t[0]][t[1]]!=pl:
                m[1].append((i,1))
            t1=getPos(pl,x,y,2*i,2)
            if t1[0]>8 or t1[0]<0:
                continue
            if y+2>8 or b[t1[0]][t1[1]]==-1:
                m[2].append((2*i,2))
                m[2]+=checkMovesSingle(pl,x+2*i,y+2)[2]
    return m

def checkMovesAll(pl):
    m = []
    for pos in l[pl]:
        m.append((pos,checkMovesSingle(pl,pos[0],pos[1])))
    return m

def checkPremoves(pl):
    m = []
    for x in range(9):
        if pool!=0 or (p[pl][x] in [1,2]):
            m.append(x)

def choosemove(pl,m):
    pass

def choosepremove(pl,m,avoid):
    pass

turn = 0
passedTurns=0
while passedTurns<4:
    moves = checkMovesAll(turn%4)
    avoid = -1
    if len(moves)==0:
        pmoves = checkPremoves(turn%4)
        if len(moves)==0:
            passedTurns+=1
            turn+=1
            continue
        avoid = choosepremove(turn%4,pmoves,avoid)
        premove(turn%4,avoid)
    else
        mm = choosemove(turn%4,moves)
        if mm[0]==1:
            for ll in l:
                ll.discard(getPos(turn%4,mm[1][0][0],mm[1][0][1],mm[1][1][0],mm[1][1][1]))
            if mm[1][0][1]==-1:
                moveFromPre(turn%4,mm[1][0][0],mm[1][0][1],mm[1][1][0],mm[1][1][1])
            elif mm[1][0][1]+mm[1][1][1]>8:

            else:
                moveOnBoard(turn%4,mm[1][0][0],mm[1][0][1],mm[1][1][0],mm[1][1][1])
