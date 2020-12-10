import matplotlib.pyplot as plt
import numpy as np
import random
import os
from colorama import init
from numpy.ma.core import right_shift

init()

GREEN = "\u001b[32m"
RED = "\u001b[31m"
RESET = "\u001b[0m"

global info
info = ""


class Board:
    def __init__(self, dim):
        self.board = np.array(
            [["•" for x in range(dim)] for y in range(dim)], dtype="object"
        )
        self.dim = dim
        return


class Pionek:
    def __init__(self, pawn, n, board):
        self.cords = []
        self.icon = pawn
        self.n = n  # ilosc
        self.boardInstance = board

    def placeOnBoard(self):

        for _ in range(self.n):

            x, y = random.randint(0, self.boardInstance.dim - 1), random.randint(
                0, self.boardInstance.dim - 1
            )
            new_cord = (x, y)
            if new_cord in self.cords:
                while True:
                    x, y = (
                        random.randint(0, self.boardInstance.dim - 1),
                        random.randint(0, self.boardInstance.dim - 1),
                    )
                    new_cord = (x, y)
                    if new_cord not in self.cords:
                        self.cords.append(new_cord)
                        break
            else:
                self.cords.append(new_cord)

        for cord in self.cords:
            self.boardInstance.board[cord[0]][cord[1]] = self.icon

        return

    def drawTab(self):
        draw = f""
        for i in range(0, len(self.boardInstance.board)):
            draw += f"{str(i).rjust(2)}│"
            for j in range(0, len(self.boardInstance.board[i])):
                if j == len(self.boardInstance.board[i]) - 1:
                    draw += "".join(str(self.boardInstance.board[i][j]))
                    draw += "".join("\n")
                else:
                    draw += "".join(str(self.boardInstance.board[i][j]))
                    draw += "".join(" ")  # •
        return draw


class Hetman(Pionek):
    def mergeCords(self, skoczek_cord, goniec_cord):
        self.other_cord = []
        for cord in skoczek_cord:
            self.other_cord.append(cord)
        for cord in goniec_cord:
            self.other_cord.append(cord)

        return self.other_cord

    def doesCheck(self, x, y, option):
        if self.boardInstance.board[x][y] == f"{GREEN}{option}{RESET}":
            return True
        return False

    def markChecked(self, x1, y1, x2, y2, option):
        global info
        self.boardInstance.board[x1][y1] = f"{RED}♛{RESET}"
        self.boardInstance.board[x2][y2] = f"{RED}{option}{RESET}"
        info += f"♛ na [{x1}][{y1}]\t szachuje {option} na [{x2}][{y2}]\n"

    def checkTakeDown(self, skoczek_cord, goniec_cord):
        global info

        self.other_cord = self.mergeCords(skoczek_cord, goniec_cord)

        for i in range(0, len(self.cords)):
            for j in range(0, len(self.other_cord)):
                x1 = self.cords[i][0]
                y1 = self.cords[i][1]

                x2 = self.other_cord[j][0]
                y2 = self.other_cord[j][1]
                # przepraszam kazdego za to co teraz robie bo to jest giga zjebane
                if (
                    self.boardInstance.board[x1][y1] == f"{GREEN}♛{RESET}"
                    or self.boardInstance.board[x1][y1] == f"{RED}♛{RESET}"
                ):
                    if x1 == x2:
                        if self.doesCheck(x2, y2, "♞") == True:
                            self.markChecked(x1, y1, x2, y2, "♞")
                        elif self.doesCheck(x2, y2, "♛") == True:
                            self.markChecked(x1, y1, x2, y2, "♛")
                        elif self.doesCheck(x2, y2, "♝") == True:
                            self.markChecked(x1, y1, x2, y2, "♝")
                        # info += f"♛ {self.cords[i]} szachuje  na {self.other_cord[j]}\n"

                    if y1 == y2:
                        if self.doesCheck(x2, y2, "♞") == True:
                            self.markChecked(x1, y1, x2, y2, "♞")
                        elif self.doesCheck(x2, y2, "♛") == True:
                            self.markChecked(x1, y1, x2, y2, "♛")
                        elif self.doesCheck(x2, y2, "♝") == True:
                            self.markChecked(x1, y1, x2, y2, "♝")
                        # info += f"♛ {self.cords[i]} szachuje  na {self.other_cord[j]}\n"

                    if x2 - x1 == y2 - y1:
                        if self.doesCheck(x2, y2, "♞") == True:
                            self.markChecked(x1, y1, x2, y2, "♞")
                        elif self.doesCheck(x2, y2, "♛") == True:
                            self.markChecked(x1, y1, x2, y2, "♛")
                        elif self.doesCheck(x2, y2, "♝") == True:
                            self.markChecked(x1, y1, x2, y2, "♝")
                        # info += f"♛ {self.cords[i]} szachuje  na {self.other_cord[j]}\n"

                    if -x2 + x1 == y2 - y1:
                        if self.doesCheck(x2, y2, "♞") == True:
                            self.markChecked(x1, y1, x2, y2, "♞")
                        elif self.doesCheck(x2, y2, "♛") == True:
                            self.markChecked(x1, y1, x2, y2, "♛")
                        elif self.doesCheck(x2, y2, "♝") == True:
                            self.markChecked(x1, y1, x2, y2, "♝")
                        # info += f"♛ {self.cords[i]} szachuje  na {self.other_cord[j]}\n"

        for i in range(0, len(self.cords)):
            for j in range(i + 1, len(self.cords)):
                x1 = self.cords[i][0]
                y1 = self.cords[i][1]

                x2 = self.cords[j][0]
                y2 = self.cords[j][1]

                if (
                    self.boardInstance.board[x1][y1] == f"{GREEN}♛{RESET}"
                    or self.boardInstance.board[x1][y1] == f"{RED}♛{RESET}"
                ):
                    if x1 == x2:
                        self.markChecked(x1, y1, x2, y2, "♛")
                    if y1 == y2:
                        self.markChecked(x1, y1, x2, y2, "♛")
                    if x2 - x1 == y2 - y1:
                        self.markChecked(x1, y1, x2, y2, "♛")
                    if -x2 + x1 == y2 - y1:
                        self.markChecked(x1, y1, x2, y2, "♛")

        return self.boardInstance.board


