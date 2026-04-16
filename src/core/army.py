from typing import TYPE_CHECKING, Optional
from src.core.types import ColorPiece, ArmyClass
from copy import deepcopy

from src.core.protocol_uci import from_coord_to_uci
from src.core.types import ObjetiveChess

if TYPE_CHECKING:
    from src.core.coordinate import Coord
    from src.core.piece import PieceChess
    from src.core.movs.piece_mov import PieceMov
    from src.core.data_classes import DataArmy

class Army:

    def __init__(self, data_army: "DataArmy",  console_color: "ColorPiece", army_class: Optional[ArmyClass] = None) -> None:     
        self.__active_short_castling: bool = True
        self.__active_long_castling: bool = True
        
        # passant atributes
        self.__pawn_passant: Optional["PieceChess"] = None
        self.__coord_passant: Optional["Coord"] = None
        
        self.__class: str = \
            army_class.value \
            if army_class != None else \
            f"id: {id(self)}"
        
        self.__console_color: "ColorPiece" = console_color
        
        self.__coords_priority: list[tuple["Coord", ObjetiveChess]]  = []
        self.__pieces_defending: list["PieceChess"]  = []
        self.__pieces_cemetery: list["PieceChess"] = []
        
        self.__init_data_pieces: "DataArmy" = data_army
        self.__data_pieces: "DataArmy" = deepcopy(data_army)
        
        # Configuracion inicial de Piezas
        for _, piece in self.pieces:
            piece.army = self
    
    
    # propiedad active_short_castling
    @property
    def active_short_castling(self) -> bool:
        '''
        Propiedad estado que representa si esta activo e enrroque corto
        '''
        return self.__active_short_castling
    
    @active_short_castling.setter
    def active_short_castling(self, value: bool) -> None:
        self.__active_short_castling = value
    
    
    # propiedad active_long_castling
    @property
    def active_long_castling(self) -> bool:
        '''
        Propiedad estado que representa si esta activo e enrroque largo
        '''
        return self.__active_long_castling
    
    @active_long_castling.setter
    def active_long_castling(self, value: bool) -> None:
        self.__active_long_castling = value
    
    
    # propiedad pieces
    @property
    def pieces(self)  -> list[tuple["Coord", "PieceChess"]]:
        '''
        Propiedad que devuelve todas las piezas de la armada con su respectiva coordenada inicial
        '''
        data_ficha: list[tuple["Coord", PieceChess]] = self.__data_pieces.pieces.copy()
        data_rey: tuple["Coord", PieceChess] | None = self.__data_pieces.king
        
        if data_rey != None:
            data_ficha.append(data_rey)
        
        return data_ficha
    
    @pieces.setter
    def pieces(self, data: "DataArmy") -> None:
        self.__init_data_pieces = data
        self.__data_pieces = deepcopy(self.__init_data_pieces)
        
        # Configuracion de Pieces
        for _, piece in self.pieces:
            piece.army = self
    
    
    @property
    def pieces_in_cementery(self) ->list["PieceChess"]:
        '''
        Propiedad de devuelve las fichas que se encuentran en el cementerio de piezas
        '''
        return self.__pieces_cemetery
    
    
    # propiedad Rey
    @property
    def king(self) -> Optional["PieceChess"]:
        '''
        Propiedad que devuelve la pieza rey de la armada
        '''
        data: tuple["Coord", PieceChess] | None = self.__data_pieces.king
        
        if data == None:
            return None
        
        _, king = data
        return king
    
    
    @property
    def console_color(self) -> ColorPiece:
        '''
        Propiedad que repreenta el color que tendra todas las fichas de la armada
        '''
        return self.__console_color
    
    
    @property
    def clase(self)  -> str:
        '''
        Propiedad que identifica y diferencia una rmada de otra
        '''
        return self.__class
    
    
    @property
    def in_hacke(self) -> bool:
        '''
        Propiedad estado que representa si el rey de la armada esta en hacke o no
        '''
        if self.king == None:
            return False
        
        mov_enemy: Optional["PieceMov"] = self.king.square.is_attacked()
        return  not mov_enemy is None
    
    
    @property 
    def in_hacke_mate(self) -> bool:
        '''
        Propiedad estado que representa si el rey de la armada esta en hacke mate o no
        '''
        
        coords_disp: list[tuple["Coord", ObjetiveChess]] = [
            coord 
            for _, piece in self.pieces 
            for coord in piece.get_coords_objetive()
        ]
        
        return not any([
            coord
            for coord, objetive in coords_disp
            if objetive != ObjetiveChess.INVALID
        ])
    
    
    @property
    def coords_priority(self) -> list[tuple["Coord", ObjetiveChess]]:
        '''
        Propiedad que devuelve la lista de coordenadas prioridad a los que se deben mover 
        las fichas para sacar al rey del estado de hacke
        '''
        if self.king is None:
            return []
        
        mov_enemy:  Optional["PieceMov"] = self.king.square.is_attacked()
        
        if mov_enemy is None:
            return []
        
        piece_prowl: PieceChess = mov_enemy.piece
        
        return \
            [(piece_prowl.coord, ObjetiveChess.ENEMY)] + \
            piece_prowl.square.admin_objetives.get_data_off_mov(mov_enemy)
    
    
    @property
    def notation_FEN_enrroque(self) -> str:
        '''
        Propiedad que representa en formato FEN el estado re enrroque largo y corto
        '''
        notation: str = \
            f"{"k" if self.active_short_castling else ""}" +\
            f"{"q" if self.active_long_castling else ""}"
        
        return notation if notation != "" else "-"
    
    
    @property
    def notation_FEN_passant(self) -> str:
        '''
        Propiedad que representa en formato FEN el estado passant de un peon
        '''
        if self.__coord_passant is None:
            return "-"
        
        return from_coord_to_uci(self.__coord_passant)
    
    
    def init_influence(self) -> None:
        '''
        Funcion que propaga la influencia de todas las fichas de la armada en el tablero
        ''' 
        for _, piece in self.pieces:
            piece.spread_influence()
    
    
    def update_influence_king(self) -> None: 
        '''
        Funcion que actualiza la influencia del rey para que pueda registar las fichas en defenza
        '''
        if self.king == None:
            return
        
        self.clear_pieces_defending()
        
        self.king.clear_influence()
        self.king.spread_influence()
    
    
    def restart(self) -> None: 
        '''
        Funcion que reinicia los datos de las piezas de la armada
        '''
        self.active_short_castling = True
        self.active_long_castling= True

        self.delete_data_passant()
        
        self.__data_pieces = deepcopy(self.__init_data_pieces)
        
        # Configuracion de Pieces
        for _, piece in self.pieces:
            piece.army = self
        
        self.clear_cemetery()
        self.__pieces_defending.clear()
        self.__coords_priority.clear()
    
    
    def add_piece_to_cemetery(self, piece: "PieceChess") -> None:
        '''
        Funcion para añadir piezas en el cementerio
        '''
        self.__pieces_cemetery.append(piece)
    
    
    def clear_cemetery(self) -> None:
        '''
        Funcion que elimina las piezas del cementerio de piezas
        '''
        self.__pieces_cemetery.clear()
    
    
    def add_piece_defending(self, piece: "PieceChess", alloweds_movs: list["PieceMov"]) -> None:
        '''
        Funcion que registra una pieza que esta en defenza del rey
        '''
        piece.in_still = True
        self.__pieces_defending.append(piece)
        
        for mov in alloweds_movs:
            piece.add_allowed_mov(mov)
    
    
    def clear_pieces_defending(self) -> None:
        '''
        Funcion que elimina el registro de las piezas que estan en defenza dek rey
        '''
        for piece in self.__pieces_defending:
            piece.in_still = False
            piece.clear_allowed_movs()
        
        self.__pieces_defending.clear()
    
    
    # Peon passant Functions
    def set_data_passant(self, pawn: "PieceChess", initial_coord: "Coord") -> None:
        '''
        Funcion que setea los datos de coordenada y peon passant para validar el movimiento
        '''
        pawn.data_pawn.is_passant = True
        self.__coord_passant = initial_coord
        self.__pawn_passant = pawn
    
    
    def delete_data_passant(self) -> None:
        '''
        Funcion que elimina los datos de cordenada y peon passant para invalidar el movimiento
        '''
        if self.__pawn_passant == None:
            return
        
        self.__coord_passant = None
        self.__pawn_passant.data_pawn.is_passant = False
        self.__pawn_passant.update_presence()
        self.__pawn_passant = None
