from board import Board
from typing import List, Dict, Tuple, Optional, Union
import random

class Player:
    def __init__(self, player: int, name: str = None):
        self.player = player
        self.name = name

    def get_player_num(self) -> int:
        return self.player

    def get_action(self, board: Board) -> Tuple[int,int]:
        if len(board.get_putable_places(self.player)) == 0:
            return None
        while(1):
            x = int(input("何行目に置くかを入力してください1~8 :"))
            y = int(input("何列目に置くかを入力してください1~8 :"))
            if(board.can_put(self.player, x-1, y-1)):
                break
            else:
                print("そこには置けません")
        return x-1, y-1
    

class RandomPlayer(Player):
    def get_action(self, board: Board) -> Tuple[int,int]:
        if len(board.get_putable_places(self.player)) == 0:
            return None
        putable_places = board.get_putable_places(self.player)
        return random.choice(putable_places)
    

class DQNPlayer(Player):
    def get_action(self, board: Board) -> Tuple[int,int]:
        if len(board.get_putable_places(self.player)) == 0:
            return None
        