from typing import Optional
from enum import Enum
from src.core.data_classes import PawnDirectionData


class ObjetiveChess(Enum):
    ENEMY   = "enemy"
    EMPTY   = "empty"
    INVALID = "invalid"


class CharViewPiece(Enum):
    KING =  "♔"        # chr(9812)
    QUEEN = "♕"        # chr(9813)
    ROOK = "♖"         # chr(9814)
    BISHOP = "♗"       # chr(9815)
    KNIGHT = "♘"       # chr(9816)
    PAWN =  "♙"        # chr(9817)



class CharFenPiece(Enum):
    KING = "k"
    QUEEN = "q"
    ROOK = "r"
    BISHOP = "b"
    KNIGHT = "n"
    PAWN =  "p"


class IdPiece(Enum):
    KING = "king"
    QUEEN = "queen"
    ROOK = "rook"
    BISHOP = "bishop"
    KNIGHT = "knight"
    PAWN =  "pawn"



class ColorPiece(Enum):
    WHITE = "blue"
    BLACK = "red"
    



class PromotionPiece(Enum):
    QUEEN = ("♕", "q")
    ROOK = ("♖", "r")
    BISHOP = ("♗" , "b")
    KNIGHT = ("♘" , "n")
    
    @property
    def char_fen(self) -> str:
        return self.value[1]

    @property
    def char_view(self) -> str:
        return self.value[0]

    @classmethod
    def char_is_promotion(cls, char: str) -> bool:
        return char in ("q", "r", "b", "n")
    
    @classmethod
    def make_to__char_fen(cls, char_fen: str) -> Optional["PromotionPiece"]:
        result: Optional["PromotionPiece"] = None
        
        match(char_fen):
            case cls.QUEEN.char_fen: result = cls.QUEEN
            case cls.ROOK.char_fen: result = cls.ROOK
            case cls.BISHOP.char_fen: result = cls.BISHOP
            case cls.KNIGHT.char_fen: result = cls.KNIGHT
            case _: pass
        
        return result



class ArmyClass(Enum):
    BLACK = "army_black"
    WHITE = "army_white"



class EDirectionPawn(Enum):
    DOWN = PawnDirectionData(1, 7)
    UP  = PawnDirectionData(-1, 0)
