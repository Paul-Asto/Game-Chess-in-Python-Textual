from coord import Coord
from piece import EntityChess
from mov_piece import MovPiece
    


class Scuare:
    __coord: Coord
    __ficha: EntityChess
    __movs_on_prowl: dict[MovPiece, None] = {}

    def __init__(self, coord: Coord, ficha: EntityChess):
        self.coord = coord
        self.ficha = ficha

    # propiead Coord
    @property
    def coord(self) -> Coord: 
        return self.__coord
    
    @coord.setter
    def coord(self, value: Coord) -> None: 
        self.__coord = value


    # propiedad Ficha
    @property
    def ficha(self) -> EntityChess: 
        return self.__ficha
    
    @ficha.setter
    def ficha(self, value: EntityChess) -> None: 
        self.__ficha = value
        self.__ficha.scuare = self


    # Propiedad movs_prowl
    @property
    def movs_on_prowl(self) -> list[MovPiece]:
        return list(self.__movs_on_prowl.keys())


    def add_mov_prowl(self, mov: MovPiece) -> None: 
        self.__movs_on_prowl[mov] = None

    
    def deleted__mov_prowl(self, mov: MovPiece)-> None: 
        self.__movs_on_prowl.pop(mov)