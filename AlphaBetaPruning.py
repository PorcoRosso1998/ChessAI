import chess
import math
import random
import sys
import time 
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

from fastABP import minimaxRoot as mrc
from pythonABP import minimaxRoot as mrp

SEED = 5
DEPTH = 2

def abp_run(mr):
    board = chess.Board()
    n = 0
    random.seed(SEED)
    
    if rank == 0:
        # Computer Move Time:
        ai_times = []

    while not board.is_stalemate() and not board.is_checkmate():
        if (n % 2) == 0:
            possible_moves = list(board.legal_moves)
            move = possible_moves[random.randrange(0,len(possible_moves))]
            move = chess.Move.from_uci(str(move))
            board.push(move)
            if board.is_checkmate():
                print("THE HUMAN HAS WON\n")
        else:
            # Perform and Time Move
            if rank == 0: start = time.time()
            move = mr(DEPTH,board,True)
            if rank == 0:
                end = time.time()

                # Append time to list
                ai_times.append(end - start)

            move = chess.Move.from_uci(str(move))
            board.push(move)
            if board.is_checkmate():
                print("THE MACHINE HAS WON\n")
        n += 1
    if not board.is_checkmate():
            print("A TIE\n")
    
    if rank == 0: return ai_times

def main():
    # Run with ABP (Cython)
    if rank == 0: print("Beginning Run with Cython...")
    start = time.time()
    ai_times = abp_run(mrc)
    end = time.time()
    print("TOTAL EXEC TIME: {}".format(end - start))

    if rank == 0:
        mean = np.mean(ai_times)
        max_time = np.max(ai_times)
        min_time = np.min(ai_times)

        print("======== CYTHON ========")
        print("Average Time per Move: {}".format(mean))
        print("Max Move Time: {}".format(max_time))
        print("Min Move Time: {}".format(min_time))

    # Run wth ABP (Python)
    if rank == 0: print("Beginning Run with Python...")
    start = time.time()
    ai_times = abp_run(mrp)
    end = time.time()
    print("TOTAL EXEC TIME: {}".format(end - start))

    if rank == 0:
        mean = np.mean(ai_times)
        max_time = np.max(ai_times)
        min_time = np.min(ai_times)
        
        print("======== PYTHON ========")
        print("Average Time per Move: {}".format(mean))
        print("Max Move Time: {}".format(max_time))
        print("Min Move Time: {}".format(min_time))

if __name__ == "__main__":
    main()