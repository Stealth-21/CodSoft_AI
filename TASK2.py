import tkinter as tk
from tkinter import messagebox
import random
class TicTacToe:
    def __init__(self, ai_difficulty, play_again_button):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.buttons = [[None for i in range(3)] for j in range(3)]
        self.current_player = "X"
        self.ai_difficulty = ai_difficulty
        self.play_again_button = play_again_button
        # Add these lines to initialize the win and draw counters
        self.user_wins = 0
        self.ai_wins = 0
        self.draws = 0
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, text="", font=("Helvetica", 20), width=6, height=2,
                                               command=lambda row=i, col=j: self.on_click(row, col, self.play_again_button))
                self.buttons[i][j].grid(row=i, column=j)
    def on_click(self, row, col, play_again_button):
        if self.buttons[row][col]["text"] == "":
            self.buttons[row][col]["text"] = self.current_player
            if self.check_win(row, col):
                messagebox.showinfo("Congratulations!", f"Player {self.current_player} wins!")
                self.user_wins += 1  # Increment user wins counter
                self.ask_play_again(play_again_button)
            elif self.check_draw():
                messagebox.showinfo("Draw", "It's a draw!")
                self.draws += 1  # Increment draws counter
                self.ask_play_again(play_again_button)
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.ai_move()
    def ai_move(self):
        if self.ai_difficulty == "easy":
            self.ai_move_easy()
        elif self.ai_difficulty == "medium":
            self.ai_move_medium()
        elif self.ai_difficulty == "hard":
            self.ai_move_hard()
    def ai_move_easy(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]["text"] == ""]
        if empty_cells:
            move = random.choice(empty_cells)
            self.buttons[move[0]][move[1]]["text"] = "O"

            if self.check_win(move[0], move[1]):
                messagebox.showinfo("AI Wins!", "AI wins the game!")
                self.ai_wins += 1  # Increment AI wins counter
                self.ask_play_again(self.play_again_button)
            elif self.check_draw():
                messagebox.showinfo("Draw", "It's a draw!")
                self.draws += 1  # Increment draws counter
                self.ask_play_again(self.play_again_button)
            else:
                self.current_player = "X"
    def ai_move_medium(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]["text"] == ""]
        if empty_cells:
            move = None
            # Check if AI can win in the next move
            for cell in empty_cells:
                self.buttons[cell[0]][cell[1]]["text"] = "O"
                if self.check_win(cell[0], cell[1]):
                    move = cell
                self.buttons[cell[0]][cell[1]]["text"] = ""
            if move is None:
                # Check if player can win in the next move, block them
                for cell in empty_cells:
                    self.buttons[cell[0]][cell[1]]["text"] = "X"
                    if self.check_win(cell[0], cell[1]):
                        move = cell
                    self.buttons[cell[0]][cell[1]]["text"] = ""
            if move is None:
                move = random.choice(empty_cells)
            self.buttons[move[0]][move[1]]["text"] = "O"
            if self.check_win(move[0], move[1]):
                messagebox.showinfo("AI Wins!", "AI wins the game!")
                self.ask_play_again(self.play_again_button)
            elif self.check_draw():
                messagebox.showinfo("Draw", "It's a draw!")
                self.ask_play_again(self.play_again_button)
            else:
                self.current_player = "X"
    def ai_move_hard(self):
        def minimax(depth, is_maximizing):
            if self.check_win():
                return -1 if is_maximizing else 1
            elif self.check_draw():
               return 0
            if is_maximizing:
                best_score = float('-inf')
                for i in range(3):
                    for j in range(3):
                        if self.buttons[i][j]["text"] == "":
                            self.buttons[i][j]["text"] = "O"
                            score = minimax(depth + 1, False)
                            self.buttons[i][j]["text"] = ""
                            best_score = max(score, best_score)
                return best_score
            else:
                best_score = float('inf')
                for i in range(3):
                    for j in range(3):
                        if self.buttons[i][j]["text"] == "":
                            self.buttons[i][j]["text"] = "X"
                            score = minimax(depth + 1, True)
                            self.buttons[i][j]["text"] = ""
                            best_score = min(score, best_score)
                return best_score
        best_score = float('-inf')
        move = None
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = "O"
                    score = minimax(0, False)
                    self.buttons[i][j]["text"] = ""
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        if move:
            self.buttons[move[0]][move[1]]["text"] = "O"

            if self.check_win(move[0], move[1]):
                messagebox.showinfo("AI Wins!", "AI wins the game!")
                self.ask_play_again(self.play_again_button)
            elif self.check_draw():
                messagebox.showinfo("Draw", "It's a draw!")
                self.ask_play_again(self.play_again_button)
            else:
                self.current_player = "X"
    def check_win(self, row=None, col=None):
        if row is not None and col is not None:
            return self.check_row(row) or self.check_column(col) or self.check_diagonal(row, col)
        else:
            return any(self.check_row(i) or self.check_column(i) for i in range(3)) or \
                   any(self.check_diagonal(i, j) for i in range(3) for j in range(3))
    def check_row(self, row):
        return self.buttons[row][0]["text"] == self.buttons[row][1]["text"] == self.buttons[row][2]["text"] != ""
    def check_column(self, col):
        return self.buttons[0][col]["text"] == self.buttons[1][col]["text"] == self.buttons[2][col]["text"] != ""
    def check_diagonal(self, row, col):
        if row == col or row + col == 2:
            return self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != "" or \
                   self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != ""
        return False
    def check_draw(self):
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3))
    def generate_statistics(self):
        return f"User Wins: {self.user_wins}, AI Wins: {self.ai_wins}, Draws: {self.draws}"
    def restart_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""
        self.current_player = "X"
    def ask_play_again(self, play_again_button):
        choice = messagebox.askyesno("Play Again?", "Do you want to play another game?")
        if choice:
            self.restart_game()
            feedback_scale.pack()
            feedback_button.pack_forget()
            play_again_button.pack_forget()
        else:
            feedback_scale.pack()
            feedback_button.pack()
            self.window.destroy()
    def run(self):
        self.window.mainloop()
