import { getPieceImageUrlSVG, processFen } from "./chessUtils.js";

export function initializeBoard(boardElement) {
  const squares = [];
  for (let i = 0; i < 64; i++) {
    const cell = document.createElement("div");
    cell.className = Math.floor(i / 8) % 2 === i % 2 ? "white" : "black";
    boardElement.appendChild(cell);
    squares.push(cell);
  }
  return squares;
}

export function updateBoard(fen, squares) {
  console.log("Updating board with FEN:", fen);
  squares.forEach((square) => {
    square.style.backgroundImage = "";
  });

  const { board_data } = processFen(fen);

  for (let position in board_data) {
    const pieceInfo = board_data[position];
    const imageUrl = getPieceImageUrlSVG(pieceInfo[0], pieceInfo[1]);
    const cell = squares[position];
    cell.style.backgroundImage = `url('${imageUrl}')`;
  }
}
