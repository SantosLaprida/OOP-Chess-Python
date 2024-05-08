
const fen_length = 6;

const pieceTypeMapping = { 
	"R": "ROOK",
	"N": "KNIGHT",
	"B": "BISHOP",
	"Q": "QUEEN",
	"K": "KING",
	"P": "PAWN",
};

const pieceAllianceMapping = {
	"WHITE": 'w',
	"BLACK": 'b',
}

export function getFormattedPieceType(pieceType, imageType) {
	
	// TODO: Implement this function
	
	return;
}

export function getPieceImageUrlSVG(pieceType, alliance){

	// Convert alliance to lowercase for the filename format
	let formattedAlliance = pieceAllianceMapping[alliance];

	// Since the pieceType is a single character, convert it to the full piece name in uppercase
	let formattedPieceType = pieceType.toLowerCase();

	// console.log("Debbuging");
	// console.log(formattedAlliance);
	// console.log(formattedPieceType);

	return `/static/chessgame/chess_pieces_images/1echecs-svg-main/svg/${formattedAlliance}${formattedPieceType}.svg`;
	
}

export function getPieceImageUrl(pieceType, alliance) { // Get the URL of the image for the given piece type and alliance
	

	// Convert alliance to lowercase for the filename format
	let formattedAlliance = alliance.toLowerCase();

	// Since the pieceType is a single character, convert it to the full piece name in uppercase
	let formattedPieceType = pieceTypeMapping[pieceType];

	return `/static/chessgame/chess_pieces_images/${formattedAlliance}PieceType.${formattedPieceType}.png`;
}



export function processFen(fen, position = 0){

	// Initialize the board state (dictionary with keys as positions and values as piece info (array with piece type and alliance)
	let board_data = {};
	// Loop through fenLength
	for (let i = 0; i < fen_length; i++){

		// loop through the first part of the fen string (before the space)
		if (i == 0){
			
			let fenString = fen.split(" ")[i];

			for(let character of fenString){

				// if the character is a /, continue
				if(character == '/'){
					continue;
				}

				if(isNaN(character)){
					// Character is a piece
					let pieceColor;
					if(character == character.toUpperCase()){
						pieceColor = "WHITE";
					}else{
						pieceColor = "BLACK";
					}
					board_data[position] = [character.toUpperCase(), pieceColor];
					position += 1;
				}
				
				else{
					// character is a number
					position += parseInt(character);
				}
			}
		}else{
			// TODO: Implement the second part of the fen string
		}
		
	}

	return board_data;
	

}

export function highlightLegalMoves(fen, sourceSquare){
	// TODO implement this function
	return;

}