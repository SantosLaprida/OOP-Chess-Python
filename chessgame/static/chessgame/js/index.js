import { initializeBoard, updateBoard } from "./board.js";
import { setupEventListeners } from "./events.js";
import { getCSRFToken } from "./utils.js"; // Move getCSRFToken to a utility file

let gameState = {
  currentFen: "",
  currentPlayer: "WHITE",
};

async function fetchInitialBoard(squares) {
  try {
    const response = await fetch("/initial-board-fen");
    const data = await response.json();

    gameState.currentFen = data.fen;
    gameState.currentPlayer = data.currentPlayer;

    updateBoard(gameState.currentFen, squares);

    setupEventListeners(squares, gameState, (from, to) => {
      // Handle the move callback
      handleMove(from, to, squares, gameState);
    });

  } catch (error) {
    console.error("Failed to initialize Initial Game position", error);
  }
}

async function handleMove(from, to, squares, gameState) {
  try {
    const move = { from, to, fen: gameState.currentFen };
    const response = await fetch("/make-move/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify(move),
    });

    const data = await response.json();

    if (data.status === "success") {
      gameState.currentFen = data.fen;
      updateBoard(gameState.currentFen, squares);
    }
  } catch (error) {
    console.error("Error processing the move:", error);
    alert("There was an error processing the move.");
  }
}

async function initializeGame() {
  const board = document.getElementById("chessBoard");

  // Step 1: Initialize the board
  const squares = initializeBoard(board);

  await fetchInitialBoard(squares);
}

// Initialize the game
initializeGame();
