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
