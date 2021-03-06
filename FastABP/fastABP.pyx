import chess
from cython.parallel import prange
import numpy as np
import functools
import operator
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

cpdef minimaxRoot(depth, board, isMaximizing):
    cdef int bestMove, value
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
cdef minimax(depth, board, alpha, beta, is_maximizing):
    cdef int bestMove
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

cdef int evaluation(board):
    cdef int i, evaluation
    i = 0
    evaluation = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        evaluation = evaluation + (getPieceValue(str(board.piece_at(i))) if x else -getPieceValue(str(board.piece_at(i))))
    return evaluation

cdef int getPieceValue(piece):
    if(piece == None):
        return 0
    cdef int value 
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == 'K' or piece == 'k':
        value = 900
    #value = value if (board.piece_at(place)).color else -value
    return value