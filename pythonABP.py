import chess
import math
import random
import sys
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

from common import evaluation

def minimaxRoot(depth, board,isMaximizing):
    possibleMoves = board.legal_moves
    bestMove = -9999
    bestMoveFinal = None
    for x in possibleMoves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(bestMove, minimax(depth - 1, board,-10000,10000, not isMaximizing))
        board.pop()
        if(value > bestMove):
            bestMove = value
            bestMoveFinal = move
    return bestMoveFinal

def minimaxRootParallel(depth, board,isMaximizing):
    possibleMoves = board.legal_moves
    bestMove = -9999
    bestMoveFinal = None

    if rank == 0:
        # Split possible moves into num_threads chunks
        data = np.array(list(possibleMoves))
        data = np.array_split(data, size)
    else:
        data = None

    data = comm.scatter(data, root=0)
    values = []
    moves = []
    for x in data:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(bestMove, minimax(depth - 1, board,-10000,10000, not isMaximizing))
        values.append(value)
        moves.append(str(move))
        board.pop()
    
    results_v = np.hstack(np.array(comm.allgather(values)))
    results_m = np.hstack(np.array(comm.allgather(moves)))
    
    for i, v in enumerate(results_v): 
        if(v > bestMove):
            bestMove = v
            bestMoveFinal = results_m[i]

    return bestMoveFinal

def minimax(depth, board, alpha, beta, is_maximizing):
    if(depth == 0):
        return -evaluation(board)
    possibleMoves = board.legal_moves
    if(is_maximizing):
        bestMove = -9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = max(bestMove,minimax(depth - 1, board,alpha,beta, not is_maximizing))
            board.pop()
            alpha = max(alpha,bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = min(bestMove, minimax(depth - 1, board,alpha,beta, not is_maximizing))
            board.pop()
            beta = min(beta,bestMove)
            if(beta <= alpha):
                return bestMove
        return bestMove