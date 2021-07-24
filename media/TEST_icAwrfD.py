class Node(object):
    def __init__(self,data):
        self.data = data
        self.left = self.right = None

class BTS(object):
    def __init__(self):
        self.root = None

    def insert(self,data):
        self.root = self._insert_value(self.root,data)
        return self.root is not None

    def _insert_value(self,node,data):
        if node is None:
            node = Node(data)
        else:
            if data <= node.data:
                node.left = self._insert_value(node.left,data)
            else:
                node.right = self._insert_value(node.right,data)
        return node

    def delete(self,key):
        self.root, deleted = self._delete_value(self.root,key)
        return deleted

    def _delete_value(self,node,key):
        if node is None:
            return node,False

        delete = False
        if key == node.data: #키값 맞는게 있으면
            deleted = True
            if node.left and node.right:
                parent,child = node,node.left
                while child.right is not None:
                    parent, child = child,child.right
                child.right = node.right

                if parent != node:
                    parent.right = child.left
                    child.left = node.left
                node = child
            elif node.left or node.right:
                node = node.left or node.right
            else:
                node = None
        elif key < node.data:
            node.left,deleted = self._delete_value(node.left,key)
        else:
            node.right,deleted = self._delete_value(node.right,key)
        return node,deleted

    def level_order_traversal(self,num,type):
        def _level_order_traversal(root):
            queue=[root]
            dep = [1]
            leafArr=[]
            while(queue):
                root = queue.pop(0)
                depth = dep.pop(0)
                if root is not None:
                    if depth == num and type == "depth":
                        print(root.data)
                    if root.left:
                        queue.append(root.left)
                        dep.append(depth+1)
                    if root.right:
                        queue.append(root.right)
                        dep.append(depth+1)
                    if root.left is None and root.right is None:
                        leafArr.append(root.data)

            if type == "leaf":
                for i in leafArr:
                    print(i,end=' ')
                print()
        _level_order_traversal(self.root)


bst = BTS()
N = int(input())
while N > 0:
    N = N-1
    str = input().split()
    if str[0] == "+":
        bst.insert(str[1])
    elif str[0] == "-":
        bst.delete(str[1])
    elif str[0] == "leaf":
        bst.level_order_traversal(0,str[0])
    else:
        bst.level_order_traversal(int(str[1]),str[0])





