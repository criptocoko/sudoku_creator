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
from maximize0 import maximize
import sys
"""Driver method"""
def count_zeros(matrix_in, side):
    counter=0
    for i in range(side):
        for j in range(side):
            if matrix_in[i][j]==0:
                counter+=1
    return counter
def print_board(board):
    print(end='[')
    for i in range(rows):
        print(end='[')
        # iterate through columns
        for j in range(cols):
            # if sub grid columns are over
            # print solution element
            print(board[i,j], end='')
            print(end=',')
        print(end='],')
        print()
    print(end=']')
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 cli_main.py <base>, ex: python3 cli_main.py 3 for classic 9x9 sudoku')
        exit(1)
    base  = int(sys.argv[1])
    side  = base*base
    squares = side*side
    ratio = 0.1/base #make the denominator bigger to have less max ceros, it makes loop stop earlier and make board easier
    min_ceros = 270
    print('squares:', squares)
    print('starting ceros:', min_ceros)
    max_ceros = 278
    print("loop until find board with:",max_ceros,"ceros, if can't reach start again")
    ceros=0
    while ceros<max_ceros:

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
        for p in sample(range(squares),min_ceros):
            board[p//side][p%side] = 0
        print('trying to solve for base sudoku:')
        for line in board: print(line)
        # note start time
        matrix=board
        num_rows_sub_grid = base
        # num of cols in sub grid
        num_cols_sub_grid = num_rows_sub_grid
        start = time()
        while True:
        # input the puzzle
            matrix = np.array(matrix, dtype=int)
            # num of rows in sub grid

            # get solution_list from the class
            solution_list = Sudoku(matrix.copy(),
                box_row=num_rows_sub_grid,
                box_col=num_cols_sub_grid).get_solution()
            if len(solution_list)==1: break
            diffPos = [(r,c) for r in range(side) for c in range(side)
                    if solution_list[0][r][c] != solution_list[1][r][c] ] 
            r,c = random.choice(diffPos)
            matrix[r][c] = realsolution[r][c]
        # get shape of the matrix
        rows, cols = matrix.shape
        # iterate through all the solutions
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
        print('Found a base board with only 1 solution with:',count_zeros(matrix,side),'ceros, now we try to increase it until we reach:',max_ceros,'ceros')
        for line in board: print(line)
        #count number of ceros in board
        generator = maximize(matrix, base, side)
        for board in generator:
            print('Found a harder board:')
            print_board(board)
            print("\n Program stops when it finds board with at least:",max_ceros,"ceros and next board has more than 1 solution\n. If it can't reach it, it starts again with new base board.\n. Stop program if max_ceros is too high")
            ceros= count_zeros(board,side)
            if ceros>=max_ceros:
                break
            print('Current ceros:',ceros)