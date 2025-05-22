from typing import TYPE_CHECKING, Optional

from copy import deepcopy

from src.core.chess_constant import OBJ_INVALID, OBJ_ENEMY

if TYPE_CHECKING:
    from core.types_chess import DataArmy
    from src.core.coordinate import Coord
    from src.core.piece import PieceChess
    from src.core.mov_piece import MovPiece
    from src.core.pieces import Peon, Rey
    from src.core.board import Board
    from src.core.types_chess import ColorPiece

class Army:
    peon_passant: "Peon" = None
    
    
    def __init__(self,data_army: "DataArmy",  console_color: "ColorPiece" = "white", id_army: str | None = None) -> None:     
        self.active_enrroque_corto: bool = True
        self.active_enrroque_largo: bool = True
        
        # Condicion de generacion de id
        self.id: str = id_army if id_army != None else f"id: {id(self)}"
        
        self.console_color: "ColorPiece" = console_color
        
        self.coords_priority: list[tuple["Coord", str]]  = []
        self.pieces_defending: list["PieceChess"]  = []
        self.pieces_cemetery: list["PieceChess"] = []
        
        self.__data_pieces: "DataArmy" = {"data_rey": None, "data_pieces": []}
        self.__copy_data_pieces: "DataArmy" = {"data_rey": None, "data_pieces": []}
        
        self.pieces = data_army 
    
    
    # propiedad pieces
    @property
    def pieces(self)  -> list[tuple["Coord", "PieceChess"]]:
        data_ficha: list[tuple["Coord", "PieceChess"]] = self.__copy_data_pieces["data_pieces"].copy()
        data_rey: tuple["Coord", "Rey"] | None = self.__copy_data_pieces["data_rey"]
        
        if data_rey != None:
            data_ficha.append(data_rey)
        
        return data_ficha
    
    @pieces.setter
    def pieces(self, value: "DataArmy") -> None:
        self.__data_pieces["data_rey"] = value["data_rey"]
        self.__data_pieces["data_pieces"] = value["data_pieces"]
        
        self.__copy_data_pieces = deepcopy(self.__data_pieces)
        
        # Configuracion de Pieces
        for _, piece in self.pieces:
            piece.army = self
    
    # propiedad Rey
    @property
    def rey(self) -> Optional["Rey"]:
        data: tuple[Coord, "Rey"] | None = self.__copy_data_pieces["data_rey"]
        
        if data == None:
            return None
        
        _, rey = data
        return rey
    
    
    @property
    def in_hacke(self) -> bool:
        if self.rey == None:
            return False
        
        in_hacke, _ = self.rey.square.is_attacked()
        return  in_hacke
    
    
    @property 
    def in_hacke_mate(self) -> bool:
        if not self.in_hacke:
            return False
        
        coords_disp: list[tuple[Coord, str]] = [
            coord 
            for _, piece in self.pieces 
            for coord in piece.get_coords_objetive()
        ]
        
        for _, tipo in coords_disp:
            if tipo != OBJ_INVALID:
                return  False
        
        return True
    
    
    
    def init_influence(self, board: "Board") -> None: 
        for _, piece in self.pieces:
            piece.spread_influence(board)
    
    
    def update_influence_rey(self, board: "Board") -> None: 
        if self.rey == None:
            return
        
        self.clear_pieces_defending()
        self.rey.spread_influence(board)
    
    
    def restart(self) -> None: 
        self.active_enrroque_corto = True
        self.active_enrroque_largo= True
        
        self.__copy_data_pieces = deepcopy(self.__data_pieces)
        
        # Configuracion de Pieces
        for _, piece in self.pieces:
            piece.army = self
        
        self.clear_cemetery()
        self.pieces_defending.clear()
        self.coords_priority.clear()
    
    
    def notation_FEN_enrroque(self) -> str:
        notation: str = \
            f"{"k" if self.active_enrroque_corto else ""}" +\
            f"{"q" if self.active_enrroque_largo else ""}"
        
        return notation if notation != "" else "-"
    
    
    # Cemetery functions
    def add_piece_to_cemetery(self, piece: "PieceChess") -> None:
        self.pieces_cemetery.append(piece)
    
    
    def clear_cemetery(self) -> None:
        self.pieces_cemetery.clear()
    
    
    def add_piece_defending(self, piece: "PieceChess", alloweds_movs: list["MovPiece"]) -> None:
        piece.in_still = True
        
        for mov in alloweds_movs:
            piece.allowed_movs.append(mov)
        
        self.pieces_cemetery.append(piece)
    
    
    def clear_pieces_defending(self) -> None:
        for piece in self.pieces_defending:
            piece.in_still = False
            piece.allowed_movs.clear()
        
        self.pieces_defending.clear()
    
    
    def reset_coords_priority(self) -> None:
        self.coords_priority.clear()
        
        in_hacke, mov_origin_hacke = self.rey.square.is_attacked()
        
        if in_hacke:
            piece_prowl: PieceChess = mov_origin_hacke.ficha
            
            coords_prioridad: list[tuple] = \
                [(piece_prowl.coord, OBJ_ENEMY)] + \
                piece_prowl.square.admin_objetives.get_data_off_mov(mov_origin_hacke)
            
            for coord in coords_prioridad:
                self.coords_priority.append(coord)
    
    
    # Peon passant Functions
    def set_peon_passant(self, peon: "PieceChess") -> None:
        self.peon_passant = peon
    
    
    def delete_peon_passant(self, tablero: "Board") -> None:
        if self.peon_passant == None:
            return
        
        self.peon_passant.is_passant = False
        self.peon_passant.update_presence(tablero)
        self.peon_passant = None
