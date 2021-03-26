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

def BFS(start, goal):
    fringe = []
    expanded = []
    count = 0
    root = Node(start, None, None, None)
    fringe.append(root)
    expanded.append(root)
    generated_children = expand_node(start, root)
    
    for child in generated_children:
        count = count + 1
        fringe.append(child)

    goal_node = None
    goal_not_found = True
    while fringe and goal_not_found:
        s = fringe.pop(0)
        #print(s.get_state(), end = " ")
        for i in fringe:
            if count < 1000:
                generated_children = expand_node(i.get_state(), i)
                expanded_children = []
                for exp in expanded:
                    expanded_children.append(exp.get_children())
                if i.get_children() not in expanded_children:
                    if i not in expanded:
                        #s = fringe.pop(0)
                        expanded.append(i)
                        if i.get_state() == goal:
                            goal_not_found = False
                            goal_node = i
                            break
                        for child in generated_children:
                            count = count + 1
                            fringe.append(child)
            else:
                print(count)
                print("No solution found.")
                return

    path_to_goal = []
    root_not_found = True
    current_node = goal_node
    while root_not_found:
        if current_node == None:
            break
        else:
            path_to_goal.append(current_node.get_state())
            current_node = current_node.get_parent()
            if current_node == None:
                break
            else:
                path_to_goal.append(current_node.get_state())
                if current_node.get_state() == start:
                    root_not_found = False
                    break
                else:
                    current_node = current_node.get_parent()

    states_expanded = []
    for i in expanded:
        states_expanded.append(i.get_state())
    states_expanded = [i for i in states_expanded if i]
    path_to_goal = path_to_goal[::-1]
    path_to_str = ' '.join([str(elem) for elem in path_to_goal])
    expanded_to_str = ' '.join([str(elem) for elem in states_expanded])
    print(path_to_str)
    print(expanded_to_str)
    return path_to_goal, states_expanded

    
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
    

