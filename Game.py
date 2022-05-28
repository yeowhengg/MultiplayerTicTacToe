# -*- coding: utf-8 -*-
"""
Created on Thu May 26 19:18:40 2022

@author: YeowHeng
"""
from random import Random

from Board import *
from Player import *



def game():
    print("Welcome to online tic tac toe!")
    board = Board()
    ran = Random()
    p1 = Player(ran.choice(["X", "O"]))
    p2 = Player("")
    p2.symbol = "O" if p1.symbol == "X" else "X"
    p1.turn = ran.choice([True, False])
    p2.turn = True if p1.turn == False else False
    starting_msg = "Player 1, you go first" if p1.turn == 1 else "Player 2, you go first"
    print(f"Player 1: {p1.symbol}\nPlayer 2: {p2.symbol}\n{starting_msg}")

    while True:
        PlayerMove(p1, p2)


def PlayerMove(p1, p2):
    move = int(input("Enter your position: "))

    if p1.turn:
        p1.move(move)
        p1.turn = False
        p2.turn = True
        board.Board.SetPlayerInBoard(board, move, p1)
    else:
        p2.move(move)
        p2.turn = False
        p1.turn = True
        board.Board.SetPlayerInBoard(board, move, p2)

    nextTurn = "Player 2, it is your turn." if p1.turn == False else "Player 1, it is your turn."
    print(nextTurn)


game()
