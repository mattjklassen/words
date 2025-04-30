# read in n-m-edges.txt and convert to n-m-indices.txt, where this file
# has the same information but instead of the additional letters there is an index
# into the file mnodes.txt which is also the same index for file mwords.txt

# run with:  python inidices.py n m 

import sys

print("Argument List:", str(sys.argv))
args = len(sys.argv)

n = sys.argv[1]
m = sys.argv[2]

def import_alphas(file):
    alphas = []
    with open(file, 'r') as f:
        alphas = f.readlines()
        f.close()
    n = len(alphas)
    for i in range(n):
        alphas[i] = alphas[i].strip()
    return alphas

file1 = "../nodes/" + n + "nodes.txt"
nodes1 = import_alphas(file1)
n1 = len(nodes1)
print("n1: ", n1)

file2 = "../nodes/" + m + "nodes.txt"
nodes2 = import_alphas(file2)
n2 = len(nodes2)
print("n2: ", n2)

file3 = "../edges/" + n + "-" + m + "-edges.txt"
edges = import_alphas(file3)
n3 = len(edges)
print("n3: ", n3)

file = "../edges/" + n + "-" + m + "-indices.txt"
indices = []

for i in range(n1):
    indices.append(nodes1[i] + ";")
# array indices now has same number of entries as n-m-edges.txt

# step through edges (lines) which are n-nodes followed by letter sets
# and convert each additional set of letters into new node
# then write index of new node to file indices

def iof_word(alpha, words):
    low = 0
    high = len(words)-1
    while (low <= high):
        guess = (low + high) // 2
        if words[guess] == alpha:
            return guess
        elif words[guess] < alpha:
            low = guess + 1
        else:
            high = guess - 1
    return -1

i = 0  # index of lines 

while i < n3 :
    line = edges[i]
    array = line.split(";")
    alpha = array[0]
    if len(array[1]) > 0 :
        adds = array[1].split(",")
        for add in adds :
            beta = alpha + add
            beta = "".join(sorted(beta))
            # beta is now target alphabetized string or m-node
            index = iof_word(beta, nodes2)
            if indices[i][-1] == ";" :
                indices[i] += str(index)
            else :
                indices[i] += "," + str(index)
    i += 1
                
def write_indices(file, indices) :
    output = []
    for i in range(len(indices)) :
        output.append(indices[i])
        output.append('\n')
    with open(file, 'w') as f:
        f.writelines(output)
        f.close()

write_indices(file, indices)

exit(0)



# other functions not being used here:

def is_word(alpha, words):
    low = 0
    high = len(words)-1
    while (low <= high):
        guess = (low + high) // 2
        if words[guess] == alpha:
            return True
        elif words[guess] < alpha:
            low = guess + 1
        else:
            high = guess - 1
    return False 

def remove_i(alpha, i):
# Removes the character at the i-th index of a string.
  if not 0 <= i < len(alpha):
        raise IndexError("Index is out of bounds")
  return alpha[:i] + alpha[i+1:]

def subalphas(alpha):
    n = len(alpha)
    subs = []
    previous = ""
    for i in range(n):
        if alpha[i] != previous:
            new = remove_i(alpha, i)
            subs.append(new)
        previous = alpha[i]
    return subs

# the alpha-string which remains after removing alpha from beta
def remains(alpha, beta):
    n = len(alpha)
    m = len(beta)
    rem = beta
    for char1 in alpha:
        i = 0
        for char2 in rem:
            if char1 == char2:
                rem = remove_i(rem, i)
                break
            i += 1
    return rem

        
    






