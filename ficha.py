from dataEstructures import Coord, Mov, AbstractCoord
from adminStructures import Movement




class MovFicha(AbstractCoord):
    def __init__(self, ficha, mov: tuple, isSpreadable: bool = False, isOccupiable: bool = True, isOffensive: bool = True):
        super().__init__(mov[0], mov[1])

        self.ficha: Ficha = ficha
        self.isSpreadable: bool = isSpreadable

        self.isOccupiable: bool = isOccupiable
        self.isOfensive: bool = isOffensive



class EntityChees:
    def __init__(self, army) -> None:
        self.army = army
        self.scuare: object
        self.char: str
        
        self.listDirections: list[MovFicha] = []
        self.coordsObjetives: dict[tuple, dict[tuple, str]] 
        

    
    

    def coordInObjetivo(self, coord: Coord, type: str) -> bool:
        for mov in self.coordsObjetives.values():
            if mov.get(coord.value, "") == type:
                return True

        return False

    
    def getClase(self) -> str:
        return self.army.clase


    # scuare funcions
    def setScuare(self, scuare) -> None:
        self.scuare = scuare

    def getCoord(self) -> Coord:
        return self.scuare.coord

    def registerPiecesOnProwl(self ,mov: MovFicha):
        self.scuare.registerPieceOnProwl(mov)

    def clearInfluence(self, app): ...

    def spreadInfluence(self, app):
        self.reportPresence(app)

        for direct in self.listDirections:
            self.registrarObjectives(app, direct)

    def reportPresence(self, app):
        self.scuare.updateMovOffPieceOnProwl(app)

    # coord objetives funcions
    def getCoordsObjetives(self) -> list[tuple[tuple, str]]: 
        result = []

        for mov in self.coordsObjetives.values():
            result += mov.items()

        return result


    def addCoordObjetives(self, mov: tuple, coord: tuple, typeObj: str): ...
        




class EmptyChess(EntityChees):
    
    def __init__(self):
        super().__init__(None)

        self.char = ""

    def getClase(self) -> str: return ""



        


class Ficha(EntityChees):
    def __init__(self, army):
        super().__init__(army)



    def clearInfluence(self, app):
        for mov in self.coordsObjetives.keys():
            self.clearInfluenceOffMov(app, mov)

    def clearInfluenceOffMov(self, app, mov: tuple):
        for coord in self.coordsObjetives[mov].keys():
            app.getScuare(coord).deletedPieceOnProwl(mov)

        self.coordsObjetives[mov].clear()
    


        
    def registrarObjectives(self, app, mov: MovFicha):

        def registerRecursive(coord: Coord):
            ficha: EntityChees = app.getFicha(coord)

            match ficha:
                case Ficha():
                    if mov.isOfensive and ficha.getClase() != self.getClase():
                        self.addCoordObjetives(mov.value, coord.value, "enemy")

                    else:
                        self.addCoordObjetives(mov.value, coord.value, "friend")
                    
                    ficha.registerPiecesOnProwl(mov)
                    return
                

                case EmptyChess():
                    if mov.isOccupiable:
                        self.addCoordObjetives(mov.value, coord.value, "empty")

                    ficha.registerPiecesOnProwl(mov)

                case None:
                    return
                
            if mov.isSpreadable:
                registerRecursive(coord + mov)
        
        registerRecursive(self.getCoord() + mov)


    def addCoordObjetives(self, mov, coord, typeObj):
        self.coordsObjetives[mov][coord] = typeObj


    def setOrdChar(self, ordChar: int) -> None:
        self.ordChar = ordChar
        self.char = chr(ordChar)




class Rey(Ficha):
    
    def __init__(self, army):
        super().__init__(army)

        self.setOrdChar(9812)

        self.listDirections = [
            MovFicha(self, (0, 1)),
            MovFicha(self, (0, -1)),
            MovFicha(self, (-1, 0)),
            MovFicha(self, (1, 0)),
            MovFicha(self, (-1, -1)),
            MovFicha(self, (-1, 1)),
            MovFicha(self, (1, -1)),
            MovFicha(self, (1, 1)),
        ]

        self.coordsObjetives = {mov.value : {} for mov in self.listDirections}





class Reina(Ficha):
    
    def __init__(self, army):
        super().__init__(army)

        self.setOrdChar(9813)

        self.listDirections = [
            MovFicha(self, (0, 1), True),
            MovFicha(self, (0, -1), True),
            MovFicha(self, (-1, 0), True),
            MovFicha(self, (1, 0), True),
            MovFicha(self, (-1, -1), True),
            MovFicha(self, (-1, 1), True),
            MovFicha(self, (1, -1), True),
            MovFicha(self, (1, 1), True),
        ]

        self.coordsObjetives = {mov.value : {} for mov in self.listDirections}



class Torre(Ficha):

    def __init__(self, army):
        super().__init__(army)


        self.setOrdChar(9814)

        self.listDirections = [
            MovFicha(self, (0, 1), True),
            MovFicha(self, (0, -1), True),
            MovFicha(self, (-1, 0), True),
            MovFicha(self, (1, 0), True),
        ]

        self.coordsObjetives = {mov.value : {} for mov in self.listDirections}


class Alfil(Ficha):
    
    def __init__(self, army):
        super().__init__(army)

        self.setOrdChar(9815)

        self.listDirections = [
            MovFicha(self, (-1, -1), True),
            MovFicha(self, (-1, 1), True),
            MovFicha(self, (1, -1), True),
            MovFicha(self, (1, 1), True),
        ]

        self.coordsObjetives = {mov.value : {} for mov in self.listDirections}



class Caballo(Ficha):
    
    def __init__(self, army):
        super().__init__(army)

        self.setOrdChar(9816)
        
        self.listDirections = [
            MovFicha(self, (2, 1)),
            MovFicha(self, (2, -1)),
            MovFicha(self, (-1, 2)),
            MovFicha(self, (1, 2)),
            MovFicha(self, (-2, -1)),
            MovFicha(self, (-2, 1)),
            MovFicha(self, (-1, -2)),
            MovFicha(self, (1, -2)),
        ]

        self.coordsObjetives = {mov.value : {} for mov in self.listDirections}



class Peon(Ficha):

    def __init__(self, army):
        super().__init__(army)
        
        self.setOrdChar(9817)
        self.direct: int = self.army.orientacion
    
        self.listDirections = [
            MovFicha(self, (self.direct, -1), isOccupiable = False),
            MovFicha(self, (self.direct, 0), isOffensive = False),
            MovFicha(self, (self.direct, 1), isOccupiable = False),
        ]

        self.coordsObjetives = {mov.value : {} for mov in self.listDirections}


