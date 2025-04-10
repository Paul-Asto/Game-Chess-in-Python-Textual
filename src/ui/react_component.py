from src.core.square import Square
from typing import TYPE_CHECKING

from src.observer_interface import Observed

if TYPE_CHECKING:
    from src.core.piece import PieceChess


class ReactScuare(Square, Observed):

    def __init__(self, coord, ficha):
        Observed.__init__(self)
        super().__init__(coord, ficha)

    @property
    def ficha(self) -> "PieceChess": 
        return self.sealed_ficha
    
    @ficha.setter
    def ficha(self, value: "PieceChess") -> None: 
        self.sealed_ficha = value
        self.sealed_ficha.scuare = self

        self.report_changes() # Metodo de reporte a observers