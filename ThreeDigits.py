"""
Given two 3-digit numbers: a goal, a start
Given a set of 3-digit numbers: Forbidden states

Aim: We want to go from S -> G by adding or subtracting one digit e.g 953 -> 853

Constraints:
- Cant add to the digit 9
- Cant transform into a forbidden state
- Cant change the same digit twice in a row
"""
import sys, collections

forbidden = []

class Node:
    def __init__(self, state, parent, children, expanded_index):
        self.state = state
        self.parent = parent
        self.children = children
        self.expanded_index = expanded_index
    
    def get_state(self):
        return self.state
    
    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children
    
    def set_children(self, children):
        self.children = children

    def get_index(self):
        return self.expanded_index

    def set_index(self, expanded_index):
        self.expanded_index = expanded_index
    
    def generate_ancestors(self):
        ancestor = self
        while ancestor.get_parent() is not None:
            ancestor = ancestor.get_parent()
            yield ancestor.get_state()

    def get_ancestors(self):
        return list(self.generate_ancestors())
    
    def path_to_goal(self):
        path_to_goal = self.get_ancestors()
        path_to_goal = path_to_goal[::-1]
        path_to_str = ' '.join([str(elem) for elem in path_to_goal]) + " " + self.get_state()
        return path_to_str



def add_digit(state, index):
    """
    adds a digit based on the str state and int index given (0 or 1 or 2)
    """
    if state != None:
        new_digit = int(state[index]) + 1
        if state[index] == "9":
            return None
        elif index == 0: 
            state = str(new_digit) + state[1:]
        elif index == 1: 
            state = state[0] + str(new_digit) + state[-1]
        elif index == 2: 
            state = state[:2] + str(new_digit)
    else:
        return None
    
    if state not in forbidden:
        return state
    else:
        return None

def subtract_digit(state, index):
    """
    subtracts a digit based on int index given
    """
    if state != None:
        new_digit = int(state[index]) - 1
        if state[index] == "0":
            return None
        elif index == 0: 
            state = str(new_digit) + state[1:]
        elif index == 1: 
            state = state[0] + str(new_digit) + state[-1]
        elif index == 2: 
            state = state[:2] + str(new_digit)
    else:
        return None
    if state not in forbidden:
        return state
    else:
        return None

def expand_node(node_state, parent):
        """Expands node and adds the children to the tree""" 
        children = []
        if parent.get_index() != 0:
            children.append(Node(subtract_digit(node_state, 0),parent, None, 0))
            children.append(Node(add_digit(node_state, 0),parent, None, 0))
        if parent.get_index() != 1:
            children.append(Node(subtract_digit(node_state, 1),parent, None, 1))
            children.append(Node(add_digit(node_state, 1),parent, None, 1))
        if parent.get_index() != 2:
            children.append(Node(subtract_digit(node_state, 2),parent, None, 2))
            children.append(Node(add_digit(node_state, 2),parent, None, 2))
        children_not_none = []
        for node in children:
            if node.get_state() != None:
                if node.get_state() not in forbidden:
                    children_not_none.append(node)
        parent.set_children(children_not_none)
        return children_not_none

def get_expanded_states(expanded):
    states_expanded = [i.get_state() for i in expanded]
    states_expanded = [i for i in states_expanded if i] # Gets rid of none values
    expanded_to_str = ' '.join([str(elem) for elem in states_expanded])
    return expanded_to_str

def BFS(start, goal):
    fringe = []
    expanded = []
    # Create a dict for nodes to check there are no two same nodes
    exp_map = dict()
    # Init the root node and add to fringe
    root = Node(start, None, None, None)
    # Add root to the fringe
    fringe.append(root)

    goal_node = None
    while fringe and goal_node == None:
        # Loop through each node in fringe
        for current_node in fringe:
            # Ensure less than 1000 nodes are expanded
            if len(expanded) <= 1000:
                # Check if we have expanded this before and Check if it has the same children
                if current_node.get_state() in exp_map.keys() and current_node.get_index() == exp_map[current_node.get_state()]:
                    continue
                else:
                    # Expand the current node
                    generated_children = expand_node(current_node.get_state(), current_node)
                    gen_children_states = [child.get_state() for child in generated_children]
                    # Continue by adding the new node to expanded and new children to fringe
                    expanded.append(current_node)
                    exp_map[current_node.get_state()] = current_node.get_index()
                    # Check if current node is a goal node, break for loop and while condition == false
                    if current_node.get_state() == goal:
                        goal_node = current_node
                        break
                    # Add children to the fringe
                    for child in generated_children:
                        fringe.append(child) 
            else:
                print("No solution found.")
                return 
    if goal_node == None:
        print("No solution found.")
        return 
    else:
        print(goal_node.path_to_goal())
        print(get_expanded_states(expanded))
        return

if __name__ == "__main__":
    search = sys.argv[1]
    file_name = sys.argv[2]
    f = open(file_name, "r")
    start = f.readline().rstrip()
    goal = f.readline().rstrip()
    forbidden = f.readline().rstrip().split(",")
    f.close()

    if search == "B":
        BFS(start, goal)
    #elif search == "D":
        #DFS(start, goal)

