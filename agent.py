"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions from othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache = {} # Use this for state caching

def eprint(*args, **kwargs): #use this for debugging, to print to sterr
    print(*args, file=sys.stderr, **kwargs)
    
def compute_utility(board, color):
    # IMPLEMENT!
    """
    Method to compute the utility value of board.
    INPUT: a game state and the player that is in control
    OUTPUT: an integer that represents utility
    """
    dark_player_score, light_player_score = get_score(board)
    if color == 1:
        diff = dark_player_score - light_player_score
        return diff
    else:
        diff = light_player_score - dark_player_score
        return diff

def compute_heuristic(board, color):
    # IMPLEMENT! 
    """
    Method to heuristic value of board, to be used if we are at a depth limit.
    INPUT: a game state and the player that is in control
    OUTPUT: an integer that represents heuristic value
    """

    CORNER_WEIGHT = 25
    EDGE_WEIGHT = 5
    STABLE_WEIGHT = 15
    MOBILITY_WEIGHT = 10
    DISK_WEIGHT = 1

    opponent_color = 3 - color

    corners = [(0, 0), (0, len(board) - 1), (len(board) - 1, 0), (len(board) - 1, len(board) - 1)]

    corner_score = 0
    for i, j in corners:
        if board[i][j] == color:
            corner_score += 1
        elif board[i][j] == opponent_color:
            corner_score -= 1

    edge_score = 0
    for i in range(1, len(board) - 1):
        if board[0][i] == color:
            edge_score += 1
        elif board[0][i] == opponent_color:
            edge_score -= 1

        if board[len(board) - 1][i] == color:
            edge_score += 1
        elif board[len(board) - 1][i] == opponent_color:
            edge_score -= 1

        if board[i][0] == color:
            edge_score += 1
        elif board[i][0] == opponent_color:
            edge_score -= 1

        if board[i][len(board) - 1] == color:
            edge_score += 1
        elif board[i][len(board) - 1] == opponent_color:
            edge_score -= 1

    stable_score = 0
    rows, cols = len(board), len(board[0])

    def is_stable(i, j):
        if board[i][j] != color:
            return False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for x, y in directions:
            n_x, n_y = i + x, j + y
            while 0 <= n_x < rows and 0 <= n_y < cols:
                if board[n_x][n_y] == 0 or board[n_x][n_y] == opponent_color:
                    break
                n_x, n_y = n_x + x, n_y + y
            else:
                return True
        return False

    for i in range(rows):
        for j in range(cols):
            if is_stable(i, j):
                stable_score += 1 if board[i][j] == color else -1

    player_moves = len(get_possible_moves(board, color))
    opponent_moves = len(get_possible_moves(board, opponent_color))
    mobility_score = player_moves - opponent_moves

    player_disks = sum(row.count(color) for row in board)
    opponent_disks = sum(row.count(opponent_color) for row in board)
    disk_score = player_disks - opponent_disks

    total_squares = len(board) * len(board[0])
    empty_squares = sum(row.count(0) for row in board)

    if empty_squares > total_squares * 0.5:
        corner_weight = CORNER_WEIGHT
        edge_weight = EDGE_WEIGHT
        stable_weight = 0 
        mobility_weight = MOBILITY_WEIGHT
        disk_weight = 0 
    elif empty_squares > total_squares * 0.2:
        corner_weight = CORNER_WEIGHT
        edge_weight = EDGE_WEIGHT // 2
        stable_weight = STABLE_WEIGHT
        mobility_weight = MOBILITY_WEIGHT // 2
        disk_weight = DISK_WEIGHT
    else: 
        corner_weight = CORNER_WEIGHT
        edge_weight = 0 
        stable_weight = STABLE_WEIGHT * 2
        mobility_weight = 0  
        disk_weight = DISK_WEIGHT * 2

    heuristic_value = (
        corner_weight * corner_score +
        edge_weight * edge_score +
        stable_weight * stable_score +
        mobility_weight * mobility_score +
        disk_weight * disk_score
    )

    return heuristic_value

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    A helper function for minimax that finds the lowest possible utility
    """
    # HINT:
    # 1. Get the allowed moves
    # 2. Check if w are at terminal state
    # 3. If not, for each possible move, get the max utiltiy
    # 4. After checking every move, you can find the minimum utility
    # ...

    best_move = None

    if limit == 0:
        return best_move, compute_utility(board, color)
    
    if caching and board in cache:
        return best_move, cache[board]

    opponent_color = 3 - color
    possible_moves = get_possible_moves(board, opponent_color)

    if not possible_moves:
        return best_move, compute_utility(board, color)

    min_utility = float('inf')
    for possible_move in possible_moves:
        new_board = play_move(board, opponent_color, possible_move[0], possible_move[1])
        old_node, utility = minimax_max_node(new_board, color, limit - 1, caching)
        if utility < min_utility:
            best_move = possible_move
        min_utility = min(min_utility, utility)

    if caching:
        cache[board] = min_utility
    return best_move, min_utility

def minimax_max_node(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    A helper function for minimax that finds the highest possible utility
    """
    # HINT:
    # 1. Get the allowed moves
    # 2. Check if w are at terminal state
    # 3. If not, for each possible move, get the min utiltiy
    # 4. After checking every move, you can find the maximum utility
    # ...

    best_move = None

    if limit == 0:
        return best_move, compute_utility(board, color)
    
    if caching and board in cache:
        return best_move, cache[board]

    possible_moves = get_possible_moves(board, color)

    if not possible_moves:
        return best_move, compute_utility(board, color)

    max_utility = float('-inf')
    for possible_move in possible_moves:
        new_board = play_move(board, color, possible_move[0], possible_move[1])
        old_node, utility = minimax_min_node(new_board, color, limit - 1, caching)
        if utility > max_utility:
            best_move = possible_move
        max_utility = max(max_utility, utility)

    if caching:
        cache[board] = max_utility
    return best_move, max_utility

    
