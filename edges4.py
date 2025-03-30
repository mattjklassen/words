# this version will do difference of 4 between n and m, 
# n < m to generate n-m-edges.txt or examples.

# We loop through m-nodes beta and build lists of leaves and nodes
# of lengths n through m-1 which are subsets of the m-node beta. 
# We then check for edges from the list of n-nodes to any of the 
# other nodes of length n+1 to m-1, eliminating the n-node when such 
# edge is found.  The remaining n-nodes need an n->m edge.

import sys

print("Argument List:", str(sys.argv))
args = len(sys.argv)

nstr = sys.argv[1]
n = int(nstr)
mstr = sys.argv[2]
m = int(mstr)
        
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    # children will be all subalphas of alpha = self.data
    def create_children(self, depth):
        if depth == 0:    # base case
            return
        alpha = self.data
        child_data = subalphas(alpha)
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

def nodes_with_length(node, length, result_list):
    if node is None:
        return
    if len(node.data) == length :
        result_list.append(node.data)
    for child in node.children:
        nodes_with_length(child, length, result_list)

def get_nodes(root, length):
    result = []
    nodes_with_length(root, length, result)
    return result    


# get list of leaves of tree
def get_leaves(root):
    if root is None:
        return []
    if not root.children :
        return [root.data]
    leaves = []
    for child in root.children:
        leaves.extend(get_leaves(child))
    return leaves    

# get rid of dups: 
def get_unique(alpha_list) :
    unique = []
    k = len(alpha_list)
    for i in range(k) :
        leaf = alpha_list[i]
        u = len(unique)
        dup = 0
        for j in range(u) :
            if leaf == unique[j] :
                dup = 1
        if dup == 0 :
            unique.append(leaf)
    return unique
            
def import_alphas(file) :
    alphas = []
    with open(file, 'r') as f :
        alphas = f.readlines()
        f.close()
    n = len(alphas)
    for i in range(n) :
        alphas[i] = alphas[i].strip()
    return alphas

# k-alpha means an alphabetized string of length k
# k-node means a k-alpha which has a word permutation
# alpha-graph means the graph of k-nodes (k=1,...,15) with directed edges
# of type n-m with n<m from an n-node to an m-node if the letters of n-node
# are a subset of the letters of m-node, and there does not exists a 
# simpler path from the n-node to this m-node through shorter i-j-edges.
# This is equivalent to the statement that the group of m-n letters to be
# added to the m-node can be done in steps of size smaller than m-n,
# passing through other j-nodes in the path.
#
# need to work with nodes for n, n+1, ... , m so that we can determine
# if an edge from n to m should exist by checking if a path already
# exists of type n -> n+1 -> m.  

# need to generate all the *nodes.txt file names, then in a loop create
# each of the nodes* arrays and put those into an array of arrays.

# form arrays of m-n-edges organized by difference m-n
# start with m-n=1 in edges1, and m-n=2 in edges2:

all_edges = []
all_lens = []

edges1 = []
lens1 = []

for i in range(2, 15) :
    file = str(i) + "-" + str(i+1) + "-" + "edges.txt"
    edges = import_alphas(file)
    k = len(edges)
    lens1.append(k)
    edges1.append(edges)

all_edges.append(edges1)
all_lens.append(lens1)

edges2 = []
lens2 = []

for i in range(2, 14) :
    file = str(i) + "-" + str(i+2) + "-" + "edges.txt"
    edges = import_alphas(file)
    k = len(edges)
    lens2.append(k)
    edges2.append(edges)

all_edges.append(edges2)
all_lens.append(lens2)

edges3 = []
lens3 = []

for i in range(2, 13) :
    file = str(i) + "-" + str(i+3) + "-" + "edges.txt"
    edges = import_alphas(file)
    k = len(edges)
    lens3.append(k)
    edges3.append(edges)

all_edges.append(edges3)
all_lens.append(lens3)

# all_edges[k] is the set of n-m-edges with k=m-n-1, so for k=0 we have m-n=1
# so all_edges[0] are edges of step 1 = m-n, all_edges[1] of step 2, etc.
# for example, all_edges[1][2] contains all 4-6-edges.
# and all_lens[k] is the set of array lengths of arrays n-m-edges, k=m-n-1.
# so all_lens[0] are array lengths of step size m-n=1, etc.

# form arrays of k-nodes
        
