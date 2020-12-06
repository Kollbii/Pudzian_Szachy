import matplotlib.pyplot as plt
import numpy as np
import random
import os
from colorama import init
from numpy.ma.core import right_shift
init()
np.set_printoptions(threshold=np.inf)

GREEN = '\u001b[32m'
RED = '\u001b[31m'
RESET = '\u001b[0m'

global info
info = ''

################################################
# Ogólnie to w info chcemy zwracać wszystkie informacje więc wystarczy, że każda metoda będzie do niej dodawać informacje wg jakiejś
# templatki. Kolorki bo #fancy_wygląd i Jemioło się podoba XD <Trzeba uważać na warunki sprawdzania bo to są całe teksy znaków jak np.
# \u001b[32m♝\u001b[0m zamiast samego ♝. 
# W sumie zrobiłem tyle, że skoczek sprawdza każdą figurę i ją markuje na czerwono.
# Jedyne co chyba trzeba zrobić to napisac metody dla hetmana i gońca.
# Tylko wywołując funkcje trzeba mieć na uwadze kolejność. bo np. Jeśli moje skoczki będą pierwsze to pozamieniają
# niektóre figury na czerwone. Więc fajnie jakby ten problem jakoś rozwiązać. (albo zrezygnować z kolorwania :(( *sad noises*)
# Podczas wstępnego testowania nie zauważyłem błędów w działaniu mojej części więc powinno być wszystko gites.
# Każdy skoczek sprawdza wszystkie możliwe pola dookoła siebie 
# ~~Kollbi
#
# Jest pomysł przerobić programik tak że na początku wszystkie pionki położone są zielone i teraz tak:
# 1) wybieramy gońce i wszystkie pozostałe pionki które szachują gońce są czerwone
# 2) wybieramy skoczki i wszystkie pozostałe pionki które szachują skoczki są czerwone
# 3) wybieramy hetmany i wszystkie pozostałe pionki które szachują hetmany są czerwone
#
# więc trzeba przerobić teraz lekko programik i zrobić funkcje:
# 1)funkcja resetowania całej planszy na zielone pionki
# 2)interfejs wyboru opcji (patrz punkt wyżej)
# 
# output jaki jest czyli "♞ na [2][2] szachuje ♛ na [0][1]" jest gites i zostaje tylko będą tam pokazane odpowiednie wybrane pionki
# ~~czujsnn
#
#dobra skonczylem klase hetman, teraz zostaje zrobić tak:
#-zrobić ostatnią klasę pionka ( w sumie to można skopiować moja hetmana i wyjebać x1=x2 y1=y2 ale mi sie nie chce)
#-zrobic interfejs
#-zrobić nieskonczona petle z wyborem i resetowaniem planszy
#naprawiłem też buga z hetmanami to pora na cska B)
# ~~czujsnn
#
# To ja na dobry sen dorobiłem prosty interfejsik #bo_mogę_i_pudzian_dałby_okejkę
# Nieskonczona pętla z wyborem też jest nie jest ona bogiem user inputów więc jak ma ktoś jakieś uwagi do poprawki 
# to naprawdę nie trzymam XD 
# I na gicie podepne skrina bo wydaje mi się, że hetman nie powinien tak działać <bo działa jak przeszywajaca strzała>
# a myslałem, że zatrzymuje się na pierwszym możliwym obiekcie <co powinien chyba zrobić>
# nie wiem sam do końca dlatego na gicie i #Lab 4 jest obrazek
# ~~Kollbi
#
################################################

class Board:
    def __init__(self):
        pass

    def createBoard(self, dim): #tworzenie macierzy nxn wypelnionej kropkami <3  
        self.dim = dim
        self.board = np.array([[ '•' for x in range(self.dim)] for y in range (self.dim)], dtype="object")
        return self.board


class Pionek:
    def __init__(self, pawn, n, board, dim_board):
        self.cords = []
        self.pawn = pawn 
        self.n = n
        self.board = board
        self.dim = dim_board
        
    def placeOnBoard(self, board):

        for _ in range(self.n):
             
            x,y = random.randint(0,self.dim-1), random.randint(0,self.dim-1)
            new_cord = (x,y)
            if new_cord in self.cords:
                while True:
                    x,y = random.randint(0,self.dim-1), random.randint(0,self.dim-1)
                    new_cord = (x,y)
                    if new_cord not in self.cords:
                        self.cords.append(new_cord)
                        break
            else:
                self.cords.append(new_cord)
            
        for cord in self.cords:
            board[cord[0]][cord[1]] = self.pawn
    
        return board

    def drawTab(self, board):
        draw = f''
        for i in range (0, len(self.board)):
            draw += f"{str(i).rjust(2)}│"
            for j in range (0, len(board[i])):
                if(j == len(board[i]) - 1):
                    draw += ''.join(str(board[i][j]))
                    draw += ''.join("\n")
                else:
                    draw += ''.join(str(board[i][j]))
                    draw += ''.join(" ") # •
        return draw

