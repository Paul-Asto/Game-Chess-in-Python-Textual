from typing import TYPE_CHECKING

from mov_piece import MovPiece
from coord import Coord

if TYPE_CHECKING:
    from army import Army
    from scuare import Scuare
    from board import Board



class AdminObjetives:
    def __init__(self, *movs: list[MovPiece]) -> None:
        self.list_movs: list[MovPiece] = movs
        self.store_data: dict[MovPiece, dict[Coord, str]] = {mov : {} for mov in movs}


    def get_movs(self) -> list[MovPiece]:
        return self.list_movs
    

    def get_coords_off_mov(self, mov: MovPiece) -> list[Coord]:
        return list(self.store_data[mov].keys())

    def get_coords(self) -> list[Coord]:
        result: list[Coord] = []

        for mov in self.list_movs:
            result += self.get_coords_off_mov(mov)

        return result

    
    def get_data_off_mov(self, mov: MovPiece) -> list[tuple[Coord, str]]:
        return list(self.store_data[mov].items())

    def get_data(self) -> list[tuple[Coord, str]]:
        result: list[tuple[tuple, str]] = []

        for mov in self.list_movs:
            result += self.get_data_off_mov(mov)

        return result


    def add_coord_off_mov(self, mov: MovPiece, coord: Coord, value: str) -> None:
        self.store_data[mov][coord] = value
    

    def clear_store_off_mov(self, mov: MovPiece) -> None:
        self.store_data[mov].clear()


    def coord_in_store(self, coord: Coord, value: str) -> bool:
        for mov in self.list_movs:
            if self.coord_in_store_off_mov(mov, coord, value):
                return True
        
        return False
    
    def coord_in_store_off_mov(self, mov: MovPiece, coord: Coord, value: str) -> bool:
        input: tuple = (coord, value)

        for data in self.get_data_off_mov(mov):
            if  data == input:
                return True
        
        return False
    


class EntityChess:

    __char: str = ""
    __scuare: "Scuare"
    __army: "Army"
    __clase_alter: str = ""

    def __init__(self, army: "Army" = None) -> None:
        self.__army = army
    
    # propiedad in_hacke
    @property
    def in_hacke(self) -> bool:
        return self.army.in_hacke if self.__army != None else False

    @in_hacke.setter
    def in_hacke(self, value: bool) -> None: 
        self.__army.in_hacke = value


    # Propiedade Clase
    @property
    def clase(self) -> str: 
        if self.__army != None:
            return self.army.clase
        
        if self.__clase_alter == "":
            raise Exception("La ficha no pertenece a ninguna armada, dale un valor manualmente al atributo clase")

        return self.__clase_alter
    
    @clase.setter
    def clase(self, value: str) -> str:  
        self.__clase_alter = value


    # Propiedad Coordenada
    @property
    def coord(self) -> Coord: 
        return self.scuare.coord


    # Propiedad Army
    @property
    def army(self) -> "Army": 
        return self.__army

    @army.setter
    def army(self, army: "Army") -> None: 
        self.__army = army


    # Propiedad Char View
    @property
    def char(self) -> str: 
        return self.__char

    @char.setter
    def char(self, char: str) -> None: 
        self.__char = char


    # Propiedad Scuare
    @property
    def scuare(self) -> "Scuare": 
        return self.__scuare

    @scuare.setter
    def scuare(self, scuare: "Scuare") -> None:
        self.__scuare = scuare


    def is_equals_class(self, clase: str) -> bool:
        return self.clase == clase


    def add_mov_prowl(self ,mov: MovPiece) -> None: 
        self.scuare.add_mov_prowl(mov)

    
    def update_presence(self, board: "Board") -> None: 
        for mov in self.__scuare.movs_on_prowl.copy():
            mov.ficha.clear_influence_off_mov(board, mov)
            mov.ficha.add_objetives(board, mov)

    
    def spread_influence(self, board: "Board") -> None: 
        self.update_presence(board)

    
    def add_objetives(self, board: "Board", mov: MovPiece): ...

    
    def clear_influence(self, board: "Board") -> None: ...



class EmptyChess(EntityChess):

    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.clase = "empty"



class PieceChess(EntityChess):

    __in_defense: bool = False
    __movs_defending: list[MovPiece] = []

    admin_obj: AdminObjetives


    # propiedad movs_defending
    @property
    def movs_defending(self) -> list[MovPiece]:
        return self.__movs_defending
    
    @movs_defending.setter
    def movs_defending(self, movs: list[MovPiece]) -> None:
        self.__movs_defending = movs


    # propiedad in_defense
    @property
    def in_defense(self) -> bool: 
        return self.__in_defense

    @in_defense.setter
    def in_defense(self, value: bool) -> None: 
        self.__in_defense = value

    
    def spread_influence(self, board: "Board") -> None: 
        self.update_presence(board)

        for mov in self.admin_obj.get_movs():
            self.add_objetives(board, mov)

    
    def clear_influence(self, board: "Board") -> None: 
        for mov in self.admin_obj.get_movs():
                    self.clear_influence_off_mov(board, mov)

    
    def clear_influence_off_mov(self, board: "Board", mov: MovPiece) -> None: 
        for coord in self.admin_obj.get_coords_off_mov(mov):
            board.get_scuare(coord).deleted__mov_prowl(mov)

        self.admin_obj.clear_store_off_mov(mov)

    
    def add_objetives(self, board: "Board", mov: MovPiece) -> None: 
        coord_actual: Coord = self.coord + mov
        ficha: EntityChess

        while True:
            ficha = board.get_ficha(coord_actual)

            match ficha:
                case PieceChess():
                    condition: bool = mov.is_ofensive and not self.is_equals_class(ficha.clase)
                    tipo: str = "enemy" if condition else "invalid"

                    self.add_coord_objetive(mov, coord_actual, tipo)
                    ficha.add_mov_prowl(mov)
                    break

                case EmptyChess():
                    condition: bool = mov.is_occupiable
                    tipo: str = "empty" if condition else "invalid"

                    self.add_coord_objetive(mov, coord_actual, tipo)
                    ficha.add_mov_prowl(mov)

                case None:
                    break
                

            if not mov.is_spreadable:
                break

            coord_actual += mov

    
    def coord_is_objetive(self, coord: Coord, value: str) -> bool: 
        data = (coord, value)

        if self.in_defense:
            if self.in_hacke:
                return False
            
            for mov in self.__movs_defending:
                if self.admin_obj.coord_in_store_off_mov(mov):
                        return True

            return False

        if self.in_hacke:
            if not data in self.army.coords_priority:
                return False

            if not self.admin_obj.coord_in_store(coord, value):
                return False
                    
            return True
                    
        return self.admin_obj.coord_in_store(coord, value)

    
    def get_coords_objetive(self) -> list[tuple[Coord, str]]: 
        result: list = []

        if self.in_defense:
            if self.in_hacke:
                return result
            
            for mov in self.movs_defending:
                if mov in self.admin_obj.get_movs():
                    result += self.admin_obj.get_data_off_mov(mov)
                
            return result

        if self.in_hacke:
            for data in self.admin_obj.get_data():
                if data in self.army.coords_priority:
                    result.append(data)

            return result

        return self.admin_obj.get_data()

    
    def add_coord_objetive(self, mov: MovPiece, coord: Coord, tipo: str) -> None: 
        self.admin_obj.add_coord_off_mov(mov, coord, tipo)