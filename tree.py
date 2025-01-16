from connect_four import Board
import numpy as np

class Node:
    def __init__(self, value, children, parent):
        self.value = value      # is a matrix of the board in AStarTree and is a Board object in MCTree
        self.children = children    # is a dictionary {0: node, 1: node, ...}
        self.parent = parent    # is another node
        self.wins = 0
        self.visits = 0
        
    def setValue(self, value):
        self.value = value
        
    def setChildren(self, children):
        self.children = children
        
    def getChild(self, child):
        return self.children[child]
        
    def setParent(self, parent):
        self.parent = parent
    
    def getParent(self):
        return self.parent
    
    #Monte Carlo
    
    def win(self):
        self.wins += 1
        
    def visit(self):
        self.visits += 1
        
    def genChildren(self, player):
        children = {} # dicionário
        for i in self.value.possibleMoves():
            temporaryBoard = Board()
            temporaryBoard.board = np.copy(self.value.board)
            temporaryBoard.winner = self.value.winner
            temporaryBoard.end = self.value.end
            temporaryBoard.move(i, player)
            
            children[i] = Node(temporaryBoard, {}, self)
        
        self.setChildren(children)
    
    def nodeHeight(self):
        return self.calculateNodeHeight(self)

    def calculateNodeHeight(self, node):
        if node.parent == None: return 0
        else:
            return self.calculateNodeHeight(node.parent) + 1
        
    def copy(self):
        boardCopy = Board()
        boardCopy.board = np.copy(self.value.board)
        boardCopy.winner = self.value.winner
        boardCopy.end = self.value.end

        childrenCopy = {}
        for child in self.children:
            childrenCopy[child] = self.getChild(child).copy()
        
        node = Node(boardCopy, childrenCopy, self.parent)
        node.wins = self.wins
        node.visits = self.visits
        
        return node
        

class AStarTree:
    def __init__(self, board, player):              # player is 1 or 2, board is a board object
        self.player = player                        # 1 or 2
        self.root = Node(board, {}, None)           # root node with the matrix of the board as its value
        self.root.genChildren(player)               # generates new children for the root
        
    
class MCTree():
    def __init__(self, board, player):
        self.player = player                        # 1 or 2
        self.root = Node(board, {}, None)           # root node with the board object as its value
        
    def __str__(self):
        result = ''
        for child in self.root.children:
            result += str(child) + ": " + str(self.root.getChild(child).wins) + "/" + str(self.root.getChild(child).visits) + " Winner: " + str(self.root.getChild(child).value.winner) + "\n"
        return result