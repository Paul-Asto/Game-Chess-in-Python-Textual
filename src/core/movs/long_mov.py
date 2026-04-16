from src.core.movs.short_mov import ShortMov
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.core.piece import PieceChess
    from src.core.square import Square
    from src.core.coordinate import Coord

class LongMov(ShortMov):
    
    def __init__(self, ficha: "PieceChess", mov: tuple[int, int]) -> None:
        super().__init__(ficha, mov)
        
        self.is_spreadable: bool = True
    
    
    def register(self) -> None:
        coord_current: Coord = self.piece.coord + self
        
        while True:
            square: Optional["Square"] = self.piece.board.get_square(coord_current)
            
            if square is None:
                return
            
            if not square.piece is None:
                self.handle_register_piece(square)
                break

            self.handle_register_empty(square)
            coord_current += self
