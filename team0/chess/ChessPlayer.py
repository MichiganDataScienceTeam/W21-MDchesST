import numpy as np
import chess
from .ChessLogic import *

# lifted directly and shamelessly from OthelloPlayers.py
class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a
        
class HumanChessPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        #valid = self.game.getValidMoves(board, 1)
        gameBoard = Board().get_board_from_np(board)
        # moveList = gameBoard.legal_moves
        
        input_move = chess.Move()      
        for move in gameBoard.legal_moves:
            print(move.uci())
        while True:
            input_move_string = input()
            input_move = input_move.from_uci(input_move_string)
            if input_move in gameBoard.legal_moves:
                gameBoard.push(input_move)
                break
            print('Invalid move')

        return getMoveIndexFromUCI(input_move.uci())