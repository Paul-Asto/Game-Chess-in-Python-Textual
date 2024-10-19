
from dataEstructures import Coord

from army import Army
from ficha import EmptyChess, EntityChees, Ficha, MovFicha


class Tablero:
    def __init__(self, size: tuple) -> None:
        self.size: tuple = size
        self.Y, self.X = size

        self.content: list[EmptyChess] = self.genTableroVoid()

        self.genCoord = self.generatorSequenseCoord()

    def getGenVIew(self) -> Coord:
        return next(self.genCoord)

    # funcion Generator Content
    def genTableroVoid(self) -> list[EmptyChess]:
        return [[EmptyChess(Coord(y, x)) for x in range(self.X)] for y in range(self.Y)]
    

    def clearContent(self):
        self.content = self.genTableroVoid()
        

    # funcions Generator Coord View
    def generatorSequenseCoord(self):
        for y in range(self.Y):
            for x in range(self.X):
                yield Coord(y, x)


    def isValidCoord(self, coord: Coord) -> bool:
        return  (self.Y > coord.y >= 0) and (self.X > coord.x >= 0)
    

    def getItem(self, coord: Coord) -> EntityChees | None:
        return self.content[coord.y][coord.x] if self.isValidCoord(coord) else None
    
    
    # Funcions Add Fichas
    def addFicha(self, ficha: Ficha) -> None:
        y, x = ficha.coord
        self.content[y][x] = ficha

    def addFichas(self, fichas: list[Ficha]) -> None:
        for ficha in fichas:
            self.addFicha(ficha)

    def addArmy(self, army: Army) -> None:
        for ficha in army.fichas:
            self.addFicha(ficha)


