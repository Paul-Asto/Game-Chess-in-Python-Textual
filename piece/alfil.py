from typing import TYPE_CHECKING

from piece.piece import PieceChess
from piece.mov_piece import MovPiece

if TYPE_CHECKING:
    from army import Army



class Alfil(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.char = chr(9815)

        self.admin_obj.add_movs(
            MovPiece(self, (-1, -1), True),
            MovPiece(self, (-1, 1), True),
            MovPiece(self, (1, -1), True),
            MovPiece(self, (1, 1), True),
        )

