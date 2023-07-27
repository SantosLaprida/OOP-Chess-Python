from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from chessboard.square import Square
from chessboard.board import Board
from gui.window import ChessApp

def main():
    initial_board = Board.create_standard_board()

    print(initial_board)




if __name__ == '__main__':
    main()
    ChessApp().run()


