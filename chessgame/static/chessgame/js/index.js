console.log("Script is running");

let board = document.getElementById("chessBoard");

let squares = [];

for (let i = 0; i < 64; i++) {
	let cell = document.createElement("div");
	if (Math.floor(i / 8) % 2 == i % 2) {
		cell.className = "white";
	} else {
		cell.className = "black";
	}
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

fetch("/initial-board")
	.then((response) => response.json())
	.then((data) => {
		console.log("Initial board data:", data);

		// Loop through the board data
		for (let position in data) {
			let pieceInfo = data[position]; // [pieceType, allianUse CSS to Control Image Sizing:ce]
			let imageUrl = getPieceImageUrl(pieceInfo[0], pieceInfo[1]);

			// Set the background image of the board cell
			let cell = board.children[position];
			cell.style.backgroundImage = `url('${imageUrl}')`;
		}
	})
	.catch((error) =>
		console.error("There was an error fetching the initial board:", error)
	);

function getPieceImageUrl(pieceType, alliance) {
	// Convert alliance to lowercase for the filename format
	let formattedAlliance = alliance.toLowerCase();

	// Since the pieceType is a single character, convert it to the full piece name in uppercase
	let formattedPieceType = {
		R: "ROOK",
		N: "KNIGHT",
		B: "BISHOP",
		Q: "QUEEN",
		K: "KING",
		P: "PAWN",
	}[pieceType];

	return `/static/chessgame/chess_pieces_images/${formattedAlliance}PieceType.${formattedPieceType}.png`;
}
function darVueltaTablero() {
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
