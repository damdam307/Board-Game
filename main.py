import Crosswar as c
import time
l = '\r'+'\033[1A'*15
#print('\n'*15)
s = [0,0,0,0]
for i in range(100):
    print(i,end='\r')
    g = c.Game()
    while g.advanceGame() != 1:
        pass
        #print(l+g.write())
    a = g.getScore()
    s[0]+=a[0]
    s[1]+=a[1]
    s[2]+=a[2]
    s[3]+=a[3]
print(s)
