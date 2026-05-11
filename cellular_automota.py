'''
Job Wohali
March 19,2026
Description: This Cellular Automota is based off of Conway's Game of Life. 
Major additions include the addition of a virus entity and changes in which 
living and dead cells respond to them.
'''

import copy 
import time
import os
import random

'''functions'''

'''
Function name: Read From File
Syntax: file_name
Return value: board, rows, cols
Description: Reads a file and writes its contents to a list. This list 
is effectively a list of lists, which will be used to create a grid.
'''
def read_from_file(file_name):
    file = open(file_name, "r")

    board = []
    end_file = False
    while not end_file:
        #read a line
        row = file.readline()

        if row == "":
            end_file = True
        else:
            row = row.strip("\n")
            board.append(list(row))
    file.close()

    rows = len(board)
    cols = len(board[0])
    return board, rows, cols

'''
Function name: Create Grid
Syntax: rows, cols, dead_s
Return value: board
Description: Creates a grid based off of row and column data which
is fed into the function. On the base grid, all cells are dead. So
it initaly appends a dead symbol for each cell in the grid.
'''
def create_grid(rows, cols, dead_s):
    board = []
    #outer loop iterates over rows 
    for y in range(0, rows):
        new_row = []
        #inner loop iterates over columns
        for x in range(0, cols):
            new_row.append(dead_s)
        board.append(new_row)

    return board

'''
Function name: Update Cell
Syntax: cell, num_neighbors, infected_local, alive_s, dead_s, virus_s
Return value: alive_s OR dead_s OR virus_s
Description: This is where the game rules live. It updates cells based 
off of the game rules. Specific game rules will be identified by comments
within the function. Rules are checked/processed in the order they are written.
In other words, the processing of a rule maintains the assumption that all previous
rules were found false.
'''
def update_cell(cell, num_neighbors, infected_local, alive_s, dead_s, virus_s,):

    #if the cell is alive and has 2 or 3 neighbors, it stays alive
    if cell == alive_s and (num_neighbors == 2 or num_neighbors == 3):
        return alive_s
    #a virus cell with 8 neighbors will die
    elif cell == virus_s and infected_local == 8: #large masses of viruses with nothing to feed on die 
        return dead_s #it dies
    #if the cell is dead but has 3 or more neighbors, it revives
    elif cell == dead_s and num_neighbors >= 3:
            return alive_s
    #if a cell has 3 or more infected neighbors, OR a cell with less than 2 living neighbors and ONE virus neighbor, it becomes a virus
    elif infected_local >= 3 or (infected_local == 1 and num_neighbors < 2): #if cell has viruses near, it becomes or stays a virus
        return virus_s
    #if a cell is a virus and has no virus neighbors, it has a 50/50 chance of either reviving or dying
    elif cell == virus_s and infected_local == 0: #a quarentined infected cell will die or recover
        if random.randint(0,1,) == 0: #50/50 chance of recovery or death
            return dead_s
        else:
            return alive_s
    #if a virus cell has 4-7 infected neighbors, it has a 50/50 chance of either coming alive or staying a virus
    elif cell == virus_s and infected_local >= 4:
        if random.randint(0,1) == 0: #50/50 chance a virus cell will come back to life
            return alive_s #it comes back
        else:
            return virus_s #it stays normal
    #all other conditions result in a dead cell
    else:
        return dead_s
    
'''
Function name: Print Grid
Syntax: grid_local, generation_local, alive_s, virus_s
Return value: none; function prints to the terminal
Description: Prints the alive and virus symbols overtop of the
base grid, based off the updated grid it is given. It is in this
stage that colors are assigned to living and infected cells (green
and red, respectively) 
'''
def print_grid(grid_local, generation_local, alive_s, virus_s):
    os.system("clear") #clears the terminal so you only see one generation at a time
    for row in grid_local:
        #inner loop - columns
        for cell in row:
            if cell == alive_s:
                print(f"\033[32m{cell}\033[0m", end=" ") #prints green, then resets
            elif cell == virus_s:
                print(f"\033[31m{cell}\033[0m", end=" ") #prints red, then resets
            else:
                print(f'{cell}', end=" ")
        print()
    print(f"Generation: {generation_local}")
    

