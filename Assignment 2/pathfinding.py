import math
mapStr2 = [
         "XXXXXXXXXX",
         "X___XX_X_X",
         "X_X__X___X",
         "XSXX___X_X",
         "X_X__X___X",
         "X___XX_X_X",
         "X_X__X_X_X",
         "X__G_X___X",
         "XXXXXXXXXX"]

class Node:
    """
    用于节点的表示，parent用来在成功的时候回溯路径（相当于一个链表）
    """

    def __init__(self, parent, x, y, distance):
        self.parent = parent
        self.x = x
        self.y = y
        self.distance = distance # 这里只是g(M)


class aStar:

    # 初始化地图长和宽，开始终止节点，open集合和close集合，
    # 路径集合path用于最后反向遍历找出路径
    def __init__(self, start, goal, columnNum, rowNum, mode):
        self.start = start
        self.goal = goal
        
        self.columnNum = columnNum
        self.rowNum = rowNum

        self.okSpace = []
        self.notokSpace = []
        self.path = []
        
        if mode not in ["greedy", "astar"]:
            print("wrong input")
        else:
            self.mode = mode

    def heuristic(self, px, py, qx, qy):
        # Manhattan distance on a grid 
        return abs(px - qx) + abs(py - qy)

    # def heuristic(self, ax, ay, bx, by):
    # # Euclidean distance on a grid between node a and b
    #   return math.sqrt(pow(bx-ax,2) + pow(by - ax,2))
    
    # def heuristic(self, ax, ay, bx, by):
    #   # Chebyshev distance on a grid 
    #   return max(abs(bx-ax),abs(by-ay))

    def find_path(self, maps):
        
        # initialize a node
        node = Node(None, self.start[0], self.start[1], float(0))
        while True:
            # to explore the node with smallest f value
            # from the current node 
            self.extend_path(node,maps)

            # when there is no choice left to go next
            if len(self.okSpace) == 0:
                return

            # 获取F值最小的节点（最短路径）
            # 使用greedy的话这个函数换成get_best_greedy就可以
            if self.mode == "astar":
                index, node = self.get_best()
            elif self.mode == "greedy":
                index, node = self.get_best_greedy()
            else:
                pass

            # if the goal is found
            if self.goal[0]== node.x and self.goal[1]== node.y:
                # trace back
                while node:
                    self.path.append((node.x, node.y))
                    node = node.parent
                return
            # if it is the node with smallest f value
            # delete it from okSpace and add it into notokSpace
            else:
                self.notokSpace.append(node)
                del self.okSpace[index]

    def extend_path(self, node, maps):
        # 可以从8个方向走，可以走斜线
        # xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        # ys = (-1, -1, -1, 0, 0, 1, 1, 1)

        # we can go up, down, lefy and right but not diagonal
        # 只能走上下左右四个方向，不可以走斜线
        xMoves = (0, -1, 1, 0)
        yMoves = (-1, 0, 0, 1)
        for xMove, yMove in zip(xMoves, yMoves):

            nextX, nextY = xMove + node.x, yMove + node.y

            # check if the node hit an obstacle
            # or if the it overstep the range
            if nextX < 0 or nextX >= self.columnNum:
                continue
            elif nextY < 0 or nextY >= self.rowNum:
                continue
            elif maps[nextY][nextX] == 'X':
                continue

            # 生成新的节点和g(M)值，get_cost可以默认为1，这里为了考虑斜线和直线不同
            newNode = Node(node, nextX, nextY, node.distance + self.get_cost(node,nextX,nextY))

            # when the new generated node is in the notokSpace list
            # means the previous path is better
            # thus ignore the current node
            if self.node_in(newNode, self.notokSpace) != -1:
                continue

            # check if the new generated node in the okSpace
            index = self.node_in(newNode, self.okSpace)
            # if it is not in okSpace
            if index != -1:
                if self.okSpace[index].distance > newNode.distance:
                    self.okSpace[index].parent = node
                    self.okSpace[index].distance = newNode.distance
                continue
            else:
                self.okSpace.append(newNode)

    def get_best(self):
        best = None
        bestValue = float("inf")  # 如果你修改的地图很大，可能需要修改这个值
        bestIndex = -1
        for index, i in enumerate(self.okSpace):
            # f = i.dist + math.sqrt(
            #     (self.end[0] - i.x) * (self.end[0] - i.x)
            #     + (self.end[1] - i.y) * (self.end[1] - i.y)) * 1.2

            #使用Euclidean distance as heuristic
            fValue = i.distance + self.heuristic(self.goal[0], self.goal[1], i.x, i.y)
            currentValue = fValue
            if currentValue < bestValue:
                best = i
                bestValue = currentValue
                bestIndex = index
        return bestIndex, best

    #evaluate function for greedy algortithm

    def get_best_greedy(self):
        best = None
        bestValue = 1000000  # 如果你修改的地图很大，可能需要修改这个值
        bestIndex = -1
        for index, i in enumerate(self.okSpace):
            # f = i.dist + math.sqrt(
            #     (self.end[0] - i.x) * (self.end[0] - i.x)
            #     + (self.end[1] - i.y) * (self.end[1] - i.y)) * 1.2

            #使用Euclidean distance as heuristic，在greedy下把i.dist去掉了
            fValue = self.heuristic(self.goal[0], self.goal[1], i.x, i.y)
            currentValue = fValue  # 获取F值
            if currentValue < bestValue:  # 比以前的更好，即F值更小
                best = i
                bestValue = currentValue
                bestIndex = index
        return bestIndex, best

    def get_searched(self):
        searched = []
        for i in self.okSpace:
            searched.append((i.x, i.y))
        for i in self.notokSpace:
            searched.append((i.x, i.y))
        return searched

    def get_cost(self, p, new_x, new_y):
        """
        上下左右直走，代价为1.0，斜走，代价为1.4
        """
        # if p.x == new_x or p.y == new_y:
        #     return 1.0
        # return 1.4

        return 1.0

    def node_in(self, node, spaceList):
        for i, n in enumerate(spaceList):
            if node.x == n.x and node.y == n.y:
                return i
        return -1

