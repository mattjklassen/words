# read in 3nodes and 6nodes
# pass through 3 nodes and for each node loop through all 3nodes
# and concat the two nodes to get a 6alpha and check if it is a 6node.

            
def import_alphas(file) :
    alphas = []
    with open(file, 'r') as f :
        alphas = f.readlines()
        f.close()
    n = len(alphas)
    for i in range(n) :
        alphas[i] = alphas[i].strip()
#        if file == "../edges/4-5-edges.txt" :
#            if i > 338 and i < 350 :
#                print(alphas[i])
    return alphas

# form arrays of k-nodes
        
def load_nodes() :
    knodes = []
    for i in range(16) :
        if i < 2 :
            nodes = []
            knodes.append(nodes)
            continue
        file = "../nodes/" + str(i) + "nodes.txt"
        nodes = import_alphas(file)
        knodes.append(nodes)
    return knodes

knodes = load_nodes()
# array knodes[i] is from file knodes.txt with k = i

def load_words() :
    kwords = []
    for i in range(16) :
        if i < 2 :
            words = []
            kwords.append(words)
            continue
        file = "../nodes/" + str(i) + "words.txt"
        words = import_alphas(file)
        kwords.append(words)
    return kwords

kwords = load_words()
# array kwords[i] is from file kwords.txt with k = i


def iof_word(alpha, wordlist):
    low = 0
    high = len(wordlist)-1
    while (low <= high):
        guess = (low + high) // 2
        if wordlist[guess] == alpha:
            return guess
        elif wordlist[guess] < alpha:
            low = guess + 1
        else:
            high = guess - 1
    return -1

def remove_i(alpha, i):
# Removes the character at the i-th index of a string.
  if not 0 <= i < len(alpha):
        raise IndexError("Index is out of bounds")
  return alpha[:i] + alpha[i+1:]

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

# forms alphas of length k-1 from alpha of length k by removing one char
def subalphas(alpha) :
    k = len(alpha)
    subs = []
    previous = ""
    for i in range(k) :
        if alpha[i] != previous :
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

# forms list of lists of nodes of each alphas of lengths n-1, n-2, ...
# to n-depth, where n=len(alpha).

def nodes_of(alpha, depth) :
    alphas = []
    first = []
    first.append(alpha)
    alphas.append(first)
    subs = sorted(subalphas(alpha))
    alphas.append(subs)
    for i in range(2, depth+1) :
        new = []
        for j in range(0,len(subs)) :
            new.extend(subalphas(subs[j]))
        subs = sorted(list(set(new)))
        alphas.append(subs)
    nodes = list(map(nodes_only, alphas))
    return nodes

def nodes_only(alphas) :
    nodes = []
    for x in alphas :
        n = len(x)
        if is_word(x, knodes[n]) :
            nodes.append(x)
    return nodes
        
########################################################################

# main part of script:

def forward() :
    i = 0
    for node1 in knodes[3] :
        print(node1)
        i += 1
        for node2 in knodes[3] :
            alpha = node1 + node2
            alpha = "".join(sorted(alpha))
            k = iof_word(alpha, knodes[6])
            if k > -1 :
                print("   " + kwords[6][k])
        if i > 3 :
            break
        
# did this part, which generates too much stuff, not uniquely, so maybe
# it is better to go back to the old method that I did with perl years ago:
# start with the 6-nodes and find all splittings into 3-node plus 3-node.

def backward() :
    i = 0
    for alpha in knodes[6] :
        print(alpha)
        nodes = nodes_of(alpha, 3)
        print(nodes[3])
        for node1 in nodes[3] :
            # remove node1 from alpha
            node2 = remains(node1, alpha)
            k1 = iof_word(node1, knodes[3])
            k2 = iof_word(node2, knodes[3])
            if k2 > -1 :
                # print("found 3+3: ", node1, " + ", node2)
                print(kwords[3][k1], " + ", kwords[3][k2], " = ", kwords[6][i])
        i += 1
        if i > 7 :
            break

backward()



