class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

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

def prune_tree(node, condition):
    if node is None:
        return None
    
    node.children = [prune_tree(child, condition) for child in node.children]
    node.children = [child for child in node.children if child is not None]
    
    if condition(node) and not node.children:
        return None
    
    return node

def print_tree(node, indent=0):
    if node:
        print("  " * indent + str(node.data))
        for child in node.children:
            print_tree(child, indent + 1)

def remove_i(alpha, i):
# Removes the character at the i-th index of a string.
  if not 0 <= i < len(alpha):
        raise IndexError("Index is out of bounds")
  return alpha[:i] + alpha[i+1:]

def make_tree(alpha, depth):
    # alpha is string of length n,  depth is number of levels down
    # so depth = 1 means top node has len n, leaves are alphas of len n-1 
    n = len(alpha)
            




# Example Usage
# word ALBA has node AABL
root = TreeNode('AABL')
child_aab = TreeNode('AAB')
child_aal = TreeNode('AAL')
child_abl = TreeNode('ABL')

root.add_child(child_aab)
root.add_child(child_aal)
root.add_child(child_abl)

child_aa = TreeNode('AA')
child_ab = TreeNode('AB')
child_al = TreeNode('AL')
child_bl = TreeNode('BL')

child_aab.add_child(child_aa)
child_aab.add_child(child_ab)
child_aal.add_child(child_aa)
child_aal.add_child(child_al)
child_abl.add_child(child_ab)
child_abl.add_child(child_al)
child_abl.add_child(child_bl)



# Condition to prune nodes with even data values
def is_even(node):
  return node.data % 2 == 0

print("Original Tree:")
print_tree(root)

pruned_tree = prune_tree(root, is_even)

print("\nPruned Tree (even nodes without children removed):")
print_tree(pruned_tree)


