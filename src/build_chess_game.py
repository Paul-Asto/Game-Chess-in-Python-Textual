from src.core.chessGame import ChessGame
from src.core.army import Army
from src.core.board import Board
from src.core.square import Square
from src.ui.react_component import ReactSquare, ReactArmy

from src.core.build_data_army import build_data_army_black, build_data_army_white

from src.core.chess_constant import (
    COLOR_ARMY_WHITE,
    COLOR_ARMY_BLACK,

    ID_ARMY_BLACK,
    ID_ARMY_WHITE,

    CHESS_BOARD_SIZE_X,
    CHESS_BOARD_SIZE_Y,
)


def build_chess_game() -> ChessGame[Square]:
    army_white: Army = Army(
        data_army= build_data_army_white(),
        console_color= COLOR_ARMY_WHITE,
        id_army= ID_ARMY_WHITE,
    )

    army_black: Army = Army(
        data_army= build_data_army_black(),
        console_color= COLOR_ARMY_BLACK,
        id_army= ID_ARMY_BLACK,
    )

    board = Board[Square](
        size_y= CHESS_BOARD_SIZE_Y,
        size_x= CHESS_BOARD_SIZE_X,
        type_square= Square,
    )

    return ChessGame[Square](
        army_white= army_white,
        army_black= army_black,
        board= board,
    )


def build_react_chess_game() -> ChessGame[ReactSquare]:
    army_white: Army = ReactArmy(
        data_army= build_data_army_white(),
        console_color= COLOR_ARMY_WHITE,
        id_army= ID_ARMY_WHITE,
    )

    army_black: Army = ReactArmy(
        data_army= build_data_army_black(),
        console_color= COLOR_ARMY_BLACK,
        id_army= ID_ARMY_BLACK,
    )

    board = Board[ReactSquare](
        size_y= CHESS_BOARD_SIZE_Y,
        size_x= CHESS_BOARD_SIZE_X,
        type_square= ReactSquare,
    )

    return ChessGame[ReactSquare](
        army_white= army_white,
        army_black= army_black,
        board= board,
    )
