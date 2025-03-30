# this version does n=m-1 so edges of type 2-3, 3-4 etc.

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

file1 = n + "nodes.txt"
nodes1 = import_alphas(file1)
n1 = len(nodes1)

m = int(n) + 1
file2 = str(m) + "nodes.txt"
nodes2 = import_alphas(file2)
n2 = len(nodes2)

file = n + "-" + str(m) + "-" + "edges.txt"

edges = []
for i in range(n1):
    edges.append(nodes1[i] + ";")

def write_edges(file, edges) :
    output = []
    for i in range(len(edges)) :
        output.append(edges[i])
        output.append('\n')
    with open(file, 'w') as f:
        f.writelines(output)
        f.close()

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

for beta in nodes2:
    subs = subalphas(beta)
    index = -1
    for alpha in subs:
        index = iof_word(alpha, nodes1)
        if index > -1 :
            edge = remains(alpha, beta)
            if edges[index][-1] == ";" :
                edges[index] += edge
            else :
                edges[index] += "," + edge 
                
write_edges(file, edges)

# for i in range(len(edges)):
#    print(edges[i])


        
    






