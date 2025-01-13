import { initializeBoard, updateBoard } from "./board.js";
import { setupEventListeners } from "./events.js";
import { getCSRFToken } from "./utils.js"; // Move getCSRFToken to a utility file

let currentFen = "";
let currentPlayer = "WHITE";

async function fetchLegalMoves(fen) {
  try {
    const response = await fetch("/get-all-legal-moves/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({ fen }),
    });

    const data = await response.json();

    if (data.status === "success") {
      console.log("Legal moves:", data.fen);
    } else {
      console.error("Failed to fetch legal moves:", data.message);
    }
  } catch (error) {
    console.error("Error fetching legal moves:", error);
  }
}

async function initializeGame() {
  const board = document.getElementById("chessBoard");

  // Step 1: Initialize the board
  const squares = initializeBoard(board);

  // Step 2: Fetch initial board state from the backend
  try {
    const response = await fetch("/initial-board-fen");
    const data = await response.json();
    currentFen = data.fen;
    currentPlayer = data.currentPlayer;

    // Step 3: Update the board with the initial FEN
    updateBoard(currentFen, squares);

    // Step 4: Set up event listeners
    setupEventListeners(squares, { currentFen, currentPlayer }, (from, to) => {
      // Handle the move callback
      handleMove(from, to, squares);
    });

    console.log("Game initialized successfully.");
  } catch (error) {
    console.error("Failed to initialize the game:", error);
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
      await fetchLegalMoves(currentFen);
    } else {
      console.error("Invalid move:", data.message);
      alert("Invalid move. Try again.");
    }
  } catch (error) {
    console.error("Error processing the move:", error);
    alert("There was an error processing the move.");
  }
}

// Initialize the game
initializeGame();

// import {
//   getPieceImageUrl,
//   getPieceImageUrlSVG,
//   processFen,
// } from "./chessUtils.js";

// let currentFen = "";
// let currentPlayer = "WHITE";
// let board = document.getElementById("chessBoard");
// let squares = [];

// function getCSRFToken() {
//   let csrfToken = null;

//   // First, try to get the token from the cookie
//   const cookies = document.cookie.split(";");
//   for (let i = 0; i < cookies.length; i++) {
//     const cookie = cookies[i].trim();
//     if (cookie.startsWith("csrftoken=")) {
//       csrfToken = cookie.substring("csrftoken=".length, cookie.length);
//       break;
//     }
//   }

//   // If not found in cookie, look for it in the DOM
//   if (!csrfToken) {
//     const tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
//     if (tokenElement) {
//       csrfToken = tokenElement.value;
//     }
//   }

//   return csrfToken;
// }

// for (let i = 0; i < 64; i++) {
//   let cell = document.createElement("div");

//   cell.className = Math.floor(i / 8) % 2 === i % 2 ? "white" : "black";

//   board.appendChild(cell);
//   squares.push(cell);
// }

// let expand = () => {
//   let board = document.getElementById("chessBoard");
//   if (board.style.width < "80vh") {
//     board.style.width = "85vh";
//     board.style.height = "85vh";
//   } else {
//     board.style.width = "70vh";
//     board.style.height = "70vh";
//   }
// };

// function updateBoard(fen) {
//   console.log("Update board called");
//   squares.forEach((square) => {
//     square.style.backgroundImage = "";
//   });
//   const { board_data, activePlayer } = processFen(fen);
//   currentPlayer = activePlayer;

//   for (let position in board_data) {
//     let pieceInfo = board_data[position];
//     let imageUrl = getPieceImageUrlSVG(pieceInfo[0], pieceInfo[1]);
//     let cell = board.children[position];
//     cell.style.backgroundImage = `url('${imageUrl}')`;
//   }
// }

// fetch("/initial-board-fen")
//   .then((response) => response.json())
//   .then((data) => {
//     // Set the FEN and process it to get the board state and active player
//     currentFen = data.fen;
//     const { board_data, activePlayer } = processFen(currentFen);
//     currentPlayer = activePlayer;

//     updateBoard(currentFen);

//     window.chessBoard = board;
//   })
//   .catch((error) =>
//     console.error("There was an error fetching the initial board:", error)
//   );

