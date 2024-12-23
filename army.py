from copy import deepcopy
from coord import Coord

from piece.rey import Rey
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
                
