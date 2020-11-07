import chess.polyglot

if __name__ == "__main__":
    board = chess.Board()
    print(board)
    print(board.legal_moves)
    board.push_san("Nh3")
    print(board)
    board.push_san("Nh6")
    print(board)