class Goniec(Pionek):
    def mergeCords(self, skoczek_cord, goniec_cord):
        self.other_cord = []
        for cord in skoczek_cord:
            self.other_cord.append(cord)
        for cord in goniec_cord:
            self.other_cord.append(cord)

        return self.other_cord

    def doesCheck(self, x, y, option):
        if self.boardInstance.board[x][y] == f"{GREEN}{option}{RESET}":
            return True
        return False

    def markChecked(self, x1, y1, x2, y2, option):
        global info
        self.boardInstance.board[x1][y1] = f"{RED}♝{RESET}"
        self.boardInstance.board[x2][y2] = f"{RED}{option}{RESET}"
        info += f"♝ na [{x1}][{y1}]\t szachuje {option} na [{x2}][{y2}]\n"

    def checkTakeDown(self, skoczek_cord, goniec_cord):
        global info

        self.other_cord = self.mergeCords(skoczek_cord, goniec_cord)

        for i in range(0, len(self.cords)):
            for j in range(0, len(self.other_cord)):
                x1 = self.cords[i][0]
                y1 = self.cords[i][1]

                x2 = self.other_cord[j][0]
                y2 = self.other_cord[j][1]
                # przepraszam kazdego za to co teraz robie bo to jest giga zjebane (jest)
                if (
                    self.boardInstance.board[x1][y1] == f"{GREEN}♝{RESET}"
                    or self.boardInstance.board[x1][y1] == f"{RED}♝{RESET}"
                ):

                    if x2 - x1 == y2 - y1:
                        if self.doesCheck(x2, y2, "♞") == True:
                            self.markChecked(x1, y1, x2, y2, "♞")
                        elif self.doesCheck(x2, y2, "♛") == True:
                            self.markChecked(x1, y1, x2, y2, "♛")
                        elif self.doesCheck(x2, y2, "♝") == True:
                            self.markChecked(x1, y1, x2, y2, "♝")
                        # info += f"♛ {self.cords[i]} szachuje  na {self.other_cord[j]}\n"

                    if -x2 + x1 == y2 - y1:
                        if self.doesCheck(x2, y2, "♞") == True:
                            self.markChecked(x1, y1, x2, y2, "♞")
                        elif self.doesCheck(x2, y2, "♛") == True:
                            self.markChecked(x1, y1, x2, y2, "♛")
                        elif self.doesCheck(x2, y2, "♝") == True:
                            self.markChecked(x1, y1, x2, y2, "♝")
                        # info += f"♛ {self.cords[i]} szachuje  na {self.other_cord[j]}\n"

        for i in range(0, len(self.cords)):
            for j in range(i + 1, len(self.cords)):
                x1 = self.cords[i][0]
                y1 = self.cords[i][1]

                x2 = self.cords[j][0]
                y2 = self.cords[j][1]

                if (
                    self.boardInstance.board[x1][y1] == f"{GREEN}♝{RESET}"
                    or self.boardInstance.board[x1][y1] == f"{RED}♝{RESET}"
                ):
                    if x2 - x1 == y2 - y1:
                        self.markChecked(x1, y1, x2, y2, "♝")
                    if -x2 + x1 == y2 - y1:
                        self.markChecked(x1, y1, x2, y2, "♝")

        return self.boardInstance.board


