import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from chessengine.chessboard.board import Board
from chessengine.gui.window import ChessApp

def main():
    initial_board = Board.create_standard_board()

    print(initial_board)




if __name__ == '__main__':
    main()
    ChessApp().run()


# python src/chessengine/gui/main.py