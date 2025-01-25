import { getCSRFToken } from "./utils.js";

const fen_length = 6;

const pieceTypeMapping = {
  R: "ROOK",
  N: "KNIGHT",
  B: "BISHOP",
  Q: "QUEEN",
  K: "KING",
  P: "PAWN",
};

const pieceAllianceMapping = {
  WHITE: "w",
  BLACK: "b",
};

export function getFormattedPieceType(pieceType, imageType) {
  // TODO: Implement this function

  return;
}

export async function fetchLegalMoves(fen, sourceSquare) {
  try {
    const response = await fetch("/get-legal-moves/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({ fen, sourceSquare }),
    });

    const data = await response.json();

    if (data.status === "success") {
      return data.destinations;
    } else {
      console.error("Failed to fetch legal moves:", data.message);
    }
  } catch (error) {
    console.error("Error fetching legal moves:", error);
  }
}

export function getPieceImageUrlSVG(pieceType, alliance) {
  // Convert alliance to lowercase for the filename format
  let formattedAlliance = pieceAllianceMapping[alliance];

  // Since the pieceType is a single character, convert it to the full piece name in uppercase
  let formattedPieceType = pieceType.toLowerCase();

  // console.log("Debbuging");
  // console.log(formattedAlliance);
  // console.log(formattedPieceType);

  return `/static/chessgame/chess_pieces_images/1echecs-svg-main/svg/${formattedAlliance}${formattedPieceType}.svg`;
}

export function getPieceImageUrl(pieceType, alliance) {
  // Get the URL of the image for the given piece type and alliance

  // Convert alliance to lowercase for the filename format
  let formattedAlliance = alliance.toLowerCase();

  // Since the pieceType is a single character, convert it to the full piece name in uppercase
  let formattedPieceType = pieceTypeMapping[pieceType];

  return `/static/chessgame/chess_pieces_images/${formattedAlliance}PieceType.${formattedPieceType}.png`;
}

export function processFen(fen, position = 0) {
  // Initialize the board state (dictionary with keys as positions and values as piece info (array with piece type and alliance)
  let board_data = {};

  // Split the FEN to extract different parts
  const fenParts = fen.split(" ");
  const fenString = fenParts[0];
  const activePlayer = fenParts[1]; // "w" for white, "b" for black

  // Loop through fenString to set up board data
  for (let character of fenString) {
    if (character === "/") {
      continue;
    }

    if (isNaN(character)) {
      // Character is a piece
      let pieceColor;
      if (character === character.toUpperCase()) {
        pieceColor = "WHITE";
      } else {
        pieceColor = "BLACK";
      }
      board_data[position] = [character.toUpperCase(), pieceColor];
      position += 1;
    } else {
      // Character is a number representing empty squares
      position += parseInt(character);
    }
  }

  // Return both board data and the active player
  return {
    board_data: board_data,
    activePlayer: activePlayer === "w" ? "WHITE" : "BLACK",
  };
}

export function highlightLegalMoves(fen, sourceSquare) {
  // TODO implement this function
  return;
}
