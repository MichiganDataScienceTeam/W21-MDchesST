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

        # I don't know what actions are in this
        
    def getValidMoves(self,board,player):
      arr = np.zeros((8,8,8,8,5))
      move_list = list(board.legal_moves)
      promote_dict = {'q':1,'r':2,'b':3,'n':4} 

      for move in move_list:
        uci = move.uci()
        startsquare = uci[:2]
        startrow = startsquare[0] - 'a'
        startcol = int(startsquare[1])-1

        endsquare = uci[2:]
        endrow = endsquare[0] - 'a'
        endcol = int(endsquare[1])-1
        
        if(uci.size()==5): #if it's a promotion
          p = promote_dict[uci[-1]]
        else:
          p = 0
        
        arr[startrow][startcol][endrow][endcol][p] = 1
      
      return arr.flatten()


        
