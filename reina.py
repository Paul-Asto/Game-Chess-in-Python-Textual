from piece import PieceChess, AdminObjetives
from mov_piece import MovPiece



class Reina(PieceChess):
    def __init__(self, army = None):
        super().__init__(army)
        self.char = chr(9813)

        self.admin_obj = AdminObjetives(
            MovPiece(self, (0, 1), True),
            MovPiece(self, (0, -1), True),
            MovPiece(self, (-1, 0), True),
            MovPiece(self, (1, 0), True),
            MovPiece(self, (-1, -1), True),
            MovPiece(self, (-1, 1), True),
            MovPiece(self, (1, -1), True),
            MovPiece(self, (1, 1), True),    
        )