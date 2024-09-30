import {
  getPieceImageUrl,
  getPieceImageUrlSVG,
  processFen,
} from "./chessUtils.js";

let currentFen = "";
let currentPlayer = "WHITE";
let board = document.getElementById("chessBoard");
let squares = [];

for (let i = 0; i < 64; i++) {
  let cell = document.createElement("div");

  cell.className = Math.floor(i / 8) % 2 === i % 2 ? "white" : "black";

  board.appendChild(cell);
  squares.push(cell);
}

let expand = () => {
  let board = document.getElementById("chessBoard");
  if (board.style.width < "80vh") {
    board.style.width = "85vh";
    board.style.height = "85vh";
  } else {
    board.style.width = "70vh";
    board.style.height = "70vh";
  }
};

fetch("/initial-board-fen")
  .then((response) => response.json())
  .then((data) => {
    // Set the FEN and process it to get the board state and active player
    currentFen = data.fen;
    const { board_data, activePlayer } = processFen(currentFen);
    currentPlayer = activePlayer;

    // Loop through the board data to set up the pieces
    for (let position in board_data) {
      let pieceInfo = board_data[position]; // [pieceType, alliance]
      let imageUrl = getPieceImageUrlSVG(pieceInfo[0], pieceInfo[1]);
      let cell = board.children[position];
      cell.style.backgroundImage = `url('${imageUrl}')`;
    }

    window.chessBoard = board;
  })
  .catch((error) =>
    console.error("There was an error fetching the initial board:", error)
  );

//*************************************// //TESTING

function darVueltaTablero() {
  console.log("Flip board called");

  let chessBoard = document.getElementById("chessBoard");
  chessBoard.classList.toggle("dadoVuelta");

  // Recorre los hijos del tablero
  for (let i = 0; i < chessBoard.children.length; i++) {
    let tile = chessBoard.children[i];

    // Obtener la imagen de fondo dentro de la casilla
    let imageUrl = tile.style.backgroundImage;

    // Si hay una imagen de fondo, rotarla
    if (imageUrl) {
      tile.style.transform =
        tile.style.transform === "rotate(180deg) rotateY(180deg)"
          ? "rotate(0deg) rotateY(0deg)"
          : "rotate(180deg) rotateY(180deg)";
    }
  }
}
// Add the event listener at the end of the file
document
  .querySelector(".btnRotate")
  .addEventListener("click", darVueltaTablero);

// function checkIfSquareShouldBeHighlighted(squareIndex, callback) {

// 	//let boardState = globalBoardState;

// 	fetch('/check-highlight/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//             squareIndex: squareIndex,  // Pass the square index to the server
//             boardState: boardState,
//             currentPlayer: currentPlayer
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (callback && typeof callback === 'function') {
//             callback(data.shouldHighlight);
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         if (callback && typeof callback === 'function') {
//             callback(false);
//         }
//     });
// 	}

//***************************************************************************************************
//***************************************************************************************************
// CURRENTLY DOING
//***************************************************************************************************
//***************************************************************************************************

let sourceSquare = null;
let destinationSquare = null;

//console.log(squares);

// // Right-click handling
// squares.forEach((square, index) => {
// 	square.addEventListener('contextmenu', function(event) {
// 		event.preventDefault();
// 		console.log("Right-clicked on square: " + index);
// 	});
// });

squares.forEach((square, index) => {
  // Right-click handling

  square.addEventListener("contextmenu", function (event) {
    event.preventDefault();
    if (sourceSquare != null) {
      squares.forEach((s, i) => {
        console.log("Removing highlight from square: " + i);
        s.classList.remove("highlight");
      });
      sourceSquare = null;
      destinationSquare = null;
    }
  });

  square.addEventListener("click", function (event) {
    if (event.button !== 0) return;

    // Left-click handling
    if (sourceSquare === null) {
      sourceSquare = index;
      squares[index].classList.add("highlight");
      console.log("Source square selected: " + index);
    } else if (sourceSquare === index) {
      // Unselect if the same square is clicked again
      squares[index].classList.remove("highlight");
      sourceSquare = null;
      console.log("Source square unselected: " + index);
    } else {
      destinationSquare = index;
      squares[index].classList.add("highlight");
      console.log("Destination square selected: " + index);

      // Send move to backend or handle it
      // Reset after processing the move

      let move = {
        from: sourceSquare,
        to: destinationSquare,
        fen: currentFen,
      };

      squares[sourceSquare].classList.remove("highlight");
      squares[destinationSquare].classList.remove("highlight");
      sourceSquare = null;
      destinationSquare = null;
    }
  });
});

// Prevent the default right-click menu
document
  .getElementById("chessBoard")
  .addEventListener("contextmenu", (event) => event.preventDefault());
