from typing import TYPE_CHECKING, Optional

from src.core.objetives_store import ObjetivesStore

if TYPE_CHECKING:
    from src.core.types import ObjetiveChess
    from src.core.piece import PieceChess
    from src.core.coordinate import Coord
    from src.core.movs.piece_mov import PieceMov
    from src.core.board import Board



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
    en el Board hay en total 64 (8 x 8) clases Square,  \n
    estas estan hechas para quedarse siempre en su posicion en la matriz.  \n
    
    > Las clases square contienen siempre una ficha o un None,  \n
    esta ficha puede ser reemplazada por otra muchas veces,   \n
    al obtener una nueva ficha la ficha tambien guarda   \n
    la referencia del square en su atributo square  \n
    
    > La lista de movs_on_prowl contiene los movimientos   \n
    de fichas que tienen como objetivo este square, esto   \n
    quiere decir que estas fichas tienen la capacidad de trasladarse a este square.  \n
    
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
    - piece (PieceyChess)                         ficha contenida actualmente en el square, el square puede cambiar de ficha  \n
    - movs_on_prowl (dict[""MovPiece"", None])        lista de movimientos de fichas que tienen como objetivo este Square  \n
    '''
    
    def __init__(self, coord: "Coord", board: "Board") -> None:
        self.__board: "Board" = board
        self.__coord: "Coord" = coord
        self.__sealed_piece: Optional["PieceChess"] = None
        
        self.__admin_objetives: ObjetivesStore = ObjetivesStore() 
        self.__movs_on_prowl: dict["PieceMov", None] = {}
    
    
    # propiedad Piece
    @property
    def piece(self) -> Optional["PieceChess"]: 
        '''
        Atributo que hace referencia a la ficha que contiene la casilla
        La ficha contenida en la casilla puede cambiar
        '''
        return self.__sealed_piece
    
    @piece.setter
    def piece(self, value: Optional["PieceChess"]) -> None: 
        self.__sealed_piece = value
    
    
    #Propiedad Coord
    @property
    def coord(self) ->" Coord":
        '''
        Atributo que representa la coordenada de la casilla en el tablero 
        '''
        return self.__coord
    
    
    # Propiedad Board
    @property
    def board(self) -> "Board":
        '''
        Atributo que representa el tablero en el que se encuentra la casilla
        '''
        return self.__board
    
    
    #  Propiedad AdminOdjetives
    @property
    def admin_objetives(self) -> ObjetivesStore:
        '''
        Atributo que representa la clase que administra el registro de las coordenadas objetivos
        de la ficha que contiene la casilla
        '''
        return self.__admin_objetives
    
    
    # Propiedad movs_prowl
    @property
    def movs_on_prowl(self) -> list["PieceMov"]:
        '''
        Atributo que contiene la lista de todos los movimientos de otras fichas 
        que tienen como objetivo a esta casilla
        '''
        return list(self.__movs_on_prowl.keys())
    
    
    def delete_piece(self) -> None:
        '''
        Funcion que elimina de manera segura los datos de influencia que ejerce la ficha 
        de esta casilla, ademas de eliminarla
        '''
        self.clear_influence()
        self.pop_piece()
    
    
    def pop_piece(self) -> Optional["PieceChess"]:
        '''
        Funcion que elimina las referencias que enlazan a una ficha y una casilla, ademas de retornar la ficha retirada
        '''
        piece: Optional["PieceChess"] = self.piece
        
        if not piece is None:
            piece.square = None
        
        self.piece = None
        
        return piece
    
    
    def receive_piece(self, piece: "PieceChess") -> None:
        '''
        Funcion que crea un enlace entre la ficha y la casilla, ademas de configurar el administrador de objetivoa
        '''
        self.pop_piece()
        self.piece = piece
        piece.square = self
        self.admin_objetives.set_movs(*self.piece.movs)
    
    
    def deliver_piece(self, other: "Square") -> None:
        '''
        Funcion que envia una ficha a la casilla pasada como parametro, eliminando primero la influencia de ambas fichas
        para luego reiniciar la influencia en la nueva posicion
        '''
        self.clear_influence()
        other.clear_influence()
        
        piece: Optional["PieceChess"] = self.pop_piece()
        
        if not piece is None:
            other.receive_piece(piece)
        
        self.update_influence()
        other.update_influence()
    
    
    def add_mov_prowl(self, mov: "PieceMov") -> None: 
        '''
        Añade una clase ""MovPiece"" al diccionario movs_on_prowl
        '''
        self.__movs_on_prowl[mov] = None
    
    
    def deleted_mov_prowl(self, mov: "PieceMov")-> None: 
        '''
        Elimina una clase ""MovPiece"" al diccionario movs_on_prowl
        '''
        self.__movs_on_prowl.pop(mov)
    
    
    def is_attacked(self, substitute_clase: Optional[str] = None , clase_enemy: Optional[str] = None ) -> Optional["PieceMov"]:
        '''
        - Devuelve True si el square esta siendo atacado por alguna ficha que tenga diferente clase que la clase de la ficha del square
        - Opcionalmente se puede definir una clase enemiga en especifica 
        - Opcionalmente se puede definir una clase susttuta en caso la casilla no tenga una pieza con l cual comparar clases
        - Si la casilla no tiene ficha entonces no sera requerido validar la clase enemiga
        - Solo se tomara en cuenta los movimientos ofensivos
        - En caso no haya movimientos enemigos que cumplan estas condiciones retornara None
        '''
        
        if  not self.piece is None and self.piece.clase == clase_enemy or\
            not substitute_clase is None and substitute_clase == clase_enemy:
            raise Exception("Error de busqueda: la clase enemiga pasado como parametro es la misma que de la pieza en la casilla")
        
        movs_offensives: list["PieceMov"] = list(filter(
            lambda mov: mov.is_offensive, 
            self.movs_on_prowl
        ))
        
        if not clase_enemy is None:
            movs_offensives = list(filter(
                lambda mov: mov.piece.clase == clase_enemy,
                movs_offensives
            ))
        
        elif clase_enemy is None:
            movs_offensives = list(filter(
                lambda mov:    \
                    substitute_clase != mov.piece.clase\
                    if not substitute_clase is None else\
                    self.piece.clase != mov.piece.clase\
                    if not self.piece is None else\
                    True,
                
                movs_offensives
            ))
        
        if len(movs_offensives) == 0:
            return None
        
        return movs_offensives[0]
    
    
    def clear_influence(self) -> None:
        '''
        Funcion que limpia la imfluencia de la pieza que contiene
        '''
        if self.piece == None:
            return
        
        self.piece.clear_influence()
    
    
    def spread_influence(self) -> None:
        '''
        Funcion que propaga la influencia de la pieza que contiene
        '''
        if self.piece == None:
            return
        
        self.piece.spread_influence()
    
    
    def update_presence(self) -> None:
        '''
        Actualiza la presencia de los movimientos que recibe la casilla
        '''
        for mov in self.movs_on_prowl.copy():
            mov.clear_register()
            mov.register()
    
    
    def update_influence(self) -> None:
        '''
        Actualiza la presencia y la influencia de la pieza que contiene
        '''
        self.update_presence()
        self.spread_influence()
    
    
    def get_coords_objetive(self) -> list[tuple["Coord", "ObjetiveChess"]]: 
        '''
        Funcion que devuelve el registro de las coordenadas objetivos de la pieza que contiene
        '''
        return self.piece.get_coords_objetive() if not self.piece is None else []
    
    
    def get_mov_on_prowl_to_piece(self, piece: "PieceChess") -> Optional["PieceMov"]:   
        '''
        Funcion que obtiene el movimiento que recibe la casilla de una ficha en especifico
        en caso en el que la pieza no envie movimiento alguno, retornar None
        '''
        movs: list["PieceMov"] = list(filter(
            lambda mov: mov.piece == piece,
            self.movs_on_prowl
        ))
        
        return movs[0] if len(movs) > 0 else None
