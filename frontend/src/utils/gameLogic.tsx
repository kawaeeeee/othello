import { CellValue, BoardState, Player } from "./types";

export const initializeBoard = (): BoardState => {
    const board: BoardState = Array.from({ length: 8 }, () => Array(8).fill(null));
    board[3][3] = "white";
    board[3][4] = "black";
    board[4][3] = "black";
    board[4][4] = "white";
    return board;
};

export const flipStones = (
    board: BoardState,
    row: number,
    col: number,
    player: Player
): BoardState | null => {
    if (board[row][col] !== null) return null;

    let canFlip = false;
    const directions = [
        [-1, 0], 
        [1, 0], 
        [0, -1], 
        [0, 1], 
        [-1, -1], 
        [-1, 1], 
        [1, -1], 
        [1, 1]
    ];
    const newBoard = board.map(row => [...row]); // Create a deep copy of the board

    directions.forEach(([dx, dy]) => {
        let x = row + dx;
        let y = col + dy;
        let stonesToFlip: [number, number][] = [];

        while(x >= 0 && x < 8 && y >= 0 && y < 8 && board[x][y] === (player === "black" ? "white" : "black")) {
            stonesToFlip.push([x, y]);
            x += dx;
            y += dy;
        }

        if (stonesToFlip.length > 0 && x >= 0 && x < 8 && y >= 0 && y < 8 && board[x][y] === player) {
            canFlip = true;
            stonesToFlip.forEach(([flipX, flipY]) => {
                newBoard[flipX][flipY] = player;
            });
        }
    });

    if (!canFlip) return null;

    newBoard[row][col] = player;
    return newBoard;

};


export const countStones = (bord: BoardState): { black: number; white: number } => {
    let black = 0, white = 0;
    bord.forEach(row => {
        row.forEach(cell => {
            if (cell === 'black') black++;
            else if (cell === 'white') white++;
        });
    });

    return { black, white };
}

export const canMove = (board: BoardState, player: Player): boolean => {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++){
            if (flipStones(board, row, col, player)) {
                return true;
            }
        }
    }

    return false;
}

export const checkWinner = (board: BoardState): Player | null | 'draw' => {
    const { black, white } = countStones(board);

    if (black + white === 64 || black === 0 || white === 0){
        if (black > white) return "black";
        else if (white > black) return "white";
        else return 'draw';
    }

    return null;
}