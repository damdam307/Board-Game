import CrosswarNp as c
import MCts as mcts
import time as t
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', dest='time', type=float, default=0,help='How much to wait between moves')
parser.add_argument('-n', '--games_number', dest='number', type=int, default=1,help='How many games to run')
parser.add_argument('-p', '--print_board', dest='prt', action='store_true',help='print board after every move')
parser.add_argument('-d', '--search_depth', dest='depth', type=int, default=-1,help='How many turns foreward to execute')


args = parser.parse_args()   

time = args.time
number = args.number
prt = args.prt
depth = args.depth

l = '\r'+'\033[1A'*16
if prt: print('\n'*16)
s = [0,0,0,0]
for i in range(number):
    print(i,end='\r')
    g = mcts.MonteCarloTreeSearchNode(c.CrosswarBase(pool=0),depth = depth)
    while not g.state.is_game_over():
        if prt: print(l+g.state.to_pretty_string())
        if time != 0: t.sleep(time)
        g = g.best_action()
    a = g.state.getScore()
    s[0]+=a[0]
    s[1]+=a[1]
    s[2]+=a[2]
    s[3]+=a[3]
    if prt: print('\n'*15)
print(s)
