from typing import TYPE_CHECKING
from constant import CHAR_VIEW_REINA

from piece.piece import PieceChess
from piece.mov_piece import MovPieceSpreadable

if TYPE_CHECKING:
    from army import Army



class Reina(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)
        self.char = CHAR_VIEW_REINA

        self.admin_obj.add_movs(
            MovPieceSpreadable(self, (0, 1)),
            MovPieceSpreadable(self, (0, -1)),
            MovPieceSpreadable(self, (-1, 0)),
            MovPieceSpreadable(self, (1, 0)),
            MovPieceSpreadable(self, (-1, -1)),
            MovPieceSpreadable(self, (-1, 1)),
            MovPieceSpreadable(self, (1, -1)),
            MovPieceSpreadable(self, (1, 1)),    
        )