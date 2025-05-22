from src.core.square import Square
from src.core.army import Army
from typing import TYPE_CHECKING

from src.ui.observer_interface import Observed

if TYPE_CHECKING:
    from src.core.piece import PieceChess
    from src.core.types_chess import DataArmy
    from src.core.types_chess import ColorPiece


class ReactSquare(Square, Observed):

    def __init__(self, coord) -> None:
        Observed.__init__(self)
        super().__init__(coord)

    @property
    def piece(self) -> "PieceChess": 
        return self.sealed_piece
    
    @piece.setter
    def piece(self, value: "PieceChess") -> None:
        self.sealed_piece = value
        
        if value == None:
            self.admin_objetives.set_movs()

        else:
            self.admin_objetives.set_movs(*value.movs)

        self.report_changes() # # Metodo rectivo


class ReactArmy(Army, Observed):

    def __init__(self, data_army: "DataArmy", console_color: "ColorPiece" = "white", id_army: str | None = None) -> None:
        Observed.__init__(self)
        super().__init__(data_army, console_color, id_army)
        
    
    def add_piece_to_cemetery(self, piece: "PieceChess") -> None:
        super().add_piece_to_cemetery(piece)
        self.report_changes() # Metodo rectivo


    def clear_cemetery(self) -> None:
        super().clear_cemetery()
        self.report_changes() # Metodo rectivo
