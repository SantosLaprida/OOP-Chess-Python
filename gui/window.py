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
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color


from chessboard.boardutils import BoardUtils, NUM_SQUARES
from chessboard.board import Board
from .panels import SquarePanel, BoardPanel

class SideBar(GridLayout):
    def __init__(self, **kwargs):
        super(SideBar, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 5 # Adjust this value as per your requirement
        self.padding = 10
        self.spacing = 10
        self.bind(size=self._update_rect, pos=self._update_rect)

        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)  # set the color to grey
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Create the buttons for the sidebar
        preferences_button = Button(text='Preferences', size_hint_y=None, height=44)
        exit_button = Button(text='Exit', size_hint_y=None, height=44, on_press=exit)

        # Add buttons to the sidebar
        self.add_widget(preferences_button)
        self.add_widget(exit_button)
        # Add empty widgets to the remaining rows
        for _ in range(self.rows - 2):
            self.add_widget(Widget())

    # Update the size and position of the colored rectangle
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class ChessApp(App):
    def build(self):
        # Create standard board
        board = Board.create_standard_board()
        

        # Create the root layout
        root_layout = BoxLayout(orientation='horizontal')

        # Create the sidebar
        sidebar = SideBar(size_hint_x=0.2)  # Adjust this value to fit your needs
        
        root_layout.add_widget(sidebar)

        # Create BoardPanel and pass the standard board to it
        board_layout = BoxLayout(orientation='vertical')
        board_layout.add_widget(Widget(size_hint_y=0.2))  # Spacer at the top, taking up 20% of the height
        
        board_panel = BoardPanel(board, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        board_panel.board = board
        board_panel.assign_all_square_piece_icons()
        board_layout.add_widget(board_panel)
        
        board_layout.add_widget(Widget(size_hint_y=0.2))  # Spacer at the bottom, taking up 20% of the height
        
        root_layout.add_widget(board_layout)

        return root_layout



