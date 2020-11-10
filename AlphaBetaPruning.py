import chess
import sunfish
import math
import random
import sys

from fastABP import minimaxRoot

def main():
    board = chess.Board()
    n = 0
    print(board)
    while n < 100:
        if n%2 == 0:
            move = input("Enter move: ")
            move = chess.Move.from_uci(str(move))
            board.push(move)
        else:
            print("Computers Turn:")
            move = minimaxRoot(3,board,True)
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)
        n += 1

if __name__ == "__main__":
    main()