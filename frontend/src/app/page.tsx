"use client"

import Cell from "@/components/Cell";
import Board from "@/components/Board";
import { canMove, checkWinner, flipStones, initializeBoard } from "@/utils/gameLogic";
import React, { useEffect, useState } from "react";
import { BoardState, Player } from "@/utils/types";
import WinnerAnnouncement from "@/components/WinnerAnnouncement";

export default function Home() {
  const [board, setBoard] = useState<BoardState>(initializeBoard());
  const [currentPlayer, setCurrentPlayer] = useState<Player>("black");
  const [winner , setWinner] = useState<Player | null | 'draw'>(null);

  const handleCellClick = (row: number, col: number) => {
    const newBoard = flipStones(board, row, col, currentPlayer);
    if (newBoard) {
      setBoard(newBoard);
      const winner = checkWinner(newBoard);
      if (winner) {
        setWinner(winner);
      }else{
        setCurrentPlayer(currentPlayer === "black" ? "white" : "black");
      }
    }
  }

  const handleWinnerDismis = () => {
    setWinner(null);
    setBoard(initializeBoard());
    setCurrentPlayer("black");
  };

  useEffect(() => {
    if (winner === null && !canMove(board, currentPlayer)){
      alert(`${currentPlayer}はパスします`);
      setCurrentPlayer(currentPlayer === "black" ? "white" : "black");
    }
  }, [board, currentPlayer, winner]);

  return (
    <div>
      <div className="container mx-auto p-8 bg-gray-100">
        <Board board={board} onCellClick={handleCellClick} />
        {winner && <WinnerAnnouncement winner={winner} onDismiss={handleWinnerDismis} />}
      </div>
      <div className="text-center mt-4">
        <h2 className="text-xl font-bold">Current Player: {currentPlayer}</h2>
      </div>
    </div>
  );
};