# take all inputs as variables
INPUT = input("enter input here, e.g. : 3,5,(1,1),(1,5),(2,4)")
INPUT_LIST = [int(x.strip('(').strip(')'))-1 for x in INPUT.split(',')]
HEIGHT = INPUT_LIST.pop(0)+1
WIDTH = INPUT_LIST.pop(0)+1

# write a helper function build_list_of_blocked_squares()
# input is an array of integers
# returns an array of x-y tuples as x-y coordinates of blocked-off squares at (i, j),
# where i is the HEIGHT and j is the WIDTH
def build_list_of_blocked_squares(list):
    temp_list = []
    for i in range(0, len(list)-1, 2):
        temp_list.append((list[i], list[i+1]))
    return temp_list

list_of_blocked_squares = build_list_of_blocked_squares(INPUT_LIST)
#print(list_of_blocked_squares)

# build a function build_list_of_open_squares()
# that takes dimensions: height, width, and a list of coordinates
# return a list of coordinates in range i <= height, j <= width, as tuples (i, j) that do not include the coordinates
# in the input list of coordinates
def build_list_of_open_squares(height, width, coordinate_list):
    open_squares_in_grid = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if (i, j) not in open_squares_in_grid:
                    if (i, j) not in list_of_blocked_squares:
                        open_squares_in_grid.append((i, j))
    return open_squares_in_grid

open_squares_list = build_list_of_open_squares(HEIGHT, WIDTH, list_of_blocked_squares)
#print(open_squares_list)

# write a function, squares_of(s)
# inputs a tuple of the coordinate points i, j of the square that the domino is covering, and the way the domino
# is placed on the square, top, bottom, left, or right
def squares_of(s):
    i, j, placement = s
    val = []
    if placement == 'top':
        val = [(i, j), (i-1, j)]
    if placement == 'bottom':
        val = [(i, j), (i+1, j)]
    if placement == 'left':
        val = [(i, j), (i, j-1)]
    if placement == 'right':
        val = [(i, j), (i, j+1)]
    return [(x[0], x[1]) for x in val
            if not square_blocked_off((x[0],x[1]), list_of_blocked_squares) and
            x[0] >= 0 and x[0] < HEIGHT and x[1] >= 0 and x[1] < WIDTH]









# write a function, square_not_blocked_off(),
# that takes a square's coordinates as a tuple as input and
# a list of the coordinates of the blocked squares
def square_blocked_off(square_xy, list_of_forbidden_coordinates):
    if square_xy in list_of_forbidden_coordinates:
        return True
    return False

# test = squares_of ((0, 1, 'bottom'))
# print(test)

# helper function, dominoes_not_stacked(list, domino)
# takes in a list and a domino as parameters
# return true if the squares of the domino share no two identical coordinates with the squares of a given
# domino in the list
def dominoes_not_stacked(list_of_dominoes, candidate_domino):
    list_of_squares_of_each_domino_in_list_of_dominoes = [squares_of(domino) for domino in list_of_dominoes]
    squares_of_candidate_domino = squares_of(candidate_domino)
    if squares_of_domino_distinct_from_those_in_list_of_domino(list_of_squares_of_each_domino_in_list_of_dominoes, squares_of_candidate_domino):
        return True
    return False

# squares_of_domino_distinct_from_those_in_list_of_domino(list_of_dominos, domino)
# input: a list of dominos as a list of lists of coordinates, where each list of coordinates has exactly two coordinates
# also inputs a domino
# return true if at least one element of each domino in the list of dominos is distinct from the elements of the candidate domino
def squares_of_domino_distinct_from_those_in_list_of_domino(list_of_squares_of_each_domino_in_list_of_dominoes, squares_of_candidate_domino):
    for squares_of_some_domino in list_of_squares_of_each_domino_in_list_of_dominoes:
        if stacked(squares_of_some_domino, squares_of_candidate_domino):
            return False
    return True

