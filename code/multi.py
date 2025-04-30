# input:  a word of length at least 3, and integer e
# output: lists of possible extensions of this word
# by adding e letters which also form a word.
# This is called a "multi-word steal" in stealwords.

# We build on the script ext.py which forms a tree of extensions of word
# by up to e letters.  Now we focus on exactly e letters and save only
# those cases where those e letters form a word.

import sys

class TreeNode:
    def __init__(self, data):
#       data format should already be set as string: "k;alpha;word1,word2,..."
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    # children will be all extensions of alpha = self.data
    def create_children(self, m):  # m = max length of extensions
        data = self.data
        array = data.split(";")
        index = array[0]
        alpha = array[1]
        n = len(alpha)
        depth = m - n
        if depth == 0 :    # base case
            return
        child_data = extend_node(data, m)
        # print(child_data)
        num_children = len(child_data)
        if num_children == 0 :
            return
        for i in range(num_children):
            child = TreeNode(child_data[i])
            self.children.append(child)
            child.create_children(m)   # recurse!

    # for printing:
    def __str__(self, level=0):
        ret = "._" * level + str(self.data) + "\n"
        # ret = "  " * level + "+1 " + str(self.data) + "\n"
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
#        if file == "../edges/4-5-edges.txt" :
#            if i > 338 and i < 350 :
#                print(alphas[i])
    return alphas

# all_edges[i,j] contains edges from file i-j-edges.txt
# i ranges 2 to 14, and j goes i+1 to 15

def load_edges() :
    all_edges = []
    for i in range(15) :
        some_edges = []
        if i < 2 :
            edges = []
            some_edges.append(edges)
            all_edges.append(some_edges)
            continue
        for j in range(16) :
            if j < i+1 :
                edges = []
                some_edges.append(edges)
                continue
            file = "../edges/" + str(i) + "-" + str(j) + "-" + "edges.txt"
            edges = import_alphas(file)
#            if i == 4 and j == 5 :
#                print(edges)
            some_edges.append(edges)
        all_edges.append(some_edges)
    return all_edges

all_edges = load_edges()

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

def load_indices() :
    all_indices = []
    for i in range(15) :
        some_indices = []
        if i < 2 :
            indices = []
            some_indices.append(indices)
            all_indices.append(some_indices)
            continue
        for j in range(16) :
            if j < i+1 :
                indices = []
                some_indices.append(indices)
                continue
            file = "../edges/" + str(i) + "-" + str(j) + "-" + "indices.txt"
            indices = import_alphas(file)
            some_indices.append(indices)
        all_indices.append(some_indices)
    return all_indices

all_indices = load_indices()


# To build the tree of all edges to nodes which add at most e letters to word
# we can describe the root as word, then the children of root are all nodes
# reached from word by adding at most e letters by using one edge from the digraph.
# This means finding the line with word in each of the edge files of form
# n-m-edges, with n = len(word) and m=n+1,...,n+e. These children of root can
# then be traversed and same procedure can be run adding letters to form new
# nodes with at most n+e letters.  This max value n+e needs to be global in
# this procedure since it is not intrinsic to any node in any layer.
# The length of data at node determines whether to expand into more children

# Note: we can now use updated arrays: all_indices and kwords.
# all_indices contains edges but now instead of letters to add there is an index
# into the target knodes array, which also matches the kwords array index.
# This way we avoid any new lookups.

def extend_node(data, m) :  # m = max number of letters in new knodes
    # assume data has (string) format: index;alpha;word1,word2,...
    # return alphas = array of new data for nodes
    array = data.split(";")
    index = array[0]
    alpha = array[1]
    alpha = "".join(sorted(alpha))  # to be sure we are starting alphabetized
    words = array[2]
    n = len(alpha)
    alphas = []
    if n == m :
        return alphas
    e = m - n           # e = number of letters to add
    for i in range(e) :
        line = all_indices[n][n+1+i][int(index)]
        if line[-1] == ";" :
            continue
        array = line.split(";")
        indices = array[1].split(",")
        for k in indices :
            # print("converting to int: ", k)
            beta = kwords[n+1+i][int(k)]
            beta = k + ";" + beta
            alphas.append(beta)
    return(alphas)

# n = length of alpha node, k = index in nodes array
# output is index into nodes array of length n + 1
def gen_step(n, k, step) :  
    line = all_indices[n][n+step][k]
    array = line.split(";")
    if len(array[1]) > 0 :
        alpha = array[0]
        indices = array[1].split(",")
        num = len(indices)
        r = random.randint(0, num-1)
        index = int(indices[r])
        beta = knodes[n+1][index]
        # print(beta)
        return index
    return -1

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

########################################################################

# main part of script:

# print("Argument List:", str(sys.argv))
args = len(sys.argv)

word = sys.argv[1]
e = int(sys.argv[2])
n = len(word)        
m = n + e
alpha = "".join(sorted(word))
k = iof_word(alpha, knodes[n])
data = str(k) + ";" + kwords[n][k]

tree = TreeNode(data)
tree.create_children(m)
print(tree)


