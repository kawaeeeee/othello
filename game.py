from board import Board
from typing import List, Dict, Tuple, Optional, Union
from player import Player, DQNPlayer, RandomPlayer
import random

class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = Player(1, "you")
        self.player2 = RandomPlayer(-1, "AI")
        self.turn = 1
        self.current_player = self.player1

    def switch_turn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play(self):
        print("ゲーム開始")
        self.board.show_board()
        end = False
        while not self.board.is_full():
            player_num = self.current_player.get_player_num()
            print(f"{self.current_player.name}のターンです. {self.current_player.name}の石は{self.board.get_player_stone(player_num)}です")
            move = self.current_player.get_action(self.board)
            if move is None:
                if self.board.count_stones(player_num) == 0:
                    print(f"{self.current_player.name}の負けです")
                    end = True
                    break
                else:
                    print(f"{self.current_player.name}はパスしました")
                    self.switch_turn()
                    continue
            else:
                self.board.proceed_state(player_num, move)
                self.board.show_board()
                self.switch_turn()

        if not end:
            if(self.board.count_stones(1) > self.board.count_stones(-1)):
                print(f"{self.player1.name}の勝ちです")
            elif(self.board.count_stones(1) < self.board.count_stones(-1)):
                print(f"{self.player2.name}の勝ちです")
            else:
                print("引き分けです")
        print("ゲーム終了")

if __name__ == "__main__":
    game = Game()
    game.play()
