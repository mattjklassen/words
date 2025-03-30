# this version will do difference of 3 between n and m, n < m
# to generate n-m-edges.txt or examples.

# the first case is 2-5-edges and we already have a complication
# that didn't arise when m-n=2:  It is not sufficient to work with
# the tree built from each 5-node, collect leaves1, reduce to nodes,
# then prune tree, again collect leaves2, then prune out leaves2
# from leaves1 to get leaves3.  
# 
# Unfortunately this will miss paths from a 2-node to a 5-node 
# through paths which are of type 2-3-5 or 2-4-5.  It is possible
# to have a 2-node which is indicated by the previous process, ie.
# is in leaves3, but it also has path of these other types which
# is not yet flagged. Those paths have been constructed, and now
# need to be used for the final pruning of leaves3.  So leaves4
# will be those that also do not have a 2-3-5 or 2-4-5 path to
# the 5-node.  
#
# We can detect those by simply opening 3-5-edges and 2-4-edges
# and check if 1) any 2-node in leaves3 has a 2-4 edge to a 4-node
# in the pruned tree (these are all 4-nodes which are children of
# the 5-node), or 2) any 3-node which has a 3-5 edge to the 5-node
# also has a 2-3 edge from a 2-node in leaves3.  
#
# We have new function:  is_edge(a,b) which returns T/F and
# requires looking in the correct array of n-m-edges, where n is
# len(a) and m is len(b).  For the 2 cases above, we call this
# a minimal number of times by restricting 2-nodes to leaves3,
# and restricting 4-nodes to the children of the 5-node.
# 
# Bigger gaps between n and m will make this process more difficult.

# Another approach:
# To extend these methods to higher gaps m - n, we could organize around
# the process of building the sub-digraph which could play the role of
# tree in the previous cases for small m - n.  For example, for n=2, m=5
# we already have the paths of type 2-3-5 or 2-4-5 which need to be
# used to eliminate certain 2-nodes from needing a 2-5 edge.  So we
# could start with the process of forming all possible nodes which
# can be part of the sub-digraph starting with some fixed 5-node.
# Clearly such nodes all need to be built out of subsets of the
# letters making the 5-node alpha.  We can do this with the tree 
# construction using the function rootof(alpha), but also make lists
# in each case of 4-nodes, 3-nodes, and 2-nodes.  Then we prune those
# lists of dups and non-words.  This gives all possible nodes that
# can have paths leading to the 5-node.  To construct the sub-digraph
# we need to identify all edges of type 2-3, 2-4, 3-4, 3-5, all of
# which are already computed and listed in edges-n-m.txt files.
# In this sub-digraph there cannot be any isolated nodes of degree
# greater than 2, since such isolation would imply a necessary edge
# directly to the 5-node.  For example, an isolated 3-node has no
# path 3-4-5 to the 5-node, which is exactly the criterion for a
# 3-5 edge, which would have already been constructed.  In summary,
# to find any 2-5 edges, we build the above sub-digraph and look
# for any isolated 2-nodes.  These are the required 2-5-edges.
#
# Note: An important step above is to be sure to build nodes before
# pruning. This is because there may be a 4-alpha which is a sub-alpha
# of the 5-node, but it is not a 4-node, ie. not a word.  It may also
# happen this 4-alpha has a sub-alpha which is a 3-node, and that this
# 3-node does not occur under other 4-nodes.  In this case, pruning
# the tree, or simply pruning out non-4-nodes from the initial list
# before generating 3-alphas, would miss this 3-node.  

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
# if leaves1 is empty the there are no 2-4 edges in this case,
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

def do_example(alpha, n, m) :
    depth = m - n
    root = rootof(alpha, depth)
    print("Original Tree:\n")
    print(root)
    print("leaves which are nodes:")
    leaves1 = getlist(root, n)
    print(leaves1)
    root = prune_tree(root, not_word_node)
    print("\nTree after pruning:")
    print(root)    
    leaves2 = getlist(root, n)
    print("leaves after pruning which are nodes:")
    print(leaves2)
    leaves3 = prune_leaves(leaves1, leaves2)
    print("\nleaves which become n-m-edges:")
    print(leaves3)
    print("\n")

def do_example2(alpha, n, m) :
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
    # for depth 3, say n=2, m=5, we now have 3 layers of nodes:
    # 1) leaves: 2-nodes 
    # 2) 3-nodes 
    # 3) 4-nodes 
    # now need to check for edges from 2-nodes to any of the 3- or 4-nodes. 
    # if such an edge exists for a 2-node, it can be deleted from list
    # since it does not need a 2-5 edge.  This process can be done in a
    # cumulative way, eliminating more 2-nodes at each stage. 
    leaves1 = elim_leaves(leaves, nodes1)
    leaves2 = elim_leaves(leaves1, nodes2)
    print("leaves2:")
    print(leaves2)


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
        print(beta)
        root = rootof(beta, depth)
        leaves = getlist(root, n)
        print(leaves)
        depth -= 1
        root = rootof(beta, depth)
        nodes1 = getlist(root, n+1)
        print(nodes1)
        depth -= 1
        root = rootof(beta, depth)
        nodes2 = getlist(root, n+2)
        print(nodes2)
        leaves1 = elim_leaves(leaves, nodes1)
        leaves2 = elim_leaves(leaves1, nodes2)
        print(leaves2)
        # if leaves2 :
        #    print("non-empty!")
        for alpha in leaves2 :
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
# do_example2(alpha, n, m)
    

fill_edges(n,m)
write_edges(file, edges)

exit(0)

# Example: (This one has an interesting tree after pruning, only: root -> node -> node -> leaf
# 
# Original Tree:
# 
# AADDX
#   ADDX
#     DDX
#       DX
#       DD
#     ADX
#       DX
#       AX
#       AD
#     ADD
#       DD
#       AD
#   AADX
#     ADX
#       DX
#       AX
#       AD
#     AAX
#       AX
#       AA
#     AAD
#       AD
#       AA
#   AADD
#     ADD
#       DD
#       AD
#     AAD
#       AD
#       AA
# 
# leaves which are nodes:
# ['AX', 'AD', 'AA']
# 
# Tree after pruning:
# AADDX
#   AADD
#     ADD
#       AD
# 
# leaves after pruning which are nodes:
# ['AD']
# 
# leaves which become n-m-edges:
# ['AX', 'AA']
# 
# 