class Skoczek(Pionek):
    def doesCheck(self, i, j, x, y, option):
        if self.boardInstance.board[i + x][j + y] == f"{GREEN}{option}{RESET}":
            return True
        return False

    def markChecked(self, i, j, x, y, option):
        global info
        self.boardInstance.board[i][j] = f"{RED}♞{RESET}"
        self.boardInstance.board[i + x][j + y] = f"{RED}{option}{RESET}"
        info += f"♞ na [{i}][{j}]\t szachuje {option} na [{i + x}][{j + y}]\n"

    def isSafe(self, i, j, x, y):
        if (i + x >= 0 and i + x < len(self.boardInstance.board)) and (
            j + y >= 0 and j + y < len(self.boardInstance.board)
        ):
            return True
        return False

    def getChecked(self):
        moves = [[1, 2], [2, 1], [-1, 2], [-2, 1], [-1, -2], [-2, -1], [1, -2], [2, -1]]

        for i in range(0, len(self.boardInstance.board)):
            for j in range(0, len(self.boardInstance.board[i])):
                if (
                    self.boardInstance.board[i][j] == f"{GREEN}♞{RESET}"
                    or self.boardInstance.board[i][j] == f"{RED}♞{RESET}"
                ):  # Tutaj wybiera też czerwone skoczki bo czerwony może szachować jakiegoś hetmana jeszcze.
                    for (
                        x,
                        y,
                    ) in (
                        moves
                    ):  # duplikaty się NIE robią bo w sprawdzaniu jest ustawiony "zielony skoczek" :)
                        if self.isSafe(i, j, x, y):
                            if self.doesCheck(i, j, x, y, "♞") == True:
                                self.markChecked(i, j, x, y, "♞")
                            elif self.doesCheck(i, j, x, y, "♛") == True:
                                self.markChecked(i, j, x, y, "♛")
                            elif self.doesCheck(i, j, x, y, "♝") == True:
                                self.markChecked(i, j, x, y, "♝")
        return self.boardInstance.board


def start():
    os.system("cls")

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
                os.system("cls")
                print("Podaj poprawną opcję!")
        except ValueError:
            os.system("cls")
            print("Podaj poprawną opcję!")

    os.system("cls")
    b = Board(10)
    h = Hetman(f"{GREEN}♛{RESET}", 2, b)
    s = Skoczek(f"{GREEN}♞{RESET}", 5, b)
    g = Goniec(f"{GREEN}♝{RESET}", 3, b)
    hetmanPlacement = h.placeOnBoard()
    knightPlacement = s.placeOnBoard()
    bishopPlacement = g.placeOnBoard()

    print("┌──────────────────┐")
    print(f"│  Wybrałeś {user_option}      │")
    print("└──────────────────┘")
    if user_option == 1:
        s.getChecked()
        print(s.drawTab())
        print(info)
    elif user_option == 2:
        g.checkTakeDown(s.cords, h.cords)
        print(g.drawTab())
        print(info)
    elif user_option == 3:
        h.checkTakeDown(s.cords, g.cords)
        print(h.drawTab())
        print(info)


if __name__ == "__main__":
    start()


# Test Cases
# TODO