def select_move_minimax(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using Minimax algorithm. 
    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    INPUT: a game state, the player that is in control, the depth limit for the search, and a flag determining whether state caching is on or not
    OUTPUT: a tuple of integers (i,j) representing a move, where i is the column and j is the row on the board.
    """
    possible_moves = get_possible_moves(board, color)
    
    if not possible_moves:
        return None

    best_move = None
    best_utility = float('-inf')

    for possible_move in possible_moves:
        new_board = play_move(board, color, possible_move[0], possible_move[1])
        old_node, utility = minimax_min_node(new_board, color, limit-1, caching)
        if utility > best_utility:
            best_utility = utility
            best_move = possible_move
    return best_move

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    A helper function for alpha-beta that finds the lowest possible utility (don't forget to utilize and update alpha and beta!)
    """

    best_move = None

    if limit == 0:
        return best_move, compute_utility(board, color)
    
    if caching and board in cache:
        return best_move, cache[board]
    
    opponent_color = 3 - color
    possible_moves = get_possible_moves(board, opponent_color)

    if not possible_moves:
        return best_move, compute_utility(board, color)

    if ordering:
        possible_moves.sort(key=lambda move: compute_utility(
            play_move(board, opponent_color, move[0], move[1]), color
        ))

    min_utility = float('inf')
    for possible_move in possible_moves:
        new_board = play_move(board, opponent_color, possible_move[0], possible_move[1])
        old_move, utility = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
        if utility < min_utility:
            best_move = possible_move
        min_utility = min(min_utility, utility)

        beta = min(beta, min_utility)
        
        if beta <= alpha:
            break
        
    
    if caching:
        cache[board] = min_utility
    return best_move, min_utility

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    A helper function for alpha-beta that finds the highest possible utility (don't forget to utilize and update alpha and beta!)
    """

    best_move = None

    if limit == 0:
        return best_move, compute_utility(board, color)
    
    if caching and board in cache:
        return best_move, cache[board]
    
    possible_moves = get_possible_moves(board, color)

    if not possible_moves:
        return best_move, compute_utility(board, color)
    
    if ordering:
        possible_moves.sort(key=lambda move: compute_utility(
            play_move(board, color, move[0], move[1]), color
        ), reverse=True)
        
    max_utility = float('-inf')
    for possible_move in possible_moves:
        new_board = play_move(board, color, possible_move[0], possible_move[1])
        old_move, utility = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
        if utility > max_utility:
            best_move = possible_move
        max_utility = max(max_utility, utility)

        alpha = max(alpha, max_utility)
        
        if alpha >= beta:
            break        

    if caching:
        cache[board] = max_utility
    return best_move, max_utility

def select_move_alphabeta(board, color, limit = -1, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using Alpha-Beta algorithm. 
    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    INPUT: a game state, the player that is in control, the depth limit for the search, a flag determining whether state caching is on or not, a flag determining whether node ordering is on or not
    OUTPUT: a tuple of integers (i,j) representing a move, where i is the column and j is the row on the board.
    """
    possible_moves = get_possible_moves(board, color)

    if not possible_moves:
        return None

    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    if ordering:
        possible_moves.sort(key=lambda move: compute_utility(
            play_move(board, color, move[0], move[1]), color
        ), reverse=True)

    for possible_move in possible_moves:
        new_board = play_move(board, color, possible_move[0], possible_move[1])
        old_move, utility = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
        if utility > alpha:
            alpha = utility
            best_move = possible_move
    return best_move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) # Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) # Depth limit
    minimax = int(arguments[2]) # Minimax or alpha beta
    caching = int(arguments[3]) # Caching 
    ordering = int(arguments[4]) # Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): # run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: # else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
