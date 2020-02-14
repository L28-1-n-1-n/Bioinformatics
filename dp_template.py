#!/usr/bin/python
import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------

def al(n, m): # formula to calculate the number of alignments looked at
    if ((n == 0) or (m == 0)):
        return (1)
    else:
        return(al(n - 1, m - 1) + al(n - 1, m) + al(n, m - 1))

def result_str(matrix, best_alignment, seq1, seq2):

    # Write down the sequences that have the best alignment,
    # starting by the end of the sequence and work backwards to the front
    i = len(seq2)
    j = len(seq1)
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


def calc(seq1, seq2, i, j):

    # This function returns the score for each comparison of two letters
    up = seq2[i - 1]
    left = seq1[j - 1]

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
    return (match)

def recursion(seq1, seq2, i, j, arr, matrix):

    # recursion start with i and j equal to length of seq2 and seq1
    if (i == 0):
        if (j == 0):

            # ends when we reach i = 0 and j = 0
            arr[i][j] = 0
            matrix[i][j] = "E"
            return (0)

        else:

            # uppermost row can only obtain value from the left box
            arr[i][j] = -4 * j
            matrix[i][j] = "L"
            return( -4 * j)

    elif (j == 0):

        # leftmost row can only obtain value from the upper box
        arr[i][j] = -4 * i
        matrix[i][j] = "U"
        return (-4 * i)
    else:

        # create 3 key=>value pairs, each carrying the score from the Diagonal box "D", Upper box "U", and Left box "L"
        dict = {"D" : 0, "U" : 0, "L" : 0}

        # calculate these 3 scores for each box recursively, starting with the lower rightmost box,
        # ending when upper leftmost box[0][0] is reached
        dict.update({"D" : calc(seq1, seq2, i, j) + recursion(seq1, seq2, i - 1, j - 1, arr, matrix)})
        dict.update({"U": recursion(seq1, seq2, i - 1, j, arr, matrix) - 4})
        dict.update({"L": recursion(seq1, seq2, i, j - 1, arr, matrix) - 4})

        # for each box, find the max value, starting from the lower rightmost box (i = len(seq2), j = len(seq1))
        arr[i][j] = max(dict.values())

        # matrix stores the key ("D", "U" or "L") for each box in arr
        matrix[i][j] = list(dict.keys())[list(dict.values()).index(arr[i][j])]

        return(max(dict.values()))

def compose(seq1, seq2):

    # matrix is a 2d array storing the origin of the scores:
    # "D" for diagonal, "U" for the box above, "L" for the box on the left
    matrix = [matrix[:] for matrix in [['*'] * (len(seq1) + 1)] * (len(seq2) + 1)]

    # arr is a 2d array storing the score at each box
    arr = [arr[:] for arr in [['*'] * (len(seq1) + 1)] * (len(seq2) + 1)]

    # recursive function to find best_score
    best_score = (recursion(seq1, seq2, len(seq2), len(seq1), arr, matrix))

    # allocate an array of size 2, to store 2 strings, each having max size amongst seq1 and seq2
    best_alignment = [best_alignment[:] for best_alignment in [[] * (max(len(seq1), len(seq2)) + 1)] * 2]

    # store the augmented string containing best alignment of seq1 and seq2
    best_alignment = result_str(matrix, best_alignment, seq1, seq2)

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

# calculate the number of alignments looked at by the algorithm
num_alignments = al(len(seq1), len(seq2))
print('Alignments calculated: ' + str(num_alignments))
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

