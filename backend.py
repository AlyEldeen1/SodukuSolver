import numpy as np
from dokusan import generators


def generate_sudoku_board(difficulty=50):
    """Generates a random Sudoku board with a given difficulty."""
    board = np.array(list(str(generators.random_sudoku(avg_rank=difficulty))), dtype=int).reshape(9, 9)
    return board.tolist()


def is_valid_move(grid, row, col, num):
    # Row check
    for i in range(9):
        if grid[row][i] == num:
            return False

    # Column check
    for i in range(9):
        if grid[i][col] == num:
            return False

    # 3x3 grid check
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True


def initialize_domains(grid):
    # create a domain dictionary each cell is a variable
    domains = {}
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                domains[(i, j)] = list(range(1, 10))  # Assign all possible values to empty cells
            else:
                domains[(i, j)] = [grid[i][j]]  # Assign the given value to non-empty cells
    # Print  domains for debugging 
    print("Initialized Domains:")
    for cell, values in domains.items():
        print(f"Cell {cell}: {values}")
    return domains


def get_neighbors(cell):
    """Get all cells related by row, column, or subgrid."""
    row, col = cell
    neighbors = set()

    # Add row and column neighbors
    for i in range(9):
        neighbors.add((row, i))  # Same row
        neighbors.add((i, col))  # Same column

    # Add subgrid neighbors
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            neighbors.add((start_row + i, start_col + j))

    neighbors.discard(cell)  # Remove the cell 
    return neighbors


def revise(domains, Xi, Xj):
    # Revise the domain of Xi based on the domain of Xj
    revised = False
    for x in domains[Xi][:]:  # Copy the domain to avoid modifying during iteration
        if not any(x != y for y in domains[Xj]):
            domains[Xi].remove(x)
            revised = True
            print(f"Removed {x} from {Xi}'s domain due to inconsistency with {Xj}") # indication
    return revised


def apply_arc_consistency(grid, domains):
    """Enforce arc consistency on all arcs."""
    queue = [(cell, neighbor) for cell in domains for neighbor in get_neighbors(cell) if cell != neighbor]

    while queue:
        Xi, Xj = queue.pop(0)
        print(f"Revising arc between {Xi} and {Xj}")
        if revise(domains, Xi, Xj):
            print(f"Domains updated: {Xi} -> {domains[Xi]}")
            if not domains[Xi]:  # If a domain is empty, the puzzle is unsolvable
                print("Domain is empty! Puzzle unsolvable.")
                return False
            for Xk in get_neighbors(Xi) - {Xj}:
                queue.append((Xk, Xi))
    return True


def update_grid_from_domains(grid, domains):
    """Update the Sudoku grid based on singleton domains."""
    for (row, col), values in domains.items():
        if len(values) == 1:
            grid[row][col] = values[0]
    print("Updated grid:")
    for row in grid:
        print(row)


def backtrack(grid, domains):
    """Backtracking algorithm with arc consistency."""
    if all(len(domains[cell]) == 1 for cell in domains):  # If all variables are assigned
        for (row, col), values in domains.items():
            grid[row][col] = values[0]
        return True

    # Select the variable with the smallest domain
    unassigned = [cell for cell in domains if len(domains[cell]) > 1]
    variable = min(unassigned, key=lambda x: len(domains[x]))

    for value in domains[variable]:
        grid[variable[0]][variable[1]] = value
        # copy domains for backtracking
        new_domains = {k: v[:] for k, v in domains.items()}
        new_domains[variable] = [value]

        if apply_arc_consistency(grid, new_domains):
            if backtrack(grid, new_domains):
                return True

    grid[variable[0]][variable[1]] = 0  # Undo assignment
    return False


def solve_sudoku_csp(grid):
    """Solve the Sudoku puzzle using CSP with arc consistency and backtracking."""
    domains = initialize_domains(grid)
    if not apply_arc_consistency(grid, domains):
        print("Sudoku puzzle is unsolvable.")
        return False

    update_grid_from_domains(grid, domains)

    if backtrack(grid, domains):
        return True
    else:
        print("No solution exists.")
        return False


# Example Sudoku Puzzle (0 represents an empty cell)
grid = generate_sudoku_board(difficulty=50)

print("Initial Sudoku Puzzle:")
for row in grid:
    print(row)

if solve_sudoku_csp(grid):
    print("Sudoku solved successfully:")
    for row in grid:
        print(row)
else:
    print("Failed to solve Sudoku.")