def choose_difficulty(difficulty):
    hide_difficulty_options()
    play_again_button = tk.Button(root, text="Play Again", command=lambda: play_again(game, difficulty))
    play_again_button.pack_forget()
    game = TicTacToe(difficulty, play_again_button)
    game.run()
def hide_difficulty_options():
    easy_radio.pack_forget()
    medium_radio.pack_forget()
    hard_radio.pack_forget()
    start_game_button.pack_forget()
def show_difficulty_options():
    easy_radio.pack(anchor=tk.W)
    medium_radio.pack(anchor=tk.W)
    hard_radio.pack(anchor=tk.W)
    start_game_button.pack()
def give_feedback():
    rating = feedback_scale.get()
    messagebox.showinfo("Feedback", f"Thank you for your feedback. You rated your experience as: {rating}/10")
    hide_difficulty_options()
    feedback_scale.pack_forget()
    feedback_button.pack_forget()
    show_difficulty_options()
def play_again(game, difficulty):
    game.restart_game()
    game.play_again_button.pack_forget()
root = tk.Tk()
var = tk.StringVar(root)
var.set("medium")  # Set default value
easy_radio = tk.Radiobutton(root, text="Easy", variable=var, value="easy")
medium_radio = tk.Radiobutton(root, text="Medium", variable=var, value="medium")
hard_radio = tk.Radiobutton(root, text="Hard", variable=var, value="hard")
start_game_button = tk.Button(root, text="Start Game", command=lambda: choose_difficulty(var.get()))
feedback_scale = tk.Scale(root, from_=0, to=10, orient="horizontal", label="Rate your experience (0 to 10)")
feedback_scale.pack_forget()
feedback_button = tk.Button(root, text="Submit Feedback", command=give_feedback)
feedback_button.pack_forget()
show_difficulty_options()
root.mainloop()