class Hetman(Pionek):
    def mergeCords(self,skoczek_cord,goniec_cord):
        self.other_cord = []
        for cord in skoczek_cord:
            self.other_cord.append(cord)
        for cord in goniec_cord:
            self.other_cord.append(cord)

        return self.other_cord
    
    def doesCheck(self, board,x,y, option):
        if board[x][y] == f'{GREEN}{option}{RESET}':
            return True
        return False

    def markChecked(self, board, x1, y1, x2, y2, option):
        global info
        board[x1][y1] = f'{RED}♛{RESET}'
        board[x2][y2] = f'{RED}{option}{RESET}'
        info += f"♛ na [{x1}][{y1}]\t szachuje {option} na [{x2}][{y2}]\n"

    def checkTakeDown(self,board,skoczek_cord,goniec_cord):
        global info
        
        self.other_cord = self.mergeCords(skoczek_cord,goniec_cord)
        
        for i in range(0,len(self.cords)):
            for j in range(0,len(self.other_cord)):
                x1 = self.cords[i][0]
                y1 = self.cords[i][1]

                x2 = self.other_cord[j][0]
                y2 = self.other_cord[j][1]
                
                if self.board[x1][y1] == f'{GREEN}♛{RESET}' or self.board[x1][y1] == f'{RED}♛{RESET}':
                    if x1 == x2:
                        if self.doesCheck(board,x2,y2, "♞") == True:
                            self.markChecked(board,x1,y1,x2,y2,"♞")
                        elif self.doesCheck(board,x2, y2, "♛") == True:
                            self.markChecked(board,x1,y1,x2,y2,"♛")
                        elif self.doesCheck(board,x2, y2, "♝") == True:
                            self.markChecked(board,x1,y1,x2,y2,"♝")
                        #info += f"♛ {self.cords[i]} szachuje  na {self.other_cord[j]}\n"

                    if y1 == y2:
                        if self.doesCheck(board,x2, y2, "♞") == True:
                            self.markChecked(board,x1, y1,x2,y2,"♞")
                        elif self.doesCheck(board,x2, y2, "♛") == True:
                            self.markChecked(board,x1,y1,x2,y2,"♛")
                        elif self.doesCheck(board,x2,y2, "♝") == True:
                            self.markChecked(board,x1,y1,x2,y2,"♝")
                        #info += f"♛ {self.cords[i]} szachuje  na {self.other_cord[j]}\n"

                    if x2 - x1 == y2 - y1:
                        if self.doesCheck(board,x2, y2, "♞") == True:
                            self.markChecked(board,x1, y1,x2,y2,"♞")
                        elif self.doesCheck(board,x2, y2, "♛") == True:
                            self.markChecked(board,x1,y1,x2,y2,"♛")
                        elif self.doesCheck(board,x2, y2, "♝") == True:
                            self.markChecked(board,x1,y1,x2,y2,"♝")
                        #info += f"♛ {self.cords[i]} szachuje  na {self.other_cord[j]}\n"

                    if -x2 + x1 == y2 - y1:
                        if self.doesCheck(board,x2, y2, "♞") == True:
                            self.markChecked(board,x1, y1,x2,y2,"♞")
                        elif self.doesCheck(board,x2, y2, "♛") == True:
                            self.markChecked(board,x1,y1,x2,y2,"♛")
                        elif self.doesCheck(board,x2, y2, "♝") == True:
                            self.markChecked(board,x1,y1,x2,y2,"♝")                    
                        #info += f"♛ {self.cords[i]} szachuje  na {self.other_cord[j]}\n"
        
        #przepraszam kazdego za to co teraz robie bo to jest giga zjebane
        for i in range(0,len(self.cords)):
            for j in range(i+1,len(self.cords)):
                x1 = self.cords[i][0]
                y1 = self.cords[i][1]

                x2 = self.cords[j][0]
                y2 = self.cords[j][1]
                
                if self.board[x1][y1] == f'{GREEN}♛{RESET}' or self.board[x1][y1] == f'{RED}♛{RESET}':
                    if x1 == x2:
                        self.markChecked(board,x1,y1,x2,y2,"♛")
                    if y1 == y2:
                        self.markChecked(board,x1,y1,x2,y2,"♛")
                    if x2 - x1 == y2 - y1:
                        self.markChecked(board,x1,y1,x2,y2,"♛")
                    if -x2 + x1 == y2 - y1:
                        self.markChecked(board,x1,y1,x2,y2,"♛")

        return board

