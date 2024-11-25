import {
  getPieceImageUrl,
  getPieceImageUrlSVG,
  processFen,
} from "./chessUtils.js";

let currentFen = "";
let currentPlayer = "WHITE";
let board = document.getElementById("chessBoard");
let squares = [];

function getCSRFToken() {
  let csrfToken = null;

  // First, try to get the token from the cookie
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith("csrftoken=")) {
      csrfToken = cookie.substring("csrftoken=".length, cookie.length);
      break;
    }
  }

  // If not found in cookie, look for it in the DOM
  if (!csrfToken) {
    const tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    if (tokenElement) {
      csrfToken = tokenElement.value;
    }
  }

  return csrfToken;
}

for (let i = 0; i < 64; i++) {
  let cell = document.createElement("div");

  cell.className = Math.floor(i / 8) % 2 === i % 2 ? "white" : "black";

  let img = document.createElement("img");
  img.draggable = true;
  img.className = "piece"; // Optional for styling
  cell.appendChild(img);

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

function updateBoard(fen) {
  console.log("Update board called");
  const { board_data, activePlayer } = processFen(fen);
  currentPlayer = activePlayer;

  squares.forEach((square, index) => {
    const img = square.querySelector("img"); // Get the <img> tag inside the square
    const pieceInfo = board_data[index]; // Get the piece info for this square (if any)

    if (pieceInfo) {
      // If there is a piece on this square, set the image
      const imageUrl = getPieceImageUrlSVG(pieceInfo[0], pieceInfo[1]);
      img.src = imageUrl;
      img.style.visibility = "visible"; // Ensure the piece is visible
    } else {
      // If there is no piece on this square, clear the image
      img.src = ""; // Clear the src attribute
      img.style.visibility = "hidden"; // Hide the <img> tag
    }
  });
}

fetch("/initial-board-fen")
  .then((response) => response.json())
  .then((data) => {
    // Set the FEN and process it to get the board state and active player
    currentFen = data.fen;
    const { board_data, activePlayer } = processFen(currentFen);
    currentPlayer = activePlayer;

    updateBoard(currentFen);

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

let sourceSquare = null;
let destinationSquare = null;

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

      let move = {
        from: sourceSquare,
        to: destinationSquare,
        fen: currentFen,
      };

      // Send move to the backend
      fetch("/make-move/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(move),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            // The move was successful, update the board with the new FEN
            currentFen = data.fen; // Update the current FEN
            updateBoard(currentFen); // Call the updateBoard function with the new FEN
          } else {
            console.error(data.message);
            alert("Invalid move. Try again.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("There was an error processing the move.");
        });

      squares[sourceSquare].classList.remove("highlight");
      squares[destinationSquare].classList.remove("highlight");
      sourceSquare = null;
      destinationSquare = null;
    }
  });
});

squares.forEach((square, index) => {
  const img = square.querySelector("img");

  img.addEventListener("dragstart", (event) => {
    event.dataTransfer.setData("sourceSquare", index);
    event.dataTransfer.setData("fen", currentFen);
    img.classList.add("dragging");
  });

  img.addEventListener("dragend", () => {
    img.classList.remove("dragging");
  });

  square.addEventListener("dragover", (event) => {
    event.preventDefault();
  });
  square.addEventListener("drop", (event) => {
    event.preventDefault();

    const sourceSquare = parseInt(event.dataTransfer.getData("sourceSquare"));
    const fen = event.dataTransfer.getData("fen");
    const destinationSquare = index;

    // Create the move object
    const move = {
      from: sourceSquare,
      to: destinationSquare,
      fen: fen,
    };

    // Send the move to the backend
    fetch("/make-move/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify(move),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          // Update the board with the new FEN
          currentFen = data.fen; // Update the current FEN
          updateBoard(currentFen); // Call the updateBoard function
        } else {
          console.error(data.message);
          alert("Invalid move. Try again.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("There was an error processing the move.");
      });
  });
});

// Prevent the default right-click menu
document
  .getElementById("chessBoard")
  .addEventListener("contextmenu", (event) => event.preventDefault());
