
console.log("Script is running")

let board = document.getElementById("chessBoard");
for (let i = 0; i < 64; i++) {
	let cell = document.createElement("div");
	if (Math.floor(i / 8) % 2 == i % 2) {
		cell.className = "white";
	} else {
		cell.className = "black";
	}
	board.appendChild(cell);
}

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

fetch('/initial-board')
	.then(response => response.json())
	.then(data => {
		console.log('Initial board data:', data);
	})
	.catch(error => console.error('There was an error fetching the initial board:', error));