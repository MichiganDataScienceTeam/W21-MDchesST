from Game import Game
import chess
import copy
from .ChessLogic import *
import numpy as np
import time

#from chess import ChessLogic
def display(board):
    gameBoard = Board()
    gameBoard.get_board_from_np(board)
    print(gameBoard)

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

        move_indices = np.unravel_index(action, (8, 8, 8, 8, 5))
        uci_string = ''
        # Coodrinates

        # convert 1 -> a, 2 -> b, etc
        v = str(chr(move_indices[0] + 97))
        w = str(move_indices[1] + 1)
        x = str(chr(move_indices[2] + 97))
        y = str(move_indices[3] + 1)

        uci_string = v + w + x + y
        
        time.sleep(0.5)

        # if there is a pawn promotion, add 5th character to uci
        if move_indices[4] != 0:
            print(move_indices[4])
            z = str(chr(move_indices[4] + 97))
            uci_string += z
        
        print(uci_string)

        # copy the board and play the specified move
        nextboard = Board()
        nextboard.get_board_from_np(board)
        next_move = chess.Move.from_uci(uci_string)
        nextboard.push(next_move)
        array_rep = nextboard.get_np_representation()
        display(array_rep)
        return array_rep, -player

    def getValidMoves(self, board, player):
        # player 1 is black
        arr = np.zeros((8, 8, 8, 8, 5))
        gameBoard = Board()
        gameBoard.get_board_from_np(board)
        if player == 1:
            newFen = gameBoard.fen()
            newFen.replace('w', 'b', 1)
            gameBoard.set_fen(newFen)

        
        move_list = list(gameBoard.legal_moves)
        promote_dict = {'q': 1, 'r': 2, 'b': 3, 'n': 4}

        for move in move_list:
            uci = move.uci()
            startsquare = uci[:2]
            startrow = ord(startsquare[0]) - ord('a')
            startcol = int(startsquare[1]) - 1

            endsquare = uci[2:]
            endrow = ord(endsquare[0]) - ord('a')
            endcol = int(endsquare[1]) - 1

            if(len(uci) == 5):  # if it's a promotion
                p = promote_dict[uci[-1]]
            else:
                p = 0

            arr[startrow][startcol][endrow][endcol][p] = 1

        return arr.flatten()

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        
        # takes in a numpy array as (board) and returns a numpy array
        # player 1 is black
        if player == 1:
            new_board = Board()
            new_board.get_board_from_np(board)
            new_board.mirror()
            return new_board.get_np_representation()
        return board

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        return []

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        new_board = Board()
        new_board.get_board_from_np(board)
        return  str(getArrayFromFen(new_board.fen()))

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        #print(board)
        b = Board()
        #print(b)
        b.get_board_from_np(board)
        #print(b)
        #print(
        #b = b.get_board_from_np(board)

        if b.is_game_over():
            if b.outcome().winner == chess.WHITE:
                return 1
            else:
                return -1
        else:
            return 0

    