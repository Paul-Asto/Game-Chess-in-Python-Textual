from enum import Enum
from src.core.types_chess import CharFenPiece, CharViewPiece

class EObjetiveChess(Enum):
    ENEMY: str = "enemy"
    EMPTY: str = "empty"
    INVALID: str = "invalid"


BLOCK_WHITE = "blanco"
BLOCK_BLACK = "negro"

ID_ARMY_WHITE = "armyWhite"
ID_ARMY_BLACK = "armyBlack"
ID_NONE_ARMY = "none"

OBJ_ENEMY = "enemy"
OBJ_EMPTY = "empty"
OBJ_INVALID = "invalid"

CHESS_BOARD_SIZE_X = 8
CHESS_BOARD_SIZE_Y = 8

COLOR_ARMY_WHITE = "blue"
COLOR_ARMY_BLACK = "red"


# Caracteres de Piezas
CHAR_VIEW_REY: CharViewPiece = "♔"     # chr(9812)
CHAR_VIEW_REINA: CharViewPiece  = "♕"   # chr(9813)
CHAR_VIEW_TORRE: CharViewPiece  = "♖"   # chr(9814)
CHAR_VIEW_ALFIL: CharViewPiece  = "♗"   # chr(9815)
CHAR_VIEW_CABALLO: CharViewPiece  = "♘" # chr(9816)
CHAR_VIEW_PEON: CharViewPiece  = "♙"    # chr(9817)

CHAR_FEN_REY: CharFenPiece = "k"     
CHAR_FEN_REINA: CharFenPiece  = "q"   
CHAR_FEN_TORRE: CharFenPiece  = "r"  
CHAR_FEN_ALFIL: CharFenPiece  = "b"   
CHAR_FEN_CABALLO: CharFenPiece  = "n" 
CHAR_FEN_PEON: CharFenPiece  = "p"    

