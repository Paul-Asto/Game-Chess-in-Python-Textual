from typing import TYPE_CHECKING
from src.chess_constant import (
    CHAR_VIEW_ALFIL,
    CHAR_VIEW_CABALLO,
    CHAR_VIEW_PEON, 
    CHAR_VIEW_REINA,
    CHAR_VIEW_REY,
    CHAR_VIEW_TORRE,
    )

from src.core.piece import PieceChess
from src.core.mov_piece import MovPiece, MovPieceSpreadable

if TYPE_CHECKING:
    from src.core.army import Army


class Alfil(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.str_fen = "b" 
        self.char = CHAR_VIEW_ALFIL

        self.admin_obj.add_movs(
            MovPieceSpreadable(self, (-1, -1)),
            MovPieceSpreadable(self, (-1, 1)),
            MovPieceSpreadable(self, (1, -1)),
            MovPieceSpreadable(self, (1, 1)),
        )



class Torre(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.str_fen = "r" 
        self.char = CHAR_VIEW_TORRE

        self.admin_obj.add_movs(
            MovPieceSpreadable(self, (0, 1)),
            MovPieceSpreadable(self, (0, -1)),
            MovPieceSpreadable(self, (-1, 0)),
            MovPieceSpreadable(self, (1, 0)),
        )



class Caballo(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.str_fen = "n" 
        self.char = CHAR_VIEW_CABALLO
        
        self.admin_obj.add_movs(
            MovPiece(self, (2, 1)),
            MovPiece(self, (2, -1)),
            MovPiece(self, (-1, 2)),
            MovPiece(self, (1, 2)),
            MovPiece(self, (-2, -1)),
            MovPiece(self, (-2, 1)),
            MovPiece(self, (-1, -2)),
            MovPiece(self, (1, -2)),
        )



class Reina(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.str_fen = "q" 
        self.char = CHAR_VIEW_REINA

        self.admin_obj.add_movs(
            MovPieceSpreadable(self, (0, 1)),
            MovPieceSpreadable(self, (0, -1)),
            MovPieceSpreadable(self, (-1, 0)),
            MovPieceSpreadable(self, (1, 0)),
            MovPieceSpreadable(self, (-1, -1)),
            MovPieceSpreadable(self, (-1, 1)),
            MovPieceSpreadable(self, (1, -1)),
            MovPieceSpreadable(self, (1, 1)),    
        )



from src.core.mov_piece import  MovPeonDoubleFrontal, MovPeonFrontal, MovPeonDiagonal, MovPeonPassant



class Peon(PieceChess):
    orientacion: int
    is_passant: bool = False

    double_frontal_mov: MovPeonDoubleFrontal
    frontal_mov: MovPeonFrontal
    diagonal_left_mov: MovPeonDiagonal
    diagonal_right_mov: MovPeonDiagonal
    passant_left_mov: MovPeonPassant
    passant_right_mov: MovPeonPassant

    def __init__(self, orientacion: int , army: "Army" = None):
        super().__init__(army)
        
        self.str_fen = "p" 
        self.char = CHAR_VIEW_PEON
        self.orientacion = orientacion

        self.double_frontal_mov = MovPeonDoubleFrontal(self, (self.orientacion * 2, 0))
        self.frontal_mov =  MovPeonFrontal(self, (self.orientacion, 0))

        self.diagonal_left_mov = MovPeonDiagonal(self, (self.orientacion, -1))
        self.diagonal_right_mov = MovPeonDiagonal(self, (self.orientacion, 1))

        self.passant_left_mov = MovPeonPassant(self, (0, -1))
        self.passant_right_mov = MovPeonPassant(self, (0, 1))

        self.diagonal_left_mov.mov_off_passant = self.passant_left_mov
        self.diagonal_right_mov.mov_off_passant = self.passant_right_mov

        self.passant_left_mov.mov_off_final_position = self.diagonal_left_mov
        self.passant_right_mov.mov_off_final_position = self.diagonal_right_mov
    
        self.admin_obj.add_movs(
            self.frontal_mov,
            self.double_frontal_mov,
            
            self.diagonal_left_mov,
            self.diagonal_right_mov,

            self.passant_left_mov,
            self.passant_right_mov,
        )



from src.core.mov_piece import MovPieceRey, MovReyEnrroqueCorto, MovReyEnrroqueLargo
from src.chess_constant import OBJ_INVALID, OBJ_EMPTY, OBJ_ENEMY, CHAR_VIEW_REY
from src.coordinate import Coord

if TYPE_CHECKING:
    from src.core.board import Board
    from src.core.army import Army



class Rey(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.str_fen = "k" 
        self.char = CHAR_VIEW_REY

        self.admin_obj.add_movs(
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
        )


    def spread_influence(self, board: "Board") -> None:
        # Cambiar estado de fichas defensivas anteriores
        for ficha in self.army.pieces_defending:
            ficha.in_still = False
        
        self.army.pieces_defending.clear()

        # Verificar Hacke 
        self.army.in_hacke = False

        in_hacke, mov_causes_hacke = self.scuare.is_attacked()

        if in_hacke:
            self.army.in_hacke = True

            coords_prioridad: list[tuple] = [(mov_causes_hacke.ficha.coord, OBJ_ENEMY)] + mov_causes_hacke.ficha.admin_obj.get_data_off_mov(mov_causes_hacke)
            self.army.coords_priority = coords_prioridad

        # llamada a la funcion de la superclase
        super().spread_influence(board)

        # se sobre esribe el registro de coordenada de la parte trasera de la ficha como invalida en caso de un mov_causes_hacke spreadable
        if in_hacke:
            coord = self.coord + mov_causes_hacke

            if  mov_causes_hacke.is_offensive and mov_causes_hacke.is_spreadable and board.is_valid_coord(coord):  
                self.admin_obj.add_coord_off_mov(mov_causes_hacke, coord, OBJ_INVALID)

        # Verificar Hacke Mate
        if self.in_hacke:
            coords_disp: list[tuple[Coord, str]] = []

            for _, ficha in self.army.fichas:
                coords_disp += ficha.get_coords_objetive()
            
            result: bool = True

            for _, tipo in coords_disp:
                if tipo != OBJ_INVALID:
                    result = False
                    break
            
            if result:
                self.army.in_hacke_mate = True


    def coord_is_objetive(self, coord: Coord, value: str) -> bool:
        return self.admin_obj.coord_in_store(coord, value)
    

    def get_coords_objetive(self):
        return self.admin_obj.get_data()