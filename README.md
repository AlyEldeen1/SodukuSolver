# Sudoku Solver with CSP and GUI 🧠🎮

This project is a Sudoku puzzle solver that uses **Constraint Satisfaction Problem (CSP)** techniques such as **arc consistency** and **backtracking** to solve puzzles. It also features a **Tkinter-based GUI** for generating, solving, and visualizing Sudoku boards.

## Features

- ✅ Sudoku puzzle generation with variable difficulty
- 🤖 CSP solver using:
  - Arc Consistency (AC-3)
  - Backtracking
  - Domain pruning
- 🎨 Tkinter GUI:
  - Load a puzzle
  - Solve with one click
  - Generate random boards
  - Choose difficulty (Easy / Medium / Hard)

## Requirements

- Python 3.6+
- Libraries:
  - `numpy`
  - `dokusan`
  - `tkinter` (standard with Python)
  - `random` (standard)
  - `time` (standard)

You can install the required third-party libraries using:

```bash
pip install numpy dokusan
