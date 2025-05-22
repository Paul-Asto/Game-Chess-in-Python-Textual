from src.core.coordinate import Coord
from src.core.types_chess import DataArmy, EDirectionPeon
from src.core.pieces import (
    Rey,
    Peon,
    Torre,
    Caballo,
    Alfil,
    Reina
)


def build_data_army_white() -> DataArmy:
    return{
        "data_rey": (Coord(7, 4), Rey()),
        "data_pieces": [
                (Coord(6, 0), Peon(EDirectionPeon.UP)),
                (Coord(6, 1), Peon(EDirectionPeon.UP)),
                (Coord(6, 2), Peon(EDirectionPeon.UP)),
                (Coord(6, 3), Peon(EDirectionPeon.UP)),
                (Coord(6, 4), Peon(EDirectionPeon.UP)),
                (Coord(6, 5), Peon(EDirectionPeon.UP)),
                (Coord(6, 6), Peon(EDirectionPeon.UP)),
                (Coord(6, 7), Peon(EDirectionPeon.UP)), 
                (Coord(7, 0), Torre()),
                (Coord(7, 1), Caballo()),
                (Coord(7, 2), Alfil()),
                (Coord(7, 3), Reina()),
                (Coord(7, 5), Alfil()),
                (Coord(7, 6), Caballo()),
                (Coord(7, 7), Torre()),
        ]
    }


def build_data_army_black() -> DataArmy:
    return{
        "data_rey": (Coord(0, 4), Rey()),
        "data_pieces": [
                (Coord(1, 0), Peon(EDirectionPeon.DOWN)),
                (Coord(1, 1), Peon(EDirectionPeon.DOWN)),
                (Coord(1, 2), Peon(EDirectionPeon.DOWN)),
                (Coord(1, 3), Peon(EDirectionPeon.DOWN)),
                (Coord(1, 4), Peon(EDirectionPeon.DOWN)),
                (Coord(1, 5), Peon(EDirectionPeon.DOWN)),
                (Coord(1, 6), Peon(EDirectionPeon.DOWN)),
                (Coord(1, 7), Peon(EDirectionPeon.DOWN)),
                (Coord(0, 0), Torre()),
                (Coord(0, 1), Caballo()),
                (Coord(0, 2), Alfil()),
                (Coord(0, 3), Reina()),
                (Coord(0, 5), Alfil()),
                (Coord(0, 6), Caballo()),
                (Coord(0, 7), Torre()),
        ]
    }
