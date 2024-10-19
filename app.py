from tablero import Tablero
from ficha import EntityChees, EmptyChess, Ficha
from army import Army, AdminFichas
from dataEstructures import Coord, Mov

class ChessGame:

    def __init__(self, tablero: Tablero, adminFichas: AdminFichas) -> None:
        self.tablero: Tablero = tablero
        self.adminFichas: AdminFichas = adminFichas

        self.turno: str = self.adminFichas.claseA

        self.previousFicha: EntityChees = EmptyChess()
        self.selectedFicha: EntityChees = EmptyChess()

        self.PiezaGenHacke: Ficha
        self.directGenHacke: tuple

        self.Init()

    
    def Init(self) -> None:
        self.tablero.addFichas(self.adminFichas.getTotalFichas())
        self.genObjetivesForTurno()


    def reStartDataFromAtributos(self):
        self.adminFichas.reStartArmys()
        self.tablero.clearContent()

        self.turno = self.adminFichas.claseA

        self.previousFicha = EmptyChess()
        self.selectedFicha = EmptyChess()

    
    def reStartGame(self):
        self.reStartDataFromAtributos()
        self.Init()



    def generatorView(self) -> Coord:
        return self.tablero.getGenVIew()


    def iteration(self, front)-> None:
        self.previousFicha.searchObjectives(self)

        '''        if self.previousFicha.verifyHacke(self):
            self.EventHacke(self.previousFicha)'''

        self.updateTurno()
        self.genObjetivesForTurno()
        front.updateTurno(self.turno)
    
    # implementar proceso de verificacion de hacke
    # verifica si la pieza seleccionada despues de realizar su movimiento, 
    # tiene como objetivo el ryy enemygo, lo cual se activa el estado hacke 

    # Turno Funcions
    def updateTurno(self) -> None: 
        self.turno: str = self.adminFichas.getEnemyForClass(self.turno)


    def isEqualClassTurno(self, classTurno: str) -> str:
        return self.turno == classTurno


    # PreviousFicha Funcions
    def setPreviousFicha(self, value: EntityChees) -> None:
        self.previousFicha = value

    def getPreviousFicha(self) -> EntityChees | None:
        return self.previousFicha


    # SelectedFicha Funcions
    def getSelectedFicha(self) -> EntityChees:
        return self.selectedFicha

    def setSelectedFicha(self, value: EntityChees) -> None:
        self.selectedFicha = value


    # tablero Funcions
    def setFicha(self, value: EntityChees) -> None:
            self.tablero.addFicha(value)
    
    def getFicha(self, coord: Coord) -> EntityChees | None:
        return self.tablero.getItem(coord)

    def tradeFicha(self, ficha_A: EntityChees, ficha_B: EntityChees) -> None:
        coordA: Coord = ficha_A.coord
        coordB: Coord = ficha_B.coord

        ficha_A.setCoord(coordB)
        ficha_B.setCoord(coordA)    

        self.setFicha(ficha_A)
        self.setFicha(ficha_B)

    def fusionFicha(self, ficha_A: EntityChees, ficha_B: EntityChees, app) -> None:
        coordB: Coord = ficha_B.coord
        coordA: Coord = ficha_A.coord

        ficha_A.setCoord(coordB)
        ficha_B.setCoord(coordA)
        
        self.setFicha(ficha_A)
        self.setFicha(EmptyChess(coordA))

        app.saveKillFicha(ficha_B)


    # Verifica si a ficha pasada como parametro esta dentro de la lista e objetivos de la ficha anterior,
    # especificamente en una de las llaves pasada como parametro
    def inCoordsSelected(self, ficha: EntityChees, key: str) -> bool:
        return self.previousFicha.register.fichaInRegister(ficha, key)

    # implementar e proceso de verificacion antihacke
    # al generar los objetivos, primero verifica si la pieza esta siendo atacada,
    #  si es asi, hace un ejercicio con el primer movimiento de la pieza, si las piezas que le atacban
    #  tienen omo nuevo objetivo al rey, entonces todos los movimintos de esa direccion estan prohibidos
    # esto se realiza para no mover una pieza que desproteja al rey
    def genObjetivesForTurno(self): 
        self.genCoordsObjetivesForArmy(self.adminFichas.getArmyForClass(self.turno))

    # Genera la lista de objetivos de todas as fichas de la armada pasada como parametro
    def genCoordsObjetivesForArmy(self, army: Army) -> None:
        if not(army.inHacke):
            army.searchObjetives(self)

        else:
            army.searchGenHacke(self)

    def EventHacke(self, ficha: Ficha):
        self.PiezaGenHacke = ficha
        self.adminFichas.getEnemyArmyForClass(ficha.clase).setInHacke(True)



