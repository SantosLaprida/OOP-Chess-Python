from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')

import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar, ActionButton, ActionView, ActionPrevious
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.actionbar import ActionDropDown, ActionGroup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.actionbar import ActionOverflow, ActionButton, ActionGroup

from chessboard.boardutils import BoardUtils, NUM_SQUARES
from chessboard.board import Board
from .panels import SquarePanel, BoardPanel


from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


class ChessApp(App):
    def build(self):
        # Create standard board
        board = Board.create_standard_board()
        

        layout = FloatLayout()
        action_bar_layout = BoxLayout(size_hint=(1, None), height=50, pos_hint={'top': 1})
        action_bar = ActionBar(pos_hint={'top': 1})
        action_view = ActionView()
        action_previous = ActionPrevious(title="ChessApp", with_previous=False)
        action_view.add_widget(action_previous)
        
        # create ActionOverflow (the three vertical dots button)
        action_overflow = ActionOverflow()

        # create ActionButton for the Exit option
        exit_button = ActionButton(text="Exit", on_release=exit)

        # create ActionGroup for the File menu and add the exit button to it
        file_menu = ActionGroup(text='File')
        file_menu.add_widget(exit_button)

        # add the file menu to the overflow
        action_overflow.add_widget(file_menu)

        # add the overflow to the action view
        action_view.add_widget(action_overflow)
        
        action_bar.add_widget(action_view)
        action_bar_layout.add_widget(action_bar)
        layout.add_widget(action_bar_layout)

        # Create BoardPanel and pass the standard board to it
        board_panel = BoardPanel(board, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        board_panel.board = board

        board_panel.assign_all_square_piece_icons()

        layout.add_widget(board_panel)

        return layout