from typing import TYPE_CHECKING

from src.core.chess_constant import (
    CHAR_VIEW_ALFIL,
    CHAR_VIEW_CABALLO,
    CHAR_VIEW_PEON, 
    CHAR_VIEW_REINA,
    CHAR_VIEW_REY,
    CHAR_VIEW_TORRE,    

    CHAR_FEN_ALFIL,
    CHAR_FEN_CABALLO,
    CHAR_FEN_PEON,
    CHAR_FEN_REINA,
    CHAR_FEN_REY,
    CHAR_FEN_TORRE
    )

from src.core.piece import PieceChess
from src.core.mov_piece import MovPiece, MovPieceSpreadable

if TYPE_CHECKING:
    from src.core.board import Board
    from src.core.army import Army
    from src.core.square import Square
    from src.core.coordinate import Coord



class Alfil(PieceChess):
    def __init__(self, console_color: str = "white", clase: str = "", army: "Army" = None, square: "Square" = None) -> None:
        super().__init__(
            char_view= CHAR_VIEW_ALFIL, 
            char_fen= CHAR_FEN_ALFIL,
            console_color= console_color, 
            clase=clase, 
            army=army, 
            square=square,
        )
        
        self.movs = [
            MovPieceSpreadable(self, (-1, -1)),
            MovPieceSpreadable(self, (-1, 1)),
            MovPieceSpreadable(self, (1, -1)),
            MovPieceSpreadable(self, (1, 1)),
        ]



class Torre(PieceChess):
    def __init__(self, console_color: str = "white", clase: str = "", army: "Army" = None, square: "Square" = None) -> None:
        super().__init__(
            char_view=CHAR_VIEW_TORRE, 
            char_fen=CHAR_FEN_TORRE, 
            console_color=console_color, 
            clase=clase, 
            army=army, 
            square=square,
        )
        
        self.movs = [
            MovPieceSpreadable(self, (0, 1)),
            MovPieceSpreadable(self, (0, -1)),
            MovPieceSpreadable(self, (-1, 0)),
            MovPieceSpreadable(self, (1, 0)),
        ]



class Caballo(PieceChess):
    def __init__(self, console_color: str = "white", clase: str = "", army: "Army" = None, square: "Square" = None) -> None:
        super().__init__(
            char_view=CHAR_VIEW_CABALLO, 
            char_fen=CHAR_FEN_CABALLO, 
            console_color=console_color, 
            clase=clase, 
            army=army, 
            square=square,
        )
        
        self.movs = [
            MovPiece(self, (2, 1)),
            MovPiece(self, (2, -1)),
            MovPiece(self, (-1, 2)),
            MovPiece(self, (1, 2)),
            MovPiece(self, (-2, -1)),
            MovPiece(self, (-2, 1)),
            MovPiece(self, (-1, -2)),
            MovPiece(self, (1, -2)),
        ]



class Reina(PieceChess):
    def __init__(self, console_color: str = "white", clase: str = "", army: "Army" = None, square: "Square" = None) -> None:
        super().__init__(
            char_view=CHAR_VIEW_REINA, 
            char_fen=CHAR_FEN_REINA, 
            console_color=console_color, 
            clase=clase, 
            army=army, 
            square=square,
        )
        
        self.movs = [
            MovPieceSpreadable(self, (0, 1)),
            MovPieceSpreadable(self, (0, -1)),
            MovPieceSpreadable(self, (-1, 0)),
            MovPieceSpreadable(self, (1, 0)),
            MovPieceSpreadable(self, (-1, -1)),
            MovPieceSpreadable(self, (-1, 1)),
            MovPieceSpreadable(self, (1, -1)),
            MovPieceSpreadable(self, (1, 1)),    
        ]



from src.core.mov_piece import  MovPeonDoubleFrontal, MovPeonFrontal, MovPeonDiagonal, MovPeonPassant
from src.core.types_chess import EDirectionPeon


