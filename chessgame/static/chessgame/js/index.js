import { initializeBoard, updateBoard } from "./board.js";
import { setupEventListeners } from "./events.js";
import { getCSRFToken } from "./utils.js"; // Move getCSRFToken to a utility file

let currentFen = "";
let currentPlayer = "WHITE";

async function fetchInitialBoard(squares) {
  try {
    const response = await fetch("/initial-board-fen");
    const data = await response.json();

    currentFen = data.fen;
    currentPlayer = data.currentPlayer;

    updateBoard(currentFen, squares);

    setupEventListeners(squares, { currentFen, currentPlayer }, (from, to) => {
      // Handle the move callback
      handleMove(from, to, squares);

      // console.log("Game initialized successfully.");
    });
  } catch (error) {
    console.error("Failed to initialize Initial Game position", error);
  }
}

async function handleMove(from, to, squares) {
  try {
    const move = { from, to, fen: currentFen };
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
      currentFen = data.fen;
      updateBoard(currentFen, squares); // Update the board
    } else {
      console.error("Invalid move:", data.message);
      alert("Invalid move. Try again.");
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
