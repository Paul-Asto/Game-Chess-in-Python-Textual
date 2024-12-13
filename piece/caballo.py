from typing import TYPE_CHECKING

from piece.piece import PieceChess
from piece.mov_piece import MovPiece

if TYPE_CHECKING:
    from army import Army



class Caballo(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.char = chr(9816)
        
        self.admin_obj.add_movs(
            MovPiece(self, (2, 1)),
            MovPiece(self, (2, -1)),
            MovPiece(self, (-1, 2)),
            MovPiece(self, (1, 2)),
            MovPiece(self, (-2, -1)),
            MovPiece(self, (-2, 1)),
            MovPiece(self, (-1, -2)),
            MovPiece(self, (1, -2)),
        )