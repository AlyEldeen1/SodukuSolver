import tkinter as tk
from tkinter import messagebox
from backend import generate_sudoku_board, solve_sudoku_csp  
import time  
import random

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.difficulty = tk.IntVar(value=50)  # Default difficulty
        self.create_widgets()
        self.new_puzzle()

    def create_widgets(self):
        """Creates the grid and buttons."""
        # Create Sudoku grid
        self.grid_entries = [[None for _ in range(9)] for _ in range(9)]
        
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=5, font=("Arial", 18), borderwidth=2, relief="solid", justify="center")
                entry.grid(row=row, column=col)
                entry.bind("<KeyRelease>", self.limit_input)
                self.grid_entries[row][col] = entry

        # Difficulty selection
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.grid(row=9, column=0, columnspan=9, pady=10)

        tk.Label(difficulty_frame, text="Difficulty:").pack(side="left")
        difficulties = [
            ("Easy", 20),
            ("Medium", 50),
            ("Hard", 100)
        ]
        for text, value in difficulties:
            tk.Radiobutton(difficulty_frame, text=text, variable=self.difficulty, value=value).pack(side="left")

        # Create buttons
        self.generate_button = tk.Button(self.root, text="Generate Sudoku", command=self.new_puzzle)
        self.generate_button.grid(row=10, column=0, columnspan=3, pady=10)

        self.random_board_button = tk.Button(self.root, text="Random Board", command=self.generate_random_board)
        self.random_board_button.grid(row=10, column=3, columnspan=3, pady=10)

        self.solve_button = tk.Button(self.root, text="Solve Sudoku", command=self.solve_puzzle)
        self.solve_button.grid(row=11, column=0, columnspan=3, pady=10)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid)
        self.clear_button.grid(row=11, column=3, columnspan=3, pady=10)

    def limit_input(self, event):
        # limits input to single digits
        widget = event.widget
        value = widget.get()
        if not (value.isdigit() and 1 <= int(value) <= 9):
            widget.delete(0, tk.END)

    def new_puzzle(self):
        # generates a new soduku
        difficulty = self.difficulty.get()
        self.grid = generate_sudoku_board(difficulty=difficulty)
        self.clear_grid()  # Clear the grid before displaying a new puzzle
        self.display_sudoku(self.grid)

    def generate_random_board(self):
        """Generates a random board of numbers without using difficulties."""
        random_board = [[random.choice(range(1, 10)) if random.random() > 0.7 else 0 for _ in range(9)] for _ in range(9)]
        self.clear_grid()  # Clear the grid before displaying a new random board
        self.display_sudoku(random_board)

    def display_sudoku(self, board):
        """Display the Sudoku board in the grid."""
        for row in range(9):
            for col in range(9):
                value = board[row][col]
                entry = self.grid_entries[row][col]
                if value != 0:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(value))
                    entry.config(state="readonly")  # Make non-editable if filled
                else:
                    entry.delete(0, tk.END)
                    entry.config(state="normal")  # Allow editing if empty

    def solve_puzzle(self):
        """Solve the Sudoku puzzle using the CSP solver."""
        grid = self.get_grid_values()

        start_time = time.time()  # Start timer
        if solve_sudoku_csp(grid):
            end_time = time.time()  # End timer
            elapsed_time = end_time - start_time
            self.display_sudoku(grid)
            messagebox.showinfo("Sudoku Solver", f"Sudoku solved successfully in {elapsed_time:.2f} seconds!")
        else:
            messagebox.showerror("Sudoku Solver", "This Sudoku puzzle is unsolvable.")

    def get_grid_values(self):
        """Retrieve values from the grid."""
        grid = []
        for row_entries in self.grid_entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                if value.isdigit():
                    row.append(int(value))
                else:
                    row.append(0)  # If empty, treat as 0
            grid.append(row)
        return grid

    def clear_grid(self):
        """Clear the Sudoku grid."""
        for row in range(9):
            for col in range(9):
                entry = self.grid_entries[row][col]
                entry.config(state="normal")
                entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

