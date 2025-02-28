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
def maximize(matrix, base, side):
    # pattern for a baseline valid solution
    matrix = np.array(matrix, dtype=int)
    # num of cols in sub grid
    rand = random.randint(1,side)
    for i in range(side):
        for j in range(side):
            # num of rows in sub grid
            randi = (rand + i)%side
            randj = (rand + j)%side
            if matrix[randi][randj]==0: continue
            value_before = matrix[randi][randj]
            matrix[randi][randj] = 0

            # get solution_list from the class
            solution_list = Sudoku(matrix.copy(),
                box_row=base,
                box_col=base).get_solution()
            #print('solved')
            if len(solution_list)==1: 
                print('positions',randi,randj)
                yield matrix
            else:
                matrix[randi][randj] = value_before
    return None