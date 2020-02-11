#!/usr/bin/python
import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------



# ------------------------------------------------------------



# DO NOT EDIT ------------------------------------------------
# Given an alignment, which is two strings, display it
#
# def displayAlignment(alignment):
#     string1 = alignment[0]
#     string2 = alignment[1]
#     string3 = ''
#     for i in range(min(len(string1),len(string2))):
#         if string1[i]==string2[i]:
#             string3=string3+"|"
#         else:
#             string3=string3+" "
#     print('Alignment ')
#     print('String1: '+string1)
#     print('         '+string3)
#     print('String2: '+string2+'\n\n')

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

def calc(arr, i, j):
    if (i == (len(seq1) + 1)) or (j == (len(seq1) + 1)):
        return (arr)
    print(i)
    print(j)
    up = seq1[i - 1]
    left = seq2[j - 1]
    if (up == left):
        if (up == 'A'):
            match = 3
        elif (up == 'C'):
            match = 2
        elif (up == 'G'):
            match = 1
        elif (up == 'T'):
            match = 2
    else:
        match = -3
    top = arr[i - 1][j] - 4
    left = arr[i][j - 1] - 4
    diagonal = arr[i - 1][j - 1] + match
    arr[i][j] = max(top, left, diagonal);
    print("match is " + str(match))

    return (arr[i + 1][j + 1])
def compose(seq1, seq2):
    print(seq1)
    print(seq2)

    arr = [arr[:] for arr in [['*'] * len(seq1)] * len(seq2)]
    for i in range(0, len(seq1)):
        arr[0][i] = -1 * i
    for j in range(0, len(seq2)):
        arr[j][0] = -1 * j
    print(calc(arr, 1, 1))


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

