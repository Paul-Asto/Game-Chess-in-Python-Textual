from typing import TYPE_CHECKING, Generator
from constant import CHAR_VIEW_PEON, OBJ_ENEMY

from piece.piece import PieceChess
from piece.mov_piece import  MovPeonDoubleFrontal, MovPeonFrontal, MovPeonDiagonal, MovPeonPassant
from coord import Coord

if TYPE_CHECKING:
    from board import Board
    from army import Army
    


class Peon(PieceChess):
    orientacion: int
    is_passant: bool = False

    double_frontal_mov: MovPeonDoubleFrontal
    frontal_mov: MovPeonFrontal
    diagonal_left_mov: MovPeonDiagonal
    diagonal_right_mov: MovPeonDiagonal
    passant_left_mov: MovPeonPassant
    passant_right_mov: MovPeonPassant

    def __init__(self, orientacion: int , army: "Army" = None):
        super().__init__(army)
        
        self.str_fen = "p" 
        self.char = CHAR_VIEW_PEON
        self.orientacion = orientacion

        self.double_frontal_mov = MovPeonDoubleFrontal(self, (self.orientacion * 2, 0))
        self.frontal_mov =  MovPeonFrontal(self, (self.orientacion, 0))

        self.diagonal_left_mov = MovPeonDiagonal(self, (self.orientacion, -1))
        self.diagonal_right_mov = MovPeonDiagonal(self, (self.orientacion, 1))

        self.passant_left_mov = MovPeonPassant(self, (0, -1))
        self.passant_right_mov = MovPeonPassant(self, (0, 1))

        self.diagonal_left_mov.mov_off_passant = self.passant_left_mov
        self.diagonal_right_mov.mov_off_passant = self.passant_right_mov

        self.passant_left_mov.mov_off_final_position = self.diagonal_left_mov
        self.passant_right_mov.mov_off_final_position = self.diagonal_right_mov
    
        self.admin_obj.add_movs(
            self.frontal_mov,
            self.double_frontal_mov,
            
            self.diagonal_left_mov,
            self.diagonal_right_mov,

            self.passant_left_mov,
            self.passant_right_mov,
        )