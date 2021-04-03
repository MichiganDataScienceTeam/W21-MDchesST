from sklearn.preprocessing import LabelBinarizer
import chess
import random


def preprocess_moves(moves):
    board = chess.Board()
    lb = LabelBinarizer()
    lb.fit(str(board).split())
    
    board_array = []
    string_board = str(board).split()
    string_board = lb.transform(string_board)
    board_array.append(string_board)
    for move in moves:
        name = who(board.turn)
        board.push_uci(move)
        string_board = str(board).split()
        string_board = lb.transform(string_board)
        board_array.append(string_board)
        
    return board_array


def xy_split(game, player_white):
    # make deep copies of game boards for X and y
    if player_white:
        # If player goes first, then before_p1 is input (X) and after_p1 is expected output (y)
        X = game[:-1:2].copy() # Every other board starting at 0
        y = game[1::2].copy() # Every other board starting at 1
    else:
        # Opposite configuration if player goes second
        X = game[1::2].copy() # Every other board starting at 1
        y = game[2::2].copy() # Every other board starting at 2
    
    # Balance list lengths if unbalanced because of starting indices
    print(len(X), len(y))
    if len(X) > len(y):
        X = X[:-1]
    elif len(X) < len(y):
        y = y[:-1]
    return X,y
    
    
    
    def display_game(moves, pause):
    board = chess.Board()
    counter = 0
    try:
        while not board.is_game_over(claim_draw=True):
            uci = moves[counter]
            name = who(board.turn)
            board.push_uci(uci)
            board_stop = "<pre>" + str(board) + "</pre>"
            html = "<b>Move %s %s, Play '%s':</b><br/>%s" % (
                       len(board.move_stack), name, uci, board_stop)
            clear_output(wait=True)
            display(HTML(html))
            counter += 1
            sleep(pause)
    except KeyboardInterrupt:
        msg = "Game interrupted!"
        return (None, msg, board)
    result = None
    if board.is_checkmate():
        msg = "checkmate: " + who(not board.turn) + " wins!"
        result = not board.turn
    elif board.is_stalemate():
        msg = "draw: stalemate"
    elif board.is_fivefold_repetition():
        msg = "draw: 5-fold repetition"
    elif board.is_insufficient_material():
        msg = "draw: insufficient material"
    elif board.can_claim_draw():
        msg = "draw: claim"
    
    print(msg)
    return (result, msg, board)