import random
import os
import copy

def solve_sudoku(grid):
    """
    A backtracking algorithm to solve a Sudoku grid.
    This also serves as the puzzle generator.
    """
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                # Randomize the numbers to generate a different puzzle each time
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(grid, i, j, num):
                        grid[i][j] = num
                        if solve_sudoku(grid):
                            return True
                        grid[i][j] = 0  # Backtrack
                return False
    return True

def is_valid(grid, row, col, num):
    """
    Checks if a number is valid in a given cell.
    """
    # Check row
    for x in range(9):
        if grid[row][x] == num:
            return False

    # Check column
    for x in range(9):
        if grid[x][col] == num:
            return False

    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False

    return True

def generate_sudoku():
    """
    Generates a single complete and solved Sudoku grid.
    """
    grid = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(grid)
    return grid

def create_unsolved_puzzle(solved_grid, difficulty=35):
    """
    Creates an unsolved puzzle by removing a number of cells from a solved grid.
    The difficulty parameter indicates how many cells to leave filled.
    A good number is between 25 and 35.
    """
    puzzle_grid = copy.deepcopy(solved_grid)
    cells_to_remove = 81 - difficulty  # 81 total cells
    all_cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(all_cells)

    for i in range(cells_to_remove):
        row, col = all_cells[i]
        puzzle_grid[row][col] = 0
    
    return puzzle_grid

def save_grid_to_file(grid, filename):
    """
    Saves a Sudoku grid to a file.
    """
    with open(filename, 'w') as f:
        for row in grid:
            f.write(" ".join(map(str, row)) + "\n")

def main():
    """
    Main function to generate 2000 unsolved and solved Sudoku puzzles.
    """
    puzzles_dir = "unsolved_puzzles"
    solutions_dir = "solved_puzzles"

    if not os.path.exists(puzzles_dir):
        os.makedirs(puzzles_dir)
    if not os.path.exists(solutions_dir):
        os.makedirs(solutions_dir)

    print("Generating 2000 unique Sudoku puzzles and solutions...")
    for i in range(2000):
        # Generate a new, solved puzzle
        solved_grid = generate_sudoku()
        
        # Create an unsolved version of the puzzle
        unsolved_grid = create_unsolved_puzzle(solved_grid, difficulty=random.randint(25, 35))
        
        # Save both the unsolved puzzle and its solved version
        unsolved_filename = os.path.join(puzzles_dir, f"puzzle_{i+1}.txt")
        solved_filename = os.path.join(solutions_dir, f"solution_{i+1}.txt")
        
        save_grid_to_file(unsolved_grid, unsolved_filename)
        save_grid_to_file(solved_grid, solved_filename)

        if (i + 1) % 100 == 0:
            print(f"Generated {i+1} puzzles and solutions...")

    print(f"\nCompleted! 2000 unsolved puzzles and their solutions have been saved to the '{puzzles_dir}' and '{solutions_dir}' directories.")

if __name__ == "__main__":
    main()