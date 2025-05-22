from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.piece import PieceChess
    from src.core.coordinate import Coord
    from src.core.mov_piece import MovPiece
    from src.core.board import Board



class AdminObjetives:
    
    def __init__(self) -> None:
        self.store_data: dict["MovPiece", dict["Coord", str]] = {}
    
    
    def set_movs(self, *movs_piece: "MovPiece") -> None:
        self.store_data.clear()
        
        for mov in movs_piece:
            self.store_data[mov] = {}
    
    
    def get_coords_off_mov(self, mov: "MovPiece") -> list["Coord"]:
        return list(self.store_data[mov].keys())
    
    
    def get_coords(self) -> list["Coord"]:
        result: list["Coord"] = []
        
        for data in self.store_data.values():
            result += data.keys()
        
        return result
    
    
    def get_data_off_mov(self, mov: "MovPiece") -> list[tuple["Coord", str]]:
        return list(self.store_data[mov].items())
    
    
    def get_data(self) -> list[tuple["Coord", str]]:
        result: list[tuple[tuple, str]] = []
        
        for data in self.store_data.values():
            result += data.items()
        
        return result
    
    
    def add_coord_off_mov(self, mov: "MovPiece", coord: "Coord", value: str) -> None:
        self.store_data[mov][coord] = value
    
    
    def clear_store_off_mov(self, mov: "MovPiece") -> None:
        self.store_data[mov].clear()
    
    
    def coord_in_store(self, coord: "Coord", value: str) -> bool:
        for mov in self.store_data.keys():
            if self.coord_in_store_off_mov(mov, coord, value):
                return True
        
        return False
    
    
    def coord_in_store_off_mov(self, mov: "MovPiece", coord: "Coord", value: str) -> bool:
        input: tuple = (coord, value)
        
        for data in self.get_data_off_mov(mov):
            if  data == input:
                return True
        
        return False



class Square:
    '''
    Class Scuare:  \n
    
    "Coord": (n, m) \n
    ___________________  \n
    |     Scuare       |  \n
    |__________________|  \n
    |  Piece or Empty  |  <----    Movs on Prowl: list[MovFicha] = [Mov, Mov, Mov]  \n
    |__________________|  \n
    
    > La clase Scuare representa una casilla del tablero,  \n
    en el Board hay en total 64 (8 x 8) clases Scuare,  \n
    estas estan hechas para quedarse siempre en su posicion en la matriz.  \n
    
    > Las clases scuare contienen siempre una ficha o un empty,  \n
    esta ficha puede ser reemplazada por otra muchas veces,   \n
    al obtener una nueva ficha la ficha tambien guarda   \n
    la referencia del scuare en su atributo scuare  \n
    
    > La lista de movs_on_prowl contiene los movimientos   \n
    de fichas que tienen como objetivo este scuare, esto   \n
    quiere decir que estas fichas tienen la capacidad de trasladarse a este scuare.  \n
    
    > Los movPieces son almacenados como llaves con valor None, 
    estos se diferencian entre si con su atributo value que es una tupla 
    de 2 int que representan la direccion de movimiento, ejemplo: \n
    
    - up -> (-1, 0)\n
    - down -> (1, 0)\n
    - left -> (0, -1)\n
    - right -> (0, 1)\n
    
    > pueden existir 2 movsPieces con un  mismo valor
    
    - Atributos:  \n
    - coord ("Coord"):                              coordenada  inmutable  \n
    - ficha (EntityChess)                         ficha contenida actualmente en el scuare, el scuare puede cambiar de ficha  \n
    - movs_on_prowl (dict[""MovPiece"", None])        lista de movimientos de fichas que tienen como objetivo este Scuare  \n
    '''
    
    def __init__(self, coord: "Coord") -> None      :
        self.coord: "Coord" = coord
        self.sealed_piece: "PieceChess" = None
        
        self.admin_objetives: AdminObjetives = AdminObjetives()
        self.__movs_on_prowl: dict["MovPiece", None] = {}
    
    
    # propiedad Ficha
    @property
    def piece(self) -> "PieceChess": 
        return self.sealed_piece
    
    @piece.setter
    def piece(self, value: "PieceChess") -> None: 
        self.sealed_piece = value

    
    # Propiedad movs_prowl
    @property
    def movs_on_prowl(self) -> list["MovPiece"]:
        return list(self.__movs_on_prowl.keys())
    
    def reset(self, board: "Board"):
        self.clear_influence(board)
        self.piece = None
    
    
    def trade_piece(self, square: "Square") -> None:
        piece_start = self.piece
        
        self.piece = None
        
        square.piece = piece_start
        piece_start.square = square
    
    
    def add_mov_prowl(self, mov: "MovPiece") -> None: 
        '''
        Añade una clase ""MovPiece"" al diccionario movs_on_prowl
        '''
        self.__movs_on_prowl[mov] = None
    
    
    def deleted_mov_prowl(self, mov: "MovPiece")-> None: 
        '''
        Elimina una clase ""MovPiece"" al diccionario movs_on_prowl
        '''
        self.__movs_on_prowl.pop(mov)
    
    
    def is_attacked(self, clase: str = None ) -> tuple[bool, "MovPiece"]:
        '''
        Devuelve True si el scuare esta siendo atacado por alguna ficha
        que tenga diferente clase que la clase de la ficha del scuare y 
        si el movimiento es ofensivo
        '''
        
        clase_attacked: str
        
        if clase == None:
            clase_attacked = self.piece.clase
        
        else:
            clase_attacked = clase
        
        for mov in self.movs_on_prowl:
            if clase_attacked == mov.ficha.clase:
                continue
            
            if mov.is_offensive:
                return (True, mov)
        
        return (False, None)
    
    
    def clear_influence(self, board: "Board") -> None:
        if self.piece == None:
            return
        
        self.piece.clear_influence(board)
    
    
    def spread_influence(self, board: "Board") -> None:
        if self.piece == None:
            return
        
        self.piece.spread_influence(board)
    
    
    def update_presence(self, board: "Board") -> None:
        for mov in self.movs_on_prowl.copy():
            mov.clear_register(board)
            mov.register(board)
    
    
    def update_influence(self, board: "Board") -> None:
        self.update_presence(board)
        self.spread_influence(board)
    
    
    def get_coords_objetive(self) -> list[tuple["Coord", str]]: 
        if self.piece == None:
            return []
        
        return self.piece.get_coords_objetive()
    

    def get_mov_on_prowl_to_piece(self, piece: "PieceChess") -> "MovPiece":
        for mov in self.movs_on_prowl:
            if mov.ficha == piece:
                return mov
                
        return None
