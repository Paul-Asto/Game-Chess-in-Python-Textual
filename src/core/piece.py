from rich.text import Text
from typing import Literal
from typing import TYPE_CHECKING
from src.chess_constant import OBJ_EMPTY, OBJ_ENEMY, OBJ_INVALID, ID_NONE_ARMY

from src.core.mov_piece import MovPiece
from src.coordinate import Coord

if TYPE_CHECKING:
    from src.core.army import Army
    from src.core.scuare import Scuare
    from src.core.board import Board



ColorPiece = Literal[
    "black",
    "grey",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "light_grey",
    "dark_grey",
    "light_red",
    "light_green",
    "light_yellow",
    "light_blue",
    "light_magenta",
    "light_cyan",
    "white",
]



class AdminObjetives:
    list_movs: list[MovPiece] 
    store_data: dict[MovPiece, dict[Coord, str]]

    def __init__(self, *movs_piece: MovPiece ) -> None:
        self.list_movs = []
        self.store_data = {}
        
        self.add_movs(*movs_piece)


    def add_movs(self, *movs_piece: MovPiece) -> None:
        for mov in movs_piece:
            if not mov in self.list_movs:
                self.list_movs.append(mov)
                self.store_data[mov] = {}


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
    console_color: ColorPiece = "white"
    view: Text

    str_fen: str = "-"
    __char: str = ""
    __scuare: "Scuare" = None
    __army: "Army"
    __clase_alter: str = ""

    def __init__(self, army: "Army" = None) -> None:
        self.__army = army
    
    # propiedad in_hacke
    @property
    def char(self) -> str:
        if self.__char == "":
            raise Exception("La ficha no tiene un caracter de vista")

        return self.__char

    @char.setter
    def char(self, value: str) -> None: 
        self.__char = value


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
            return self.army.id
        
        if self.__clase_alter == "":
            raise Exception("La ficha no pertenece a ninguna clase")

        return self.__clase_alter
    
    @clase.setter
    def clase(self, value: str) -> str:  
        self.__clase_alter = value


    # Propiedad Coordenada
    @property
    def coord(self) -> Coord: 
        if self.scuare == None:
            raise Exception("La ficha no se encuentra en un board")

        return self.scuare.coord 

    # Propiedad Army
    @property
    def army(self) -> "Army":
        if self.__army == None:
            raise Exception("La ficha no pertenece a ninguna armada")
        
        return self.__army

    @army.setter
    def army(self, army: "Army") -> None: 
        self.__army = army


    # Propiedad Scuare
    @property
    def scuare(self) -> "Scuare": 
        if self.__scuare == None:
            raise Exception("La ficha no se encuentra en ningun scuare")
        
        return self.__scuare

    @scuare.setter
    def scuare(self, scuare: "Scuare") -> None:
        self.__scuare = scuare


    def is_equals_class(self, clase: str) -> bool:
        return self.clase == clase


    def add_mov_prowl(self ,mov: MovPiece) -> None: 
        self.scuare.add_mov_prowl(mov)


    def update_presence(self, board: "Board") -> None: 
        for mov in self.scuare.movs_on_prowl.copy():
            mov.clear_register(board)
            mov.register(board)

    def spread_influence(self, board: "Board") -> None: ...

    def update_influence(self, board: "Board") -> None: ...

    
    def clear_influence(self, board: "Board") -> None: ...


    def make_mov(self, ficha_final: "EntityChess") -> tuple[bool, bool]: ...



class EmptyChess(EntityChess):

    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.clase = ID_NONE_ARMY
        self.char = " "

    @property
    def view(self) -> Text:
        result: Text = Text("\n")

        result.append("____________________________\n")
        result.append("|       EmptyChess          |\n")
        result.append("|___________________________|\n")
        result.append(self.scuare.view)

        return result

        
    def update_influence(self, board: "Board") -> None: 
        self.update_presence(board)



