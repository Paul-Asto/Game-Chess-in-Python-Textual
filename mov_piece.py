from coord import AbstractCoord
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from piece import PieceChess



class MovPiece(AbstractCoord):
    def __init__(self, ficha: "PieceChess", mov: tuple, is_spreadable: bool = False, is_occupiable: bool = True, is_offensive: bool = True):
        super().__init__(mov[0], mov[1])

        self.ficha: PieceChess = ficha

        self.is_spreadable: bool = is_spreadable
        self.is_occupiable: bool = is_occupiable
        self.is_ofensive: bool = is_offensive
    
    def GetOpuesto(self):
        return MovPiece(-(self.y), -(self.x))