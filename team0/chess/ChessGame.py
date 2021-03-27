from Game import Game
import chess
import copy
from .ChessLogic import *
import numpy as np

from chess import ChessLogic


class ChessGame(Game):
    def __init__(self):
        Game.__init__(self)
        self._base_board = Board()

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        return getArrayFromFen(chess.STARTING_FEN)

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (8, 8)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return 64*64*5

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """

        # Take in array index as action

        # [a, b, c, d, e] --> i = e + 5*d + 40*c + 320*b + 2560*a
        # i -->     a = i // 2560
        #           b = (i - a*2560) // 320
        #           c = (i - a*2560 - b*320) // 40
        #           d = (i - a*2560 - b*320 - c*40) // 5
        #           e = i - a*2560 * b*320 - c*40 - d*5

        # reverse it to get a UCI string
        #

        move_indices = np.unravel_index(action, (8, 8, 8, 8, 5))
        uci_string = ''
        # Coodrinates

        # convert 1 -> a, 2 -> b, etc
        v = str(chr(move_indices[0] + 97))
        w = str(move_indices[1])
        x = str(chr(move_indices[2] + 97))
        y = str(move_indices[3])

        uci_string = v + w + x + y

        # if there is a pawn promotion, add 5th character to uci
        if move_indices[4] != 0:
            z = str(chr(move_indices[4] + 97))
            uci_string += z

        # copy the board and play the specified move
        nextboard = copy.deepcopy(board)
        next_move = chess.Move.from_uci(uci_string)
        nextboard.push(next_move)

        return nextboard, -player

    def getValidMoves(self, board, player):
        arr = np.zeros((8, 8, 8, 8, 5))
        move_list = list(board.legal_moves)
        promote_dict = {'q': 1, 'r': 2, 'b': 3, 'n': 4}

        for move in move_list:
            uci = move.uci()
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

            arr[startrow][startcol][endrow][endcol][p] = 1

        return arr.flatten()
