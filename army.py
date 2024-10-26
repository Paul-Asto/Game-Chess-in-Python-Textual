from typing import Literal

from dataEstructures import Coord
from ficha import Ficha, Torre, Caballo, Alfil, Reina, Rey, Peon


# funcions generator Army Fichas
def getFilePeon(file: int, clase: str, orientacion: int) -> list[Ficha]: 
    return [Peon(Coord(file, x), clase, orientacion) for x in range(8)]

def getFileFichas(file: int, clase: str) -> list[Ficha]: 
    return  [
        Torre(Coord(file, 0), clase),
        Alfil(Coord(file, 1), clase),
        Caballo(Coord(file, 2), clase),
        Reina(Coord(file, 3), clase),
        Caballo(Coord(file, 5), clase),
        Alfil(Coord(file, 6), clase),
        Torre(Coord(file, 7), clase),
    ]



class Army:
    def __init__(self) -> None:
        self.inHacke: bool = False
        self.orientacion: int 
        self.clase: str
        self.fichas: list[Ficha] 
        self.rey: Ficha


    def reStartFichas(self): ...
        
    def setInHacke(self, value: bool):
        self.inHacke = value

    def setClase(self, clase: str) -> None:
        self.clase = clase


    def definirOrientacion(self, orientacion: Literal[1, -1]) -> None:
        self.orientacion = orientacion

    def searchObjetives(self, app):
        self.rey.searchObjectives(app)
        for ficha in self.fichas:
            ficha.searchObjectives(app)

    def searchGenHacke(self, app):
        self.rey.searchObjectives(app)
        for ficha in self.fichas:
            ficha.searchGenHacke(app)

        app.adminFichas.getArmyForClass(self.clase).setInHacke(False)

    
    


class ArmyBlack(Army):    
    def __init__(self) -> None:
        super().__init__()

        self.setClase("armyBlack")
        self.definirOrientacion(1) 
        
        self.reStartFichas()

    def reStartFichas(self):
            self.rey = Rey(Coord(0, 4), self.clase)
            self.fichas = getFilePeon(1, self.clase, self.orientacion) + getFileFichas(0, self.clase)



class ArmyWhite(Army):
    def __init__(self) -> None:
        super().__init__()

        self.setClase("armyWhite")
        self.definirOrientacion(-1)
        
        self.reStartFichas()

    def reStartFichas(self):
            self.rey = Rey(Coord(7, 4), self.clase)
            self.fichas = getFilePeon(6, self.clase, self.orientacion) + getFileFichas(7, self.clase)



class AdminFichas:
    def __init__(self, armyA: Army, armyB: Army) -> None:
        self.claseA = armyA.clase
        self.claseB = armyB.clase

        # Estructura que guarda 2 armys por su clase
        self.relatedEnemy: dict[str, str] = {
            armyA.clase : armyB.clase,
            armyB.clase : armyA.clase
        }
        
        # Estructura armys por su clase
        self.armys: dict[str, Army] = {
            armyA.clase : armyA,
            armyB.clase : armyB
        }
        

    def getTotalFichas(self) -> list[Ficha]:
        result: list[Ficha] = []

        for army in self.armys.values():
            result += army.fichas + [army.rey]

        return result


    def getFichasForClass(self, clase: str) -> list[Ficha]:
        return self.armys[clase].fichas
    
    def getArmyForClass(self, clase: str) -> Army:
        return self.armys[clase]

    def getEnemyArmyForClass(self, clase: str) -> Army:
        return self.armys[self.getEnemyForClass(clase)]

    def reStartArmys(self):
        for army in self.armys.values():
            army.reStartFichas()

    
    def getEnemyForClass(self, clase: str) -> str:
        return self.relatedEnemy[clase]



fichasChess = AdminFichas(ArmyWhite(), ArmyBlack())



