from Game import Game
import chess
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
        return 8*8*(8*7+8+9)

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

        # I don't know what actions are in this
        



        