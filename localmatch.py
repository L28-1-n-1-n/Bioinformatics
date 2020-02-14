#!/usr/bin/python
import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------


def result_str(matrix, best_alignment, seq1, seq2, pos_i, pos_j):

    # i and j stores the position of the box with best_score
    i = pos_i
    j = pos_j

    # fin_i and fin_j stores the bottom rightmost box
    fin_i = len(seq2)
    fin_j = len(seq1)

    # initialize 2 empty strings to store future alignments
    str0 = ""
    str1 = ""

    # starting from the end of the 2 sequences,
    # copy each letter of the sequence to the alignment up until the box where best_score is stored
    while (i < fin_i):
        str1 += str(seq2[fin_i - 1])
        fin_i -= 1
    while (j < fin_j):
        str0 += str(seq1[fin_j - 1])
        fin_j -= 1

    # Write down the sequences that have the best alignment
    while ((i != 0) and (j != 0)):
        if (matrix[i][j] == "D"):
            str1 += str(seq2[i - 1])
            str0 += str(seq1[j - 1])
            i -= 1
            j -= 1

        elif (matrix[i][j] == "U"):
            str1 += str(seq2[i - 1])
            str0 += "-"
            i -= 1

        elif (matrix[i][j] == "L"):
            str1 += "-"
            str0 += str(seq1[j - 1])
            j -= 1
        else: # case "E"
            break

    # if the alignment has ended, and one of the sequences have not finished, copy the rest of the sequence
    while (i > 0):
        str1 += str(seq2[i - 1])
        str0 += "-"
        i -= 1
    while (j > 0):
        str0 += str(seq1[j - 1])
        str1 += "-"
        j -= 1

    # Reverse and store the sequence into output array, so that the sequence starts with the beginning, not the end
    best_alignment[1] = str1[::-1]
    best_alignment[0] = str0[::-1]

    return(best_alignment)

def search_pos(arr, best_score, seq1, seq2):

    # this function searches the score matrix arr and returns the position of the box containing best_score
    # the search starts from the bottom right box and moves upwards and leftwards
    i = len(seq2)

    pos_i = 0
    pos_j = 0
    sum = 0
    for i in range (i, 0, -1):
        j = len(seq1)
        for j in range(j, 0, -1):
            if (arr[i][j] == best_score):
                if (i + j > sum):
                    sum = i + j
                    pos_i = i
                    pos_j = j
    return(pos_i, pos_j)


def calc(seq1, seq2, i, j):

    # This function returns the score for each comparison of two letters
    up = seq2[i - 1]
    left = seq1[j - 1]

    # case mis-match
    match = -3

    #case match
    if (up == left):
        if (up == 'A'):
            match = 3
        elif (up == 'C'):
            match = 2
        elif (up == 'G'):
            match = 1
        elif (up == 'T'):
            match = 2
    return (match)

def local(seq1, seq2, i, j, arr, matrix):

    # negative entries are not allowed, hence key=>value pair "E" : 0 is added
    dict = {"D": 0, "U": 0, "L": 0, "E": 0}
    dict.update({"D": calc(seq1, seq2, i, j) + arr[i - 1][j - 1]})
    dict.update({"U": arr[i - 1][j] - 4})
    dict.update({"L": arr[i][j - 1] - 4})

    # for each box, find the max value
    arr[i][j] = max(dict.values())

    # matrix stores the key ("D", "U", "L" or "E") for each box in arr
    matrix[i][j] = list(dict.keys())[list(dict.values()).index(arr[i][j])]

def compose(seq1, seq2):

    # matrix is a 2d array storing the origin of the scores:
    # "D" for diagonal, "U" for the box above, "L" for the box on the left
    # "E" for Zero
    matrix = [matrix[:] for matrix in [['*'] * (len(seq1) + 1)] * (len(seq2) + 1)]

    # arr is a 2d array storing the score at each box
    arr = [arr[:] for arr in [['*'] * (len(seq1) + 1)] * (len(seq2) + 1)]

    # initial condition for scoring matrix: uppermost row and leftmost column has value zero,
    # to avoid negative scores
    # this causes gaps at beginning of sequence free
    for i in range(0, len(seq2) + 1):
        arr[i][0] = 0
        matrix[i][0] = "E"
    for j in range(0, len(seq1) + 1):
        arr[0][j] = 0
        matrix[0][j] = "E"
    matrix[0][0] = "E"
    arr[0][0] = 0

    # negative entries are not allowed, hence key=>value pair "E" : 0 is added
    for i in range (1, len(seq2) + 1):
        for j in range(1, len(seq1) + 1):
            local(seq1, seq2, i, j, arr, matrix)


    # list(map(max, arr)) gives max value from each row in arr
    best_score = max(map(max, arr)) # gives max of those max-values

    # look for the position (i,j) of the box with best_score, store the tuple in coord
    coord = search_pos(arr, best_score, seq1, seq2)
    pos_i = coord[0]
    pos_j = coord[1]

    # allocate an array of size 2, to store 2 strings, each having max size amongst seq1 and seq2
    best_alignment = [best_alignment[:] for best_alignment in [[] * (max(len(seq1), len(seq2)) + 1)] * 2]

    # store the augmented string containing best alignment of seq1 and seq2
    best_alignment = result_str(matrix, best_alignment, seq1, seq2, pos_i, pos_j)

    # un-comment to print arr and matrix
    for row in arr:
        print(row)
    for row in matrix:
        print(row)
    # return the results in a tuple
    return (best_score, best_alignment)

# ------------------------------------------------------------



# DO NOT EDIT ------------------------------------------------
# Given an alignment, which is two strings, display it
#
def displayAlignment(alignment):
    string1 = alignment[0]
    string2 = alignment[1]
    string3 = ''
    for i in range(min(len(string1),len(string2))):
        if string1[i]==string2[i]:
            string3=string3+"|"
        else:
            string3=string3+" "
    print('Alignment ')
    print('String1: '+string1)
    print('         '+string3)
    print('String2: '+string2+'\n\n')

# ------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This opens the files, loads the sequences and starts the timer
file1 = open(sys.argv[1], 'r')
seq1=file1.read()
file1.close()
file2 = open(sys.argv[2], 'r')
seq2=file2.read()
file2.close()
start = time.time()

#-------------------------------------------------------------


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# To work with the printing functions below the best local alignment should be called best_alignment and its score should be called best_score. 


# store best_score and best_alignment in a tuple to work with the default printing function
tuple = compose(seq1, seq2)
best_score = tuple[0]
best_alignment = tuple[1]

#-------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)

#-------------------------------------------------------------

