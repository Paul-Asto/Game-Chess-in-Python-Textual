from enum import Enum

class EOrientationArmy(Enum):
    DOWN = 1
    UP = -1



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

ORIENT_ARMY_WHITE = EOrientationArmy.UP
ORIENT_ARMY_BLACK = EOrientationArmy.DOWN

# Caracteres de Piezas
CHAR_VIEW_REY = "♔"     # chr(9812)
CHAR_VIEW_REINA = "♕"   # chr(9813)
CHAR_VIEW_TORRE = "♖"   # chr(9814)
CHAR_VIEW_ALFIL = "♗"   # chr(9815)
CHAR_VIEW_CABALLO = "♘" # chr(9816)
CHAR_VIEW_PEON = "♙"    # chr(9817)

CHAR_VIEW_EMPTY = " "