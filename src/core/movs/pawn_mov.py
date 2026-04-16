from src.core.coordinate import Coord
from typing import TYPE_CHECKING, Optional

from src.core.types import ObjetiveChess, IdPiece
from src.core.movs.short_mov import ShortMov
from src.core.piece import PieceChess


if TYPE_CHECKING:
    from src.core.board import Board
    from src.core.square import Square
    from src.core.movs.piece_mov import PieceMov


class PawnMov(ShortMov):
    
    def __init__(self, piece: "PieceChess", mov: tuple[int, int]) -> None:
        super().__init__(piece, mov)
    
    
    def handle_register_piece(self, square: "Square") -> None:
        if square.piece is None:
            return
        
        condition: bool = self.is_offensive and not self.piece.is_equals_class(square.piece.clase)
        objetive: ObjetiveChess = ObjetiveChess.ENEMY if condition else ObjetiveChess.INVALID
        
        self.piece.add_coord_objetive(self, square.coord, objetive)
        square.add_mov_prowl(self)
    
    
    def handle_register_empty(self, square: "Square") -> None:
        condition: bool = self.is_occupiable
        objetive: ObjetiveChess = ObjetiveChess.EMPTY if condition else ObjetiveChess.INVALID
        
        self.piece.add_coord_objetive(self, square.coord, objetive)
        square.add_mov_prowl(self)
    
    
    def execute(self, square_obj: "Square", is_kiler_mov: bool) -> None:
        self.piece.data_pawn.double_frontal_mov.is_active = False
        super().execute( square_obj, is_kiler_mov)



class PawnMovFrontal(PawnMov):
    
    def __init__(self, ficha: "PieceChess", mov: tuple[int, int]) -> None:
        super().__init__(ficha, mov)
        
        self.is_offensive = False
    
    
    def register(self) -> None:
        board: "Board" = self.piece.board
        coord: Coord = self.piece.coord + self
        square: Optional["Square"] = board.get_square(coord)
        
        if square is None:
            return
        
        if not square.piece is None:
            self.piece.data_pawn.double_frontal_mov.clear_register()
            self.handle_register_piece(square)
            return
        
        self.handle_register_empty(square)
        self.piece.data_pawn.double_frontal_mov.register()



class PawnMovDoubleFrontal(PawnMov):
    
    def __init__(self, ficha: "PieceChess", mov: tuple[int, int]) -> None:
        super().__init__(ficha, mov)
        
        self.is_active = True
        self.is_offensive = False
    
    
    def register(self) -> None:
        if not self.is_active:
            return
        
        board: "Board" = self.piece.board
        square: Optional["Square"]= board.get_square(self.piece.coord + self)
        
        if square is None:
            return
        
        if not square.piece is None:
            self.piece.add_coord_objetive(self, square.coord, ObjetiveChess.INVALID)
            square.add_mov_prowl(self)
            return
        
        self.handle_register_empty(square)
    
    
    def execute(self, square_obj: "Square", is_kiler_mov: bool) -> None:
        # se guarda la coordenada inicial antes del movimiento
        coord_register_passant: Coord = self.piece.coord
        board: "Board" = self.piece.board
        
        # se ejecuta el movimiento normal
        super().execute( square_obj, is_kiler_mov)
        
        left_coord: Coord = self.piece.coord + Coord(0, -1)
        rigth_coord: Coord = self.piece.coord + Coord(0, 1)
        
        left_square: Optional["Square"] = board.get_square(left_coord)
        rigth_square: Optional["Square"] = board.get_square(rigth_coord)
        
        # se analizan las condiciones para validar un movimiento passant
        if(left_square != None and\
        not left_square.piece is None and\
        left_square.piece.id == IdPiece.PAWN and\
        left_square.piece.clase != self.piece.clase) or \
        (rigth_square != None and\
        not rigth_square.piece is None and\
        rigth_square.piece.id == IdPiece.PAWN and\
        rigth_square.piece.clase != self.piece.clase):
            # Se registra los datos del passant en el army
            self.piece.army.set_data_passant(self.piece,coord_register_passant)
            # se actualiza la presencia de la pieza para que el movimiento pasant del peon enemigo pueda registrarlo 
            self.piece.update_presence()



class PawnMovPassant(PawnMov):
    mov_off_final_position: "PieceMov"
    
    def __init__(self, ficha: "PieceChess", mov: tuple[int, int]) -> None:
        super().__init__(ficha, mov)
        self.is_offensive = False
    
    
    def register(self) -> None:
        coord: Coord = self.piece.coord + self
        board: "Board" = self.piece.board
        square: Optional["Square"]= board.get_square(coord)
        
        if square is None:
            return
        
        self.piece.add_coord_objetive(self, square.coord, ObjetiveChess.INVALID)
        square.add_mov_prowl(self)
        
        piece: Optional[PieceChess]= square.piece
        
        if piece is None or piece.id != IdPiece.PAWN:
            return
        
        if not piece.data_pawn.is_passant:
            # Se actualiza el movimiento diagonal en caso de que el peon ya no este en estado passant
            self.mov_off_final_position.register()
            return
        
        square_in_final_passant: Optional["Square"] = board.get_square(self.piece.coord + self.mov_off_final_position)
        
        if square_in_final_passant == None or square_in_final_passant.piece != None:
            return
        
        # se registra un objetivo valido para realizar el movimiento passant
        self.piece.add_coord_objetive(self.mov_off_final_position, square_in_final_passant.coord, ObjetiveChess.EMPTY)
        square_in_final_passant.add_mov_prowl(self.mov_off_final_position)



class PawnMovDiagonal(PawnMov):
    mov_off_passant: "PieceMov"
    
    def __init__(self, ficha: "PieceChess", mov: tuple[int, int]) -> None:
        super().__init__(ficha, mov)
        
        self.is_occupiable = False
    
    def execute(self, square_obj: "Square", is_kiler_mov: bool) -> None:
        board: "Board" = self.piece.board
        
        if is_kiler_mov:
            super().execute( square_obj, is_kiler_mov)
            return
        
        
        square_in_passant: Optional["Square"] = board.get_square(self.piece.coord + self.mov_off_passant)
        
        if square_in_passant is None:
            return
        
        piece_in_passant: Optional[PieceChess] = square_in_passant.piece
        
        if piece_in_passant is None or not piece_in_passant.data_pawn.is_passant:
            return
        
        super().execute( square_in_passant, True)
        
        
        square_in_final_passant: Optional["Square"] = board.get_square(self.piece.coord + self.piece.data_pawn.frontal_mov)
        
        if square_in_final_passant is None:
            return
        
        piece_in_final_passant: Optional[PieceChess] = square_in_final_passant.piece
        
        if not piece_in_final_passant is None:
            return
        
        super().execute( square_in_final_passant, False)
