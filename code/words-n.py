# read in knodes.txt and ksort.txt and merge into kwords.txt
# kwords.txt should be same as knodes.txt but with all words after alpha

# run with:  python words-n.py n  (where n is length of words)

import sys

print("Argument List:", str(sys.argv))
args = len(sys.argv)

n = sys.argv[1]

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

file2 = "../dict/" + n + "sort.txt"
nodes2 = import_alphas(file2)
n2 = len(nodes2)
print("n2: ", n2)

file = "../nodes/" + n + "words.txt"
words = []

for i in range(n1):
    words.append(nodes1[i] + ";")

# step through nodes1 (nodes) and nodes2 (lines)
# and write each word matching node into words array.

i = 0  # index of nodes
j = 0  # index of lines 

while i < n1 and j < n2 :
    node1 = nodes1[i]
    line = nodes2[j]
    word_array = line.split(",")
    alpha = word_array[0]
    word = word_array[1]
    if alpha == node1 :
        if words[i][-1] == ";" :
            words[i] +=  word
        else :
            words[i] += "," + word
        j += 1
    else :
        i += 1

def write_words(file, words) :
    output = []
    for i in range(len(words)) :
        output.append(words[i])
        output.append('\n')
    with open(file, 'w') as f:
        f.writelines(output)
        f.close()


write_words(file, words)

exit(0)



# other functions not being used here:

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

        
    