knodes = []
klens = []

for i in range(2, 16) :
    file = str(i) + "nodes.txt"
    nodes = import_alphas(file)
    length = len(nodes)
    klens.append(length)
    knodes.append(nodes)

# print("knodes array has lens: ")
# print(klens)

# now array knodes[i] is from file knodes.txt with k = i + 2
# so for nodes in knodes.txt use knodes[k-2]

# initialize edges array: (for n=2, m=5 use knodes[n-2]=knodes[0])
edges = []
for i in range(klens[n-2]) :
    edges.append(knodes[n-2][i] + ";")

file = nstr + "-" + mstr + "-" + "edges.txt"

# returns T if there is an n-m-edge, alpha -> beta
# (assumes m - n < 4, by previous computations)
def is_edge(alpha, beta) :
    a = len(alpha)
    b = len(beta)
    d = b - a
    if d < 1 :
        print("alpha not shorter than beta")
        return False
    # make sure alpha is a subset of beta 
    temp = beta
    for i in range(a) :
        good = 0
        for j in range(b) :
            if alpha[i] == temp[j] :
                good = 1
                temp = temp[:j] + "*" + temp[j+1:]
                break
        if good == 0 :
            # print("alpha not a subset of beta")
            return False
    if not is_word(alpha, knodes[a-2]) :
        print("alpha is not a word")
        return False
    if not is_word(beta, knodes[b-2]) :
        print("beta is not a word")
        return False
    # for alpha -> beta to be an edge we need to find remains(alpha,beta)
    # in the list of strings after the semicolon in edge_str.
    k = edge_index(alpha)
    edge_str = all_edges[d-1][a-2][k]
    temp = edge_str.split(";")
    rems = temp[1].split(",")
    rem = remains(alpha, beta)
    for i in range(len(rems)) :
        good = 0
        if rem == rems[i] :
            good = 1
            # print("found edge of type: ", str(a), "->", str(b))
    # print(edge_str)
    return True
    
def sort_str(alpha, beta) :
    gamma = alpha + beta 
    letters = list(gamma)
    newsort = sorted(letters)
    gamma = "".join(newsort)
    return gamma

def edge_index(alpha) :
    n = len(alpha)
    k = iof_word(alpha, knodes[n-2])
    return k

def write_edges(file, edges) :
    output = []
    for i in range(len(edges)) :
        output.append(edges[i])
        output.append('\n')
    with open(file, 'w') as f :
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

# Tree formation was used initially to create strings from one alpha
# of length n, with lower lengths n-1, n-2, etc., by leaving out one letter
# at a time. This was convenient, but too redundant.  In the latest methods
# we are creating such strings with those lengths but not using the tree
# structure.  So we need to optimize the string creation but not miss
# any strings in the process. The function subalphas forms these strings
# without redundancy. This can be done recursively, then the lists can
# be reduced to only nodes of each length.  

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
        if is_word(x, knodes[n-2]) :
            nodes.append(x)
    return nodes
        
# form tree from alpha, with (possibly redundant) nodes, and depth m - n
def rootof(alpha, depth) :
    # depth = m - n
    root = TreeNode(alpha)
    root.create_children(depth)
    return root        

# getlist finds all leaves on tree built from rootof(alpha), depth m - n,
# with dups deleted and only n-nodes

def getlist(root, n) :
    leaves = get_leaves(root)
    unique = get_unique(leaves)
    nodes = []
    for x in unique :
        if is_word(x, knodes[n-2]) :
            nodes.append(x)
    return nodes
                    
# Recursively traverses a tree and removes nodes that meet the given condition.
def prune_tree(node, condition):
    # Base case: If the current node should be removed, return None
    if not_word_node(node):
        return None
    # Recursively filter children
    new_children = []
    for child in node.children:
        updated_child = prune_tree(child, not_word_node)
        if updated_child:
            new_children.append(updated_child)
    node.children = new_children
    return node

def print_tree(node, level=0):
    """Helper function to print the tree structure"""
    if node is not None:
        print("  " * level + str(node.value))
        for child in node.children:
            print_tree(child, level + 1)

def not_word_node(node) :
    alpha = node.data
    k = len(alpha)
    return not is_word(alpha, knodes[k-2])

