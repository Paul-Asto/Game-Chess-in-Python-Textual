from dataclasses import dataclass
from enum import Enum
from typing import  Literal, Optional, TypeVar, TypedDict, TYPE_CHECKING

from src.core.square import Square

if TYPE_CHECKING:
    from src.core.coordinate import Coord
    from src.core.piece import PieceChess
    from src.core.pieces import Rey
    

T_Square = TypeVar("T_Square", bound= Square)

CharFenPiece = Literal[
    "r",
    "b",
    "q",
    "n",
    "p",
    "k",
]

CharViewPiece = Literal[
    "♔",
    "♕",
    "♖",
    "♗",
    "♘",
    "♙",
]

ColorPiece = Literal[
    "black",
    "grey",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "light_grey",
    "dark_grey",
    "light_red",
    "light_green",
    "light_yellow",
    "light_blue",
    "light_magenta",
    "light_cyan",
    "white",
]

class DataArmy(TypedDict):
    data_rey: Optional[tuple["Coord", "Rey"]]
    data_pieces: list[tuple["Coord", "PieceChess"]]

class PromotioPiece(Enum):
    Q: str = "q"
    R: str = "r"
    B: str = "b"
    N: str = "n"


@dataclass
class PeonDirectionData:
    direction: int
    index_goal_column: int
    

class EDirectionPeon(Enum):
    DOWN = PeonDirectionData(1, 7)
    UP  = PeonDirectionData(-1, 0)
