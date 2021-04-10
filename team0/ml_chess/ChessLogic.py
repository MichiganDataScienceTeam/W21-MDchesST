from collections import namedtuple
import chess
import numpy as np

DEFAULT_HEIGHT = 8
DEFAULT_WIDTH = 8
# DEFAULT_WIN_LENGTH = 4

WinState = namedtuple('WinState', 'is_ended winner')

def getArrayFromFen(fen):
    board_arr = np.zeros(64)
    #fen = self.board.fen()
    #print(fen)

    # lowercase = black
    # uppercase = white
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
        # print(currentPiece)
        if currentPiece.isdigit():
            # do this 
            arrayIndex += int(currentPiece)
            
        elif currentPiece.isalpha():
            board_arr[arrayIndex] = piece_dict[currentPiece]
            arrayIndex += 1

        stringIndex += 1
    
    return board_arr

def getMoveIndexFromUCI(uci):
    promote_dict = {'q': 1, 'r': 2, 'b': 3, 'n': 4}
    startsquare = uci[:2]
    startrow = startsquare[0] - 'a'
    startcol = int(startsquare[1])-1

    endsquare = uci[2:]
    endrow = endsquare[0] - 'a'
    endcol = int(endsquare[1])-1

    if(uci.size() == 5):  # if it's a promotion
        p = promote_dict[uci[-1]]
    else:
        p = 0
    
    flat_index = np.ravel_multi_index((startcol, startrow, endcol, endrow, p), (8, 8, 8, 8, 5))
    return flat_index

class Board(chess.Board):
    """
    Chess Board, extended from the chess library board class.
    This way we can run chess library commands directly but also
    write custom functions.

    For example, code outside this class can do this:
        nb = Board()
        print(nb.get_np_representation())
        move = chess.Move.from_uci("c2c3")
        nb.push(move)
        print(nb.get_np_representation())

    And this will move the pawn from c2 to c3 and print the np array
    of the associated fen
    """



    # def __init__(self):
    #     self.board = chess.Board()

    def get_board_from_np(self, np_array):
        self.clear_board()
        for idx, piece in enumerate(np_array):
            # set_piece_at(square: chess.Square, piece: Optional[chess.Piece], promoted: bool = False) 
            #sets piece type and color at positiond idx
            if piece != 0:
                # NEGATIVE NUMBERS ARE WHITE
                color = chess.BLACK
                if piece < 0:
                    color = chess.WHITE
                self.set_piece_at(int(idx), piece = chess.Piece(int(abs(piece)), color))
            


    def get_np_representation(self):
        return getArrayFromFen(self.fen())