// //*************************************// //TESTING

// function darVueltaTablero() {
//   console.log("Flip board called");

//   let chessBoard = document.getElementById("chessBoard");
//   chessBoard.classList.toggle("dadoVuelta");

//   // Recorre los hijos del tablero
//   for (let i = 0; i < chessBoard.children.length; i++) {
//     let tile = chessBoard.children[i];

//     // Obtener la imagen de fondo dentro de la casilla
//     let imageUrl = tile.style.backgroundImage;

//     // Si hay una imagen de fondo, rotarla
//     if (imageUrl) {
//       tile.style.transform =
//         tile.style.transform === "rotate(180deg) rotateY(180deg)"
//           ? "rotate(0deg) rotateY(0deg)"
//           : "rotate(180deg) rotateY(180deg)";
//     }
//   }
// }
// // Add the event listener at the end of the file
// document
//   .querySelector(".btnRotate")
//   .addEventListener("click", darVueltaTablero);

// // function checkIfSquareShouldBeHighlighted(squareIndex, callback) {

// // 	//let boardState = globalBoardState;

// // 	fetch('/check-highlight/', {
// //         method: 'POST',
// //         headers: {
// //             'Content-Type': 'application/json',
// //         },
// //         body: JSON.stringify({
// //             squareIndex: squareIndex,  // Pass the square index to the server
// //             boardState: boardState,
// //             currentPlayer: currentPlayer
// //         })
// //     })
// //     .then(response => response.json())
// //     .then(data => {
// //         if (callback && typeof callback === 'function') {
// //             callback(data.shouldHighlight);
// //         }
// //     })
// //     .catch(error => {
// //         console.error('Error:', error);
// //         if (callback && typeof callback === 'function') {
// //             callback(false);
// //         }
// //     });
// // 	}

// //***************************************************************************************************
// //***************************************************************************************************
// // CURRENTLY DOING
// //***************************************************************************************************
// //***************************************************************************************************

// let sourceSquare = null;
// let destinationSquare = null;

// squares.forEach((square, index) => {
//   // Right-click handling

//   square.addEventListener("contextmenu", function (event) {
//     event.preventDefault();
//     if (sourceSquare != null) {
//       squares.forEach((s, i) => {
//         console.log("Removing highlight from square: " + i);
//         s.classList.remove("highlight");
//       });
//       sourceSquare = null;
//       destinationSquare = null;
//     }
//   });

//   square.addEventListener("click", function (event) {
//     if (event.button !== 0) return;

//     // Left-click handling
//     if (sourceSquare === null) {
//       sourceSquare = index;
//       squares[index].classList.add("highlight");
//       console.log("Source square selected: " + index);
//     } else if (sourceSquare === index) {
//       // Unselect if the same square is clicked again
//       squares[index].classList.remove("highlight");
//       sourceSquare = null;
//       console.log("Source square unselected: " + index);
//     } else {
//       destinationSquare = index;
//       squares[index].classList.add("highlight");
//       console.log("Destination square selected: " + index);

//       let move = {
//         from: sourceSquare,
//         to: destinationSquare,
//         fen: currentFen,
//       };

//       // Send move to the backend
//       fetch("/make-move/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//           "X-CSRFToken": getCSRFToken(),
//         },
//         body: JSON.stringify(move),
//       })
//         .then((response) => response.json())
//         .then((data) => {
//           if (data.status === "success") {
//             // The move was successful, update the board with the new FEN
//             currentFen = data.fen; // Update the current FEN
//             updateBoard(currentFen); // Call the updateBoard function with the new FEN
//           } else {
//             console.error(data.message);
//             alert("Invalid move. Try again.");
//           }
//         })
//         .catch((error) => {
//           console.error("Error:", error);
//           alert("There was an error processing the move.");
//         });

//       squares[sourceSquare].classList.remove("highlight");
//       squares[destinationSquare].classList.remove("highlight");
//       sourceSquare = null;
//       destinationSquare = null;
//     }
//   });
// });

// // Prevent the default right-click menu
// document
//   .getElementById("chessBoard")
//   .addEventListener("contextmenu", (event) => event.preventDefault());
