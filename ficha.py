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

    def inHacke(self) -> bool:
        return self.army.inHacke
    
    def getClase(self) -> str:
        return self.army.clase

    def setOrdChar(self, ordChar: int) -> None:
        self.ordChar = ordChar
        self.char = chr(ordChar)

    # scuare funcions
    def setScuare(self, scuare) -> None:
        self.scuare = scuare

    def getCoord(self) -> Coord:
        return self.scuare.coord

    def registerPiecesOnProwl(self ,mov: MovFicha):
        self.scuare.registerPieceOnProwl(mov)

    def clearInfluence(self, app): ...

    def registrarObjectives(self, app, mov: MovFicha): ...

    def spreadInfluence(self, app) -> None:
        self.reportPresence(app)

    def reportPresence(self, app):
        self.scuare.updateMovOffPieceOnProwl(app)




class EmptyChess(EntityChees):
    def __init__(self):
        super().__init__(None)

        self.char = ""

    def getClase(self) -> str: return ""



        


class Ficha(EntityChees):
    def __init__(self, army):
        super().__init__(army)

        self.listDirections: list[MovFicha] = []
        self.coordsObjetives: dict[tuple, dict[tuple, str]] 


    def clearInfluence(self, app):
        for mov in self.coordsObjetives.keys():
            self.clearInfluenceOffMov(app, mov)

    def clearInfluenceOffMov(self, app, mov: tuple):
        for coord in self.coordsObjetives[mov].keys():
            app.getScuare(coord).deletedPieceOnProwl(mov)

        self.coordsObjetives[mov].clear()
    
    def spreadInfluence(self, app) -> None:
        super().spreadInfluence(app)

        for direct in self.listDirections:
            self.registrarObjectives(app, direct)


    def registrarObjectives(self, app, mov: MovFicha):

        def registerRecursive(coord: Coord):
            ficha: EntityChees = app.getFicha(coord)

            match ficha:
                case Ficha():
                    if mov.isOfensive and (ficha.getClase() != self.getClase()):
                        self.addCoordObjetives(mov.value, coord.value, "enemy")

                    else:
                        self.addCoordObjetives(mov.value, coord.value, "invalid")
                    
                    ficha.registerPiecesOnProwl(mov)
                    return
                

                case EmptyChess():
                    if mov.isOccupiable:
                        self.addCoordObjetives(mov.value, coord.value, "empty")

                    else:
                        self.addCoordObjetives(mov.value, coord.value, "invalid")

                    ficha.registerPiecesOnProwl(mov)



                case None:
                    return
                
            if mov.isSpreadable:
                registerRecursive(coord + mov)
        
        registerRecursive(self.getCoord() + mov)


    # coord objetives funcions
    def coordInObjetivo(self, coord: Coord, type: str) -> bool:

        for mov in self.coordsObjetives.values():
            if mov.get(coord.value, "") == type:
                if not(self.inHacke()):
                    return True
                
                if coord.value in self.army.coordsPriority:
                    return True
                
                break

        return False
    
    def getCoordsObjetives(self) -> list[tuple[tuple, str]]: 
        result = []

        for mov in self.coordsObjetives.values():
            if not(self.inHacke()):
                result += mov.items()
                continue

            for coord, typeObj in mov.items():
                if coord in self.army.coordsPriority:
                    result.append((coord, typeObj))

        return result

    def addCoordObjetives(self, mov, coord, typeObj):
        self.coordsObjetives[mov][coord] = typeObj






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


    def spreadInfluence(self, app) -> None:
        super().spreadInfluence(app)

        self.army.setInHacke(False)


        # Descartar opciones de coordenadas en amenaza
        for direct, objetivo in list(self.coordsObjetives.items()).copy():
            if len(objetivo) == 0:
                continue

            coord = list(objetivo.keys())[0]
            scuare = app.getScuare(coord)

            isInvalid = False

            for mov in scuare.pieces_on_prowl.values():
                if (mov.ficha.getClase() != self.getClase()) and mov.isOfensive:
                    isInvalid = True
                    break
            
            if isInvalid:
                self.addCoordObjetives(direct, coord, "invalid")


        # Verificar Hacke 
        for mov in self.scuare.pieces_on_prowl.values():
            if not(mov.ficha.getClase() != self.getClase()):
                continue

            self.army.setInHacke(True)
            self.army.addCoordsPriority([mov.ficha.getCoord().value] + list(mov.ficha.coordsObjetives[mov.value].keys()))


            coord = self.getCoord() + mov
            if mov.isOfensive and mov.isSpreadable and app.tablero.isValidCoord(coord):
                self.addCoordObjetives(mov.value, coord.value, "invalid")
            break

        # Verificar Hacke Mate
        if self.inHacke():
            result: bool = True
            coordsDisp: list[tuple[tuple, str]] = []

            for ficha in self.army.fichas.values():
                coordsDisp += ficha.getCoordsObjetives()
            
            for _, tipo in coordsDisp:
                if tipo != "invalid":
                    result = False
                    break
            
            if result:
                self.army.setInHackeMate(True)



            



    def coordInObjetivo(self, coord: Coord, type: str) -> bool:
        for mov in self.coordsObjetives.values():
            if mov.get(coord.value, "") == type:
                    return True
        return False
    

    def getCoordsObjetives(self) -> list[tuple[tuple, str]]: 
        result = []

        for mov in self.coordsObjetives.values():       
            result += mov.items()

        return result
    

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


