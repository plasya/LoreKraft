#python
class Node:
    def __init__(self, key, image):
        self.key = key       # Key for the node
        self.image = image   # Image data (e.g., file path)
        self.next = None     # Pointer to the next node
        self.prev = None     # Pointer to the previous node

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, key, image):
        new_node = Node(key, image)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last

    def delete(self, key):
        current = self.head
        while current:
            if current.key == key:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                return
            current = current.next

    def display(self):
        current = self.head
        while current:
            print(f"Key: {current.key}, Image: {current.image}")
            current = current.next