# function stacked(squares_of_some_domino, squares_of_candidate_domino) inputs two pairs of coordinates
# return true if they contain the same elements in any order, false otherwise
def stacked(squares_of_some_domino, squares_of_candidate_domino):
    if squares_of_candidate_domino[0] in squares_of_some_domino and squares_of_candidate_domino[1] in squares_of_some_domino:
        return True
    return False

# build a list of all dominoes that can possibly fit inside the board
all_dominoes = []
for square in open_squares_list: # a square is a list of tuples
    i, j = square[0], square[1] # get the x-and y-coordinates
    for posn in ['top', 'bottom','left','right']: # for each configuration
        if len(squares_of((i, j, posn))) == 2:
            if dominoes_not_stacked(all_dominoes, (i, j, posn)):
                all_dominoes.append((i, j, posn))
                #print("all dominoes: + " + str(all_dominoes))
print(all_dominoes)
# build a variable for each domino
# variables don't exist in this scope, so
# we have to make the variables a stringified domino with the added 'var : ' substring
num_variables = len(all_dominoes)
#print(num_variables)

variables  = {}
for domino in all_dominoes:
    variable_representing_this_domino_in_all_dominoes = all_dominoes.index(domino)+1
    variables[domino] = variable_representing_this_domino_in_all_dominoes

#print(variables)

# loop over the variables/dominoes
# map each domino to a list of squares it covers, and
# map each square that is, of course, not blocked-off to a list of squares that cover it
map_of_dominoes_to_their_squares = {}
map_of_squares_to_their_dominoes = {}
for domino in all_dominoes:
    map_of_dominoes_to_their_squares[domino] = squares_of(domino)
    for square in map_of_dominoes_to_their_squares[domino]:
        if square not in map_of_squares_to_their_dominoes:
            map_of_squares_to_their_dominoes[square] = [domino]
        else:
            map_of_squares_to_their_dominoes[square].append(domino)
#print(map_of_squares_to_their_dominoes)
#print(map_of_dominoes_to_their_squares)

# for every square, map the dominoes that can fit onto it to the coordinate of the square
new_map_of_squares_to_their_dominoes = {}
new_map_of_dominoes_to_the_squares_they_cover = {}
for square in open_squares_list:
    new_map_of_squares_to_their_dominoes[square] = [] # we're going to build an array of all the valid dominoes that all the squares have
    for domino in all_dominoes:
        if square in squares_of(domino):
            new_map_of_squares_to_their_dominoes[square].append(domino)
    # we also want to map all dominoes that are valid to the squares they cover.
        new_map_of_dominoes_to_the_squares_they_cover[domino] = squares_of(domino)
print("New map of dominoes to squares: " + str(new_map_of_dominoes_to_the_squares_they_cover))
print("New map of squares to dominoes: " + str(new_map_of_squares_to_their_dominoes))

# or_the_domino_variable_to_the_clause(domino_variable, clause) takes a domino (i, j, 'configuration') and a string
# output is a clause that is a disjunction of variables
def or_the_domino_variable_to_the_clause(domino, clause):
    temporary_string = clause
    if temporary_string == '':
        temporary_string = str(variables[domino])
    else:
        temporary_string = temporary_string + " OR " + str(variables[domino])
    return temporary_string

# and_the_clauses_to_the_super_clause(clause, super_clause) returns a string that is a conjunction of clauses.
# if the super_clause is empty, then don't begin with and
# use parentheses to keep track of ANDs
def and_the_clauses_to_the_super_clause(clause, super_clause):
    temporary_clause = super_clause
    if temporary_clause == '':
        temporary_clause = "(" + clause + ")"
    else:
        temporary_clause = temporary_clause + " ^ (" + clause + ")"
    return temporary_clause

