from dataEstructures import Coord, Mov, AbstractCoord
from adminStructures import Movement


class MovFicha(AbstractCoord):
    def __init__(self, ficha, movY, movX, isSpreadable: bool = False, isOccupiable: bool = True, isOffensive: bool = True):
        super().__init__(movY, movX)

        self.ficha: Ficha = ficha
        self.isSpreadable: bool = isSpreadable

        self.isOccupiable: bool = isOccupiable
        self.isOfensive: bool = isOffensive



class EntityChees:
    
    def __init__(self, coord: Coord, clase: str) -> None:
        self.coord: Coord = coord
        self.clase: str = clase
        self.char: str


        # depredated
        self.register: AbstractRegister



        self.pieces_on_prowl: dict[tuple, MovFicha] = {}
        self.coordsObjetives: dict[tuple, str] = {}

        self.listDirections: list[MovFicha] = []



    def getCoordsObjetives(self): 
        return self.coordsObjetives.items()

    def addCoordObjetives(self, coord: str, typeObj: str): ...
        
    def registerPiecesOnProwl(self, direct: tuple, mov: MovFicha): ...



    def getCoord(self) -> Coord:
        return self.coord.value
    
    def setCoord(self, value: Coord) -> None:
        self.coord = value


    # depredated
    def verifyHacke(self, app): ...
    
    def searchObjectives(self, app): ...

    def searchGenHacke(self, app): ...

    def search(self, app, callBack) -> None: ...


    



class EmptyChess(EntityChees):
    
    def __init__(self, coord: Coord = Coord(0, 0), clase: str = "") -> None:
        super().__init__(coord, clase)

        self.char = ""




        


class Ficha(EntityChees):
    def __init__(self, coord: Coord, clase: str) -> None:
        super().__init__(coord, clase)
        
        # depredated
        self.isDireccional: bool
        self.listDirecciones: list[Mov]


    def discoverObjectives(self, app):
        for direct in self.listDirections:
            self.registrarObjectives(app, direct)


    def addCoordObjetives(self, coord, typeObj):
        self.coordsObjetives[coord] = typeObj


    def registerPiecesOnProwl(self, direct, mov):
        self.pieces_on_prowl[direct] = mov

        
    def registrarObjectives(self, app, mov: MovFicha):

        def registerRecursive(coord):
            ficha: EntityChees = app.getFicha(coord)

            match ficha:
                case Ficha():
                    if mov.isOfensive and ficha.clase != self.clase:
                        self.addCoordObjetives(coord, "enemy")
                    
                    self.registerPiecesOnProwl(mov.value, mov)
                    return
                

                case EmptyChess():
                    if mov.isOccupiable:
                        self.addCoordObjetives(coord, "empty")

                    self.registerPiecesOnProwl(mov.value, mov)

                case None:
                    return
                
            if mov.isSpreadable:
                registerRecursive(coord + mov)
        
        registerRecursive(self.coord + mov)



    def setOrdChar(self, ordChar: int) -> None:
        self.ordChar = ordChar
        self.char = chr(ordChar)



    ###### DEPREDATED
    def verifyHacke(self, app) -> bool:
        return self.register.verifyHacke(app)

    def getobjetivesForDirect(self, mov: tuple) -> list[Coord]:
        if self.isDireccional:
            return self.register.getDataForDirect(mov)
        
        return []
    
    def searchGenHacke(self, app):
        self.search(app, self.registrarGenHacke)
        

    def registrarGenHacke(self, app, mov: Mov, key: str, coord: Coord) -> None: 
        if app.PiezaGenHacke.coord == coord or coord in app.PiezaGenHacke.getobjetivesForDirect(app.directGenHacke):
            self.register.registrarObjetivo(app, mov, key, coord)

    
    def searchObjectives(self, app):
        self.search(app, self.register.registrarObjetivo)


    def PatronObjetives(
            self,
            app,
            mov: Mov,
            callBack,
            nIteration: int = 7,
            isOnlyMovement: bool = False,
            isSelected:     bool = True,
        ) -> None:
        
        count: int = 0
        coordActual: Coord = self.coord 
        
        while count != nIteration:
            coordActual += mov
            ficha: EntityChees = app.getFicha(coordActual)

            match ficha:
                case Ficha():
                    if isOnlyMovement:
                        break

                    if ficha.clase == self.clase: 
                        break

                    callBack(app, mov, "enemy", coordActual)
                    break


                case EmptyChess():
                    if isSelected: 
                        callBack(app, mov, "empty", coordActual)

                    count += 1


                case None:
                    break




class Rey(Ficha):
    
    def __init__(self, coord: Coord, clase: str) -> None:
        super().__init__(coord, clase)

        self.isDireccional = False
        self.setOrdChar(9812)
        self.register = RegisterSimple()

    # Implementar proceso de verificacion de movimientos del rey: 
    # si el estado del army esta en hacke, solo podra hacer movimientos el rey y la pieza que lo saque del hacke
    #  -> La manera de saca al rey del hacke es matando a la pieza que genero el hacke o interrumpiendo su direccion al rey

    # despues de obtener los movimientos del rey y el movimiento de las piezas que lo sacan del hacke, 
    # se tiene que filtrar los movimientos a los que el rey puede acceder, esta accion lo realiza independiente de hacke

    def search(self, app, callBack) -> None:
        self.register.clearRegister()

        movs: list[Mov] = Movement.GetListMovs_Total()

        for mov in movs: 
            self.PatronObjetives(app, mov, callBack , 1)



