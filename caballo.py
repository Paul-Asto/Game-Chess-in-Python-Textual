from piece import PieceChess, AdminObjetives
from mov_piece import MovPiece



class Caballo(PieceChess):
    def __init__(self, army = None):
        super().__init__(army)

        self.char = chr(9816)
        
        self.admin_obj = AdminObjetives(
            MovPiece(self, (2, 1)),
            MovPiece(self, (2, -1)),
            MovPiece(self, (-1, 2)),
            MovPiece(self, (1, 2)),
            MovPiece(self, (-2, -1)),
            MovPiece(self, (-2, 1)),
            MovPiece(self, (-1, -2)),
            MovPiece(self, (1, -2)),
        )