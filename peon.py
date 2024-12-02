from piece import PieceChess, AdminObjetives
from mov_piece import MovPiece



class Peon(PieceChess):
    def __init__(self, army = None):
        super().__init__(army)
        
        self.char = chr(9817)
        self.orientacion: int = self.army.orientacion
    
        self.admin_obj = AdminObjetives(
            MovPiece(self, (self.orientacion, -1), is_occupiable = False),
            MovPiece(self, (self.orientacion, 0), is_offensive = False),
            MovPiece(self, (self.orientacion, 1), is_occupiable = False),
        )