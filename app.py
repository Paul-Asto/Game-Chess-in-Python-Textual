from tablero import Tablero, Scuare
from ficha import EntityChees, EmptyChess, Ficha
from army import Army, AdminArmys, adminArmys
from dataEstructures import Coord, Mov

class ChessGame:
    def __init__(self, tablero: Tablero, adminFichas: AdminArmys) -> None:
        self.tablero: Tablero = tablero
        self.adminFichas: AdminArmys = adminFichas

        self.turno: str = self.adminFichas.claseA

        self.previousFicha: EntityChees = EmptyChess()
        self.selectedFicha: EntityChees = EmptyChess()

        self.Init()

    
    # Funcions Starts
    def Init(self) -> None:
        self.tablero.addFichas(self.adminFichas.getTotalFichas())
        self.adminFichas.initInfluence(self)


    def reStartDataFromAtributos(self):
        self.adminFichas.reStartArmys()
        self.tablero.clearContent()

        self.turno = self.adminFichas.claseA

        self.previousFicha = EmptyChess()
        self.selectedFicha = EmptyChess()

    
    def reStartGame(self):
        self.reStartDataFromAtributos()
        self.Init()
    
    def enemyInHackeMate(self, clase):
        return adminArmys.getEnemyArmyForClass(clase).inHackeMate

    def generatorView(self) -> Coord:
        return self.tablero.getGenVIew()


    def iteration(self, front)-> None:
        self.updateTurno()
        front.updateTurno(self.turno)

        if not(isinstance(self.previousFicha, Ficha)):
            return
        # Evento de finalizacion del programa
        if self.enemyInHackeMate(self.previousFicha.getClase()):
            front.exitProgram()


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
    def getScuare(self, coord: tuple) -> Scuare:
        return self.tablero.getScuare(coord)
    
    def getFicha(self, coord: Coord) -> EntityChees | None:
        return self.tablero.getFicha(coord)

    def tradeFicha(self, ficha_A: EntityChees, ficha_B: EntityChees) -> None:
        ficha_A.clearInfluence(self)
        ficha_B.clearInfluence(self)

        scuareA:Scuare = ficha_A.scuare
        scuareB:Scuare = ficha_B.scuare

        scuareA.setFicha(ficha_B)
        scuareB.setFicha(ficha_A)

        scuareA.ficha.spreadInfluence(self)
        scuareB.ficha.spreadInfluence(self)

        self.adminFichas.getEnemyArmyForClass(ficha_A.getClase()).updateRey(self)


    def fusionFicha(self, ficha_A: EntityChees, ficha_B: EntityChees, app) -> None:
        ficha_A.clearInfluence(self)
        ficha_B.clearInfluence(self)

        scuareA:Scuare = ficha_A.scuare
        scuareB:Scuare = ficha_B.scuare

        ficha_B.setScuare(scuareA)
        scuareA.setFicha(EmptyChess())
        scuareB.setFicha(ficha_A)

        scuareA.ficha.spreadInfluence(self)
        scuareB.ficha.spreadInfluence(self)

        self.adminFichas.getEnemyArmyForClass(ficha_A.getClase()).updateRey(self)

        app.saveKillFicha(ficha_B)
