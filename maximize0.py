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
def maximize(matrix_in, base):
    side  = base*base

    # pattern for a baseline valid solution
    matrix = copy.deepcopy(matrix_in)
    counter=0
    for i in range(9):
        for j in range(9):
            if matrix[i][j]==0:
                counter+=1
    matrix = np.array(matrix, dtype=int)
    # num of cols in sub grid
    for i in range(9):
        for j in range(9):
            # num of rows in sub grid
            if matrix[i][j]==0: continue
            matrix[i][j] = 0

            # get solution_list from the class
            solution_list = Sudoku(matrix.copy(),
                box_row=base,
                box_col=base).get_solution()
            #print('solved')
            if len(solution_list)==1: 
                return matrix

            matrix[i][j] = matrix_in[i][j]
    return None