import Crosswar as c
import time
g = c.Game()
l = '\r'+'\033[1A'*15
print('\n'*15)
while g.advanceGame() != 1:
    print(l+g.write())
    time.sleep(0.1)
print(g.getScore())
