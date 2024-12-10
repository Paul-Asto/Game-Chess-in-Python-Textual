from coord import Coord
from army import Army
from rey import Rey
from reina import Reina
from alfil import Alfil
from torre import Torre
from peon import Peon
from caballo import Caballo

from piece import PieceChess

from typing import TYPE_CHECKING
from constant import ARMY_BLACK, ARMY_WHITE

if TYPE_CHECKING:
    from board import Board


class ArmyBlack(Army):    
    def __init__(self) -> None:
        super().__init__()

        self.clase = ARMY_BLACK
        self.orientacion = 1 
        
        self.fichas = {
            Coord(1, 0): Peon(self),
            Coord(1, 1): Peon(self),
            Coord(1, 2): Peon(self),
            Coord(1, 3): Peon(self),
            Coord(1, 4): Peon(self),
            Coord(1, 5): Peon(self),
            Coord(1, 6): Peon(self),
            Coord(1, 7): Peon(self),
            Coord(0, 0): Torre(self),
            Coord(0, 1): Caballo(self),
            Coord(0, 2): Alfil(self),
            Coord(0, 3): Reina(self),
            Coord(0, 4): Rey(self),
            Coord(0, 5): Alfil(self),
            Coord(0, 6): Caballo(self),
            Coord(0, 7): Torre(self),
        }



class ArmyWhite(Army):
    def __init__(self) -> None:
        super().__init__()

        self.clase = ARMY_WHITE
        self.orientacion = -1

        self.fichas = {
            Coord(6, 0): Peon(self),
            Coord(6, 1): Peon(self),
            Coord(6, 2): Peon(self),
            Coord(6, 3): Peon(self),
            Coord(6, 4): Peon(self),
            Coord(6, 5): Peon(self),
            Coord(6, 6): Peon(self),
            Coord(6, 7): Peon(self), 
            Coord(7, 0): Torre(self),
            Coord(7, 1): Caballo(self),
            Coord(7, 2): Alfil(self),
            Coord(7, 3): Reina(self),
            Coord(7, 4): Rey(self),
            Coord(7, 5): Alfil(self),
            Coord(7, 6): Caballo(self),
            Coord(7, 7): Torre(self),
        }



class AdminArmys:
    def __init__(self, armyA: Army, armyB: Army) -> None:
        self.claseA = armyA.clase
        self.claseB = armyB.clase

        # Estructura que relaciona Las clases enemigas
        self.related_enemy: dict[str, str] = {
            armyA.clase : armyB.clase,
            armyB.clase : armyA.clase
        }
        
        # Estructura armys por su clase
        self.armys: dict[str, Army] = {
            armyA.clase : armyA,
            armyB.clase : armyB
        }


    @property
    def fichas(self) -> list[tuple[Coord, PieceChess]]:
        return \
        self.armys[self.claseA].fichas + \
        self.armys[self.claseB].fichas



    def init_influence(self, board: "Board") -> None:
        self.armys[self.claseA].init_influence(board)
        self.armys[self.claseB].init_influence(board)

    
    def get_army_for_class(self, clase: str) -> Army:
        return self.armys[clase]


    def get_enemy_army_for_class(self, clase: str) -> Army:
        return self.armys[self.get_enemy_for_class(clase)]
    

    def get_enemy_for_class(self, clase: str) -> str:
        return self.related_enemy[clase]


    def reStartArmys(self):
        self.armys[self.claseA].restart()
        self.armys[self.claseB].restart()



admin_armys = AdminArmys(ArmyWhite(), ArmyBlack())