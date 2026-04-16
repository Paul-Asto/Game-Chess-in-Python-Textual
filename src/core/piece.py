from typing import TYPE_CHECKING, Optional, Sequence
from src.core.types import CharViewPiece, CharFenPiece, ColorPiece, ObjetiveChess, IdPiece


if TYPE_CHECKING:
    from src.core.army import Army
    from src.core.square import Square
    from src.core.board import Board
    from src.core.movs.piece_mov import PieceMov
    from src.core.coordinate import Coord
    from src.core.data_classes import DataPawn



class PieceChess:  
    
    def __init__(
            self,
            id: IdPiece,
            character_view: CharViewPiece,
            character_fen: CharFenPiece,
            console_color: ColorPiece = ColorPiece.WHITE,
            value_class: str = "",
            army: Optional["Army"] = None,
            square: Optional["Square"] = None,
            movs: Sequence["PieceMov"] = [],
            data_pawn: Optional["DataPawn"] = None,
            hacked_restricted: bool = True
        ) -> None:
        
        self.__in_still: bool = False
        self.__hacked_restricted: bool = hacked_restricted
        
        self.__id: IdPiece = id
        self.__character_view: CharViewPiece = character_view
        self.__character_fen: CharFenPiece = character_fen
        self.__console_color: ColorPiece = console_color
        self.__class: str = value_class
        
        self.__square: Optional["Square"]  = square
        self.__army: Optional["Army"] = army
        self.__data_pawn: Optional["DataPawn"] = data_pawn
        
        self.__movs: Sequence["PieceMov"] = movs
        self.__allowed_movs: list["PieceMov"] = []
    
    
    # propiedad id
    @property
    def id(self) -> IdPiece: 
        '''
        Propiedad que identifica el tipo de pieza
        '''
        return self.__id
    
    
    # propiedad char view
    @property
    def char_view(self) -> str: 
        '''
        Propiedad que devuelve el caracter de vista de la pieza
        '''
        return self.__character_view.value
    
    @property
    def character_view(self) -> CharViewPiece: 
        return self.__character_view
    
    @character_view.setter
    def character_view(self, value: CharViewPiece) -> None:
        self.__character_view = value
    
    
    # propiedad char fen
    @property
    def character_fen(self) -> CharFenPiece: 
        return self.__character_fen
    
    @character_fen.setter
    def character_fen(self, value: CharFenPiece) -> None:
        self.__character_fen = value
    
    
    # propiedad console color
    @property
    def console_color(self) -> ColorPiece:
        '''
        Propiedad que representa el color de la pieza
        '''
        try:
            return self.army.console_color
        
        except:
            return self.__console_color
        
    # propiedad color
    @property
    def str_color(self) -> str:
        '''
        Propiedad que representa el color de la pieza en string
        '''
        return self.console_color.value
    
    
    # Propiedad Clase
    @property
    def clase(self) -> str: 
        '''
        Propiedad que representa la clase de la pieza, las piezas de una misma armada tienen la misma clase
        '''
        if self.__army != None:
            return self.army.clase
        
        if self.__class == "":
            raise Exception("La ficha no pertenece a ninguna clase")
        
        return self.__class
    
    @clase.setter
    def clase(self, value: str) -> None:  
        self.__class = value
    
    
    # propiedad in_still
    @property
    def in_still(self) -> bool:
        '''
        Propiedad estado que verifica si la pieza esta en un estado de quietud, en el que solo puede moverse a movimientos permitidos
        '''
        return self.__in_still
    
    @in_still.setter
    def in_still(self, value: bool)  -> None:
        self.__in_still = value
    
    
    # propiedad hacked_restrincted
    @property
    def hacked_restricted(self) -> bool:
        '''
        Propiedad estado que verifica si la pieza se mueve libremente al estar en un estado hacke, True en el caso del rey
        '''
        return self.__hacked_restricted
    
    @hacked_restricted.setter
    def hacked_restricted(self, value: bool)  -> None:
        self.__hacked_restricted = value
    
    
    # propiedad in_hacke
    @property
    def in_hacke(self) -> bool:
        '''
        Propidad estado que verifica si la armada de la pieza se encuentra en estado hacke
        '''
        return self.army.in_hacke if self.__army != None else False
    
    
    # propiedad movs
    @property
    def movs(self) -> Sequence["PieceMov"]:
        '''
        Propiedad que devuelve los movimientos de la pieza
        '''
        return self.__movs
    
    @movs.setter
    def movs(self, value: Sequence["PieceMov"]) -> None:
        self.__movs = value
    
    
    # propiedad allowed movs
    @property
    def allowed_movs(self) -> list["PieceMov"]:
        '''
        Propiedad que devuelve los movimientos permitidos de la pieza en caso de estar en un estado de quietud
        '''
        return self.__allowed_movs
    
    
    # Propiedad Army
    @property
    def army(self) -> "Army":
        '''
        Propiedad que hace referencia a la armada de la pieza
        '''
        if self.__army == None:
            raise Exception("La ficha no pertenece a ninguna armada")
        
        return self.__army
    
    @army.setter
    def army(self, army: "Army") -> None: 
        self.__army = army
    
    
    # Propiedad Board
    @property
    def board(self) -> "Board": 
        '''
        Propiedad que hace referencia al tablero en el que se encuentra la pieza
        '''
        return self.square.board
    
    
    # Propiedad Square
    @property
    def square(self) -> "Square": 
        '''
        Propiedad que hace referencia ala casilla en el que se encuentra la pieza
        '''
        if self.__square == None:
            raise Exception("La ficha no se encuentra en ningun scuare")
        
        return self.__square
    
    @square.setter
    def square(self, scuare: Optional["Square"]) -> None:
        self.__square = scuare
    
    
    # Propiedad data Pawn
    @property
    def data_pawn(self) -> "DataPawn":
        '''
        Propiedad que hace referencia a la clase de datos del peon, util solo en caso la pieza sea un peon
        '''
        if self.__data_pawn == None:
            raise Exception("La ficha no  contiene datos de peon")
        
        return self.__data_pawn
    
    @data_pawn.setter
    def data_pawn(self, data_pawn: Optional["DataPawn"]) -> None: 
        self.__data_pawn = data_pawn
    
    
    # Propiedad Coord
    @property
    def coord(self) -> "Coord": 
        '''
        Propiedad que devuelve la coordenada de la casilla en el que se encuentra la pieza
        '''
        return self.square.coord
    
    
    def add_allowed_mov(self, mov: "PieceMov") -> None:
        '''
        Funcion que registra los movimientos permitidos de la pieza en caso de estar en un estado de quietud
        '''
        self.__allowed_movs.append(mov)
    
    def clear_allowed_movs(self) -> None:
        '''
        Funcion que elimina el registro de los movimientos permitidos de la pieza en caso de estar en un estado de quietud
        '''
        self.__allowed_movs.clear()
    
    
    def send_to_cemetery(self) -> None:
        '''
        Funcion que manda a la pieza al cementerio de la armada
        '''
        self.army.add_piece_to_cemetery(self)
    
    
    def is_equals_class(self, clase: str) -> bool:
        '''
        Funcion que verifica si la clase pasada como parametro es la mism clase que de la pieza
        '''
        return self.clase == clase
    
    
    def update_presence(self) -> None: 
        '''
        Funcion que limpia y registra los movimientos que recibe su casilla
        '''
        for mov in self.square.movs_on_prowl.copy():
            mov.clear_register()
            mov.register()
    
    
    def spread_influence(self) -> None: 
        '''
        Funcion que inicializa el registro de los movimientos de la piezaa para propagar la influencia a otras casillas
        '''
        for mov in self.movs:
            mov.register()
    
    
    def update_influence(self) -> None: 
        '''
        Funcion que actualiza la precencia y propaga la influencia
        '''
        self.update_presence()
        self.spread_influence()
    
    
    def clear_influence(self) -> None: 
        '''
        Funcion que borra el registro de todos los movimientos de la pieza
        '''
        for mov in self.movs:
            mov.clear_register()
    
    
    def coord_is_objetive(self, coord: "Coord", objetive: ObjetiveChess) -> bool: 
        '''
        Funcion que verifica si una coordenada se encuentra registrada como objetivo en el registro de la casilla
        Tiene en cuenta 3 estados:
        - Si no tiene restrincion de hacke, verifica en el registro de todos los movimientos
        - Si esta en estado de quietud, verifica en el registro de solo los movimientos permitidos
        - Si se encuentra en hacke, verifica en el registro de solo las coordenadas prioridad de la armada
        '''
        if not self.hacked_restricted:
            return self.square.admin_objetives.coord_in_store(coord, objetive)
        
        if self.in_still:
            if self.in_hacke:
                return False
            
            movs_width_coord = filter(
                lambda mov: \
                    mov in self.movs and\
                    self.square.admin_objetives.coord_in_store_off_mov(mov, coord, objetive),
                self.allowed_movs
            )
            
            return any(movs_width_coord)
        
        if self.in_hacke:
            if not (coord, objetive) in self.army.coords_priority:
                return False
            
            if not self.square.admin_objetives.coord_in_store(coord, objetive):
                return False
                    
            return True
                    
        return self.square.admin_objetives.coord_in_store(coord, objetive)
    
    
    def get_coords_objetive(self) -> list[tuple["Coord", ObjetiveChess]]: 
        '''
        Funcion que devuelve el registro de las coordenadas objetivos registrados en la casilla
        Tiene en cuenta 3 estados:
        - Si no tiene restrincion de hacke, devuelve todos los registros
        - Si esta en estado de quietud, devuelve solo los registros de movimientos permitidos
        - Si se encuentra en hacke, devuelve solo los registros de coordenadas prioridad de la armada
        '''
        if self.__square is None:
            return []
        
        if not self.hacked_restricted:
            return self.square.admin_objetives.get_data()
        
        if self.in_still:
            if self.in_hacke:
                return []
            
            return [
                data
                for allowed_mov in self.allowed_movs
                if allowed_mov in self.movs
                for data in self.square.admin_objetives.get_data_off_mov(allowed_mov)
            ]
        
        if self.in_hacke:
            return [
                data
                for data in self.square.admin_objetives.get_data()
                if data in self.army.coords_priority
            ]
        
        return self.square.admin_objetives.get_data()
    
    
    def add_coord_objetive(self, mov: "PieceMov", coord: "Coord", objetive: ObjetiveChess) -> None: 
        '''
        Funcion que añade un registro de un movimiento que recibe la casilla de la pieza
        '''
        self.square.admin_objetives.add_coord_off_mov(mov, coord, objetive)   
    
    
    def promote_to(self, piece: "PieceChess") -> None:
        '''
        Funcion que modifica la pieza actual y la promueve  otra pieza para modificar su comportamiento
        util en la promocion de peon
        '''
        self.character_fen = piece.character_fen
        self.character_view = piece.character_view
        self.__id = piece.id
        
        self.data_pawn = None
        
        self.movs = [mov.copy(self) for mov in piece.movs]
        self.square.receive_piece(self)
