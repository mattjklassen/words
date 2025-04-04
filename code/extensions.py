# input:  a word of length at least 4, and integer k
# output: lists of possible extensions of this word
# by adding k letters

# the first layer just comes from one edges lookup, the second
# needs at least two lookups, using paths with one or two edges.

# the idea is to possibly reduce the lookup sizes when using
# extensions as compared to raw lookups for combined letters.
# if we do construct an entire tree of extensions of a given
# word, then as a game progresses this tree will be pruned.

# command line parameters:  word e
#
# word is a word, e is the depth for extension
# so if word has length 4 letters, and e=2, then we are
# finding all extensions of this word by 2 letters.

# It makes sense to construct a tree that captures this process.


import sys

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    # children will be all extensions of alpha = self.data
    def create_children(self, depth):
        if depth == 0:    # base case
            return
        alpha = self.data
        child_data = extend(alpha)
        num_children = len(child_data)
           
        for i in range(num_children):
            child = TreeNode(child_data[i])
            self.children.append(child)
            child.create_children(depth-1)   # recurse!

    # for printing:
    def __str__(self, level=0):
        ret = "  " * level + str(self.data) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret
    
    # for pruning:
    def remove_child(self, child_node):
        self.children = [child for child in self.children if child != child_node]

            
def import_alphas(file) :
    alphas = []
    with open(file, 'r') as f :
        alphas = f.readlines()
        f.close()
    n = len(alphas)
    for i in range(n) :
        alphas[i] = alphas[i].strip()
    return alphas


# form arrays of m-n-edges organized by difference m-n
# start with m-n=1 in some_edges, and append to all_edges, etc.
# for example, with n=2, m=7, m-n=5, we want to load up all
# edges files with m-n=1,2,3,4, and m,n between 2 and 15.

# n is word length, e is extension max, or max number of letters to add to word
def load_edges(n, e) :
    m = n + e
    all_edges = []
    for i in range(m-n-1) :
        some_edges = []
        for j in range(n, 15 - i) :
            file = str(j) + "-" + str(j+1+i) + "-" + "edges.txt"
            edges = import_alphas(file)
            k = len(edges)
            some_edges.append(edges)
        all_edges.append(some_edges)
    return all_edges

# so all_edges[i] contains edges of type m-n=i+1, or i=m-n-1.
# all_edges[i][j], with i=m-n-1, contains n-m-edges with n=j+2, or j=n-2.
# so the n-m-edges are in all_edges[m-n-1][n-2].
# for example, all_edges[1][2] contains the 4-6-edges.

# form arrays of k-nodes
        
def load_nodes(n, m) :
    knodes = []
    for i in range(n, m+1) :
        file = str(i) + "nodes.txt"
        nodes = import_alphas(file)
        length = len(nodes)
        knodes.append(nodes)
    return knodes

# print("knodes array has lens: ")
# print(klens)

# now array knodes[i] is from file knodes.txt with k = i + 2
# so for nodes in knodes.txt use knodes[k-2]

# find extensions of word node by adding up to e letters
# and doing this as only one step, so this can be used to form
# one layer of children below one node in the tree
# for example, if n=4, e=3, then we construct one layer of edges
# by using all n-m-edges for m=5,6,7. This is used in a tree to
# do layers recursively, so all of the above child nodes would 
# have the same process but with depth e=2, etc.

def extend_word(word, e) :
    n = len(word)
    word = "".join(sorted(word))
    m = n + e
    alphas = []
    # open edges arrays all_edges[i][j] and get line for word
    # for i = 0 to e-1, j = n-2
    j = n - 2
    k = iof_word(word, knodes[n-2])
    for i in range(e) :
        line = all_edges[i][j][k]
        alphas1 = line.split(";")
        alphas2 = alphas1[1].split(",")
        for alpha in alphas2 :
            beta = "".join(word, alpha)
            beta = "".join(sorted(beta))
            alphas.append(beta)
    return(alphas)


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

########################################################################

# main part of script:

print("Argument List:", str(sys.argv))
args = len(sys.argv)

word = sys.argv[1]
e = int(sys.argv[2])
n = len(word)        
alpha = "".join(sorted(word))

print("word: ")
print(word)
print("alpha: ")
print(alpha)
print("depth:")
print(e)
print("length:")
print(n)

m = n + e
all_edges = load_edges(n, e)
knodes = load_nodes(n, m)

tree = TreeNode(word)
print(tree)

