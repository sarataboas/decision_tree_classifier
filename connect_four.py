import numpy as np

class Board:
    def __init__(self):
        self.cols = 7
        self.rows = 6
        self.board = []
        self.nullSymbol = '.'
        self.p1Symbol = 'X'
        self.p2Symbol = 'O'
        self.populateBoard()
        self.end = False
        self.winner = None
        self.turn = 1
        self.algorithm1 = None 
        self.algorithm2 = None
        self.is_terminal = False
        
        
    def __str__(self):
        line = ""
        result = ""
        for i in range(self.rows-1, -1, -1):
            for ii in range(self.cols):
                line += self.board[i][ii]
            result += line + "\n"
            line = ""
        return result
    
    def copy(self):
        new_board = Board()
        new_board.board = [row[:] for row in self.board]  # Deep copy the state
        return new_board
    
    def evaluate_segment(self, segment):
        count_x = segment.count('X')
        count_o = segment.count('O')
        if count_o == 3 and count_x == 0:
            return -50
        elif count_o == 2 and count_x == 0:
            return -10
        elif count_o == 1 and count_x == 0:
            return -1
        elif count_x == 1 and count_o == 0:
            return 1
        elif count_x == 2 and count_o == 0:
            return 10
        elif count_x == 3 and count_o == 0:
            return 50
        elif count_x == 4:
            return 512
        elif count_o == 4:
            return -512
        else:
            return 0
        

    def heuristic(self, node):
        score = 0
        # Count occurrences of 'X' and 'O' in the node
        for i in range(self.rows):
            for j in range(self.cols):
                # Horizontal segments
                if j <= self.cols - 4:
                    segment = [node.board[i][j+k] for k in range(4)]
                    score += self.evaluate_segment(segment)
                # Vertical segments
                if i <= self.rows - 4:
                    segment = [node.board[i+k][j] for k in range(4)]
                    score += self.evaluate_segment(segment)
                # Diagonal segments (top-left to bottom-right)
                if i <= self.rows - 4 and j <= self.cols - 4:
                    segment = [node.board[i+k][j+k] for k in range(4)]
                    score += self.evaluate_segment(segment)
                # Diagonal segments (bottom-left to top-right)
                if i >= 3 and j <= self.cols - 4:
                    segment = [node.board[i-k][j+k] for k in range(4)]
                    score += self.evaluate_segment(segment)
        # Move bonus for player
        if self.turn == 1:
            score += 16
        elif self.turn == 2:
            score -= 16
        return score

    def populateBoard(self):
        aux = []
        for i in range(self.cols):
            aux.append(self.nullSymbol)
        for i in range(self.rows):
            self.board.append(aux.copy())

    def move(self, collumn, player):
        return self.addToCollumn(collumn, player)
        
            
    def addToCollumn(self, collumn, player):
        for i in range(len(self.board)):
            if self.board[i][collumn-1] == self.nullSymbol and self.possibleMoves().__contains__(collumn):
                self.board[i][collumn-1] = self.player(player)
                if len(self.possibleMoves()) == 0:
                    self.end = True
                if self.checkWinner(self.player(player), (i,collumn-1)):
                    self.showWinner(self.player(player))   
                self.change_player()   
                return True
        return False
        
    def checkWinner(self, player, last_move):
        if len(self.possibleMoves()) == 0:
            self.end = True
        row, col = last_move
        token = player  # assuming player's token is represented by 'X' or 'O'

        # Check horizontal
        count = 0
        for c in range(self.cols):
            if self.board[row][c] == token:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # Check vertical
        count = 0
        for r in range(self.rows):
            if self.board[r][col] == token:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # Check diagonal up-left-to-right
        count = 0
        for i in range(-3, 4):
            if 0 <= row + i < self.rows and 0 <= col + i < self.cols:
                if self.board[row + i][col + i] == token:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        
        # Check diagonal down-left-to-right
        count = 0
        for i in range(-3, 4):
            if 0 <= row + i < self.rows and 0 <= col - i < self.cols:
                if self.board[row + i][col - i] == token:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0

        return False
                    
    def showWinner(self, player):
        self.end = True
        if self.winner == None:
            self.winner = player

    def player(self, player):
        if player == 1:
            return self.p1Symbol
        elif player == 2:
            return self.p2Symbol
        
    def change_player(self):
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1 
        
        
    def possibleMoves(self):
        return [col+1 for col in range(self.cols) if self.board[self.rows-1][col] == self.nullSymbol]
    