class Goniec(Pionek):
    #TODO
    pass

class Skoczek(Pionek):
    def doesCheck(self, board, i, j, x, y, option):
        if board[i + x][j + y] == f'{GREEN}{option}{RESET}':
            return True
        return False

    def markChecked(self, board, i, j, x, y, option):
        global info
        board[i][j] = f'{RED}♞{RESET}'
        board[i + x][j + y] = f'{RED}{option}{RESET}'
        info += f"♞ na [{i}][{j}]\t szachuje {option} na [{i + x}][{j + y}]\n"

    def isSafe(self, board, i, j, x, y):
        if (i + x >= 0 and i + x < len(self.board)) and (j + y >= 0 and j + y < len(self.board)):
            return True
        return False

    def getChecked(self, board):
        moves = [[1,2],[2,1],[-1,2],[-2,1],[-1,-2],[-2,-1],[1,-2],[2,-1]]

        for i in range (0, len(self.board)):
            for j in range (0, len(self.board[i])):
                if self.board[i][j] == f'{GREEN}♞{RESET}' or self.board[i][j] == f'{RED}♞{RESET}':    # Tutaj wybiera też czerwone skoczki bo czerwony może szachować jakiegoś hetmana jeszcze.
                    for x, y in moves:                                                                  # duplikaty się NIE robią bo w sprawdzaniu jest ustawiony "zielony skoczek" :)
                        if self.isSafe(board, i, j, x, y):
                            if self.doesCheck(board, i, j, x, y, "♞") == True:
                                self.markChecked(board, i, j, x, y, "♞")
                            elif self.doesCheck(board, i, j, x, y, "♛") == True:
                                self.markChecked(board, i, j, x, y, "♛")
                            elif self.doesCheck(board, i, j, x, y, "♝") == True:
                                self.markChecked(board, i, j, x, y, "♝")
        return board

# Tutaj tego śmiesznego __init__ = '__name__' wstawić ?
# wstawiłem ale idk jak to ma działać dokładnie X"D 
def start():
    os.system('cls')
    p = os.getcwd()
    if os.path.exists(p+"/board.txt") == True:
        os.remove(p+"/board.txt")

    
    # USER INPUT
    # W sumie to nie wiem jak rozbudowane to chcemy mieć i zacząłem myśleć nad inputem usera i tak naprawdę 
    # to jest tutaj wszystko co potrzba. yolo? Zrobiony? XD Ale coś pewnie wyjdzie w trakcie #pudzian_naprwiajacy
    while True:
        try:
            print("┌──────────────────┐")
            print("│  Wybierz opcję:  │")
            print(f"│  [{GREEN}1{RESET}] - Knights   │")
            print(f"│  [{GREEN}2{RESET}] - Bishops   │")
            print(f"│  [{GREEN}3{RESET}] - Queens    │")
            print("└──────────────────┘")

            user_option = int(input("Opcja: "))
            if user_option == 1 or user_option == 2 or user_option == 3:
                break
            else:
                os.system('cls')
                print("Podaj poprawną opcję!")
        except ValueError:
            os.system('cls')
            print("Podaj poprawną opcję!")

    os.system('cls')
    b = Board()
    tablica = b.createBoard(10)
    h = Hetman(f"{GREEN}♛{RESET}",2,tablica,b.dim)
    s = Skoczek(f"{GREEN}♞{RESET}",3,tablica,b.dim)
    g = Goniec(f"{GREEN}♝{RESET}",2,tablica,b.dim)
    hetmanPlacement = h.placeOnBoard(tablica)
    knightPlacement = s.placeOnBoard(hetmanPlacement)
    bishopPlacement = g.placeOnBoard(knightPlacement)


    print("┌──────────────────┐")
    print(f"│  Wybrałeś {user_option}      │")
    print("└──────────────────┘")
    if user_option == 1:
        test1 = s.getChecked(bishopPlacement)
        print(s.drawTab(test1))
        print(info)
    elif user_option == 2:
        pass
    elif user_option == 3:
        test3 = h.checkTakeDown(bishopPlacement,s.cords,g.cords)
        print(h.drawTab(test3))
        print(info)

if __name__ == "__main__":
    start()


# Test Cases 
#TODO