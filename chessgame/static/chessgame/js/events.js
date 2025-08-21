// events.js
import { fetchLegalMoves } from "./chessUtils.js";

export function setupEventListeners(squares, gameState, makeMoveCallback) {
  squares.forEach((square, index) => {
    square.addEventListener("click", (event) => {
      handleSquareClick(event, index, squares, gameState, makeMoveCallback);
    });

    square.addEventListener("contextmenu", (event) => {
      event.preventDefault();
      clearHighlights(squares, gameState);
    });
  });
}

async function handleSquareClick(
  event,
  index,
  squares,
  gameState,
  makeMoveCallback
) {
  if (event.button !== 0) return;
  const { sourceSquare, currentFen } = gameState;
  const selectedSquare = squares[index];

  if (sourceSquare === null) {
    // Select source square
    gameState.sourceSquare = index;
    highlightSquare(index, squares, true);

    const destinations = await fetchLegalMoves(currentFen, index);
    const moveSquares = Object.keys(destinations).map(Number);

    moveSquares.forEach((destIndex) =>
      highlightSquare(destIndex, squares, true)
    );
    console.log(destinations);
  } else if (sourceSquare === index) {
    if (
      !selectedSquare.style.backgroundImage ||
      selectedSquare.style.backgroundImage === "none"
    ) {
      console.log("No piece found on square:", index);
      return;
    }

    // Unselect source square
    gameState.sourceSquare = null;
    clearHighlights(squares, gameState);
    // highlightSquare(index, squares, false);
    console.log("Source square unselected:", index);
  } else {
    // Select destination square and make a move
    gameState.destinationSquare = index;
    highlightSquare(index, squares, true);
    console.log("Destination square selected:", index);

    // Trigger move callback
    makeMoveCallback(
      sourceSquare,
      gameState.destinationSquare,
      squares,
      gameState
    );

    // Clear highlights after move
    clearHighlights(squares, gameState);
  }
}

function highlightSquare(index, squares, highlight) {
  squares[index].classList.toggle("highlight", highlight);
}

function clearHighlights(squares, gameState) {
  squares.forEach((square) => {
    square.classList.remove("highlight");
  });
  gameState.sourceSquare = null;
  gameState.destinationSquare = null;
}
