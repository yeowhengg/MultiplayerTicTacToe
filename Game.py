# -*- coding: utf-8 -*-
"""
Created on Thu May 26 19:18:40 2022

@author: YeowHeng
"""
from random import Random
from Player import *
from Board import *


def game():
    print("Welcome to online tic tac toe!")
    board = Board()
    ran = Random()
    p1 = Player(ran.choice(["X", "O"]))
    p2 = Player("")

    if p1.symbol == 'X':
        p2.symbol = "O"
    else:
        p2.symbol = "X"

    print(f"Player 1: {p1.symbol}")
    print(f"Player 2: {p2.symbol}")


game()
