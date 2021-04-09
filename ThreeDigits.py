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
    def __init__(self, state, parent, children, expanded_index, depth, h):
        self.state = state
        self.parent = parent
        self.children = children
        self.expanded_index = expanded_index
        self.depth = depth
        self.h = h
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
    
    def get_depth(self):
        return self.depth
    
    def get_h(self):
        return self.h
    
    def set_h(self, h):
        self.h = h



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
    return state


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
    return state
    

def expand_node(node_state, parent):
        """Expands node and adds the children to the tree""" 
        children = []
        if parent.get_index() != 0:
            children.append(Node(subtract_digit(node_state, 0),parent, None, 0, parent.get_depth() + 1, 0))
            children.append(Node(add_digit(node_state, 0),parent, None, 0, parent.get_depth() + 1, 0))
        if parent.get_index() != 1:
            children.append(Node(subtract_digit(node_state, 1),parent, None, 1, parent.get_depth() + 1, 0))
            children.append(Node(add_digit(node_state, 1),parent, None, 1, parent.get_depth() + 1, 0))
        if parent.get_index() != 2:
            children.append(Node(subtract_digit(node_state, 2),parent, None, 2, parent.get_depth() + 1, 0))
            children.append(Node(add_digit(node_state, 2),parent, None, 2, parent.get_depth() + 1, 0))
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
    # Create a dict for nodes to check there are no two same nodes (state:index)
    exp_map = dict()
    # Init the root node as the current node
    current_node = Node(start, None, None, None, 0)
    while current_node.get_state() != goal:
        # Add the current node to expanded
        expanded.append(current_node)
        # Now we generate the children for the current node
        generated_children = expand_node(current_node.get_state(), current_node)
        # Ensure the length of the expanded list is less than 1000
        if len(expanded) <= 1000:
            # Add the current node to the expanded dict
            # Check if that state has already been in the dict
            if current_node.get_state() in exp_map.keys():
                # We need to add to the list of values for the same state key
                exp_map[current_node.get_state()].append(current_node.get_index())
            else:
                # Havent expanded that state before make a list just incase of mulitple similar states
                exp_map[current_node.get_state()] = []
                exp_map[current_node.get_state()].append(current_node.get_index())
            # Add the new child nodes to the fringe
            fringe += generated_children
            # Find next node to expand
            for node in fringe:
                # Check the node has been expanded already using the dict
                if node.get_state() in exp_map.keys() and node.get_index() in exp_map[node.get_state()]:
                    del node
                else:
                    # New node is now the current node
                    current_node = node
                    del node
                    break
        else:
            print("No solution found.")
            return
    # for k, v in exp_map.items():
    #     print(k, v)

    # If we find the goal node
    goal_node = current_node
    expanded.append(goal_node)
    print(goal_node.path_to_goal())
    print(get_expanded_states(expanded))
    return

def DFS(start, goal):
    fringe = []
    expanded = []
    # Create a dict for nodes to check there are no two same nodes (state:index)
    exp_map = dict()
    # Init the root node as the current node
    current_node = Node(start, None, None, None, 0)
    while current_node.get_state() != goal:
        # Add the current node to expanded
        expanded.append(current_node)
        # Now we generate the children for the current node
        generated_children = expand_node(current_node.get_state(), current_node)
        # Ensure the length of the expanded list is less than 1000
        if len(expanded) <= 1000:
            # Add the current node to the expanded dict
            # Check if that state has already been in the dict
            if current_node.get_state() in exp_map.keys():
                # We need to add to the list of values for the same state key
                exp_map[current_node.get_state()].append(current_node.get_index())
            else:
                # Havent expanded that state before make a list just incase of mulitple similar states
                exp_map[current_node.get_state()] = []
                exp_map[current_node.get_state()].append(current_node.get_index())          
            # Add the new child nodes to the fringe
            fringe[:0] = generated_children
            for node in fringe:
                # Check the node has been expanded already using the dict
                if node.get_state() in exp_map.keys() and node.get_index() in exp_map[node.get_state()]:
                    del node
                else:
                    # New node is now the current node
                    current_node = node
                    del node
                    break
        else:
            print("No solution found.")
            return
    # If we find the goal node
    goal_node = current_node
    expanded.append(goal_node)
    print(goal_node.path_to_goal())
    print(get_expanded_states(expanded))
    return

def calc_heurstic(current_node, goal):
    h = 0
    for i in range(3):
        h += abs(int(current_node.get_state()[i]) - int(goal[i]))
    current_node.set_h(h)
    return h

def add_child_to_fringe(child, fringe):
    for i in range(len(fringe)):
        if fringe[i].get_h() >= child.get_h():
            fringe.insert(i, child)
            break
    else:
        fringe.append(child)

def greedy(start, goal):
    fringe = []
    expanded = []
    # Create a dict for nodes to check there are no two same nodes (state:index)
    exp_map = dict()
    # Init the root node as the current node
    current_node = Node(start, None, None, None, 0, 0)
    # Calculate h for root
    calc_heurstic(current_node, goal)
    while current_node.get_state() != goal:
        # Add the current node to expanded
        expanded.append(current_node)
        # Now we generate the children for the current node
        generated_children = expand_node(current_node.get_state(), current_node)

        # Generate heuristc for child nodes
        for i in generated_children:
            calc_heurstic(i,goal)


        

        # Ensure the length of the expanded list is less than 1000
        if len(expanded) <= 10:
            # Add the current node to the expanded dict
            # Check if that state has already been in the dict
            if current_node.get_state() in exp_map.keys():
                # We need to add to the list of values for the same state key
                exp_map[current_node.get_state()].append(current_node.get_index())
            else:
                # Havent expanded that state before make a list just incase of mulitple similar states
                exp_map[current_node.get_state()] = []
                exp_map[current_node.get_state()].append(current_node.get_index())
            
            # Add the new child nodes to the fringe
            for i in generated_children:
                add_child_to_fringe(i, fringe)                    
                        
            # Find next node to expand
            for node in fringe:
                # Check the node has been expanded already using the dict
                if node.get_state() in exp_map.keys() and node.get_index() in exp_map[node.get_state()]:
                    del node
                else:
                    # New node is now the current node
                    current_node = node
                    del node
                    break
        else:
            print([child.get_state() for child in expanded])
            print("No solution found.")
            return
    # for k, v in exp_map.items():
    #     print(k, v)

    # If we find the goal node
    goal_node = current_node
    expanded.append(goal_node)
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
    elif search == "D":
        DFS(start, goal)
    # elif search == "I":
    #     IDS(start, goal, 0)
    elif search == "G":
        greedy(start, goal)
    # elif search == "A":
    #     A_star(start, goal)
    # elif search == "H":
    #     hill_climbing(start, goal)

    # parent = Node("320", None, None, None, 0, 0)
    # current_node = Node("220", None, None, None, 0, 0)

    # print(calc_heurstic(parent, current_node))



