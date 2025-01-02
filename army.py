from copy import deepcopy
from coord import Coord

from constant import ARMY_BLACK, ARMY_WHITE

from piece.rey import Rey
from piece.reina import Reina
from piece.alfil import Alfil
from piece.torre import Torre
from piece.peon import Peon
from piece.caballo import Caballo
from piece.piece import PieceChess

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chessApp import ChessApp
    from piece.peon import Peon
    from board import Board
    from piece.piece import Color



class Army:
    console_color: "Color" = "white"

    in_hacke: bool = False
    in_hacke_mate: bool = False

    active_enrroque_corto: bool = True
    active_enrroque_largo: bool = True

    orientacion: int = 1
    clase: str

    coords_priority: list[tuple[Coord, str]] 
    pieces_defending: list[PieceChess] 

    rey: Rey 
    __fichas: dict[Coord, PieceChess]
    __copy_fichas: dict[Coord, PieceChess] 

    peon_passant: "Peon" = None

    def __init__(self):
        self.coords_priority = []
        self.pieces_defending = []
        self.__copy_fichas = {}
        

    # propiedad fichas
    @property
    def fichas(self) -> list[tuple[Coord, PieceChess]]:
        return list(self.__copy_fichas.items())
    
    @fichas.setter
    def fichas(self, value: dict[Coord, PieceChess]) -> None:
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
        for _, ficha in self.fichas:
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
                


class ArmyBlack(Army):    
    def __init__(self) -> None:
        super().__init__()

        self.clase = ARMY_BLACK
        self.orientacion = 1 
        self.console_color = "red"
        
        self.fichas = {
            Coord(1, 0): Peon(self.orientacion),
            Coord(1, 1): Peon(self.orientacion),
            Coord(1, 2): Peon(self.orientacion),
            Coord(1, 3): Peon(self.orientacion),
            Coord(1, 4): Peon(self.orientacion),
            Coord(1, 5): Peon(self.orientacion),
            Coord(1, 6): Peon(self.orientacion),
            Coord(1, 7): Peon(self.orientacion),
            Coord(0, 0): Torre(),
            Coord(0, 1): Caballo(),
            Coord(0, 2): Alfil(),
            Coord(0, 3): Reina(),
            Coord(0, 4): Rey(),
            Coord(0, 5): Alfil(),
            Coord(0, 6): Caballo(),
            Coord(0, 7): Torre(),
        }



class ArmyWhite(Army):
    def __init__(self) -> None:
        super().__init__()

        self.clase = ARMY_WHITE
        self.orientacion = -1
        self.console_color = "blue"

        self.fichas = {
            Coord(6, 0): Peon(self.orientacion),
            Coord(6, 1): Peon(self.orientacion),
            Coord(6, 2): Peon(self.orientacion),
            Coord(6, 3): Peon(self.orientacion),
            Coord(6, 4): Peon(self.orientacion),
            Coord(6, 5): Peon(self.orientacion),
            Coord(6, 6): Peon(self.orientacion),
            Coord(6, 7): Peon(self.orientacion), 
            Coord(7, 0): Torre(),
            Coord(7, 1): Caballo(),
            Coord(7, 2): Alfil(),
            Coord(7, 3): Reina(),
            Coord(7, 4): Rey(),
            Coord(7, 5): Alfil(),
            Coord(7, 6): Caballo(),
            Coord(7, 7): Torre(),
        }