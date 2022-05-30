# -*- coding: utf-8 -*-
"""
Created on Thu May 26 19:18:40 2022

@author: YeowHeng
"""
from random import Random

import Board
from Board import *
from Player import *
board = Board()

def game():
    print("Welcome to online tic tac toe!")
    ran = Random()
    p1 = Player(ran.choice(["X", "O"]))
    p2 = Player("")
    p2.symbol = "O" if p1.symbol == "X" else "X"
    p1.turn = ran.choice([True, False])
    p2.turn = True if p1.turn == False else False
    starting_msg = "Player 1, you go first" if p1.turn == 1 else "Player 2, you go first"
    print(f"Player 1: {p1.symbol}\nPlayer 2: {p2.symbol}\n{starting_msg}")
    empty_string = ""
    count = 0

    while not board.GameWinOrLose(count, empty_string):
        board.PrintBoard()
        count += 1
        empty_string = PlayerMove(p1, p2)


def PlayerMove(p1, p2):
    winner_string = ""
    row = int(input("Enter the row: "))
    column = int(input("Enter your position: "))
    if p1.turn:
        p1.move(column, row)
        while not board.CheckInBoard(row, column, p1):
            row = int(input("Enter the row: "))
            column = int(input("Enter your position: "))
        board.SetPlayerInBoard(row, column, p1)
        p1.turn = False
        p2.turn = True

    else:
        p2.move(column, row)
        while not board.CheckInBoard(row, column, p2):
            row = int(input("Enter the row: "))
            column = int(input("Enter your position: "))
        board.SetPlayerInBoard(row, column, p2)
        p2.turn = False
        p1.turn = True

    winner_string += board.DiagonalWin()
    winner_string += board.VerticalWin(column)
    winner_string += board.HorizontalWin()

    if winner_string == " ":
        nextTurn = "Player 2, it is your turn." if p1.turn == False else "Player 1, it is your turn."
        print(nextTurn)

    return winner_string

game()