class Peon(PieceChess):
    
    def __init__(self, direction:EDirectionPeon, console_color: str = "white", clase: str = "", army: "Army" = None, square: "Square" = None) -> None:
        super().__init__(
            char_view=CHAR_VIEW_PEON, 
            char_fen=CHAR_FEN_PEON, 
            console_color=console_color, 
            clase=clase, 
            army=army, 
            square=square,
        )
        
        self.is_passant: bool = False
        self.direction: int = direction.value.direction
        self.index_column_meta: int = direction.value.index_goal_column
        
        self.double_frontal_mov = MovPeonDoubleFrontal(self, (self.direction * 2, 0))
        self.frontal_mov =  MovPeonFrontal(self, (self.direction, 0))
        
        self.diagonal_left_mov = MovPeonDiagonal(self, (self.direction, -1))
        self.diagonal_right_mov = MovPeonDiagonal(self, (self.direction, 1))
        
        self.passant_left_mov = MovPeonPassant(self, (0, -1))
        self.passant_right_mov = MovPeonPassant(self, (0, 1))
        
        self.diagonal_left_mov.mov_off_passant = self.passant_left_mov
        self.diagonal_right_mov.mov_off_passant = self.passant_right_mov
        
        self.passant_left_mov.mov_off_final_position = self.diagonal_left_mov
        self.passant_right_mov.mov_off_final_position = self.diagonal_right_mov
        
        self.movs = [
            self.frontal_mov,
            self.double_frontal_mov,
            
            self.diagonal_left_mov,
            self.diagonal_right_mov,
            
            self.passant_left_mov,
            self.passant_right_mov,
        ]


    def promote_to(self, piece: PieceChess) -> None:
        self.char_fen = piece.char_fen
        self.char_view = piece.char_view
        
        del self.direction
        del self.double_frontal_mov
        del self.frontal_mov
        del self.diagonal_left_mov
        del self.diagonal_right_mov
        del self.passant_left_mov
        del self.passant_right_mov

        self.movs = [mov.copy(self) for mov in piece.movs]
        self.__class__ = piece.__class__
        self.square.piece = self



from src.core.mov_piece import MovPieceRey, MovReyEnrroqueCorto, MovReyEnrroqueLargo
from src.core.chess_constant import OBJ_INVALID, CHAR_VIEW_REY


class Rey(PieceChess):
    def __init__(self, console_color: str = "white", clase: str = "", army: "Army" = None, square: "Square" = None) -> None:
        super().__init__(
            char_view=CHAR_VIEW_REY, 
            char_fen=CHAR_FEN_REY, 
            console_color=console_color, 
            clase=clase, 
            army=army, 
            square=square,
        )

        self.movs = [
            MovPieceRey(self, (0, 1)),
            MovPieceRey(self, (0, -1)),
            MovPieceRey(self, (-1, 0)),
            MovPieceRey(self, (1, 0)),
            MovPieceRey(self, (-1, -1)),
            MovPieceRey(self, (-1, 1)),
            MovPieceRey(self, (1, -1)),
            MovPieceRey(self, (1, 1)),
            
            MovReyEnrroqueCorto(self),
            MovReyEnrroqueLargo(self),
        ]
    
    
    def spread_influence(self, board: "Board") -> None:
        # llamada a la funcion de la superclase
        super().spread_influence(board)
        
        # se invalida la casilla puesta a a direccion del movimiento de origen de hacke, para volverla invalida
        in_hacke, mov_origin_hacke = self.square.is_attacked()

        if in_hacke:
            coord = self.coord + mov_origin_hacke
            
            if  mov_origin_hacke.is_offensive and\
                mov_origin_hacke.is_spreadable and\
                board.is_valid_coord(coord):  

                self.add_coord_objetive(mov_origin_hacke, coord, OBJ_INVALID)
    
    
    def coord_is_objetive(self, coord: "Coord", value: str) -> bool:
        return self.square.admin_objetives.coord_in_store(coord, value)
    
    
    def get_coords_objetive(self) -> list[tuple["Coord", str]]:
        return self.square.admin_objetives.get_data()
    