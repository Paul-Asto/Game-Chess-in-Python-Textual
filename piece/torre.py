from typing import TYPE_CHECKING
from constant import CHAR_VIEW_TORRE

from piece.piece import PieceChess
from piece.mov_piece import MovPieceSpreadable

if TYPE_CHECKING:
    from army import Army



class Torre(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)
        self.char = CHAR_VIEW_TORRE

        self.admin_obj.add_movs(
            MovPieceSpreadable(self, (0, 1)),
            MovPieceSpreadable(self, (0, -1)),
            MovPieceSpreadable(self, (-1, 0)),
            MovPieceSpreadable(self, (1, 0)),
        )

        