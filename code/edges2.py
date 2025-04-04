# this version will do difference of 2 between n and m

import sys

print("Argument List:", str(sys.argv))
args = len(sys.argv)

nstr = sys.argv[1]
n = int(nstr)
        
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        ret = "  " * level + str(self.data) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret
    
    def remove_child(self, child_node):
        self.children = [child for child in self.children if child != child_node]

def import_alphas(file):
    alphas = []
    with open(file, 'r') as f:
        alphas = f.readlines()
        f.close()
    n = len(alphas)
    for i in range(n):
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
# need to work with nodes for n, n+1, and n+2 so that we can determine
# if an edge from n to n+2 should exist by checking if a path already
# exists of type n -> n+1 -> n+2.  

# First case is 2-4-edges. (n = 2)

# We will use tree with top node equal to one 4-node, then children are
# 3-alphas (constructed by removing one char from 4-node) and below
# those 2-alphas constructed similarly.  The leaves of this tree of depth
# 2 are potential 2-nodes that could give a 2-4 path to the 4-node.
# A leaf fails to be in a 2-4-edge if it is not a 2-node, or if it is a
# 2-node but there exists a 2-3-4 path from this 2-node to the 4-node.

# We create a list of unique 2-alphas from the leaves, then delete any
# 2-alphas which are not 2-nodes.  Then we prune the tree of any non-nodes
# meaning 2-alphas or 3-alphas in this tree which are not 2-nodes or 3-nodes
# in the context of the bigger alpha-graph, meaning they do not have an
# associated permutation which is a word.

# Finally, we check each 2-node to see if it is a leaf in the pruned tree.
# If it is not, then it becomes a 2-4-edge.

# example 1:  AIIX (word IXIA) is a 4-node which has 3 2-4 edges below it.
#           Below is the tree and the pruned list.  Note that none of the
#           3-alphas IIX, AIX, and AII are 3-nodes.  So each of the 2-nodes
#           IX, AX, and AI give 2-4 edges: IX -> AIIX, AX -> AIIX, AI -> AIIX.
# AIIX
#   IIX
#     IX
#     II
#   AIX
#     IX
#     AX
#     AI
#   AII
#     II
#     AI
# 
# ['IX', 'AX', 'AI']
# 
# After forming the list of 2-nodes, we do the pruning of the tree, which in
# this case becomes only the root.
        
# example 2:  ABDR (word BARD +3) is a 4-node which has no 2-4 edges below it.
#           Below is the tree and the pruned list.  Note that three of the
#           3-alphas ADR, ABR, and ABD are 3-nodes, and one BDR is not.  
# ABDR
#   BDR
#     DR
#     BR
#     BD
#   ADR
#     DR
#     AR
#     AD
#   ABR
#     BR
#     AR
#     AB
#   ABD
#     BD
#     AD
#     AB
# 
# ['AR', 'AD', 'AB']
# 
#           After pruning the tree of non-3-nodes and non-2-nodes, we can
#           see that the leaves still contain each 3-node in the list. So
#           no 2-4 edges are formed.
#
# Tree after pruning:
# 
# ABDR
#   ADR
#     AR
#     AD
#   ABR
#     AR
#     AB
#   ABD
#     AD
#     AB
#
# example 3: BEIX (IBEX)     
# Original Tree:
#
# BEIX
#   EIX
#     IX
#     EX
#     EI
#   BIX
#     IX
#     BX
#     BI
#   BEX
#     EX
#     BX
#     BE
#   BEI
#     EI
#     BI
#     BE
# 
# ['IX', 'EX', 'BI', 'BE']
# 
# Tree after pruning:
# BEIX
# 
# []
#
# So here we find that there are 4 2-4-edges for each of IX, EX, BI, BE.


file1 = nstr + "nodes.txt"
nodes1 = import_alphas(file1)
n1 = len(nodes1)

m = n + 1
file2 = str(m) + "nodes.txt"
nodes2 = import_alphas(file2)
n2 = len(nodes2)

m = n + 2
file3 = str(m) + "nodes.txt"
nodes3 = import_alphas(file3)
n3 = len(nodes3)

# Note: for 2-4 edges, use n = 2, so then
# nodes1 is array of 2-nodes
# nodes2 is array of 3-nodes
# nodes3 is array of 4-nodes

# initialize edges array:
edges = []
for i in range(n1):
    edges.append(nodes1[i] + ";")

