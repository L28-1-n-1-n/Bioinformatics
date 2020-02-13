#!/usr/bin/python
import time
import sys
import numpy as np


# YOUR FUNCTIONS GO HERE -------------------------------------
def find_qscore(data, qmatrix, i, j):

  # formula according to lecture slides
  qmatrix[i][j] = (len(qmatrix[0]) - 1) * data[i][j] - np.sum(data[i]) - np.sum(data[j])

def print_data(data, row_sum, letters):

  # the data matrix(data), sum of each row (row_sum) and row/column headings (letters)
  # are stored differently, but printed in such a way that they form a table

  # adding row_sum
  data_show = np.append(data, row_sum, axis=1)

  print("-", end="\t")
  for l in letters:
    print(l, end="\t")
  print("Sum")

  count = 0
  for row in data_show:
    print(letters[count], end="\t")
    for r in row:
      print(r, end="\t")
    print("\n")
    count += 1

  print("\n")


def print_qmatrix(qmatrix, letters):

  print(">>> Q Score (qmatrix) <<<")

  print("-", end="\t")
  for l in letters:
    print(l, end="\t")
  print("\n")
  count = 0
  for row in qmatrix:
    print(letters[count], end="\t")
    for r in row:
      print(r, end="\t")
    print("\n")
    count += 1
  print("\n")

def reduce(data, letters):

  # get dimension of data matrix
  size_of_data = len(data[0])

  if (size_of_data == 2): # ending condition: when data is 2x2
    return(0)

  new_letter = chr(ord('z') - size_of_data) # new_letter is what to name the new combined row or column

  # store sum of each row in an array called row_sum
  row_sum = [] * (size_of_data)
  for row in data:
    row_sum.append([np.sum(row)])

  # declare qmatrix, which will store the Q score of each element of data matrix
  qm_size = size_of_data
  qmatrix = [qmatrix[:] for qmatrix in [[0] * (qm_size)] * (qm_size)]

  # now calculate the Q score for every element
  for i in range(0, qm_size):
    j = i + 1
    for j in range(j, qm_size):
      find_qscore(data, qmatrix, i, j)

  #fill up the second half of the matrix by transposing and adding
  qmatrix = qmatrix + np.transpose(qmatrix)

  # print results at this stage
  print(">>> Initial Data Matrix (data)<<<")
  print_data(data, row_sum, letters)
  print_qmatrix(qmatrix, letters)

  # finding the min value and recording its coordinates (a,b)
  min_qmatrix = np.amin(qmatrix)
  coord = np.where(qmatrix == min_qmatrix)
  a = coord[0][0]  # coord[0] = [i, j] of coordinate with min value
  b = coord[1][0]  # there are 2 same min values in each qmatrix

  # calculate the new column and store it in to_add, without any zero values
  to_add = []
  for k in range(0, len(data)):
    if (k == a) or (k == b):
      continue
    to_add.append((data[a][k] + data[b][k] - data[a][b]) / 2)


  # Augment data matrix by first deleting 2 rows and 2 columns
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
  letters = np.insert(letters, min(a, b), new_letter)

  # insert column of updated values at appropriate location, given by min(a,b)
  data = np.insert(data, min(a, b), to_add, axis=1)

  # re-calculating row_sum according to the new data
  row_sum = [] * (len(data[0]))
  for row in data:
    row_sum.append([np.sum(row)])

  # print the reduced data matrix
  print(">>> Reduced Data Matrix (data)<<<")
  print_data(data, row_sum, letters)

  # call the same function with the newly reduced data matrix
  reduce(data, letters)
# ------------------------------------------------------------

start = time.time()

#-------------------------------------------------------------

# YOUR CODE GOES HERE ----------------------------------------

def NJ():
  with open(sys.argv[1]) as f:  # Use file to refer to the file object
      line = f.readline() # read the first line
      no_of_cols = len(line.split()) # get the number of columns of the first line

  # load only the numbers into a matrix called data
  data = np.loadtxt(sys.argv[1] , skiprows=1, usecols=range(1 , no_of_cols), dtype=np.float) # Assuming input values have range (-32768, 32767)

  # compose an initial list of letters as headings for rows and columns in data matrix
  letters = [] * (no_of_cols - 1)
  i = 0
  for row in data:
    letters.append(chr(ord('A') + i))
    i += 1

  # recursive function to reduce the data matrix
  reduce(data,letters)

NJ();
#-------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This calculates the time taken and will print out useful information
stop = time.time()
time_taken=stop-start

# Print out the best

print('Time taken: '+str(time_taken))

#-------------------------------------------------------------
