from collections import namedtuple
from random import choice
from mcts import MCTS, Node
import Crosswar

_CWB = namedtuple("CrossWarBoard", "current turn winner terminal")

# Inheriting from a namedtuple is convenient because it makes the class
# immutable and predefines __init__, __repr__, __hash__, __eq__, and others
class CrossWarBoard(_CWB, Node):
    def find_children(board):
        if board.terminal:  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        currboard = board.current
        settings = currboard.exportGame()
        player = currboard.getTurn()%4
        avoid = -1
        
        moves = currboard.checkMovesAll(player)
        moveType = "move"
        if len(moves)==0:
            moveType = "altpremove"
            moves = currboard.checkValidPremoves(player)
            if len(moves)==0:
                newBoard = Crosswar.Game()
                newBoard.importGameCopy(settings)
                newBoard.advanceWithChosenMoves({"type":"altpremove","move":None})
                is_terminal = (board.current.getPassedTurns()>=4)
                winner = None
                if is_terminal:
                    scores = newBoard.getScore()
                    winner = scores.index(max(scores))
                    if scores.count(max(scores))>1 and scores[player]==max(scores):
                        winner = None
                
                return {CrossWarBoard(newBoard,newBoard.getTurn(),winner,is_terminal)}
        if moveType == "move":
            moves = board.prep_moves(moves)
        
        boardlist = set()
        for el in moves:
            newBoard = Crosswar.Game()
            newBoard.importGameCopy(settings)
            avoid = newBoard.advanceWithChosenMoves({"type":moveType,"move":el})[1]
            pmoves = newBoard.checkValidPremoves(player,avoid)
            if len(pmoves)==0:
                newBoard.advanceWithChosenMoves({"type":"premove","move":None})
                if newBoard not in boardlist:
                    boardlist.add(CrossWarBoard(newBoard,newBoard.getTurn(),None,False))
                continue
            for premove in pmoves:
                endBoard = Crosswar.Game()
                endBoard.importGameCopy(newBoard.exportGame())
                endBoard.advanceWithChosenMoves({"type":"premove","move":premove})
                if endBoard not in boardlist:
                    boardlist.add(CrossWarBoard(endBoard,endBoard.getTurn(),None,False))
        return boardlist
    
    def find_random_child(board):
        if board.terminal:
            return None  # If the game is finished then no moves can be made
        
        currboard = board.current
        settings = currboard.exportGame()
        player = currboard.getTurn()%4
        avoid = -1
        
        moves = currboard.checkMovesAll(player)
        moveType = "move"
        if len(moves)==0:
            moveType = "altpremove"
            moves = currboard.checkValidPremoves(player)
            if len(moves)==0:
                newBoard = Crosswar.Game()
                newBoard.importGameCopy(settings)
                newBoard.advanceWithChosenMoves({"type":"altpremove","move":None})
                is_terminal = (board.current.getPassedTurns()>=4)
                winner = None
                if is_terminal:
                    scores = newBoard.getScore()
                    winner = scores.index(max(scores))
                    if scores.count(max(scores))>1 and scores[player]==max(scores):
                        winner = None
                
                return CrossWarBoard(newBoard,newBoard.getTurn(),winner,is_terminal)
        if moveType == "move":
            moves = board.prep_moves(moves)
        
        newBoard = Crosswar.Game()
        newBoard.importGameCopy(settings)
        avoid = newBoard.advanceWithChosenMoves({"type":moveType,"move":choice(moves)})[1]
        pmoves = newBoard.checkValidPremoves(player,avoid)
        if len(pmoves)==0:
            newBoard.advanceWithChosenMoves({"type":"premove","move":None})
            return CrossWarBoard(newBoard,newBoard.getTurn(),None,False)
        newBoard.advanceWithChosenMoves({"type":"premove","move":choice(pmoves)})
        return CrossWarBoard(newBoard,newBoard.getTurn(),None,False)

    def reward(board):
        if not board.terminal:
            raise RuntimeError(f"reward called on nonterminal board {board}")
        if board.winner == 0:
            return 1
        if board.winner in [1,2,3]:
            return 0  # Your opponent has just won. Bad.
        if board.winner is None:
            return 0.5  # Board is a tie
        # The winner is neither True, False, nor None
        raise RuntimeError(f"board has unknown winner type {board.winner}")

    def is_terminal(board):
        return board.terminal

    def prep_moves(board, moves):
        movel = []
        for chosenPiece in moves:
            for moveType in ["jump","capture","move"]:
                for element in chosenPiece[1][moveType]:
                    movel.append([["jump","capture","move"].index(moveType),chosenPiece[0],element])
        return movel

    def to_pretty_string(board):
        return board.current.write()


def play_game():
    l = '\r'+'\033[1A'*15
    print("\n"*16)
    tree = MCTS()
    board = CrossWarBoard(Crosswar.Game(),0,None,False)
    while True:
        if board.turn%4==0:
            for _ in range(50):
                tree.do_rollout(board)
            board = tree.choose(board)
        else:
            board.current.advanceGame()
            board = CrossWarBoard(board.current,board.current.getTurn(),None,False)
        print(l+board.to_pretty_string())
        if board.terminal:
            scores = board.current.getScore()
            print(scores)

if __name__ == "__main__":
    play_game()