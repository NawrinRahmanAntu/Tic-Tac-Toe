import tkinter as tk
from tkinter import messagebox
import math
import random  # Import random for first move

# Constants
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'
BOARD_SIZE = 3

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = initial_state()
        self.current_player = PLAYER_X
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.game_mode = "human_vs_computer"  # Default mode
        self.first_move_done = False  # Track if first move is made
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the board
        board_frame = tk.Frame(self.root)
        board_frame.pack()

        # Create buttons for the board
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                btn = tk.Button(
                    board_frame,
                    text=' ',
                    font=('Arial', 24),
                    width=5,
                    height=2,
                    command=lambda i=i, j=j: self.make_move(i, j)
                )
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        # Create a status label
        self.status_label = tk.Label(self.root, text="Player X's turn", font=('Arial', 14))
        self.status_label.pack()

        # Create a control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        # Game mode buttons
        tk.Button(control_frame, text="Human vs Computer", command=self.set_human_vs_computer).grid(row=0, column=0)
        tk.Button(control_frame, text="Computer vs Computer", command=self.set_computer_vs_computer).grid(row=0, column=1)
        tk.Button(control_frame, text="Reset", command=self.reset_game).grid(row=0, column=2)

    def set_human_vs_computer(self):
        self.game_mode = "human_vs_computer"
        self.reset_game()

    def set_computer_vs_computer(self):
        self.game_mode = "computer_vs_computer"
        self.reset_game()
        self.play_computer_vs_computer()

    def reset_game(self):
        self.board = initial_state()
        self.current_player = PLAYER_X
        self.first_move_done = False  # Reset first move flag
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j].config(text=' ', state=tk.NORMAL)
        self.status_label.config(text="Player X's turn")

    def make_move(self, i, j):
        if terminal(self.board):
            return

        if self.board[i][j] == EMPTY:
            self.board = result(self.board, (i, j))
            self.buttons[i][j].config(text=self.current_player, state=tk.DISABLED)
            winner_player = winner(self.board)

            if winner_player:
                self.status_label.config(text=f"{winner_player} wins!")
                self.disable_buttons()
            elif terminal(self.board):
                self.status_label.config(text="It's a draw!")
            else:
                self.current_player = player(self.board)
                self.status_label.config(text=f"Player {self.current_player}'s turn")
                if self.game_mode == "human_vs_computer" and self.current_player == PLAYER_O:
                    self.root.after(500, self.computer_move)

    def computer_move(self):
        if terminal(self.board):
            return

        # First move is random for Player X
        if not self.first_move_done:
            empty_cells = list(actions(self.board))
            move = random.choice(empty_cells)  # Choose a random move for Player X
            self.first_move_done = True  # Mark first move as done
        else:
            # Use minimax for subsequent moves
            _, move = minimax(self.board, math.inf, float('-inf'), float('inf'), True, PLAYER_O)
        
        if move:
            i, j = move
            self.make_move(i, j)

    def play_computer_vs_computer(self):
        if terminal(self.board):
            return

        current_player = self.current_player
        # First move for Player X is random
        if not self.first_move_done:
            empty_cells = list(actions(self.board))
            move = random.choice(empty_cells)  # Random first move for Player X
            self.first_move_done = True
        else:
            # Use minimax for subsequent moves for both players
            _, move = minimax(self.board, math.inf, float('-inf'), float('inf'), True, current_player)
        
        if move:
            i, j = move
            self.make_move(i, j)

        # Alternate turn for computer vs computer
        self.current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
        self.root.after(500, self.play_computer_vs_computer)

    def disable_buttons(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j].config(state=tk.DISABLED)

def initial_state():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def player(board):
    count_x = sum(row.count(PLAYER_X) for row in board)
    count_o = sum(row.count(PLAYER_O) for row in board)
    return PLAYER_O if count_x > count_o else PLAYER_X

def actions(board):
    return {(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == EMPTY}

def result(board, action):
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")
    player_symbol = player(board)
    new_board = [row[:] for row in board]
    new_board[i][j] = player_symbol
    return new_board

def winner(board):
    for row in board:
        if all(cell == PLAYER_X for cell in row):
            return PLAYER_X
        elif all(cell == PLAYER_O for cell in row):
            return PLAYER_O
    for j in range(BOARD_SIZE):
        if all(board[i][j] == PLAYER_X for i in range(BOARD_SIZE)):
            return PLAYER_X
        elif all(board[i][j] == PLAYER_O for i in range(BOARD_SIZE)):
            return PLAYER_O
    if all(board[i][i] == PLAYER_X for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE - 1 - i] == PLAYER_X for i in range(BOARD_SIZE)):
        return PLAYER_X
    elif all(board[i][i] == PLAYER_O for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE - 1 - i] == PLAYER_O for i in range(BOARD_SIZE)):
        return PLAYER_O
    return None

def terminal(board):
    return winner(board) is not None or all(all(cell != EMPTY for cell in row) for row in board)

def minimax(board, depth, alpha, beta, maximizing_player, player_symbol):
    if terminal(board) or depth == 0:
        return evaluate_board(board, player_symbol), None

    if maximizing_player:
        v = float("-inf")
        best_move = None
        for action in actions(board):
            new_board = result(board, action)
            val, _ = minimax(new_board, depth - 1, alpha, beta, False, player_symbol)
            if val > v:
                v = val
                best_move = action
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v, best_move
    else:
        v = float("inf")
        best_move = None
        for action in actions(board):
            new_board = result(board, action)
            val, _ = minimax(new_board, depth - 1, alpha, beta, True, player_symbol)
            if val < v:
                v = val
                best_move = action
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v, best_move

def evaluate_board(board, player_symbol):
    opponent = PLAYER_X if player_symbol == PLAYER_O else PLAYER_O
    if winner(board) == player_symbol:
        return 1
    elif winner(board) == opponent:
        return -1
    else:
        return 0

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