num_clauses = 0 # this stores the value of the number of clauses
# Build the COVER clause. This clause says that the squares are all covered by at least one domino
COVER = "" # empty string. Clauses here are strings to print. This clause is to be ANDed
print(open_squares_list)
for square in open_squares_list:
    clause = "" # empty string. This is a sub-clause to be "ORed"
    print(map_of_squares_to_their_dominoes)
    for domino in new_map_of_squares_to_their_dominoes[square]:
        clause = or_the_domino_variable_to_the_clause(domino, clause)
    #print(str(domino) + ' is the domino. ' + str(square) + ' is the square. Clause : ' + str(clause))
    COVER = and_the_clauses_to_the_super_clause(clause, COVER)
    num_clauses = num_clauses + 1
#print(COVER)

# helper function negates the conjunction of the two variables
def negate_the_and_of_two_variables(one, two):
    return "-" + str(one) + " OR -" + str(two) + ""

# helper function turns a negated conjunction into the disjunction of two negations
def not_both_dominoes(clause, list_of_dominoes, one_domino_index, another_domino_index):
    temporary_clause = clause
    one_domino_variable = variables[list_of_dominoes[one_domino_index]]
    another_domino_variable = variables[list_of_dominoes[another_domino_index]]
    temp_negation = negate_the_and_of_two_variables(one_domino_variable, another_domino_variable)
    return and_the_clauses_to_the_super_clause(temp_negation, clause)
    #if temporary_clause == '': # if the string is empty
    #    return negate_the_and_of_two_variables(one_domino_variable, another_domino_variable)
    #    print(negated_conjunction)
    #else:

# Build the ONCE clause
ONCE = "" # empty string. Clauses here are strings to print. This clause says that no two dominoes overlap
for square in open_squares_list: #loop over the squares
    dominoes_that_cover_this_square = new_map_of_squares_to_their_dominoes[square] # this is a list of dominoes
    #print("square: " + str(dominoes_that_cover_this_square))
    # loop over the pairs of dominoes covering each of the squares
    for a_domino in range(len(dominoes_that_cover_this_square)):
        #print(dominoes_that_cover_this_square[a_domino])
        for another_domino in range(a_domino+1, len(dominoes_that_cover_this_square)):
            ONCE = not_both_dominoes(ONCE, dominoes_that_cover_this_square, a_domino, another_domino)
            num_clauses = num_clauses + 1
            #print(dominoes_that_cover_this_square[another_domino])
            #print(str(a_domino) + ' ' + str(another_domino))

#print(ONCE)

# give a visual of the formula for ease of reasoning
COVER_AND_ONCE = and_the_clauses_to_the_super_clause(COVER, "")
COVER_AND_ONCE = and_the_clauses_to_the_super_clause(ONCE, COVER_AND_ONCE)

# write a function that expresses this in cnf format
def print_cnf_formula(input_string, num_vars, num_cs):
    print("p cnf " + str(num_vars) + ' ' + str(num_cs))
    # print the COVER clause in DIMACS cnf format
    for square in open_squares_list:
        clause = ""  # empty string. This is a sub-clause to be "ORed"
        for domino in new_map_of_squares_to_their_dominoes[square]:
            if clause == '':
                clause = str(variables[domino])
            else:
                clause = clause + " " + str(variables[domino])
        print(clause + " " + str(0))
        # and print the ONCE clause in DIMACS cnf format
        # loop over the pairs of dominoes covering each of the squares
    for square in open_squares_list:  # loop over the squares
        dominoes_that_cover_this_square = new_map_of_squares_to_their_dominoes[square]  # this is a list of dominoes
        # print("square: " + str(dominoes_that_cover_this_square))
        for a_domino in range(len(dominoes_that_cover_this_square)):
            # print(dominoes_that_cover_this_square[a_domino])
            for another_domino in range(a_domino + 1, len(dominoes_that_cover_this_square)):
                print("-" + str(variables[dominoes_that_cover_this_square[a_domino]]) +
                      " -" + str(variables[dominoes_that_cover_this_square[another_domino]]) + " " + str(0))

print_cnf_formula(COVER_AND_ONCE, num_variables, num_clauses)