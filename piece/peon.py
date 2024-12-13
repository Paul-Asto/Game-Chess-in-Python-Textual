from typing import TYPE_CHECKING

from piece.piece import PieceChess
from piece.mov_piece import MovPiece

if TYPE_CHECKING:
    from army import Army
    


class Peon(PieceChess):
    orientacion: int

    def __init__(self, orientacion: int, army: "Army" = None):
        super().__init__(army)
        
        self.char = chr(9817)
        self.orientacion = orientacion
        
    
        self.admin_obj.add_movs(
            MovPiece(self, (self.orientacion, -1), is_occupiable = False),
            MovPiece(self, (self.orientacion, 0), is_offensive = False),
            MovPiece(self, (self.orientacion, 1), is_occupiable = False),
        )
    