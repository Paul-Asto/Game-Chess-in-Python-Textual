
from typing import TYPE_CHECKING
from src.core.types_chess import PromotioPiece
from src.core.pieces import (
    Reina,
    Caballo,
    Torre,
    Alfil,
)
from src.core.coordinate import Coord
from src.core.chess_exceptions import UCI_SintaxisError

if TYPE_CHECKING:
    from src.core.piece import PieceChess






index_chess_x: dict[str, int] = { 
    "a": 0,
    "b": 1,
    "c": 2, 
    "d": 3, 
    "e": 4, 
    "f": 5, 
    "g": 6, 
    "h": 7, 
}

index_fen_x: dict[int, str] = { 
    0: "a",
    1: "b",
    2: "c", 
    3: "d", 
    4: "e", 
    5: "f", 
    6: "g", 
    7: "h", 
}

index_chess_y: dict[str, str] = {
    "8": 0,
    "7": 1,
    "6": 2,
    "5": 3,
    "4": 4,
    "3": 5,
    "2": 6,
    "1": 7,
}



index_fen_y: dict[int, str] = {
    0: "8",
    1: "7",
    2: "6",
    3: "5",
    4: "4",
    5: "3",
    6: "2",
    7: "1",
}



class FormatUCI:
    is_promotion: bool = False
    class_promotion: type["PieceChess"] = None
    char_promotion: str = None

    def __init__(self, uci_str: str) -> None:
        # analyze UCI
        len_uci: int = len(uci_str)

        if len_uci != 4 and len_uci != 5:
            raise UCI_SintaxisError()
        
        try:
            xa: int = index_chess_x[uci_str[0].lower()]
            ya: int = index_chess_y[uci_str[1].lower()]
            xb: int = index_chess_x[uci_str[2].lower()]
            yb: int = index_chess_y[uci_str[3].lower()]

        except IndexError:
            raise UCI_SintaxisError()
        
        else:
            self.coord_start: Coord = Coord(ya, xa)
            self.coord_end: Coord = Coord(yb, xb)
        
        if len_uci == 4:
            return

        ultimate_char:str = uci_str[-1]

        if not ultimate_char.isdigit():
            self.is_promotion = True
            self.char_promotion = ultimate_char

            if ultimate_char == PromotioPiece.Q.value:
                self.class_promotion = Reina
                
            elif ultimate_char == PromotioPiece.R.value:
                self.class_promotion = Torre

            elif ultimate_char == PromotioPiece.B.value:
                self.class_promotion = Alfil

            elif ultimate_char == PromotioPiece.N.value:
                self.class_promotion = Caballo
            
            

    @property
    def coords(self) -> tuple[Coord, Coord]:
        return (self.coord_start, self.coord_end)
    

    @classmethod
    def build_to_coords(cls, coord_start: Coord, coord_end: Coord, promotion_piece: PromotioPiece = None) -> "FormatUCI":
        ya, xa = coord_start
        yb, xb = coord_end

        try:
            uci_xa: str = index_fen_x[xa]
            uci_ya: str = index_fen_y[ya]
            uci_xb: str = index_fen_x[xb]
            uci_yb: str = index_fen_y[yb]

        except IndexError:
            raise UCI_SintaxisError()
        
        str_promotion_piece: str = promotion_piece.value if promotion_piece != None else ""
        str_uci: str = f"{uci_xa}{uci_ya}{uci_xb}{uci_yb}{str_promotion_piece}"
        
        return cls(str_uci)
