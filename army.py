from typing import Literal

from dataEstructures import Coord
from ficha import Ficha, Torre, Caballo, Alfil, Reina, Rey, Peon


class Army:
    def __init__(self) -> None:
        self.inHacke: bool = False
        self.inHackeMate: bool = False
        self.orientacion: int 
        self.clase: str
        self.fichas: dict[tuple, Ficha] = {}
        self.rey: Rey 
        self.coordsPriority: list[tuple] 

    def updateRey(self, app):
        self.rey.spreadInfluence(app)

    def addCoordsPriority(self, coords):
        self.coordsPriority = coords

    def reStartFichas(self): ...
        
    def setInHacke(self, value: bool):
        self.inHacke = value
    
    def setInHackeMate(self, value: bool):
        self.inHackeMate = value

    def setClase(self, clase: str) -> None:
        self.clase = clase

    def definirOrientacion(self, orientacion: Literal[1, -1]) -> None:
        self.orientacion = orientacion

    def initInfluence(self, app):
        for ficha in self.fichas.values():
            ficha.spreadInfluence(app)



class ArmyBlack(Army):    
    def __init__(self) -> None:
        super().__init__()

        self.setClase("armyBlack")
        self.definirOrientacion(1) 
        
        self.reStartFichas()

    def reStartFichas(self):
            self.setInHacke(False)
            self.setInHackeMate(False)

            self.rey = Rey(self)
            self.fichas = {
                (1, 0): Peon(self),
                (1, 1): Peon(self),
                (1, 2): Peon(self),
                (1, 3): Peon(self),
                (1, 4): Peon(self),
                (1, 5): Peon(self),
                (1, 6): Peon(self),
                (1, 7): Peon(self),
                (0, 0): Torre(self),
                (0, 1): Caballo(self),
                (0, 2): Alfil(self),
                (0, 3): Reina(self),
                (0, 4): self.rey,
                (0, 5): Alfil(self),
                (0, 6): Caballo(self),
                (0, 7): Torre(self),
            }



class ArmyWhite(Army):
    def __init__(self) -> None:
        super().__init__()

        self.setClase("armyWhite")
        self.definirOrientacion(-1)
        
        self.reStartFichas()

    def reStartFichas(self):
            self.setInHacke(False)
            self.setInHackeMate(False)

            self.rey = Rey(self)     
            self.fichas = {
                (6, 0): Peon(self),
                (6, 1): Peon(self),
                (6, 2): Peon(self),
                (6, 3): Peon(self),
                (6, 4): Peon(self),
                (6, 5): Peon(self),
                (6, 6): Peon(self),
                (6, 7): Peon(self),
                (7, 0): Torre(self),
                (7, 1): Caballo(self),
                (7, 2): Alfil(self),
                (7, 3): Reina(self),
                (7, 4): self.rey,
                (7, 5): Alfil(self),
                (7, 6): Caballo(self),
                (7, 7): Torre(self),
            }






class AdminArmys:
    def __init__(self, armyA: Army, armyB: Army) -> None:
        self.claseA = armyA.clase
        self.claseB = armyB.clase

        # Estructura que relaciona Las clases enemigas
        self.relatedEnemy: dict[str, str] = {
            armyA.clase : armyB.clase,
            armyB.clase : armyA.clase
        }
        
        # Estructura armys por su clase
        self.armys: dict[str, Army] = {
            armyA.clase : armyA,
            armyB.clase : armyB
        }
        

    def initInfluence(self, app) -> None:
        self.armys[self.claseA].initInfluence(app)
        self.armys[self.claseB].initInfluence(app)

    def getTotalFichas(self) -> list[tuple[tuple, Ficha]]:
        return \
        list(self.armys[self.claseA].fichas.items()) + \
        list(self.armys[self.claseB].fichas.items())

    
    def getArmyForClass(self, clase: str) -> Army:
        return self.armys[clase]

    def getEnemyArmyForClass(self, clase: str) -> Army:
        return self.armys[self.getEnemyForClass(clase)]

    def reStartArmys(self):
        self.armys[self.claseA].reStartFichas()
        self.armys[self.claseB].reStartFichas()

    
    def getEnemyForClass(self, clase: str) -> str:
        return self.relatedEnemy[clase]


adminArmys = AdminArmys(ArmyWhite(), ArmyBlack())

