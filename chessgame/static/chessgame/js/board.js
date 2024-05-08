import { square } from './square.js';


export class Board {

    constructor(){
        this.element = document.getElementById('chessBoard');
        this.squares = this.createSquares();
        this.squares.forEach(square => this.element.appendChild(square.element));
    }
    
    createSquares(){
        let squares = [];
        for(let i = 0; i < 64; i++){
            squares.push(new Square(i));
        }
        return squares;
    }

}