#!/usr/bin/python
import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------



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

def al(n, m):
    if ((n == 0) or (m == 0)):
        return (1)
    else:
        return(al(n - 1, m - 1) + al(n - 1, m) + al(n, m - 1))

def result_str(matrix, best_alignment, seq1, seq2, pos_i, pos_j):

    i = pos_i
    j = pos_j
    str0 = ""
    str1 = ""

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

        else:

            str1 += "-"
            str0 += str(seq1[j - 1])

            j -= 1

    best_alignment[1] = str1[::-1]
    best_alignment[0] = str0[::-1]
    print(best_alignment)
    return(best_alignment)

def search_pos(arr, best_score, seq1, seq2):
    i = len(seq2)
    j = len(seq1)
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

    up = seq2[i - 1]
    left = seq1[j - 1]

    if (up == left):
        # if (up == 'A'):
        #     match = 3
        # elif (up == 'C'):
        #     match = 2
        # elif (up == 'G'):
        #     match = 1
        # elif (up == 'T'):
        #     match = 2
        match = 2
    else:
        # match = -3
        match = -1
    return (match)

def local(seq1, seq2, i, j, arr, matrix):

    dict = {"D" : 0, "U" : 0, "L" : 0, "E" : 0}
    dict.update({"D" : calc(seq1, seq2, i, j) + arr[i - 1][j - 1]})
    dict.update({"U": arr[i - 1][j]- 2})
    dict.update({"L": arr[i][j - 1] - 2})

    arr[i][j] = max(dict.values())
    matrix[i][j] = list(dict.keys())[list(dict.values()).index(arr[i][j])]

def varying_i(seq1, seq2, i, j, arr, matrix):

    dict = {"D" : 0, "U" : 0, "L" : 0}
    dict.update({"D" : calc(seq1, seq2, i, j) + arr[i - 1][j - 1]})
    dict.update({"U": arr[i - 1][j]})
    dict.update({"L": int(arr[i][j - 1]) - 2})

    arr[i][j] = max(dict.values())
    matrix[i][j] = list(dict.keys())[list(dict.values()).index(arr[i][j])]

def varying_j(seq1, seq2, i, j, arr, matrix):
    dict = {"D" : 0, "U" : 0, "L" : 0}
    dict.update({"D" : calc(seq1, seq2, i, j) + arr[i - 1][j - 1]})
    dict.update({"U": arr[i - 1][j] - 2})
    dict.update({"L": arr[i][j - 1]})

    arr[i][j] = max(dict.values())
    matrix[i][j] = list(dict.keys())[list(dict.values()).index(arr[i][j])]




def compose(seq1, seq2):
    print(seq1)
    print(seq2)
    matrix = [matrix[:] for matrix in [['*'] * (len(seq1) + 1)] * (len(seq2) + 1)]
    arr = [arr[:] for arr in [['*'] * (len(seq1) + 1)] * (len(seq2) + 1)]

    for i in range(0, len(seq2) + 1):
        arr[i][0] = 0
        matrix[i][0] = "E"
    for j in range(0, len(seq1) + 1):
        arr[0][j] = 0
        matrix[0][j] = "E"
    matrix[0][0] = "E"
    arr[0][0] = 0;
    for i in range (1, len(seq2)):
        for j in range(1, len(seq1)):
            local(seq1, seq2, i, j, arr, matrix)
    print(arr)
    for i in range (1, len(seq2)):
        varying_i(seq1, seq2, i, len(seq1), arr, matrix)
    for j in range (1, len(seq1) + 1):
        varying_j(seq1, seq2, len(seq2), j, arr, matrix)
    map(max, arr)
    list(map(max, arr))  # max numbers from each sublist
    best_score = max(map(max, arr)) # max of those max-numbers

    coord = search_pos(arr, best_score, seq1, seq2)
    pos_i = coord[0]
    pos_j = coord[1]

    print(best_score)
    print(arr)
    print(matrix)
    best_alignment = [best_alignment[:] for best_alignment in [[] * (max(len(seq1), len(seq2)) + 1)] * 2]

    displayAlignment(result_str(matrix, best_alignment, seq1, seq2, pos_i, pos_j))
    # print("Number of alignments calculated: " + str(al(len(seq1), len(seq2))))

compose(seq1, seq2)
#-------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
# print('Time taken: '+str(time_taken))
# print('Best (score '+str(best_score)+'):')
# displayAlignment(best_alignment)

#-------------------------------------------------------------