class PieceChess(EntityChess):
    in_still: bool = False
    allowed_movs: list[MovPiece]
    admin_obj: AdminObjetives

    def __init__(self, army = None):
        super().__init__(army)
        self.allowed_movs = []
        self.admin_obj = AdminObjetives()


    @property
    def view(self) -> Text:
        result: Text = Text("\n")

        result.append("____________________________\n")
        result.append("|")
        result.append(f"{self.__class__.__name__}({self.char} )".center(27), f"bold {self.console_color}")
        result.append("|\n")
        result.append(f"|{f"  Clase: {self.clase}".ljust(27)}|\n")
        result.append(f"|{f"  In Hacke: {self.in_hacke}".ljust(27)}|\n")
        result.append(f"|{f"  In still: {self.in_still}".ljust(27)}|\n")

        if self.in_still:
            allowed_mov_str: str = ""

            for mov in self.allowed_movs:
                allowed_mov_str += f"{str(mov.value)}, "

            result.append(f"|{f"  Allowed movs: [{allowed_mov_str}]".ljust(27)}|\n")

        result.append("|                           |\n")

        tablero_str: list[list[str]] = [["Ｘ " for _ in range(8)] for _ in range(8)] 

        y, x = self.coord
        tablero_str[y][x] = Text(f"{self.char}  ", f"bold {self.console_color}")

        for coord, tipo in self.get_coords_objetive():
            color: ColorPiece 

            if tipo == OBJ_EMPTY: color = "green"
            elif tipo == OBJ_ENEMY: color = "red"
            elif tipo == OBJ_INVALID: color = self.console_color

            y, x = coord
            tablero_str[y][x] = Text("Ｘ ", f"bold {color}")

        for column in tablero_str:
            result.append("|  ")

            for data in column: 
                result.append(data)
                
            result.append(" |\n")

        result.append("|                           |\n" )
        result.append("|___________________________|\n")
        result.append(self.scuare.view)
    
        return result
    

    def make_mov(self, ficha_final: EntityChess, tablero: "Board") -> tuple[bool, bool]:
        tipo_objetive: str
        movement_performed: bool = None
        is_objetive_enemy: bool = None

        if isinstance(ficha_final, PieceChess):
            tipo_objetive = OBJ_ENEMY
            is_objetive_enemy = True

        elif isinstance(ficha_final, EmptyChess):
            tipo_objetive = OBJ_EMPTY
            is_objetive_enemy = False
        
        if self.coord_is_objetive(ficha_final.coord, tipo_objetive):
            movement_performed = True
            mov_current: MovPiece

            for mov in ficha_final.scuare.movs_on_prowl:
                if mov.ficha == self:
                    mov_current = mov
                    break
            
            mov_current.execute(tablero, ficha_final, is_objetive_enemy)

        else:
            movement_performed = False

        return movement_performed, is_objetive_enemy


    def spread_influence(self, board: "Board") -> None: 
        for mov in self.admin_obj.get_movs():
            mov.register(board)


    def update_influence(self, board) -> None:
        self.update_presence(board)
        self.spread_influence(board)
    

    def clear_influence(self, board: "Board") -> None: 
        for mov in self.admin_obj.get_movs():
            mov.clear_register(board)

    
    def coord_is_objetive(self, coord: Coord, value: str) -> bool: 
        if self.in_still:
            if self.in_hacke:
                return False
            
            for mov in self.allowed_movs:
                if not mov in self.admin_obj.list_movs:
                    continue
                
                if self.admin_obj.coord_in_store_off_mov(mov, coord, value):
                        return True

            return False

        if self.in_hacke:
            if not (coord, value) in self.army.coords_priority:
                return False

            if not self.admin_obj.coord_in_store(coord, value):
                return False
                    
            return True
                    
        return self.admin_obj.coord_in_store(coord, value)

    
    def get_coords_objetive(self) -> list[tuple[Coord, str]]: 
        result: list = []

        if self.in_still:
            if self.in_hacke:
                return result
            
            for mov in self.allowed_movs:
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