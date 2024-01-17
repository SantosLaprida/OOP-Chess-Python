
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

		// Loop through the board data
		for (let position in data) {
			let pieceInfo = data[position]; // [pieceType, allianUse CSS to Control Image Sizing:ce]
			let imageUrl = getPieceImageUrl(pieceInfo[0], pieceInfo[1]);

			// Set the background image of the board cell
			let cell = board.children[position];
			cell.style.backgroundImage = `url('${imageUrl}')`;
		}

		window.chessBoard = board; 

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


//***************************************************************************************************
//***************************************************************************************************
// User handling
//***************************************************************************************************
//***************************************************************************************************




//***************************************************************************************************
//***************************************************************************************************
// CURRENTLY DOING
//***************************************************************************************************
//***************************************************************************************************












function checkIfSquareShouldBeHighlighted(squareIndex, callback) {
		
	//let boardState = globalBoardState;
	
	fetch('/check-highlight/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            squareIndex: squareIndex,  // Pass the square index to the server
            boardState: boardState,
            currentPlayer: currentPlayer
        })
    })
    .then(response => response.json())
    .then(data => {
        if (callback && typeof callback === 'function') {
            callback(data.shouldHighlight);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (callback && typeof callback === 'function') {
            callback(false);
        }
    });
	}

//***************************************************************************************************
//***************************************************************************************************
// CURRENTLY DOING
//***************************************************************************************************
//***************************************************************************************************
 































let sourceSquare = null;
let destinationSquare = null;

squares.forEach((square, index) => {
    square.addEventListener('click', function(event) {
        // Right-click handling
        if (event.button === 2) {
            if (sourceSquare !== null) squares[sourceSquare].classList.remove('highlight');
            sourceSquare = null;
            destinationSquare = null;
			
        } else {

            // Left-click handling
            if (sourceSquare === null) {
                sourceSquare = index;
                squares[index].classList.add('highlight');
                console.log("Source square selected: " + index);


            } else if (sourceSquare === index) {
                // Unselect if the same square is clicked again
                squares[index].classList.remove('highlight');
                sourceSquare = null;
                console.log("Source square unselected: " + index);


            } else {

                destinationSquare = index;
                squares[index].classList.add('highlight');
                console.log("Destination square selected: " + index);

                // Send move to backend or handle it
                // Reset after processing the move

                squares[sourceSquare].classList.remove('highlight');
                squares[destinationSquare].classList.remove('highlight');
                sourceSquare = null;
                destinationSquare = null;

            }
        }
    });
});

// Prevent the default right-click menu
document.getElementById("chessBoard").addEventListener('contextmenu', event => event.preventDefault());

