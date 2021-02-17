from enum import Enum
    
class Player(Enum):
    empty = '_'
    human = 'X'
    cpu = '0'

def set_move(board, index, player):
    board_clone = board[:]
    board_clone[index] = player
    return board_clone

def opponent(player):
    return Player.cpu if player is Player.human else Player.human

def minimax(board, player, depth=1):
    if game_over(board):
        winner = win(board)
        return (10-depth, None) if winner is Player.cpu else (depth-10, None)
    else:
        evaluated_moves = []
        for possible_move in possible_moves(board):
            board_clone = set_move(board, possible_move, player)
            score, _ = minimax(board_clone, opponent(player), depth + 1)
            evaluated_moves.append((score, possible_move))
            

        sorted_evaluated_moves = sorted(evaluated_moves)

        if player is Player.human:
            return sorted_evaluated_moves[0]
        elif player is Player.cpu:
            return sorted_evaluated_moves[-1]
        else:
            raise ValueError('cant be empty')

def print_board(board):
    row0, row1, row2 = board[:3], board[3:6], board[6:]
    for row in [row0, row1, row2]:
        print(*[f.value for f in row], sep=' | ', end='\n')

def possible_moves(board):
    return [index for (index, field) in enumerate(board) if field is Player.empty]

def game_over(board):
    return not bool(len(possible_moves(board))) or win(board) is not Player.empty

def win(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    all_human = lambda f: True if f is Player.human else False
    all_cpu = lambda f: True if f is Player.cpu else False
    for combination in winning_combinations:
        line = [board[i] for i in combination]
        if all(map(all_cpu, line)):
            return Player.cpu
        if all(map(all_human, line)):
            return Player.human
    return Player.empty

def cpu(board):
    (_, index) = minimax(board, Player.cpu)
    return set_move(board, index, Player.cpu) if index is not None else board


def main():
    board = [Player.empty for n in range(9)]
    while not game_over(board):
        print_board(board)
        index = input('Enter index [0-8]:')
        board = set_move(board, int(index), Player.human)
        board = cpu(board)

    print_board(board)
    print('wins: ', win(board))

main()
