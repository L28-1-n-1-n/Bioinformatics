#!/usr/bin/python
import time
import sys
import numpy as np


# YOUR FUNCTIONS GO HERE -------------------------------------
def find_qscore(data, qmatrix, i, j):
  qmatrix[i][j] = (len(qmatrix[0]) - 2) * data[i][j] - np.sum(data[i]) - np.sum(data[j])

def print_data(data, row_sum, letters):

  data = np.append(data, row_sum, axis=1)
  print("data is :")
  count = 0
  print("-", end=" ")
  for l in letters:
    print(l, end=" ")
  print("Sum")
  for row in data:
    print(letters[count], row)
    count += 1
  print("\n")


def print_qmatrix(qmatrix, letters):

  print("qmatrix is:")
  count = 0
  print("-", letters)
  for row in qmatrix:
    print(letters[count], row)
    count += 1
  print("\n")

def reduce(data, letters):
  row_sum = [] * (len(data[0]))
  for row in data:
    row_sum.append([np.sum(row)])

  print_data(data, row_sum, letters)

  qm_size = len(data[0])
  qmatrix = [qmatrix[:] for qmatrix in [[0] * (qm_size)] * (qm_size)]

  # print(qmatrix)
  # print("len(qmatrix[0]) - 2 : " + str(len(qmatrix[0]) - 2))
  # print("data[0][1] is " + str(data[0][1]))
  # print("np.sum(0) is " + str(np.sum(data[0])))
  # print("np.sum(1) is " + str(np.sum(data[1])))

  for i in range(0, qm_size):
    j = i + 1
    for j in range(j, qm_size):
      find_qscore(data, qmatrix, i, j)
  qmatrix = qmatrix + np.transpose(qmatrix)

  # print results at this stage

  print_data(data, row_sum, letters)
  print_qmatrix(qmatrix, letters)
  # finding the min value and recording its coordinates (a,b)
  min_qmatrix = np.amin(qmatrix)
  coord = np.where(qmatrix == min_qmatrix)
  a = coord[0][0]  # coord[0] = [i, j] of coordinate with min value
  b = coord[1][0]  # there are 2 same min values in each qmatrix
  to_add = []

  for k in range(0, len(data)):
    if (k == a) or (k == b):
      continue
    to_add.append((data[a][k] + data[b][k] - data[a][b]) / 2)
  print("printing to_add:")
  print(to_add)

  # qm_size = len(qmatrix[0]) - 1
  # data = [data[:] for data in [[0] * (qm_size)] * (qm_size)]
  print("a is : " + str(a))
  print("b is : " + str(b))

  # row with larger index deleted first, via max(a,b)
  # row with smaller index: index number will not change even though row number has reduced
  # therefore deleted afterwards in min(a,b)

  data = np.delete(data, max(a, b), 0)
  data = np.delete(data, min(a, b), 0)
  data = np.delete(data, max(a, b), 1)
  data = np.delete(data, min(a, b), 1)

  # same logic applies to the deletion of letters, max(a,b) deleted first, smaller index given by min(a,b) not affected
  letters = np.delete(letters, max(a, b))
  letters = np.delete(letters, min(a, b))

  # insert row of updated values at appropriate location, given by min(a,b)
  data = np.insert(data, min(a, b), to_add, axis=0)

  # since size of data has changed with the above step,
  # add '0' to the appropriate spot (given by min(a,b)) in to_add to match new size of data
  to_add = np.insert(to_add, min(a, b), 0)

  # insert new letter at appropriate location in letters, given by min(a,b)
  letters = np.insert(letters, min(a, b), 'u')

  # insert column of updated values at appropriate location, given by min(a,b)
  data = np.insert(data, min(a, b), to_add, axis=1)

  # re-calculating row_sum according to the new data
  row_sum = [] * (len(data[0]))
  for row in data:
    row_sum.append([np.sum(row)])

  print_data(data, row_sum, letters)
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

data = np.loadtxt(sys.argv[1] , skiprows=1, usecols=range(1 , no_of_cols), dtype=np.float) # Assuming input values have range (-32768, 32767)

letters = [] * (no_of_cols - 1)
i = 0
for row in data:
  letters.append(chr(ord('A') + i))
  i += 1
print(letters)

# while (len(data[0]) > 2):
#   reduce(data, letters)

reduce(data,letters)

# row_sum = [] * (len(data[0]))
# for row in data:
#   row_sum.append([np.sum(row)])
#
# print_data(data, row_sum, letters)
#
# qm_size = len(data[0])
# qmatrix = [qmatrix[:] for qmatrix in [[0] * (qm_size)] * (qm_size)]
#
# # print(qmatrix)
# # print("len(qmatrix[0]) - 2 : " + str(len(qmatrix[0]) - 2))
# # print("data[0][1] is " + str(data[0][1]))
# # print("np.sum(0) is " + str(np.sum(data[0])))
# # print("np.sum(1) is " + str(np.sum(data[1])))
#
# for i in range(0, qm_size):
#   j = i + 1
#   for j in range(j, qm_size):
#     find_qscore(data, qmatrix, i, j)
# qmatrix = qmatrix + np.transpose(qmatrix)
#
# # print results at this stage
#
# print_data(data, row_sum, letters)
# print_qmatrix(qmatrix, letters)
# # finding the min value and recording its coordinates (a,b)
# min_qmatrix = np.amin(qmatrix)
# coord = np.where(qmatrix == min_qmatrix)
# a = coord[0][0] # coord[0] = [i, j] of coordinate with min value
# b = coord[1][0] # there are 2 same min values in each qmatrix
# to_add = []
#
# for k in range(0, len(data)):
#   if (k == a) or (k == b):
#     continue
#   to_add.append((data[a][k]+data[b][k]-data[a][b]) / 2)
# print("printing to_add:")
# print(to_add)
#
#
# # qm_size = len(qmatrix[0]) - 1
# # data = [data[:] for data in [[0] * (qm_size)] * (qm_size)]
# print("a is : " + str(a))
# print("b is : " + str(b))
#
# # row with larger index deleted first, via max(a,b)
# # row with smaller index: index number will not change even though row number has reduced
# # therefore deleted afterwards in min(a,b)
#
# data = np.delete(data, max(a,b), 0)
# data = np.delete(data, min(a,b), 0)
# data = np.delete(data, max(a,b), 1)
# data = np.delete(data, min(a,b), 1)
#
# # same logic applies to the deletion of letters, max(a,b) deleted first, smaller index given by min(a,b) not affected
# letters = np.delete(letters, max(a,b))
# letters = np.delete(letters, min(a,b))
#
# #insert row of updated values at appropriate location, given by min(a,b)
# data = np.insert(data, min(a,b), to_add, axis=0)
#
# # since size of data has changed with the above step,
# # add '0' to the appropriate spot (given by min(a,b)) in to_add to match new size of data
# to_add = np.insert(to_add, min(a, b), 0)
#
# # insert new letter at appropriate location in letters, given by min(a,b)
# letters = np.insert(letters, min(a, b), 'u')
#
# # insert column of updated values at appropriate location, given by min(a,b)
# data = np.insert(data, min(a,b), to_add, axis=1)
#
#
# # re-calculating row_sum according to the new data
# row_sum = [] * (len(data[0]))
# for row in data:
#   row_sum.append([np.sum(row)])
#
# print_data(data, row_sum, letters)
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
