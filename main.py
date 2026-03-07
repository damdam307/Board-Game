import Crosswar as c
import time as t
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', dest='time', type=float, default=0,help='How much to wait between moves')
parser.add_argument('-n', '--games_number', dest='number', type=int, default=100,help='How many games to run')
parser.add_argument('-p', '--print_board', dest='prt', action='store_true',help='print board after every move')

args = parser.parse_args()   

time = args.time
number = args.number
prt = args.prt

l = '\r'+'\033[1A'*16
if prt: print('\n'*16)
s = [0,0,0,0]
for i in range(number):
    print(i,end='\r')
    g = c.Game()
    while g.advanceGame() != 1:
        if prt: print(l+g.to_pretty_string())
        if time != 0: t.sleep(time)
    a = g.getScore()
    s[0]+=a[0]
    s[1]+=a[1]
    s[2]+=a[2]
    s[3]+=a[3]
    if prt: print('\n'*15)
print(s)
