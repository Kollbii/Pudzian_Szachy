import matplotlib.pyplot as plt
import numpy as np
import random
import os
np.set_printoptions(threshold=np.inf)


class Board:
    def __init__(self):
        pass

    def createBoard(self,dim): #tworzenie macierzy nxn wypelnionej zerami
        self.dim = dim
        self.board = np.zeros((self.dim,self.dim),dtype= "object")    
        return self.board

    def writeToFile(self):
        np.savetxt("board1.txt",self.board, fmt='%s', delimiter=' ')

    def PlaceOnBoard(self,pawn,id,n): #pawn to rodzaj, id to jego litera, n to ilość
        pass

class Pionek:
    def __init__(self,pawn,id,n,board,dim_board):
        self.cords = []
        self.pawn = pawn
        self.id = id 
        self.n = n
        self.board = board
        self.dim = dim_board
        

    def PlaceOnBoard(self):

        for _ in range(self.n):
             
            x,y = random.randint(0,self.dim-1), random.randint(0,self.dim-1)
            new_cord = (x,y)
            if new_cord in self.cords:
                while True:
                    x,y = random.randint(0,self.dim-1), random.randint(0,self.dim-1)
                    new_cord = (x,y)
                    if new_cord not in self.cords:
                        self.cords.append(new_cord)
            else:
                self.cords.append(new_cord)
            
        for cord in self.cords:
            self.board[cord[0]][cord[1]] = self.id
    

class Hetman(Pionek):
    pass

class Goniec(Pionek):
    pass

class Skoczek(Pionek):
    pass


p = os.getcwd()
if os.path.exists(p+"/board.txt") == True:
    os.remove(p+"/board.txt")

b = Board()
b.createBoard(10)