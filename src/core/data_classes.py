from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.core.coordinate import Coord
    from src.core.piece import PieceChess
    from src.core.movs.piece_mov import PieceMov


@dataclass
class DataPawn:
    
    direction: int 
    index_column_meta: int 
    
    double_frontal_mov: "PieceMov"
    frontal_mov: "PieceMov"
    
    is_passant: bool = False


@dataclass
class DataArmy:
    king: Optional[tuple["Coord", "PieceChess"]]
    pieces: list[tuple["Coord", "PieceChess"]]


@dataclass
class PawnDirectionData:
    direction: int
    index_goal_column: int

