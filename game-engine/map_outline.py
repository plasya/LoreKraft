from collections import deque
import random
import string
from map_gen_assistant import generate_dnd_map


##### test case
d, start_end_dict = generate_dnd_map("Pureblood and darkknight reluctantly join up against goblins and dragons", 10)
start = start_end_dict['start'] 
end = start_end_dict['end']     

# Define the Node class for creating nodes in the map
class Node:
    def __init__(self, name: str, node_id: int):
        self.name = name
        self.id = node_id
        self.next_nodes = []  # List of pointers to next nodes
        self.prev_nodes = []  # List of pointers to previous nodes
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

# Function to generate random numbers for the number of events
def generate_random_numbers(num_max):
    n_common = random.randint(num_max - 2, num_max + 6)
    n_triggers = random.randint(1, num_max // 4)
    n_friendly = random.randint(1, num_max // 3)
    n_delayed = random.randint(0, num_max)

    delayed_numbers = [random.randint(1, 3) for _ in range(n_delayed)]
    return n_common, n_triggers, n_friendly, n_delayed, delayed_numbers

# Helper function to generate random ID for each node
def random_gen_id(k=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=k))

# Define the Map class to represent the DND map
class Map:
    def __init__(self, d, start, end, n_common, n_triggers, n_friendly, n_delayed, delayed_numbers):
        # Creating nodes for each location in the map
        list_of_nodes = {key: Node(key, random_gen_id()) for key, val in d.items()}
        self.test = list_of_nodes
        self.head = list_of_nodes[start]
        self.tail = list_of_nodes[end]
        self.isvisited = {start: 1}

        # Linking nodes based on the map structure
        for key, val in d.items():
            for v in val:
                list_of_nodes[key].next_nodes.append(list_of_nodes[v])
                list_of_nodes[v].prev_nodes.append(list_of_nodes[key])

        
        list_of_n = list(list_of_nodes.keys())
        for i in random.choices(list_of_n, k=n_common):
            if i != self.head and i != self.tail:
                list_of_nodes[i].events['common'].append('event')
        for i, e in enumerate(random.choices(list_of_n, k=n_delayed)):
            if e != self.head and e != self.tail:
                list_of_nodes[e].events['delayed'][f'event_{random_gen_id(4)}'] = delayed_numbers[i]
        for i in random.sample(list_of_n, n_triggers):
            if i != self.head and i != self.tail:
                list_of_nodes[i].events['trigger'] = True
        for i in random.sample(list_of_n, n_friendly):
            if i != self.head and i != self.tail:
                list_of_nodes[i].events['friendly'] = True
        # Adding events to nodes based on random selections
        self.head.events['common'] = ['start the journey event']  # Modify prompt
        self.tail.events['common'] = ['end the journey event']    # Modify prompt
        self.head.events['delayed'] = {}
        self.tail.events['delayed'] = {}
        self.head.events['trigger'] = False
        self.head.events['friendly'] = False
        self.tail.events['trigger'] = False
        self.tail.events['friendly'] = False



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
        if node_name == self.head.name:
            return 0  # If the node is the head, its depth is 0

        queue = deque([(self.head, 0)])  # Queue stores (node, depth) pairs
        visited = set([self.head.name])

        while queue:
            current_node, depth = queue.popleft()

            for neighbor in current_node.next_nodes:
                if neighbor.name not in visited:
                    if neighbor.name == node_name:
                        return depth + 1  # Return the depth when node is found
                    visited.add(neighbor.name)
                    queue.append((neighbor, depth + 1))

        return -1  # Return -1 if the node is not found in the map

    # def print_map(self):
    #     for i in self.test.values():
    #         print(i)
    #         print('===========================')

# Function to create a new map with random events
def create_new_map(d, start, end):
    n_common, n_triggers, n_friendly, n_delayed, delayed_numbers = generate_random_numbers(len(d))
    return Map(d, start, end, n_common, n_triggers, n_friendly, n_delayed, delayed_numbers)

m = create_new_map(d, start = start, end = end)

def map_to_dict(map_obj):
    map_dict = {}
    for node_name, node_obj in map_obj.test.items():
        map_dict[node_name] = {
            'next_nodes': [n.name for n in node_obj.next_nodes],
            'events': node_obj.events
        }
    return map_dict
# Main function to create and simulate the map


def main():
    # Generate a new DND map with the theme and checkpoints
    m = create_new_map(d, start=start, end=end)
    # print(m.print_map())
    print(map_to_dict(m))
# Run the main function
if __name__ == "__main__":
    main()