class Reina(Ficha):
    
    def __init__(self, coord: Coord, clase: str) -> None:
        super().__init__(coord, clase)

        self.isDireccional = True
        self.setOrdChar(9813)

        self.listDirecciones = Movement.GetListMovs_Total()
        self.register = RegisterComplex(self.listDirecciones)

    def search(self, app, callBack) -> None:
        self.register.clearRegister()
    
        for mov in self.listDirecciones: 
            self.PatronObjetives(app, mov, callBack)



class Torre(Ficha):

    def __init__(self, coord: Coord, clase: str) -> None:
        super().__init__(coord, clase)

        self.isDireccional = True
        self.setOrdChar(9814)

        self.listDirecciones = Movement.GetListMovs_Rect()
        self.register = RegisterComplex(self.listDirecciones)

    def search(self, app, callBack) -> None:
        self.register.clearRegister()
    
        for mov in self.listDirecciones: 
            self.PatronObjetives(app, mov, callBack)



class Alfil(Ficha):
    
    def __init__(self, coord: Coord, clase: str) -> None:
        super().__init__(coord, clase)

        self.isDireccional = True
        self.setOrdChar(9815)

        self.listDirecciones = Movement.GetListMovs_Diagonal()
        self.register = RegisterComplex(self.listDirecciones)

    def search(self, app, callBack) -> None:
        self.register.clearRegister()

        for mov in self.listDirecciones: 
            self.PatronObjetives(app, mov, callBack)



class Caballo(Ficha):
    
    def __init__(self, coord: Coord, clase: str) -> None:
        super().__init__(coord, clase)

        self.isDireccional = False
        self.setOrdChar(9816)
        
        self.register = RegisterSimple()
        

    def search(self, app, callBack) -> None:
        self.register.clearRegister()

        movs: list[Mov] = [
            Mov(-2, -1), 
            Mov(-2, 1), 
            Mov(2, -1), 
            Mov(2, 1), 
            Mov(-1, 2), 
            Mov(1 ,2), 
            Mov(-1, -2), 
            Mov(1, -2)
            ]

        for mov in movs: 
            self.PatronObjetives(app, mov, callBack, 1)



class Peon(Ficha):

    def __init__(self, coord: Coord, clase: str, orientacion: int) -> None:
        super().__init__(coord, clase)

        self.isDireccional = False
        self.setOrdChar(9817)

        self.orientacion: int = orientacion
        self.coordInit: Coord = self.coord.copy()
        
        self.register = RegisterSimple()
        

    def search(self, app, callBack) -> None:
        self.register.clearRegister()

        iterMov: int = 1 if self.coordInit != self.coord else 2        
        movL, movF, movR =[Mov(self.orientacion, coordX) for coordX in (-1, 0, 1)]
        
        self.PatronObjetives(app, movL, callBack, 1, isSelected= False)
        self.PatronObjetives(app, movF, callBack, iterMov, isOnlyMovement= True)
        self.PatronObjetives(app, movR, callBack, 1, isSelected= False)























####  DEPREDATED


class AbstractRegister: 
    def fichaInRegister(self, ficha: Ficha, key) -> bool: ...

    def registrarObjetivo(self, app, mov: Mov, key: str, coord: Coord) -> None: ...

    def clearRegister(self) -> None: ...

    def getData(self) -> list[tuple[str, tuple]]: ...

    def verifyHacke(self, app) -> None: ...

    def getDataForDirect(self, direct: tuple) -> list[Coord]: ...



class RegisterSimple(AbstractRegister):

    def __init__(self) -> None:
        self.registro: dict[str, list[Coord]] = {"empty": [], "enemy": []}
    

    def fichaInRegister(self, ficha: Ficha, key) -> bool:
        return ficha.coord in self.registro[key]
    

    def registrarObjetivo(self, app, mov: Mov, key: str, coord: Coord) -> None:
        self.registro[key].append(coord)

    def clearRegister(self) -> None:
        self.registro["empty"].clear()
        self.registro["enemy"].clear()

    def getData(self) -> list[tuple[str, tuple]]:
        result: list[tuple[str, tuple]] = []
        
        for key, coords in self.registro.items():
            result += [(key, coord.value) for coord in coords]

        return result
    
    
    def verifyHacke(self, app):
        for coord in self.registro["enemy"]:
            if isinstance(app.getFicha(coord), Rey):
                return True
            
        return False



class RegisterComplex(AbstractRegister):

    def __init__(self, keys: list[Mov]) -> None:
        self.registro: dict[tuple, dict[str, list[Coord]]] = {}

        for direct in keys:
            self.registro[direct.value] = {"empty": [], "enemy": []}



    def fichaInRegister(self, ficha: Ficha, key) -> bool:
        for direct in self.registro.values():
            if ficha.coord in direct[key]:
                return True
                
        return False
    

    def registrarObjetivo(self, app, mov: Mov, key: str, coord: Coord) -> None:
        self.registro[mov.value][key].append(coord)

    
    def clearRegister(self) -> None:
        for direct in self.registro.values():
            direct["enemy"].clear()
            direct["empty"].clear()

    def getData(self) -> list[tuple[str, tuple]]:
        result: list[tuple[str, tuple]] = []

        for direct in self.registro.values():
            for key, coords in direct.items():
                result += [(key, coord.value) for coord in coords]  

        return result 
    
    def getDataForDirect(self, direct: tuple) -> list[Coord]:
        return self.registro[direct]["empty"]
        
    def verifyHacke(self, app) -> bool:
        for direct, registro in self.registro.items():

            if  len(registro["enemy"]) != 0:
                coord: Coord =  registro["enemy"][0]

                if isinstance(app.getFicha(coord), Rey):
                    app.directGenHacke = direct
                    return True
            
        return False








