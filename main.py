from chessboard.square import Square
from chessboard.board import Board
from gui.table import ChessApp

def main():
    initial_board = Board.create_standard_board()

    print(initial_board)




if __name__ == '__main__':
    ChessApp().run()


