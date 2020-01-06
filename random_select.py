from random import randint

def random_weighted_select(items, limit):
    """
    Generates a new list of items with a preference
    towards items near the beginning of the list

    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Better solution is to initialize weights into a BST,
    which has O(log n) time and O(n) space

    For the scope/simplicity of this intended project,
    we're going with the linear and simpler one
    """
    size = len(items)
    limit = limit if limit < size else size

    # generate inversely linear weights
    # ex: items = ['a', 'b', 'c']
    #     itemWeights = { 'a' : 3, 'b': 2, 'c': 1 }
    itemWeights = { item : size - i for i, item in enumerate(items) }
    totalWeight = size * (size + 1) / 2
    items = LinkedList(items)

    item = items.next()
    new_list = list()
    for it in range(limit):
        randWeight = randint(0, total)

        subtotal = itemWeights[items[0]]
        i = 0
        while subtotal < randWeight:
            i += 1
            subtotal += itemWeights[items[i]]

        new_list.append(items[i])
        totalWeight -= itemWeights[items[i]]
        del items[i]

    return new_list


class Node:
    def __init_(self, val, next=None):
        self.val = val
        self.next = None

    def add(self, node):
        self.next = node


class LinkedList:
    def __init__(self, list=None):
        self.head = None
        self.tail = None
        self.cur = None

        for val in list:
            self.add(val)

    def add(self, val):
        node = Node(val)

        if self.head is None:
            self.head = node
            self.cur = node
        else:
            self.tail.add(node)

        self.tail = node

    def remove(self, node):
        next = node.next

        if next is not None:
            node.val = next.val
            node.next = next.next
        else:
            node = None

    def next(self):
        val = None
        
        if self.cur is not None:
            val = self.cur.val
            self.cur = self.cur

        return val

    def getHead(self):
        self.cur = self.head
        return self.head.val
