
console.log("Script is running")

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


// Add "Hello" to the first square (index 0)
//squares[0].innerText = "Hello";

// loopear por casillas
// casilla con la casilla de initial board
// si esta ocupada, ver que pieza Y COLOR es
// poner la imagen de acuerdo a la pieza

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

// fetch('/initial-board')
// 	.then(response => response.json())
// 	.then(data => {

// 	})
// 	.catch(error => console.error('There was an error fetching the initial board:', error));

fetch('/initial-board')
    .then(response => response.json())
    .then(data => {
        console.log('Initial board data:', data);

        // Loop through the board data
        for (let position in data) {
            let pieceInfo = data[position];  // [pieceType, allianUse CSS to Control Image Sizing:ce]
            let imageUrl = getPieceImageUrl(pieceInfo[0], pieceInfo[1]);

            // Set the background image of the board cell
            let cell = board.children[position];
            cell.style.backgroundImage = `url('${imageUrl}')`;
        }
    })
    .catch(error => console.error('There was an error fetching the initial board:', error));

function getPieceImageUrl(pieceType, alliance) {
    // Convert alliance to lowercase for the filename format
    let formattedAlliance = alliance.toLowerCase();  
	
    // Since the pieceType is a single character, convert it to the full piece name in uppercase
    let formattedPieceType = {
        "R": "ROOK",
        "N": "KNIGHT",
        "B": "BISHOP",
        "Q": "QUEEN",
        "K": "KING",
        "P": "PAWN"
    }[pieceType];
	
    return `/static/chessgame/chess_pieces_images/${formattedAlliance}PieceType.${formattedPieceType}.png`;
}
	