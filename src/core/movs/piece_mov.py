from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Self

if TYPE_CHECKING:
    from src.core.square import Square
    from src.core.piece import PieceChess


class PieceMov(ABC):
    is_spreadable: bool 
    is_offensive: bool 
    is_occupiable: bool 
    is_active: bool
    
    piece: "PieceChess"
    value: tuple[int, int]
    
    @abstractmethod
    def get_opposite(self)  -> Self: ...
    
    @abstractmethod
    def copy(self, piece: Optional["PieceChess"] = None)  -> Self: ...
    
    
    @abstractmethod
    def register(self): ...
    
    
    @abstractmethod
    def clear_register(self): ...
    
    
    @abstractmethod
    def handle_register_piece(self, square: "Square") -> None: ...
    
    
    @abstractmethod
    def handle_register_empty(self, square: "Square") -> None: ...
    
    
    @abstractmethod
    def execute(self, square_obj: "Square", is_kiler_mov: bool) -> None: ...