# prune leaves1 list by removing any nodes in leaves2 of pruned tree
# note: leaves1 is list obtained from tree from alpha (removing non-nodes and dups)
# so leaves1 is the candidate list for 2-node in a 2-4-edge,
# and leaves2 is obtained from pruned tree (only has word_nodes), 
# if leaves1 is empty then there are no 2-4 edges in this case,
# if leaves2 is empty then all 2-nodes in leaves1 give 2-4 edges.

# remove elements in leaves1 which are in leaves2
# note: both leaves1 and leaves2 have only 2-nodes and no dups
def prune_leaves(leaves1, leaves2) :
    pruned = []
    m = len(leaves1)
    n = len(leaves2)
    dup = 0
    for i in range(m) :
        dup = 0
        for j in range(n) :
            if leaves1[i] == leaves2[j] :
                dup = 1
        if dup == 0 :
            pruned.append(leaves1[i])
    return pruned

# Example usage
# this function still has the old method using trees
def do_example(alpha, n, m) :
    depth = m - n
    root = rootof(alpha, depth)
    print("Original Tree:\n")
    print(root)
    print("leaves which are nodes:")
    leaves = getlist(root, n)
    print(leaves)
    depth -= 1
    root = rootof(alpha, depth)
    print("Next Tree:\n")
    print(root)
    print("nodes:")
    nodes1 = getlist(root, n+1)
    print(nodes1)
    depth -= 1
    root = rootof(alpha, depth)
    print("Next Tree:\n")
    print(root)
    print("nodes:")
    nodes2 = getlist(root, n+2)
    print(nodes2)
    depth -= 1
    root = rootof(alpha, depth)
    print("Next Tree:\n")
    print(root)
    print("nodes:")
    nodes3 = getlist(root, n+3)
    print(nodes2)
    leaves1 = elim_leaves(leaves, nodes1)
    leaves2 = elim_leaves(leaves1, nodes2)
    leaves3 = elim_leaves(leaves2, nodes3)
    print("leaves3:")
    print(leaves3)
    print("\n\nnow using get_nodes ... \n\n")
    depth = m - n
    root = rootof(alpha, depth)
    out = get_nodes(root, depth)
    out = set(out)
    print("new nodes: ")
    print(out)


def elim_leaves(leaves, nodes) :
    if not leaves or not nodes :
        return leaves
    new = []
    a = len(leaves[0])
    b = len(nodes[0])
    for leaf in leaves :
        found = 0
        for node in nodes :
            if is_edge(leaf, node) :
                # print("found edge: ", leaf, " -> ", node)
                found = 1
                break
        if found == 0 :
            new.append(leaf)
    return new

# to run do_example enter alpha as m-node to use trees to find all edges
# from n-nodes to this m-node.  For example 5-node like AAABK for alpha
# and run python edges3.py 2 5

# fill_edges passes in global ints n, m for edges of type n -> m
# then loops through m-nodes and forms tree of depth d = m - n
# so that leaves are nodes of length n, in knodes[n-2].

def fill_edges(n, m) :
    for i in range(len(knodes[m-2])) :
        depth = m - n
        beta = knodes[m-2][i]
        nodes = nodes_of(beta, m-n)
        # nodes is list of lists containing all nodes with potential edges to beta,
        # and with depth at most m-n: nodes[0] = [beta], nodes[1] = nodes of depth 1, 
        # ..., nodes[n-m] = leaves, or nodes of length n.
        leaves = nodes[depth]
        for j in range(1, depth) :
            leaves = elim_leaves(leaves, nodes[depth-j])

        for alpha in leaves :
            index = iof_word(alpha, knodes[n-2])
            if index > -1 :
                edge = remains(alpha, beta)
                if edges[index][-1] == ";" :
                    edges[index] += edge
                else :
                    edges[index] += "," + edge 


# testing is_edge:
# alpha = "AAB"
# print("alpha = ", alpha)
# beta = "AAABK"
# print("beta = ", beta)
# result = is_edge(alpha, beta)
# print(result)
 
# gamma = sort_str(alpha, beta)
# print(gamma)

# alpha = "AAABKS"
# alpha = "EFIPRX"
# alpha = "AADDX"
# alpha = "FFHSU"
# do_example(alpha, n, m)
    
# out = nodes_of(alpha, m-n)
# print("nodes of ", alpha)
# print(out)
# print("nodes[0]:")
# print(out[0])

fill_edges(n,m)
write_edges(file, edges)

exit(0)