'''
Function name: Count Neighbors
Syntax: grid_copy_local, cur_x, cur_y, alive_s
Return value: neighbor_count
Description: Counts the number of living neighbors within direct 
proximity of a cell. A neighbor is living cell touching another,
either diagonally, horizontally, or vertically. 
'''
def count_neighbors(grid_copy_local, cur_x, cur_y, alive_s):
    row_num = len(grid_copy_local)
    col_num = len(grid_copy_local[0])

    left = (cur_x - 1) % col_num
    right = (cur_x + 1) % col_num

    above = (cur_y - 1) % row_num
    below = (cur_y + 1) % row_num

    #holds alive neighbor count
    neighbor_count = 0

    neighbors = [
        grid_copy_local[above][left], grid_copy_local[above][cur_x], grid_copy_local[above][right],
        grid_copy_local[cur_y][left],                                grid_copy_local[cur_y][right], 
        grid_copy_local[below][left], grid_copy_local[below][cur_x], grid_copy_local[below][right]
    ]

    for cell in neighbors:
        if cell == alive_s:
            neighbor_count += 1

    return neighbor_count

'''
Function name: Count Infected
Syntax: grid_copy_local, cur_x, cur_y, virus_s
Return value: infected_count
Description: Counts the number of infected neighbors within direct 
proximity of a cell. A neighbor is living cell touching another, 
either diagonally, horizontally, or vertically. 
'''
def count_infected(grid_copy_local, cur_x, cur_y, virus_s):
    row_num = len(grid_copy_local)
    col_num = len(grid_copy_local[0])

    left = (cur_x - 1) % col_num
    right = (cur_x + 1) % col_num

    above = (cur_y - 1) % row_num
    below = (cur_y + 1) % row_num

    #holds infected neighbor count
    infected_count = 0

    neighbors = [
        grid_copy_local[above][left], grid_copy_local[above][cur_x], grid_copy_local[above][right],
        grid_copy_local[cur_y][left],                                grid_copy_local[cur_y][right], 
        grid_copy_local[below][left], grid_copy_local[below][cur_x], grid_copy_local[below][right]
    ]

    for cell in neighbors:
        if cell == virus_s:
            infected_count += 1

    return infected_count

'''global variables'''
# #these are my colors
# green = "\033[32m"
# red = "\033[31m"
# reset = "\033[0m"

#cell state symbols
alive = "X"
dead = "."
virus = "*"                                                                                                                                                                                                                                           

'''main code'''

os.system("clear")
print(f"\nBoards 1-3 and the r-pentomino board have no virus attributes.")
board_selection = input(f"\nWhat board would you like to use? Please enter the file name OR number as a word (e.g. 'two', 'three'), excluding removing '.txt  ")
grid, num_rows, num_cols = read_from_file(f"{board_selection}.txt")
gen_num = int(input(f"How many generations do you want to run this for? (enter an integer)"))
print_grid(grid, 1, alive, virus)StopIteration

for generation in range(0, gen_num):
    generation_global = int(generation) + 1 #+1 is needed because the range starts at zero, but logicaly we count 1 first.
    #create a copy of the grid
    grid_copy = copy.deepcopy(grid)

    #outer loop - rows
    for y in range(num_rows):
        #inner loop - columns
        for x in range(num_cols):

            #count alive neighbors 
            alive_neighbors = count_neighbors(grid_copy, x, y, alive)
            infected_neighbors = count_infected(grid_copy, x, y, virus)

            #update cell state
            grid[y][x] = update_cell(grid_copy[y][x], alive_neighbors, infected_neighbors, alive, dead, virus)

    #print new grid
    print_grid(grid, generation_global, alive, virus)
    time.sleep(1) #wait one second before doing everything again (user sees: wait one second before grid updates)
    #note: I made the refresh rate so long because adding the new characters made things more complex and happen faster
  
