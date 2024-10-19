from collections import deque
import random
import string

def generate_random_numbers(num_max):
    """Generates 4 random numbers: n_common, n_triggers, n_friendly, and n_delayed.

    Args:
    num_max: The maximum value for the random numbers.

    Returns:
    A tuple of 4 random numbers: (n_common, n_triggers, n_friendly, n_delayed).
    """

    n_common = random.randint(num_max - 2, num_max + 6)
    n_triggers = random.randint(1, num_max // 4)
    n_friendly = random.randint(1, num_max // 3)
    n_delayed = random.randint(0, num_max)

    delayed_numbers = []
    for _ in range(n_delayed):
        delayed_numbers.append(random.randint(1, 3))

    return n_common, n_triggers, n_friendly, n_delayed, delayed_numbers

def random_gen_id(k=10):
    # Define the characters to choose from: digits and letters
    characters = string.ascii_letters + string.digits
    # Generate a random 10-character alphanumeric string
    gen_id = ''.join(random.choices(characters, k=k))
    return gen_id

class Node:
    def __init__(self, name, _id):
        self.name = name
        self._id = _id
        self.next_nodes = []
        self.prev_nodes = []
        self.events = {
            'common': [],
            'delayed': {},
            'trigger': False,
            'friendly': False
        }
    def __repr__(self):
        return f'{self.name} has {len(self.next_nodes)} paths ahead and has events \n {self.events}'
    
    def __str__(self):
        return f'{self.name} has {len(self.next_nodes)} paths ahead and has events \n {self.events}'
    
class Map:
    def __init__(self, d, start, end, n_common, n_triggers, n_friendly, n_delayed, delayed_numbers):
        list_of_nodes = {key: Node(key, random_gen_id()) for key, val in d.items()}
        self.test = list_of_nodes
        self.head = list_of_nodes[start]
        self.tail = list_of_nodes[end]
        for key, val in d.items():
            for v in val:
                list_of_nodes[key].next_nodes.append(list_of_nodes[v])
                list_of_nodes[v].prev_nodes.append(list_of_nodes[key])
        self.isvisited = {start:1}
        
#         n_common, n_triggers, n_friendly, n_delayed, delayed_numbers
        
        self.head.events['common'] = ['start the journey event'] # modify prompt
        self.tail.events['common'] = ['end the journey event'] # modify prompt
        
        list_of_n = list(list_of_nodes.keys())
        for i in random.choices(list_of_n, k=n_common):
            if i != self.head and i!= self.tail:
                list_of_nodes[i].events['common'].append('event')
        for i,e in enumerate(random.choices(list_of_n, k=n_delayed)):
            if e != self.head and e != self.tail:
                list_of_nodes[e].events['delayed'][f'event_{random_gen_id(4)}'] = delayed_numbers[i]
        for i in random.sample(list_of_n, n_triggers):
            if i != self.head and i!= self.tail:
                list_of_nodes[i].events['trigger'] = True
        for i in random.sample(list_of_n, n_friendly):
            if i != self.head and i!= self.tail:
                list_of_nodes[i].events['friendly'] = True
            
    def visit_node(self, name):
        self.isvisited[name] = 1
    
    def list_visited_nodes(self):
        return list(self.isvisited.keys())
    
    def BFS(self):
        queue = deque([self.head])  # Start with the head node
        visited = set([self.head.name])  # Track visited nodes by name
        traversal = []  # List to store the BFS order
        
        while queue:
            current_node = queue.popleft()  # Get the node at the front of the queue
            traversal.append(current_node.name)  # Add to traversal order
            self.visit_node(current_node.name)  # Mark as visited
            
            # Explore the next nodes
            for neighbor in current_node.next_nodes:
                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    queue.append(neighbor)
        
        return traversal  # Return the BFS traversal order
    
    def calc_depth(self, node_name):
        """
        Calculates the depth of a node by name starting from the head (root).
        The depth is the number of edges from the head node to the target node.
        """
        if node_name == self.head.name:
            return 0  # If the node is the head, its depth is 0

        queue = deque([(self.head, 0)])  # Queue stores (node, depth) pairs
        visited = set([self.head.name])  # Track visited nodes

        while queue:
            current_node, depth = queue.popleft()

            # Explore the next nodes
            for neighbor in current_node.next_nodes:
                if neighbor.name not in visited:
                    if neighbor.name == node_name:
                        return depth + 1  # Return the depth when node is found
                    visited.add(neighbor.name)
                    queue.append((neighbor, depth + 1))

        return -1  # Return -1 if the node is not found in the map
    
    def print_map(self):
        for i in self.test.values():
            print(i)
            print('===========================')