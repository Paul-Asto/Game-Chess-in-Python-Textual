from typing import Optional

from src.core.types import PromotionPiece
from src.core.coordinate import Coord
from src.core.chess_exceptions import UCI_SintaxisError


index_fen_x: dict[int, str] = {
    0: "8",
    1: "7",
    2: "6",
    3: "5",
    4: "4",
    5: "3",
    6: "2",
    7: "1",
}

index_fen_y: dict[int, str] = { 
    0: "a",
    1: "b",
    2: "c", 
    3: "d", 
    4: "e", 
    5: "f", 
    6: "g", 
    7: "h", 
}


def from_coord_to_uci(coord: Coord) -> str:
    try:
        y, x = coord
        return index_fen_y[x] + index_fen_x[y]
    
    except IndexError:
        raise UCI_SintaxisError()


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


index_chess_y: dict[str, int] = {
    "8": 0,
    "7": 1,
    "6": 2,
    "5": 3,
    "4": 4,
    "3": 5,
    "2": 6,
    "1": 7,
}

def from_uci_to_coord(coord_uci: str) -> Coord:
    try:
        y, x = coord_uci
        return Coord(index_chess_y[x], index_chess_x[y])
    
    except IndexError:
        raise UCI_SintaxisError()


class FormatUCI:
    
    def __init__(self, uci_str: str) -> None:
        # analyze UCI
        len_uci: int = len(uci_str)
        
        if len_uci != 4 and len_uci != 5:
            raise UCI_SintaxisError()
        
        uci_start: str = uci_str[0 : 2].lower()
        uci_end: str = uci_str[2 : 4].lower()
        
        self.__coord_start: Coord = from_uci_to_coord(uci_start)
        self.__coord_end: Coord =from_uci_to_coord(uci_end)
        
        self.__: bool = False
        self.__promotion_id: Optional[PromotionPiece] = None
        self.__is_promotion = False
        
        if len_uci == 4:
            return
        
        ultimate_char:str = uci_str[-1]
        
        if not PromotionPiece.char_is_promotion(ultimate_char):
            raise Exception("Error de sintaxis")
        
        self.__is_promotion = True
        
        self.__promotion_id = PromotionPiece.make_to__char_fen(ultimate_char)
    
    
    @property
    def coords(self) -> tuple[Coord, Coord]:
        return (self.__coord_start, self.__coord_end)
    
    
    @property
    def is_promotion(self) -> bool:
        return self.__is_promotion
    
    
    @property
    def promotion_id(self) -> PromotionPiece:
        if self.__promotion_id is None:
            raise Exception("Error de atributo")
        
        return self.__promotion_id
    
    
    @classmethod
    def build_to_coords(cls, coord_start: Coord, coord_end: Coord, promotion_piece: Optional[PromotionPiece] = None) -> "FormatUCI":
        uci_start: str = from_coord_to_uci(coord_start)
        uci_end: str = from_coord_to_uci(coord_end)
        
        str_promotion_piece: str = promotion_piece.char_fen if promotion_piece != None else ""
        str_uci: str = f"{uci_start}{uci_end}{str_promotion_piece}"
        
        return cls(str_uci)
