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
    if action[0] < 0 or action[1] < 0 or action[0] >= 3 or action[1] >= 3:
        raise IndexError
    if tempboard[action[0]][action[1]] != None:
        raise AssertionError
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
    win_loss_dict = {X: 1, O: -1}
    winning_combinations = [
        [(0, 0), (0, 1), (0, 2)],  # First row
        [(1, 0), (1, 1), (1, 2)],  # Second row
        [(2, 0), (2, 1), (2, 2)],  # Third row
        [(0, 0), (1, 0), (2, 0)],  # First column
        [(0, 1), (1, 1), (2, 1)],  # Second column
        [(0, 2), (1, 2), (2, 2)],  # Third column
        [(0, 0), (1, 1), (2, 2)],  # Diagonal from top-left to bottom-right
        [(0, 2), (1, 1), (2, 0)]   # Diagonal from top-right to bottom-left
    ]
    
    for combination in winning_combinations:
        first, second, third = combination
        if board[first[0]][first[1]] != EMPTY and board[first[0]][first[1]] == board[second[0]][second[1]] == board[third[0]][third[1]]:
            return win_loss_dict[board[first[0]][first[1]]]
    
    return 0


def minimax(board, alpha=float('-inf'), beta=float('inf')):
    """
    Returns the optimal action for the current player on the board.
    """
    if utility(board) != 0:
        return None
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
            v = min_value(tempboard, alpha, beta)
            if v > curr:
                nextmove = action
                curr = v
            alpha = max(alpha, curr)
        else:
            v = max_value(tempboard, alpha, beta)
            if v < curr:
                nextmove = action
                curr = v
            beta = min(beta, curr)
        
        if beta <= alpha:
            break

    return nextmove

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        tempboard = result(board, action)
        v = max(v, min_value(tempboard, alpha, beta))
        if v >= beta:
            break
    return v

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        tempboard = result(board, action)
        v = min(v, max_value(tempboard, alpha, beta))
        if v <= alpha:
            break
    return v
