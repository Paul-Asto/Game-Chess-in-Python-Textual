
from src.core.coordinate import CardinalPair, Coord
from typing import TYPE_CHECKING, Self, Optional
from src.core.movs.piece_mov import PieceMov
from src.core.types import ObjetiveChess

if TYPE_CHECKING:
    from src.core.coordinate import Coord
    from src.core.piece import PieceChess
    from src.core.square import Square



class ShortMov(CardinalPair, PieceMov):
    is_spreadable: bool = False
    is_offensive: bool = True
    is_occupiable: bool = True
    is_active: bool = True
    
    def __init__(self, piece: "PieceChess", mov: tuple[int, int]) -> None:
        super().__init__(mov[0], mov[1])
        self.piece: "PieceChess" = piece
    
    def get_opposite(self) -> Self:
        return self.__class__(self.piece, (- self.y, - self.x))
    
    def copy(self, piece: Optional["PieceChess"] = None)  -> Self:
        new_piece: "PieceChess" = self.piece if piece ==  None else piece
        return self.__class__(new_piece, self.value)
    
    
    def register(self) -> None:
        coord: Coord = self.piece.coord + self
        square: Optional["Square"] = self.piece.board.get_square(coord)
        
        if square == None:
            return
        
        if square.piece == None:
            self.handle_register_empty(square)
            return
        
        self.handle_register_piece(square)
    
    
    def handle_register_piece(self, square: "Square") -> None:
        if square.piece is None:
            return
        
        condition: bool = not self.piece.is_equals_class(square.piece.clase)
        tipo: ObjetiveChess = ObjetiveChess.ENEMY if condition else ObjetiveChess.INVALID
        
        self.piece.add_coord_objetive(self, square.coord, tipo)
        square.add_mov_prowl(self)
    
    
    def handle_register_empty(self, square: "Square") -> None:
        tipo: ObjetiveChess = ObjetiveChess.EMPTY
        
        self.piece.add_coord_objetive(self, square.coord, tipo)
        square.add_mov_prowl(self)
    
    
    def clear_register(self) -> None:
        for coord in self.piece.square.admin_objetives.get_coords_off_mov(self):
            square: Optional["Square"] = self.piece.board.get_square(coord)
            if not square is None:
                square.deleted_mov_prowl(self)
        
        self.piece.square.admin_objetives.clear_store_off_mov(self)
    
    
    def execute(self, square_obj: "Square", is_kiler_mov: bool) -> None:
        square_start: "Square" = self.piece.square
        
        square_start.deliver_piece(square_obj)
