from piece import PieceChess, AdminObjetives
from mov_piece import MovPiece



class Alfil(PieceChess):
    def __init__(self, army = None):
        super().__init__(army)

        self.char = chr(9815)

        self.admin_obj = AdminObjetives(
            MovPiece(self, (-1, -1), True),
            MovPiece(self, (-1, 1), True),
            MovPiece(self, (1, -1), True),
            MovPiece(self, (1, 1), True),
        )

