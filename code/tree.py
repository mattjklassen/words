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

# Example usage
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


print(root)



