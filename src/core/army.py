from copy import deepcopy
from src.coordinate import Coord

from src.core.pieces import (
    Rey,
    Peon,
    )

from src.core.piece import PieceChess

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.ui.chessApp import ChessApp
    from src.core.pieces import Peon
    from src.core.board import Board
    from src.core.piece import ColorPiece
    from src.chess_constant import EOrientationArmy



class Army:
    in_hacke: bool = False
    in_hacke_mate: bool = False

    active_enrroque_corto: bool = True
    active_enrroque_largo: bool = True

    rey: Rey = None
    peon_passant: "Peon" = None

    __fichas: dict[Coord, PieceChess] = None
    __copy_fichas: dict[Coord, PieceChess]  = None


    def __init__(self, orientation: "EOrientationArmy", console_color: "ColorPiece", id_army: str = None):

        # Condicion de generacion de id
        self.id: str = id_army if id_army != None else f"id: {id(self)}"

        self.orientacion: "EOrientationArmy" = orientation
        self.console_color: "ColorPiece" = console_color

        self.coords_priority: list[tuple[Coord, str]]  = []
        self.pieces_defending: list[PieceChess]  = []
        self.__copy_fichas = {}
        

    # propiedad fichas
    @property
    def pieces(self) -> list[tuple[Coord, PieceChess]]:
        return list(self.__copy_fichas.items())
    
    @pieces.setter
    def pieces(self, value: dict[Coord, PieceChess]) -> None:
        self.__fichas = value

        self.__copy_fichas = deepcopy(self.__fichas)

        # Busqueda del rey y seteo de army
        for ficha in self.__copy_fichas.values():
            ficha.army = self
            ficha.console_color = self.console_color

            if isinstance(ficha, Rey):
                self.rey = ficha
                
    
    def set_peon_passant(self, peon: PieceChess) -> None:
        self.peon_passant = peon

    
    def delete_peon_passant(self, tablero: "Board", app: "ChessApp") -> None:
        if self.peon_passant == None:
            return
        
        self.peon_passant.is_passant = False
        self.peon_passant.update_presence(tablero)
        self.peon_passant = None

        app.tablero.update_view_blocks()


    def init_influence(self, board: "Board") -> None: 
        for _, ficha in self.pieces:
            ficha.spread_influence(board)

    
    def update_influence_rey(self, board: "Board") -> None: 
        self.rey.spread_influence(board)


    def restart(self) -> None: 
        self.in_hacke = False
        self.in_hacke_mate = False

        self.__copy_fichas = deepcopy(self.__fichas)

        # Busqueda del rey
        for ficha in self.__copy_fichas.values():
            ficha.army = self
            ficha.console_color = self.console_color

            if isinstance(ficha, Rey):
                self.rey = ficha
                


    def notation_FE_enrroque(self) -> str:
        notation: str = \
            f"{"k" if self.active_enrroque_corto else ""}" +\
            f"{"q" if self.active_enrroque_largo else ""}"
        
        return notation if notation != "" else "-"