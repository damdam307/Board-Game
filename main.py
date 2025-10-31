import Crosswar as c
import time
g = c.Game()
while g.advanceGame() != 1:
    print(g.write())
    time.sleep(1)