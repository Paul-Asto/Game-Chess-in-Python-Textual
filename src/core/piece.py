from typing import TYPE_CHECKING, Optional
from src.core.types_chess import CharFenPiece, ColorPiece, CharViewPiece

if TYPE_CHECKING:
    from src.core.army import Army
    from src.core.square import Square
    from src.core.board import Board
    from src.core.mov_piece import MovPiece
    from src.core.coordinate import Coord



class PieceChess:  
    
    def __init__(
            self, 
            char_view: CharViewPiece,
            char_fen: CharFenPiece,
            console_color: ColorPiece = "white",
            clase: str = "",
            army: Optional["Army"] = None,
            square: Optional["Square"] = None
        ) -> None:

        self.in_still: bool = False

        
        self.__char_view: CharViewPiece = char_view
        self.__char_fen: CharFenPiece = char_fen
        self.__console_color: ColorPiece = console_color
        self.__clase: str = clase
        
        self.__square: Optional["Square"]  = square
        self.__army: Optional["Army"] = army
        
        self.movs: list["MovPiece"] = []
        self.allowed_movs: list["MovPiece"] = []
    
    
    # propiedad char view
    @property
    def char_view(self) -> CharViewPiece: 
        return self.__char_view
    
    @char_view.setter
    def char_view(self, value: CharViewPiece) -> None:
        self.__char_view = value


    # propiedad char fen
    @property
    def char_fen(self) -> CharFenPiece: 
        return self.__char_fen
    
    @char_fen.setter
    def char_fen(self, value: CharFenPiece) -> None:
        self.__char_fen = value

    
    # propiedad console color
    @property
    def console_color(self) -> ColorPiece:
        try:
            return self.army.console_color
        
        except:
            return self.__console_color


    # Propiedade Clase
    @property
    def clase(self) -> str: 
        if self.__army != None:
            return self.army.id
        
        if self.__clase == "":
            raise Exception("La ficha no pertenece a ninguna clase")
        
        return self.__clase
    
    @clase.setter
    def clase(self, value: str) -> str:  
        self.__clase = value


    # propiedad in_hacke
    @property
    def in_hacke(self) -> bool:
        return self.army.in_hacke if self.__army != None else False
    
    @in_hacke.setter
    def in_hacke(self, value: bool) -> None: 
        self.__army.in_hacke = value
    

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
    def square(self) -> "Square": 
        if self.__square == None:
            raise Exception("La ficha no se encuentra en ningun scuare")
        
        return self.__square
    
    @square.setter
    def square(self, scuare: "Square") -> None:
        self.__square = scuare
    

    # Propiedad Coord
    @property
    def coord(self) -> "Coord": 
        if self.square == None:
            raise Exception("La ficha no se encuentra en un board")
        
        return self.square.coord 
    


    def send_to_cemetery(self) -> None:
        self.army.add_piece_to_cemetery(self)

    
    def is_equals_class(self, clase: str) -> bool:
        return self.clase == clase
    
    
    def add_mov_prowl(self ,mov: "MovPiece") -> None: 
        self.square.add_mov_prowl(mov)
    
    
    def update_presence(self, board: "Board") -> None: 
        for mov in self.square.movs_on_prowl.copy():
            mov.clear_register(board)
            mov.register(board)
    
    
    def spread_influence(self, board: "Board") -> None: 
        for mov in self.movs:
            mov.register(board)
    
    
    def update_influence(self, board: "Board") -> None: 
        self.update_presence(board)
        self.spread_influence(board)
    
    
    def clear_influence(self, board: "Board") -> None: 
        for mov in self.movs:
            mov.clear_register(board)
    
    
    def coord_is_objetive(self, coord: "Coord", value: str) -> bool: 
        if self.in_still:
            if self.in_hacke:
                return False
            
            for mov in self.allowed_movs:
                if not mov in self.movs:
                    continue
                
                if self.square.admin_objetives.coord_in_store_off_mov(mov, coord, value):
                        return True
            
            return False
        
        if self.in_hacke:
            if not (coord, value) in self.army.coords_priority:
                return False
            
            if not self.square.admin_objetives.coord_in_store(coord, value):
                return False
                    
            return True
                    
        return self.square.admin_objetives.coord_in_store(coord, value)
    
    
    def get_coords_objetive(self) -> list[tuple["Coord", str]]: 
        result: list = []
        
        if self.in_still:
            if self.in_hacke:
                return result
            
            for mov in self.allowed_movs:
                if mov in self.movs:
                    result += self.square.admin_objetives.get_data_off_mov(mov)
                
            return result
        
        if self.in_hacke:
            for data in self.square.admin_objetives.get_data():
                if data in self.army.coords_priority:
                    result.append(data)
        
            return result
        
        return self.square.admin_objetives.get_data()
    
    
    def add_coord_objetive(self, mov: "MovPiece", coord: "Coord", tipo: str) -> None: 
        self.square.admin_objetives.add_coord_off_mov(mov, coord, tipo)   
