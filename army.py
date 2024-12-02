from copy import deepcopy
from coord import Coord

from rey import Rey
from piece import PieceChess

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board



class Army:
    __in_hacke: bool = False
    __in_hacke_mate: bool = False
    __orientacion: int 
    __clase: str

    __rey: Rey 
    __coords_priority: list[Coord, str] = []

    __fichas: dict[Coord, PieceChess]
    __copy_fichas: dict[Coord, PieceChess] = {}


    # propiedad in_hacke
    @property
    def in_hacke(self) -> bool:
        return self.__in_hacke
    
    @in_hacke.setter
    def in_hacke(self, value: bool) -> None:
        self.__in_hacke = value


    # propiedad in_hacke_mate
    @property
    def in_hacke_mate(self) -> bool:
        return self.__in_hacke_mate
    
    @in_hacke_mate.setter
    def in_hacke_mate(self, value: bool) -> None:
        self.__in_hacke_mate = value

    
    # propiedad orientacion
    @property
    def orientacion(self) -> int:
        return self.__orientacion
    
    @orientacion.setter
    def orientacion(self, value: int) -> None:
        self.__orientacion = value


    # propiedad clase
    @property
    def clase(self) -> str:
        return self.__clase
    
    @clase.setter
    def clase(self, value: str) -> None:
        self.__clase = value


    # propiedad rey
    @property
    def rey(self) -> Rey:
        return self.__rey
    
    @rey.setter
    def rey(self, value: Rey) -> None:
        self.__rey = value


    # propiedad coords_priority
    @property
    def coords_priority(self) -> list[Coord, str] :
        return self.__coords_priority
    
    @coords_priority.setter
    def coords_priority(self, value: list[Coord, str] ) -> None:
        self.__coords_priority = value


    # propiedad fichas
    @property
    def fichas(self) -> list[tuple[Coord, PieceChess]]:
        return list(self.__copy_fichas.items())
    
    @fichas.setter
    def fichas(self, value: dict[Coord, PieceChess]) -> None:
        self.__fichas = value

        self.__copy_fichas = deepcopy(self.__fichas)

        # Busqueda del rey
        for ficha in self.__copy_fichas.values():
            if isinstance(ficha, Rey):
                self.__rey = ficha
                break


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
            if isinstance(ficha, Rey):
                self.__rey = ficha
                break


