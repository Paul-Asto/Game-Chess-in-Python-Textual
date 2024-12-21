from typing import TYPE_CHECKING, Generator
from constant import CHAR_VIEW_PEON, OBJ_ENEMY

from piece.piece import PieceChess
from piece.mov_piece import MovPiecePeon, MovPiecePeonDoubleFrontal, MovPiecePeonFrontal
from coord import Coord

if TYPE_CHECKING:
    from board import Board
    from army import Army
    


class Peon(PieceChess):
    orientacion: int
    initial_double_mov: MovPiecePeonDoubleFrontal
    frontal_mov: MovPiecePeonFrontal

    def __init__(self, orientacion: int , army: "Army" = None):
        super().__init__(army)
        
        self.char = CHAR_VIEW_PEON
        self.orientacion = orientacion
        self.initial_double_mov = MovPiecePeonDoubleFrontal(self, (self.orientacion * 2, 0), is_offensive = False)
        self.frontal_mov =  MovPiecePeonFrontal(self, (self.orientacion, 0), is_offensive = False)
    
        self.admin_obj.add_movs(
            MovPiecePeon(self, (self.orientacion, -1), is_occupiable = False),
            MovPiecePeon(self, (self.orientacion, 1), is_occupiable = False),
            self.frontal_mov,
            self.initial_double_mov,
        )