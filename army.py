from copy import deepcopy
from coord import Coord

from piece.rey import Rey
from piece.piece import PieceChess

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board
    from piece.piece import Color



class Army:
    console_color: "Color" = "white"
    in_hacke: bool = False
    in_hacke_mate: bool = False
    orientacion: int = 1
    clase: str

    coords_priority: list[tuple[Coord, str]] 
    pieces_defending: list[PieceChess] 

    rey: Rey 
    __fichas: dict[Coord, PieceChess]
    __copy_fichas: dict[Coord, PieceChess] 

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
                
