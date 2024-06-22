import tkinter as tk
from tkinter import messagebox

# Function to check if a move is valid
def is_valid_move(board, row, col):
    return board[row][col] == ' '

# Function to place a move on the board
def place_move(board, row, col, player):
    if is_valid_move(board, row, col):
        board[row][col] = player
        return True
    return False

# Function to check if a player has won
def check_winner(board, player):
    # Check rows, columns, and diagonals
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

# Function to check if the board is full
def is_board_full(board):
    return all([cell != ' ' for row in board for cell in row])

# Minimax algorithm to determine the best move for the AI
def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if is_valid_move(board, i, j):
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if is_valid_move(board, i, j):
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

# Function to determine the best move for the AI
def best_move(board):
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if is_valid_move(board, i, j):
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Main function to run the game
def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'

    def update_board():
        for i in range(3):
            for j in range(3):
                buttons[i][j].config(text=board[i][j])

    def handle_click(row, col):
        nonlocal current_player
        if place_move(board, row, col, current_player):
            if check_winner(board, current_player):
                update_board()
                messagebox.showinfo("Tic Tac Toe", f"Player {current_player} wins!")
                window.quit()
                return
            elif is_board_full(board):
                update_board()
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                window.quit()
                return

            current_player = 'O' if current_player == 'X' else 'X'

            if current_player == 'O':
                move = best_move(board)
                if move:
                    place_move(board, move[0], move[1], current_player)
                    if check_winner(board, current_player):
                        update_board()
                        messagebox.showinfo("Tic Tac Toe", f"Player {current_player} wins!")
                        window.quit()
                        return
                    current_player = 'X'
            update_board()

    window = tk.Tk()
    window.title("Tic Tac Toe")

    buttons = [[None for _ in range(3)] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            button = tk.Button(window, text=board[i][j], font=('normal', 40), width=5, height=2,
                               command=lambda row=i, col=j: handle_click(row, col))
            button.grid(row=i, column=j)
            buttons[i][j] = button

    update_board()
    window.mainloop()

if __name__ == "__main__":
    main()
