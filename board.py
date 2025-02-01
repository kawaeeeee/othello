from typing import List, Dict, Tuple, Optional, Union


class Board:
    def __init__(self):
        self.board = [[0]*8 for i in range(8)]
        self.board[4][4] = 1
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1

    # 盤面表示
    def show_board(self):
        symbol = {1: "o", -1: "x", 0: "-"}
        for row in self.board:
            print(" ".join(symbol[cell] for cell in row))

    #置くことのできる位置のリスト取得
    def get_putable_places(self,player: int) -> List[Tuple[int,int]]:
        putable_places = []
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == 0:
                    if self.can_put(player, x, y):
                        putable_places.append((x,y))

        return putable_places
    
    #指定された位置が置くことができるか判定
    def can_put(self, player: int, x: int, y: int) -> bool:
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
        
        if self.board[temp_x][temp_y] == player * -1: #相手の石がある
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


    def proceed_state(self, player : int, place : Tuple[int,int]):
        x, y = place
        self.board[x][y] = player
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]

        for dx, dy in directions:
            self.flip_stones(player, x, y, dx, dy)

    def flip_stones(self, player: int, x: int, y: int, dx: int, dy: int):
        temp_x, temp_y = x + dx, y + dy
        stones_to_flip = []

        while 0 <= temp_x < 8 and 0 <= temp_y < 8:
            if self.board[temp_x][temp_y] == player * -1:
                stones_to_flip.append((temp_x,temp_y))
            elif self.board[temp_x][temp_y] == player:
                for flip_x, flip_y in stones_to_flip:
                    self.board[flip_x][flip_y] = player
                break
            else:
                break

            temp_x += dx
            temp_y += dy
    


currentPlayer = 1
board = Board()
board.show_board()
for step in range(60):
    print(f"currentPlayer: " + ("o" if currentPlayer == 1 else "x"))
    if len(board.get_putable_places(currentPlayer)) == 0:
        print("置ける場所がないです")
        break
    while(1):
        x = int(input("何行目に置くかを入力してください1~8 :"))
        y = int(input("何列目に置くかを入力してください1~8 :"))
        if(board.can_put(currentPlayer, x-1, y-1)):
            break
        else:
            print("そこには置けません")
    
    board.proceed_state(currentPlayer,(x-1,y-1))
    board.show_board()
    currentPlayer *= -1

