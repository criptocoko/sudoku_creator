"""
  cli_main.py           :   This file can be used to solve sudoku of any dimension using CLI.
  File created by       :   Shashank Goyal
  Last commit done by   :   Shashank Goyal
  Last commit date      :   22nd September
"""

# to display time required to solve
from time import time

# import numpy module for operations on puzzle matrices
import numpy as np

# import Sudoku class to solve the puzzle using Algorithm X
from Sudoku.sudoku import Sudoku
import random
import copy
from itertools import islice


"""Driver method"""
base  = 4
side  = base*base

# pattern for a baseline valid solution
def pattern(r,c): return (base*(r%base)+r//base+c)%side

# randomize rows, columns and numbers (of valid base pattern)
from random import sample
def shuffle(s): return sample(s,len(s)) 
rBase = range(base) 
rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
nums  = shuffle(range(1,base*base+1))

# produce board using randomized baseline pattern
realsolution = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
print('solution is:')
for line in realsolution: print(line)

board = copy.deepcopy(realsolution)
squares = side*side
empties = squares * 3//4
for p in sample(range(squares),empties):
    board[p//side][p%side] = 0

numSize = len(str(side))
# for line in board: print(line)
# note start time
start = time()
matrix=board
while True:
# input the puzzle
    matrix = np.array(matrix, dtype=int)
    # num of rows in sub grid
    num_rows_sub_grid = base
    # num of cols in sub grid
    num_cols_sub_grid = num_rows_sub_grid

    # get solution_list from the class
    solution_list  = [*islice(Sudoku(matrix.copy(),
        box_row=num_rows_sub_grid,
        box_col=num_cols_sub_grid).get_solution(),2)]
    if len(solution_list)==1: break
    diffPos = [(r,c) for r in range(side) for c in range(side)
            if solution_list[0][r][c] != solution_list[1][r][c] ] 
    r,c = random.choice(diffPos)
    matrix[r][c] = realsolution[r][c]
# get shape of the matrix
rows, cols = matrix.shape
# iterate through all the solutions
print(solution_list)
for sol_num, solution in enumerate(solution_list):
    print("Solution Number {} -\n".format(sol_num + 1))
    # iterate through rows
    for i in range(rows):
        # if sub grid rows are over
        if i % num_rows_sub_grid == 0 and i != 0:
            print('-' * (2 * (cols + num_rows_sub_grid - 1)))
        # iterate through columns
        for j in range(cols):
            # if sub grid columns are over
            if j % num_cols_sub_grid == 0 and j != 0:
                print(end=' | ')
            else:
                print(end=' ')
            # print solution element
            print(solution[i, j], end='')
        # end row
        print()
    print("\n")
    # iterate through rows
for sol_num, board_found in enumerate([board]):
    print("Board found Number {} -\n".format(sol_num + 1))
    for i in range(rows):
        # if sub grid rows are over
        if i % num_rows_sub_grid == 0 and i != 0:
            print('-' * (2 * (cols + num_rows_sub_grid - 1)))
        # iterate through columns
        for j in range(cols):
            # if sub grid columns are over
            if j % num_cols_sub_grid == 0 and j != 0:
                print(end=' | ')
            else:
                print(end=' ')
            # print solution element
            print(board_found[i][j], end='')
        print()
        
# time taken to solve
print("\nSolved in {} s".format(round(time() - start, 4)))
# Key Value Error raised if solution not possible