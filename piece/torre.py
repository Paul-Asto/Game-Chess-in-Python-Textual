from piece.piece import PieceChess, AdminObjetives
from mov_piece import MovPiece



class Torre(PieceChess):
    def __init__(self, army = None):
        super().__init__(army)
        self.char = chr(9814)

        self.admin_obj.add_movs(
            MovPiece(self, (0, 1), True),
            MovPiece(self, (0, -1), True),
            MovPiece(self, (-1, 0), True),
            MovPiece(self, (1, 0), True),
        )