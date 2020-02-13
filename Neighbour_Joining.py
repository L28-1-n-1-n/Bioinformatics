#!/usr/bin/python
import time
import sys
import numpy as np


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
# file1 = open(sys.argv[1], 'r')
# seq1=file1.read()
# file1.close()
# file2 = open(sys.argv[2], 'r')
# seq2=file2.read()
# file2.close()
start = time.time()

#-------------------------------------------------------------


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# Call any functions you need here, you can define them above.
# To work with the printing functions below the best alignment should be called best_alignment and its score should be called best_score.
# The number of alignments you have checked should be stored in a variable called num_alignments.

with open(sys.argv[1]) as f:  # Use file to refer to the file object
  line = f.readline()
  no_of_cols = len(line.split())

data = np.loadtxt(sys.argv[1] , skiprows=1, usecols=range(1 , no_of_cols), dtype=np.int16) # Assuming input values have range (-32768, 32767)
print(data)
row_sum = [] * (no_of_cols - 1)

for row in data:
  row_sum.append([np.sum(row)])

def find_qscore(data, qmatrix, i, j):
  qmatrix[i][j] = (len(qmatrix[0]) - 2) * data[i][j] - np.sum(data[i]) - np.sum(data[j])

qm_size = len(data[0])
qmatrix = [qmatrix[:] for qmatrix in [['*'] * (qm_size)] * (qm_size)]

# print(qmatrix)
# print("len(qmatrix[0]) - 2 : " + str(len(qmatrix[0]) - 2))
# print("data[0][1] is " + str(data[0][1]))
# print("np.sum(0) is " + str(np.sum(data[0])))
# print("np.sum(1) is " + str(np.sum(data[1])))

for i in range(0, qm_size):
  j = i + 1
  for j in range(j, qm_size):
    find_qscore(data, qmatrix, i, j)

data = np.append(data, row_sum, axis=1)
print("data is :\n")
print(data)
print("qmatrix is:\n")
print(qmatrix)

#-------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This calculates the time taken and will print out useful information
stop = time.time()
time_taken=stop-start

# Print out the best

print('Time taken: '+str(time_taken))
#
# displayAlignment(best_alignment)

#-------------------------------------------------------------
