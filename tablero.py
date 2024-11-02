
from dataEstructures import Coord

from army import Army
from ficha import EmptyChess, EntityChees, Ficha, MovFicha


class Scuare:

    def __init__(self, coord: Coord, ficha: EntityChees) -> None:
        self.coord: Coord = coord
        self.ficha: EntityChees = ficha
        self.pieces_on_prowl: dict[tuple, MovFicha] = {}

        self.ficha.setScuare(self)

    def setFicha(self, value: EntityChees) -> None:
        self.ficha = value
        self.ficha.setScuare(self)

    def getFicha(self) -> EntityChees:
        return self.ficha
    
    def updateMovOffPieceOnProwl(self, app) -> None:
        for mov in list(self.pieces_on_prowl.values()).copy():
            mov.ficha.clearInfluenceOffMov(app, mov.value)
            mov.ficha.registrarObjectives(app, mov)
        
    
    def registerPieceOnProwl(self, mov: MovFicha):
        self.pieces_on_prowl[mov.value] = mov

    def deletedPieceOnProwl(self, mov: tuple):
        self.pieces_on_prowl.pop(mov)




class Tablero:
    def __init__(self, size: tuple) -> None:
        self.size: tuple = size
        self.Y, self.X = size

        self.content: list[list[Scuare]] = self.genTableroVoid()

        self.genCoord = self.generatorSequenseCoord()



    def getGenVIew(self) -> Coord:
        return next(self.genCoord)


    # funcion Generator Content
    def genTableroVoid(self) -> list[list[Scuare]]:
        return [[Scuare(Coord(y, x), EmptyChess()) for x in range(self.X)] for y in range(self.Y)]

    def clearContent(self):
        self.content = self.genTableroVoid()
        

    # funcions Generator Coord View
    def generatorSequenseCoord(self):
        for y in range(self.Y):
            for x in range(self.X):
                yield Coord(y, x)


    def isValidCoord(self, coord: Coord) -> bool:
        return  (self.Y > coord.y >= 0) and (self.X > coord.x >= 0)
    

    def getFicha(self, coord: tuple) -> EntityChees | None:
        return self.getScuare(coord).getFicha() if self.isValidCoord(coord) else None
    

    def getScuare(self, coord: tuple) -> Scuare:
        y, x = coord
        return self.content[y][x]
    

    # Funcions Add Fichas
    def addFicha(self, ficha: Ficha, coord: tuple) -> None:
        self.getScuare(coord).setFicha(ficha)


    def addFichas(self, fichas: list[tuple, Ficha]) -> None:
        for coord, ficha in fichas:
            self.addFicha(ficha, coord)



