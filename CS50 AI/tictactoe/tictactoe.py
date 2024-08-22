"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # If X has more moves, it's O's turn; otherwise, it's X's turn
    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_empty_spots = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                all_empty_spots.add((i,j))
    
    return all_empty_spots


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    tempboard = copy.deepcopy(board)
    tempboard[action[0]][action[1]] = player(board)
    return tempboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    nwin_loss_dict = {1: X, -1:O}
    r = utility(board)
    if r == 0:
        return None
    return nwin_loss_dict[r]



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    r = utility(board)
    if r != 0:
        return True
    count_fulls = 0
    for i in board:
        if EMPTY not in i:
            count_fulls += 1
    if count_fulls == 3:
        return True
    return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win_loss_dict = {X: 1, O:-1}
    first_edge = board[0][0]
    mid = board[1][1]
    last_edge =  board[2][2]
    #Small board so it'll do
    if mid is not EMPTY:
        if first_edge == mid == last_edge:
            return win_loss_dict[mid]
        if board[0][2] == mid == board[2][0]:
            return win_loss_dict[mid]
        if board[1][0] == mid == board[1][2]:
            return win_loss_dict[mid]
        if board[0][1] == mid == board[2][1]:
            return win_loss_dict[mid]
    if first_edge is not EMPTY:
        if first_edge == board[0][1] == board[0][2]:
            return win_loss_dict[first_edge]
        if first_edge == board[1][0] == board[2][0]:
            return win_loss_dict[first_edge]
    if last_edge is not EMPTY:
        if last_edge == board[2][0] == board[2][1]:
            return win_loss_dict[last_edge]
        if last_edge == board[2][0] == board[2][1]:
            return win_loss_dict[last_edge]
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    me = player(board)
    if me == X:
        wewantbig = True
        curr = float('-inf')
    else:
        wewantbig = False
        curr = float('inf')
    for action in actions(board):
        tempboard = result(board, action)
        if wewantbig:
            v = min_value(tempboard)
            if v > curr:
                nextmove = action
                curr = v
        else:
            v = max_value(tempboard)
            if v < curr:
                nextmove = action
                curr = v

    return nextmove

def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        tempboard = result(board, action)
        v = max(v, min_value(tempboard))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        tempboard = result(board, action)
        v = min(v, max_value(tempboard))
    return v