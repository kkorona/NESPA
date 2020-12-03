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
        if key == node.data:
            deleted = True
            if node.left and node.right:
                parent,child = node,node.right
                while child.left is not None:
                    parent, child = child,child.left
                child.left = node.left
                if parent != node:
                    parent.left = child.right
                    child.right = node.right
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
            queueTemp=[root]
            queue=[]
            depTemp = [1]
            dep = [1]
            MaxDepth = 1
            while(queueTemp):
                root = queueTemp.pop(0)
                depth = depTemp.pop(0)
                if depth > MaxDepth:
                    MaxDepth = depth
                if root is not None:
                    if depth == num and type == "depth":
                        print(root.data)
                    if root.left:
                        queueTemp.append(root.left)
                        queue.append(root.left.data)
                        depTemp.append(depth+1)
                        dep.append(depth + 1)
                    if root.right:
                        queueTemp.append(root.right)
                        queue.append(root.right.data)
                        depTemp.append(depth+1)
                        dep.append(depth+1)

            dep.reverse()
            queue.reverse()

            for i in range(0,len(queue)):
                if dep[i] == MaxDepth:
                    print(queue[i])


        _level_order_traversal(self.root)

array = ["pizza","banana","Hosting","Hello","zero","zi","absord","count","unistd","zy"]

bst = BTS()


for x in array:
    bst.insert(x)

print(bst.find("pizza")) #True
print(bst.find("baaaaa"))#false

bst.level_order_traversal(4,"depth")