def get_start_and_goal(letter, MapData):
    for y, line in enumerate(MapData):
        try:
            x = line.index(letter)
        except:
            continue
        else:
            break
    return [x, y]

def read_input(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    input_grid = []
    for line in lines:
        line = line.rstrip()
        input_grid.append(line)
    return input_grid

def write_output(maps):
    outFile = open("pathfinding_a_out.txt","a")
    for line in maps:
        outFile.write(''.join(line) + "\n")
    print("WRITING DONE!")
    print()

def search(mapA, mode):
    start = get_start_and_goal('S', mapA)
    goal = get_start_and_goal('G', mapA)

    # 初始化整个程序
    a_star = aStar(start, goal,len(mapA[0]),len(mapA), mode)

    # 从开始几点查找路径
    a_star.find_path(mapA)

    # 标记已搜索区域为'-'
    # 已搜索区域=open+close
    searched = a_star.get_searched()
    for x, y in searched:
        mapA[y] = list(mapA[y])
        mapA[y][x] ='>'

    # 标记路径为'>'
    path = a_star.path
    for x, y in path:
        mapA[y][x] = 'P'

    # 打印最短路径长度和搜索区域长度
    print("Using", mode, "search")
    print("path length is %d" % (len(path)))
    print("searched squares count is %d" % (len(searched)))

    # 恢复开始和终止节点的标记
    mapA[start[1]][start[0]] = 'S'
    mapA[goal[1]][goal[0]] = 'G'
    
def main():
    mapGreedy = read_input("pathfinding_a.txt")
    search(mapGreedy, "greedy")
    write_output(["greedy"] + mapGreedy)
    
    mapAstar = read_input("pathfinding_a.txt")
    search(mapAstar, "astar")
    write_output(["A star"] + mapAstar)

main()