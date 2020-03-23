#Solution for CISC352 Assignment 2 Part 1 by group 8.
#This program implement Astar algorithm as well as greedy algorithm to perform
#path search.

import math

"""Node class represent each node that is being seached or has been searched

Attributes:
  parent: The parent node of this current node
  x, y: Denotes the vertical, horizontal coordinates of this node
  distance: The actual cost of this node(heuristic value is not considered for this value)

"""
class Node:

    def __init__(self, parent, x, y, distance):
        self.parent = parent
        self.x = x
        self.y = y
        self.distance = distance

"""pathfind class is the main algorithm of search

Attributes:
  start: The start position of the map
  goal: The goal position of the map
  columnNum: The number of column in the map that is being searched
  rowNum: The number of row in the map that is being searched
  diag: A boolean value to see if diagonal direction is considered
  okSpace: A list where available path will be considered
  notokSpace: A list where available path will not be considered due to heuristic value
  mode: A string value which define which algorithm to use: Astar or greedy

"""
class pathfind:

    #initialze function which initialize the map and all the attributes
    def __init__(self, start, goal, columnNum, rowNum, mode, diag = True):
        self.start = start
        self.goal = goal

        self.columnNum = columnNum
        self.rowNum = rowNum

        self.diag = diag

        self.okSpace = []
        self.notokSpace = []
        self.path = []

        #Check if mode entered is accepted
        if mode not in ["greedy", "astar"]:
            print("wrong input")
        else:
            self.mode = mode

    #heuristic() defines the heuristic function which is chose to be the
    #Chebyshev distance. This function takes in positions for two nodes and
    #return their Chebyshev distance
    def heuristic(self, ax, ay, bx, by):
      return max(abs(bx-ax),abs(by-ay))

    #find_path() finds paths start from start node and append them into okSpace
    #and notokSpace respectively base on different algorithm
    def find_path(self, maps):

        #initialize a node
        node = Node(None, self.start[0], self.start[1], float(0))
        while True:
            #to explore the node with smallest f value from the current node
            self.extend_path(node,maps)

            # when there is no choice left to go next
            if len(self.okSpace) == 0:
                return

            #Get the best node base on different algorithm's evaluation
            if self.mode == "astar":
                index, node = self.get_best()
            elif self.mode == "greedy":
                index, node = self.get_best_greedy()
            else:
                pass

            #if the goal is found, then the algorithm start to trace back
            if self.goal[0]== node.x and self.goal[1]== node.y:
                while node:
                    self.path.append((node.x, node.y))
                    node = node.parent
                return

            #if it is the node with smallest evaluation, delete it from okSpace and add it into notokSpace
            else:
                self.notokSpace.append(node)
                del self.okSpace[index]

    #extend_path() expand a node and retrieve the path
    #Diagonal direction will be considered base on self.diag
    def extend_path(self, node, maps):

        if self.diag:
            xMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
            yMoves = (-1, -1, -1, 0, 0, 1, 1, 1)

        else:
            xMoves = (0, -1, 1, 0)
            yMoves = (-1, 0, 0, 1)

        for xMove, yMove in zip(xMoves, yMoves):

            nextX, nextY = xMove + node.x, yMove + node.y

            # Check if the node hit an obstacle or if the it overstep the range
            if nextX < 0 or nextX >= self.columnNum:
                continue
            elif nextY < 0 or nextY >= self.rowNum:
                continue
            elif maps[nextY][nextX] == 'X':
                continue

            #initialze new node, base on above searhc
            newNode = Node(node, nextX, nextY, node.distance + self.get_cost(node,nextX,nextY))

            #when the new generated node is in the notokSpace list, means the previous path is better
            #thus ignore the current node
            if self.node_in(newNode, self.notokSpace) != -1:
                continue

            #check if the new generated node in the okSpace
            index = self.node_in(newNode, self.okSpace)

            #if it is not in okSpace
            if index != -1:
                if self.okSpace[index].distance > newNode.distance:
                    self.okSpace[index].parent = node
                    self.okSpace[index].distance = newNode.distance
                continue
            else:
                self.okSpace.append(newNode)
    #Evaluation function for Astar algorithm
    def get_best(self):
        best = None
        bestValue = float("inf")
        bestIndex = -1
        for index, i in enumerate(self.okSpace):
            fValue = i.distance + self.heuristic(self.goal[0], self.goal[1], i.x, i.y)
            currentValue = fValue
            if currentValue < bestValue:
                best = i
                bestValue = currentValue
                bestIndex = index
        return bestIndex, best

    #Evaluation function for greedy algortithm
    def get_best_greedy(self):
        best = None
        bestValue = float("inf")
        bestIndex = -1
        for index, i in enumerate(self.okSpace):
            fValue = self.heuristic(self.goal[0], self.goal[1], i.x, i.y)
            currentValue = fValue  # 获取F值
            if currentValue < bestValue:  # 比以前的更好，即F值更小
                best = i
                bestValue = currentValue
                bestIndex = index
        return bestIndex, best

    #get_searched() append all the searched path to a list
    def get_searched(self):
        searched = []
        for i in self.okSpace:
            searched.append((i.x, i.y))
        for i in self.notokSpace:
            searched.append((i.x, i.y))
        return searched

    #get_cost() returns the cost for going from one node to another
    def get_cost(self, p, new_x, new_y):

        return 1.0

    def node_in(self, node, spaceList):
        for i, n in enumerate(spaceList):
            if node.x == n.x and node.y == n.y:
                return i
        return -1

