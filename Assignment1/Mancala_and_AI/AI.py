import copy
from Kalaha_02180 import *

# Function to evaluate the board state
def evaluate_board(board):
    return board['Man_2'] - board['Man_1'] # Difference in mancala scores

# Minimax function with alpha-beta pruning
def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or Winner(board) != 'no winner':
        return evaluate_board(board), None

    valid_pockets = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for pocket in valid_pockets:
            if board[pocket] != 0:
                new_board = copy.deepcopy(board)
                next_turn = Move(new_board, '2', pocket)
                eval_score, _ = minimax(new_board, depth - 1, False, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = pocket
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for pocket in valid_pockets:
            if board[pocket] != 0:
                new_board = copy.deepcopy(board)
                next_turn = Move(new_board, '1', pocket)
                eval_score, _ = minimax(new_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval, None


# Function for AI to make a move
def ai_move(board):
    _, best_move = minimax(board, 4, True, float('-inf'), float('inf')) # Adjust depth as needed
    return best_move

