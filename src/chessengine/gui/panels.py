import os

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar, ActionButton, ActionView, ActionPrevious
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image

from chessengine.chessboard.boardutils import BoardUtils, NUM_SQUARES
from chessengine.chessboard.move import MoveFactory, NoneMove
from chessengine.players.move_transition import MoveTransition



class SquarePanel(FloatLayout):
    def __init__(self, board_panel, square_id, **kwargs):
        super().__init__(**kwargs)
        self.board_panel = board_panel
        self.square_id = square_id
        self.highlighted = False
        self.button = Button(background_normal='', 
                             background_color=self.assign_color(),
                             size_hint=(1, 1),
                             pos_hint={'x': 0, 'y': 0})
        self.add_widget(self.button)
        self.piece_image = None
        self.button.bind(on_release=self.on_touch_down)


    def assign_color(self):
        row = self.square_id // 8
        col = self.square_id % 8
        return [0.8, 0.5, 0.2, 1] if (row + col) % 2 else [1, 0.9, 0.7, 1] 
    
    def update_color(self):
        if self.highlighted:
            self.button.background_color = [0, 1, 0, 1]  # green highlight
        else:
            self.button.background_color = self.assign_color()

    def assign_square_piece_icon(self, board):
        if board.get_square(self.square_id).is_square_occupied():
            piece = board.get_square(self.square_id).get_piece()
            piece_alliance = "white" if piece.get_piece_alliance().is_white() else "black"
            piece_type = piece.get_piece_type()
            image_file = f"{piece_alliance}{piece_type}.png"
            image_path = os.path.join('chess_pieces_images', image_file)

            if os.path.exists(image_path):
                if self.piece_image:   # Check if an image already exists
                    self.remove_widget(self.piece_image)  # Remove the old image
                self.piece_image = Image(source=image_path,
                        allow_stretch=True,
                        keep_ratio=True,
                        size_hint=(1, 1),
                        pos_hint={'center_x': .5, 'center_y': .5})
                self.add_widget(self.piece_image)   # Add the new image
            else:
                print(f"Image file not found: {image_path}")
        else:
            if self.piece_image:  # If an image exists on the square
                self.remove_widget(self.piece_image)  # Remove it
                self.piece_image = None  # Reset piece_image to None


    def on_touch_down(self, touch):

        # check if the click was inside this widget
        if not self.collide_point(*touch.pos):
            return False

        if touch.button == 'right':
            
            self.board_panel.source_square = None
            self.board_panel.destination_square = None
            self.board_panel.unhighlight_all_squares()
            self.highlighted = False
            
            self.update_color()
            return True  # To make sure the event is not propagated further

        elif touch.button == 'left':
            
            board = self.board_panel.board

            if board.get_square(self.square_id).is_square_occupied():
                piece = board.get_square(self.square_id).get_piece()
                

            if self.board_panel.source_square is None:
                self.board_panel.source_square = board.get_square(self.square_id) # Assign source square
                self.board_panel.moved_piece = self.board_panel.source_square.get_piece() # Assign piece
                

                if self.board_panel.moved_piece is None:
                    self.board_panel.source_square = None
                else:
                    self.highlighted = True
                    self.update_color()
                    self.board_panel.source_square_panel = self
                    
            else:
                self.board_panel.destination_square = board.get_square(self.square_id) 
                
                current_legal_moves = board.get_current_player().legal_moves

                #Move implementation
                move = MoveFactory.create_move(self.board_panel.board,
                                               self.board_panel.source_square.get_square_coordinate(), 
                                               self.board_panel.destination_square.get_square_coordinate())

                if isinstance(move, NoneMove):
                    self.board_panel.source_square = None
                    self.board_panel.destination_square = None
                    self.board_panel.moved_piece = None
                    self.board_panel.source_square_panel = None 
                    self.board_panel.unhighlight_all_squares()
                    self.highlighted = False
                    self.update_color()
                    return True  # To make sure the event is not propagated further
                
                else:
                    move_transition = self.board_panel.board.get_current_player().make_move(move)

                    if move_transition.status == MoveTransition.MoveStatus.DONE:
                        self.board_panel.board = move_transition.get_transition_board()
                        self.board_panel.assign_all_square_piece_icons()
                        print("Move done")
                        fen = BoardUtils.generate_fen(self.board_panel.board)
                        print(fen)

                        print(self.board_panel.board)
                        current_player = self.board_panel.board.get_current_player()

                        print(f"Current player is: {current_player.get_alliance()}")

                        print(f"Is {current_player.get_alliance()} in check?")
                        print(current_player.is_in_check())


                    # Unhighlight the source square panel
                    self.board_panel.source_square_panel.highlighted = False
                    self.board_panel.source_square_panel.update_color()

                    self.board_panel.source_square = None
                    self.board_panel.destination_square = None
                    self.board_panel.moved_piece = None
                    self.board_panel.source_square_panel = None 

        return True  # To make sure the event is not propagated further 




class BoardPanel(GridLayout):
    def __init__(self, board, **kwargs):
        super().__init__(**kwargs)
        self.board = board
        self.cols = 8
        self.rows = 8
        self.size_hint = (0.5, 0.7)
        self.source_square = None
        self.destination_square = None
        self.moved_piece = None
        self.source_square_panel = None  
        

        for i in range(NUM_SQUARES):
            self.add_widget(SquarePanel(self, i))

    def assign_all_square_piece_icons(self):
        for square_panel in self.children:
            square_panel.assign_square_piece_icon(self.board)

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    def unhighlight_all_squares(self):
         for square_panel in self.children:
            square_panel.highlighted = False
            square_panel.update_color()