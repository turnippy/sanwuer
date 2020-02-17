## N-Queens Solution by Group 8
## CISC 352 Winter 2020 Assignment 1
## Contributors: Hanyi Li, Tong Liu, Yitong Liu, Tao Ma, Yuntian Shan

class board:

    # constructor for board class
    # input: board size
    # output: board object
    def __init__(self, size):
        self.size = size
        self.board = [[0 for x in range(size)] for y in range(size)]
        self.populate(size)
    
    # function used to generate an optimized initial placement of queens
    # inputs: board size
    # outputs: none
    def populate(self, size):
        for i in range(size):
            temp = i * (i + 3) / 2 #Used to generate the sequence 0, 2, 5, 9 ... 
            self.board[i][temp % size] = 1
            
    def solve(self):
        #..
        
def nqueens():
    in_text = open('nqueens.txt', 'r')
    lines = [line.rstrip() for line in in_text]
    in_text.close()
    
    solution = []
    i = 0
    while i < len(lines):
        a_board = board(lines[i])
        solution.append(a_board.solve())

if __name__ == '__main__':
    nqueens()