#get_start_and_goal() retrieve the start position and the goal position
#from the map
def get_start_and_goal(letter, MapData):
    for y, line in enumerate(MapData):
        try:
            x = line.index(letter)
        except:
            continue
        else:
            break
    return [x, y]

#function for reading file
def read_input(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    input_grid = []
    for line in lines:
        line = line.rstrip()
        input_grid.append(line)
    return input_grid

#function for writing file
def write_output(maps, filename):
    outFile = open(filename,"a")
    for line in maps:
        outFile.write(''.join(line) + "\n")
    print("WRITING DONE!")
    print()

#search() combine all the functions define in pathfind class and perform
#the main search step
def search(mapA, mode, diag = True):
    start = get_start_and_goal('S', mapA)
    goal = get_start_and_goal('G', mapA)

    #Initialize the pathfind class
    pathway = pathfind(start, goal,len(mapA[0]),len(mapA), mode, diag)

    #Search path from start
    pathway.find_path(mapA)

    #Denote all the searced path as > in the map
    searched = pathway.get_searched()
    for x, y in searched:
        mapA[y] = list(mapA[y])
        mapA[y][x] ='>'

    #Denote the choose path as P in the map
    path = pathway.path
    for x, y in path:
        mapA[y][x] = 'P'

    #Print result
    print("Using", mode, "search")
    print("path length is %d" % (len(path)))
    print("searched squares count is %d" % (len(searched)))

    mapA[start[1]][start[0]] = 'S'
    mapA[goal[1]][goal[0]] = 'G'

def main():
    #This part of code dedicate the search without considering diagonal direction
    mapGreedy = read_input("pathfinding_a.txt")
    search(mapGreedy, "greedy", False)
    write_output(["greedy"] + mapGreedy, "pathfinding_a_out.txt")

    mapAstar = read_input("pathfinding_a.txt")
    search(mapAstar, "astar", False)
    write_output(["A star"] + mapAstar, "pathfinding_a_out.txt")

    #This part of code dedicate the search considering diagonal direction
    mapGreedy2 = read_input("pathfinding_b.txt")
    search(mapGreedy2, "greedy", True)
    write_output(["greedy"] + mapGreedy2, "pathfinding_b_out.txt")

    mapAstar2 = read_input("pathfinding_b.txt")
    search(mapAstar, "astar", True)
    write_output(["A star"] + mapAstar, "pathfinding_b_out.txt")

main()
