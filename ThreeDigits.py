"""
Given two 3-digit numbers: a goal, a start
Given a set of 3-digit numbers: Forbidden states

Aim: We want to go from S -> G by adding or subtracting one digit e.g 953 -> 853

Constraints:
- Cant add to the digit 9
- Cant transform into a forbidden state
- Cant change the same digit twice in a row
"""
import sys, numpy as np

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
        children = [i for i in children if i] #removes none values
        parent.set_children(children)
        return children

def get_exapnded_states(expanded):
    states_expanded = [i.get_state() for i in expanded]
    states_expanded = [i for i in states_expanded if i] # Gets rid of none values
    expanded_to_str = ' '.join([str(elem) for elem in states_expanded])
    return expanded_to_str

def BFS(start, goal):
    fringe = []
    expanded = []
    exp_map = dict() # Maps expanded nodes with children for the checking process
    root = Node(start, None, None, None)
    fringe.append(root)
    expanded.append(root)
    generated_children = expand_node(start, root)
    exp_map[root.get_state()] = [i.get_state() for i in generated_children]
    for child in generated_children:
        fringe.append(child)
    goal_node = None
    goal_not_found = True
    while fringe and goal_not_found:
        s = fringe.pop(0)
        for i in fringe:
            if len(expanded) <= 1000:
                if i not in expanded and i not in exp_map.keys():
                    generated_children = expand_node(i.get_state(), i)

                    # Check if any child nodes are the same
                    if [child.get_state() for child in generated_children] not in exp_map.values():
                        expanded.append(i)
                        exp_map[i.get_state()] = [i.get_state() for i in generated_children]
                        if i.get_state() == goal:
                            goal_not_found = False
                            goal_node = i
                            break
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
        print(get_exapnded_states(expanded))
        return goal_node.path_to_goal(), get_exapnded_states(expanded)

    
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
    

