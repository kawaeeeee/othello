import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import List, Dict, Tuple, Optional, Union

class OthelloEnv(gym.Env):
    def __init__(self):
        super(OthelloEnv, self).__init__()

        #8x8の盤面
        self.board = np.zeros((8,8), dtype=int)
        self.board[3][3], self.board[4][4] = 1, 1
        self.board[3][4], self.board[4][3] = -1, -1

        #行動空間: 8x8のマス
        self.action_space = spaces.Discrete(64)

        #観測空間: 8x8の盤面の状態
        self.observation_space = spaces.Box(low=-1, high=1, shape=(8, 8), dtype=int)

        self.current_player = 1 #1:先手, -1:後手

    def reset(self, seed=None) -> np.ndarray:
        super().reset(seed=seed)

        self.board = np.zeros((8,8), dtype=int)
        self.board[3][3], self.board[4][4] = 1, 1
        self.board[3][4], self.board[4][3] = -1, -1

        self.current_player = 1
        return self.board
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        x, y = divmod(action, 8)

        if not self.is_valid_move(self.current_player, x, y):
            return self.board, -100, False, False, {} #不正な手を打った場合：報酬-1
        
        #石を置く
        self.place_stone(self.current_player, x, y)

        reward = np.sum(self.board == self.current_player) - np.sum(self.board == -self.current_player)

        done = self.is_full() or len(self.get_valid_moves(-self.current_player)) == 0

        self.current_player *= -1

        return self.board, reward, done, False, {}


    #盤面の状態を表示
    def render(self):
        symbols = {1: "o", -1: "x", 0: "-"}
        for row in self.board:
            print(" ".join(symbols[cell] for cell in row))
        print()

    #指定された位置に石を置くことができるか判定
    def is_valid_move(self, player: int, x: int, y: int) -> bool:
        if self.board[x][y] != 0:
            return False
        
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        for dx, dy in directions:
            if self.check_direction(player, x, y, dx, dy):
                return True
        return False

    #指定された位置、方向で、ひっくり返すことができるか判定
    def check_direction(self, player: int, x: int, y: int, dx: int, dy: int) -> bool:
        temp_x, temp_y = x + dx, y + dy
        if not (0 <= temp_x < 8 and 0<= temp_y < 8):
            return False
        
        if self.board[temp_x][temp_y] != -player: #相手の石がある
            return False
        
        while 0 <= temp_x < 8 and 0 <= temp_y < 8:
            temp_x += dx
            temp_y += dy
            if not (0 <= temp_x < 8 and 0<= temp_y < 8):
                return False
            if self.board[temp_x][temp_y] == player:
                return True
            elif self.board[temp_x][temp_y] == 0:
                return False
        return False
    
    #石を置き、状態を更新 
    def place_stone(self, player: int, x: int, y: int):
        self.board[x][y] = player
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]

        for dx, dy in directions:
            self.flip_stones(player, x, y, dx, dy)

    #石をひっくり返す
    def flip_stones(self, player: int, x: int, y: int, dx: int, dy: int):
        temp_x, temp_y = x + dx, y + dy
        stones_to_flip = []

        while 0 <= temp_x < 8 and 0 <= temp_y < 8:
            if self.board[temp_x][temp_y] == -player:
                stones_to_flip.append((temp_x,temp_y))
            elif self.board[temp_x][temp_y] == player:
                for flip_x, flip_y in stones_to_flip:
                    self.board[flip_x][flip_y] = player
                break
            else:
                break

            temp_x += dx
            temp_y += dy

    #盤面が埋まっているか判定
    def is_full(self) -> bool:
        return np.all(self.board != 0)
    
    def is_game_over(self) -> bool:
        return len(self.get_)
    
    def get_valid_moves(self, player: int) -> List[int]:
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if self.is_valid_move(player, x, y):
                    valid_moves.append(x*8 + y)
        return valid_moves