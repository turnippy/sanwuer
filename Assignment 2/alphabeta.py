# CISC352 Assignment 2
# AlphaBeta Pruning

import re as regex

# Node structure for tree
class node:

    # Types: 1 = max, -1 = min, 0 = leaf
    def __init__(self, type, val = None):
        self.children = []
        if type == 1:
            self.max = True
            self.leaf = False
            self.value = val
        elif type == -1:
            self.max = False
            self.leaf = False
            self.value = val
        else:
            self.max = False
            self.leaf = True
            self.value = float(val)

# Helper function to parse a single line of input into tree
def parse_line (string):
    
    # Create a list of all expressions in the form "(X,Y)", where
    # X and Y are alphanumeric expressions
    parsed = regex.findall(r"\(([A-Za-z0-9_]+),([A-Za-z0-9_]+)\)", string)
    if len(parsed) <= 1:
        print("\tThis tree has one or fewer nodes!")
    
    # The tree is implemented as a dict of key-node pairs
    # The root node is the first pair in the first input set
    tree = {}
    root = parsed[0][0]
    
    for p in parsed:
        if p[1] == "MAX":
            temp = node(1)
            tree[p[0]] = temp
        elif p[1] == "MIN":
            temp = node(-1)
            tree[p[0]] = temp
        elif p[1].isdigit():
            # Adds the leaf node to its parent
            temp = node(0, p[1])
            parent = tree[p[0]]
            parent.children.append(temp)
        else:
            # Update parent-child relationships
            parent = tree[p[0]]
            child = tree[p[1]]
            parent.children.append(child)
    
    #print(tree)
    print("\tTree successfully created...")
    return tree[root]

def alphabeta (current, alpha, beta):
    
    if current.leaf:
        #if node is leaf
        return current.value
    elif current.max:
        #if node is max
        best = float("-inf")
        for node in current.children:
            #check value of all children
            best = max(best, alphabeta(node, alpha, beta))
            #update alpha if necessary
            alpha = max(alpha, best)
            
            #prune the remaining children if appropriate
            if alpha >= beta:
                return best
    else:
        #if node is min
        best = float("inf")
        for node in current.children:
            #check value of all children
            best = min(best, alphabeta(node, alpha, beta))
            #update beta if necessary
            beta = min(alpha, best)
            
            #prune the remaining children if appropriate
            if beta <= alpha:
                return best
            
    

if __name__ == "__main__":

    print("Starting minimax evaluation with alpha-beta pruning...\n")

    with open("alphabeta.txt", "r") as input:
        input_lines = input.readlines()
        
    print("Input file okay.")
    print("Processing file...\n")
    
    n = 1
    for line in input_lines:
        print("\tParsing line %d in input file..." %(n))
        root = parse_line(line)
        solution = alphabeta(root, float("-inf"), float("inf"))
        print("\tEvaluation for line %d found!" %(n))
        n += 1
        
    print("\nAll inputs processed, writing output to file...")
    print("Output file okay.\nAll done!")