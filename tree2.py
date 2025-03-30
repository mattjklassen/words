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

def remove_i(alpha, i):
# Removes the character at the i-th index of a string.
  if not 0 <= i < len(alpha):
        raise IndexError("Index is out of bounds")
  return alpha[:i] + alpha[i+1:]

# Example usage
# word ALBA has node AABL
alpha = "AABL"

def level1(alpha):
    root = TreeNode(alpha)
    n = len(alpha)
    previous = ""
    for i in range(n):
        if alpha[i] != previous:
            new = remove_i(alpha, i)
            root.add_child(TreeNode(new))
        previous = alpha[i]
    print(root)        
    for j in range(len(root.children)):
        print(root.children[j])

level1(alpha)

exit(0)

root = TreeNode(alpha)

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


print(root)



