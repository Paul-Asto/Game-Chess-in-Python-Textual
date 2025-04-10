from src.ui.chessAppGui import ChessAppGui
from src.chessGame import ChessGame
from src.core.army import Army
from src.core.board import Board
from src.coordinate import Coord
from src.ui.react_component import ReactScuare

from src.core.pieces import (
    Rey,
    Reina,
    Caballo,
    Peon,
    Torre,
    Alfil
)

from src.chess_constant import (
    COLOR_ARMY_WHITE,
    COLOR_ARMY_BLACK,

    ID_ARMY_BLACK,
    ID_ARMY_WHITE,

    ORIENT_ARMY_BLACK,
    ORIENT_ARMY_WHITE,

    CHESS_BOARD_SIZE_X,
    CHESS_BOARD_SIZE_Y,
    )



army_white: Army = Army(
    orientation= ORIENT_ARMY_WHITE,
    console_color= COLOR_ARMY_WHITE,
    id_army= ID_ARMY_WHITE,
)

army_white.pieces =  {
            Coord(6, 0): Peon(-1),
            Coord(6, 1): Peon(-1),
            Coord(6, 2): Peon(-1),
            Coord(6, 3): Peon(-1),
            Coord(6, 4): Peon(-1),
            Coord(6, 5): Peon(-1),
            Coord(6, 6): Peon(-1),
            Coord(6, 7): Peon(-1), 
            Coord(7, 0): Torre(),
            Coord(7, 1): Caballo(),
            Coord(7, 2): Alfil(),
            Coord(7, 3): Reina(),
            Coord(7, 4): Rey(),
            Coord(7, 5): Alfil(),
            Coord(7, 6): Caballo(),
            Coord(7, 7): Torre(),
        }


army_black: Army = Army(
    orientation= ORIENT_ARMY_BLACK,
    console_color= COLOR_ARMY_BLACK,
    id_army= ID_ARMY_BLACK,
)

army_black.pieces = {
            Coord(1, 0): Peon(1),
            Coord(1, 1): Peon(1),
            Coord(1, 2): Peon(1),
            Coord(1, 3): Peon(1),
            Coord(1, 4): Peon(1),
            Coord(1, 5): Peon(1),
            Coord(1, 6): Peon(1),
            Coord(1, 7): Peon(1),
            Coord(0, 0): Torre(),
            Coord(0, 1): Caballo(),
            Coord(0, 2): Alfil(),
            Coord(0, 3): Reina(),
            Coord(0, 4): Rey(),
            Coord(0, 5): Alfil(),
            Coord(0, 6): Caballo(),
            Coord(0, 7): Torre(),
        }


board: Board[ReactScuare] = Board[ReactScuare](
    size_y= CHESS_BOARD_SIZE_Y,
    size_x= CHESS_BOARD_SIZE_X,
    type_square= ReactScuare,
)

game: ChessGame = ChessGame(
    army_white= army_white,
    army_black= army_black,
    board= board,
)

app = ChessAppGui(
    chess_game= game
)


if __name__ == "__main__":
    app.run()
    