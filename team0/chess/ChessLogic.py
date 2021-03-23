from collections import namedtuple
import chess
import numpy as np

DEFAULT_HEIGHT = 8
DEFAULT_WIDTH = 8
# DEFAULT_WIN_LENGTH = 4

WinState = namedtuple('WinState', 'is_ended winner')


class Board():
    """
    Chess Board.
    """

    def __init__(self):
        self.board = chess.Board()

    def get_np_representation(self):
        # 64-length array

        # TODO: initialize with all zeros
        board_arr = np.zeros(64)
        fen = self.board.fen()
        print(fen)

        piece_dict = {
            "p": chess.PAWN,
            "n": chess.KNIGHT,
            "b": chess.BISHOP,
            "r": chess.ROOK,
            "q": chess.QUEEN,
            "k": chess.KING,
            "P": -1*chess.PAWN,
            "N": -1*chess.KNIGHT,
            "B": -1*chess.BISHOP,
            "R": -1*chess.ROOK,
            "Q": -1*chess.QUEEN,
            "K": -1*chess.KING,
        }

        arrayIndex = 0
        stringIndex = 0
        while arrayIndex < 64:
            currentPiece = fen[stringIndex]
            print(currentPiece)
            if currentPiece.isdigit():
                # do this 
                arrayIndex += int(currentPiece)
                
            elif currentPiece.isalpha():
                board_arr[arrayIndex] = piece_dict[currentPiece]
                arrayIndex += 1

            stringIndex += 1
        
        return board_arr
        