file = nstr + "-" + str(m) + "-" + "edges.txt"

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

# forms alphas of length k-1 from alpha of length k by removing one char
def subalphas(alpha):
    k = len(alpha)
    subs = []
    previous = ""
    for i in range(k):
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

# form tree from alpha, with redundant nodes, depth of 2
def rootof(alpha) :
    root = TreeNode(alpha)
    n = len(alpha)
    previous = ""
    for i in range(n) :
        if alpha[i] != previous :
            new = remove_i(alpha, i)
            root.add_child(TreeNode(new))
        previous = alpha[i]
    for j in range(len(root.children)) :
        child = root.children[j]
        alpha = child.data
        m = len(alpha)
        previous = ""
        for i in range(m) : 
            if alpha[i] != previous :
                new = remove_i(alpha, i)
                child.add_child(TreeNode(new))
            previous = alpha[i]
    return root        

# getlist finds all leaves on tree built from rootof(alpha), depth 2,
# with dups deleted and only 2-nodes.

def getlist(root) :
    leaves = []
    n = len(root.children)
    for i in range(n) :
        child = root.children[i]
        m = len(child.children)
        for j in range(m) :
            leaf = child.children[j].data
            found_dup = 0
            is_node = 0
            # now exclude dups and non-2-nodes 
            if is_word(leaf, nodes1) :
                is_node = 1
            for beta in leaves :
                if leaf == beta :
                    found_dup = 1
            if found_dup == 0 and is_node == 1 :
                leaves.append(leaf)
    return leaves 
                    
def prune_tree(node, condition):
    """
    Recursively traverses the tree and removes nodes that meet the given condition.
    :param node: The root of the tree or subtree
    :param condition: A function that takes a node and returns True if it should be removed
    :return: The modified node (or None if it should be removed)
    """
    # Base case: If the current node should be removed, return None
    if is_word_node(node):
        return None
    # Recursively filter children
    new_children = []
    for child in node.children:
        updated_child = prune_tree(child, is_word_node)
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

# this function refers to global int n
def is_word_node(node):
    alpha = node.data
    k = len(alpha)
    if k == n :
        return not is_word(alpha, nodes1)
    if k == n + 1 :
        return not is_word(alpha, nodes2)
    if k == n + 2 :
        return not is_word(alpha, nodes3)
    return 0

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

def do_example(alpha) :
    root = rootof(alpha)
    print("Original Tree:\n")
    print(root)
    print("leaves which are nodes:")
    leaves1 = getlist(root)
    print(leaves1)
    root = prune_tree(root, is_word_node)
    print("\nTree after pruning:")
    print(root)    
    leaves2 = getlist(root)
    print("leaves after pruning which are nodes:")
    print(leaves2)
    leaves3 = prune_leaves(leaves1, leaves2)
    print("\nleaves which become n-m-edges:")
    print(leaves3)
    print("\n")

alpha = "UUYZ"
do_example(alpha)
    
def fill_edges() :
    for i in range(len(nodes3)) :
        beta = nodes3[i]
        root = rootof(beta)
        leaves1 = getlist(root)
        root = prune_tree(root, is_word_node)
        leaves2 = getlist(root)
        leaves3 = prune_leaves(leaves1, leaves2)
        for alpha in leaves3 :
            index = iof_word(alpha, nodes1)
            if index > -1 :
                edge = remains(alpha, beta)
                if edges[index][-1] == ";" :
                    edges[index] += edge
                else :
                    edges[index] += "," + edge 

# fill_edges()

# write_edges(file, edges)

exit(0)

# Example:  A very lonely edge!  The 2-4 edge UY --> UUYZ has no other paths passing through or around it!
#           This means that any other path from UY will never hit UUYZ, and no other path from a 3-node
#           passes through UUYZ, and further, UUYZ has only one path exiting from it (up to higher k-nodes)
#           which is its plural UUSYZ = YUZUS.
#           Note:  YUZU = (Japanese) a type of citrus fruit.
#
# Original Tree:
# 
# UUYZ
#   UYZ
#     YZ
#     UZ
#     UY
#   UUZ
#     UZ
#     UU
#   UUY
#     UY
#     UU
# 
# leaves which are nodes:
# ['UY']
# 
# Tree after pruning:
# UUYZ
# 
# leaves after pruning which are nodes:
# []
# 
# leaves which become n-m-edges:
# ['UY']
# 
# 
