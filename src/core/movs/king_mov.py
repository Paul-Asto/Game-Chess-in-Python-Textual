from typing import TYPE_CHECKING, Optional
from src.core.types import ObjetiveChess, IdPiece
from src.core.movs.short_mov import ShortMov, PieceMov


if TYPE_CHECKING:
    from src.core.board import Board
    from src.core.coordinate import Coord
    from src.core.piece import PieceChess
    from src.core.square import Square



class KingMov(ShortMov):
    
    def __init__(self, piece: "PieceChess", mov: tuple[int, int]) -> None:
        super().__init__(piece, mov)
    
    
    def register(self) -> None:
        board: "Board" = self.piece.board
        coord: "Coord" = self.piece.coord + self
        square: Optional["Square"] = board.get_square(coord)
        
        if square == None:
            return
        
        piece: Optional["PieceChess"] = square.piece
        
        if piece == None:
            if not self.piece.coord_is_objetive(square.coord, ObjetiveChess.INVALID):
                self.handle_register_empty(square)
            
        else:
            self.handle_register_piece(square)
        
        
        # Descartar opciones de coordenadas en amenaza de primera casilla
        mov_enemy: Optional[PieceMov] = square.is_attacked(substitute_clase= self.piece.clase)
        
        if not mov_enemy is None:
            self.piece.add_coord_objetive(self, square.coord, ObjetiveChess.INVALID)
        
        
        # scan and search 2 pieces in line move
        current_coord: Coord = coord
        current_square: Optional["Square"] = square
        current_piece: Optional["PieceChess"] = square.piece
        
        first_piece: Optional["PieceChess"] = None
        second_piece: Optional["PieceChess"] = None
        
        while True:
            if current_square == None:
                break
            
            if current_piece == None:
                current_coord += self
                current_square = board.get_square(current_coord)
                current_piece = current_square.piece if current_square != None else None
                continue
            
            if first_piece == None:
                first_piece = current_piece
                current_coord += self
                current_square = board.get_square(current_coord)
                current_piece = current_square.piece if current_square != None else None
                continue
            
            second_piece = current_piece
            break
        
        # 1er case: piece enemy in atack
        if  not first_piece is None and self.piece.clase != first_piece.clase:
            movs_enemy: list[PieceMov] = list(filter(
                lambda mov: self.get_opposite() == mov and mov.is_spreadable,
                first_piece.movs
            ))
            
            if any(movs_enemy):
                mov: PieceMov = movs_enemy[0]
                coord_invalidated: "Coord" = self.piece.coord + mov
                
                square = board.get_square(coord_invalidated)
                if not square is None:
                    self.piece.add_coord_objetive(mov, coord_invalidated, ObjetiveChess.INVALID)
                    square.add_mov_prowl(mov)
        
        
        # 2do case: piece defending king off the enemy
        elif  not first_piece is None and\
            self.piece.clase == first_piece.clase and\
            not second_piece is None and\
            self.piece.clase != second_piece.clase:
            
            movs_enemy: list[PieceMov] = list(filter(
                lambda mov: self.get_opposite() == mov and mov.is_spreadable,
                second_piece.movs
            ))
            
            if any(movs_enemy):
                mov: PieceMov = movs_enemy[0]
                self.piece.army.add_piece_defending(first_piece, [self, mov])
    
    
    def execute(self, square_obj: "Square", is_kiler_mov: bool) -> None:
        super().execute( square_obj, is_kiler_mov)
        
        self.piece.army.active_short_castling = False
        self.piece.army.active_long_castling = False



class ShortCastlingMov(ShortMov):
    
    def __init__(self, piece: "PieceChess") -> None:
        super().__init__(piece, (0, 2))
    
    
    def register(self) -> None:
        if not self.piece.army.active_short_castling:
            return
        
        self.clear_register()
        
        if self.piece.in_hacke:
            return
        
        board: "Board" = self.piece.board
        square_rook: Optional["Square"] = board.get_square(self.piece.coord.move((0, 3)))
        
        if square_rook == None:
            return
        
        rook: Optional[PieceChess] = square_rook.piece
        
        if rook is None or rook.id != IdPiece.ROOK:
            self.piece.army.active_short_castling = False
            return
        
        square_empty_1: Optional["Square"] = board.get_square(self.piece.coord.move((0, 1)))
        
        if square_empty_1 == None:
            return
        
        mov_enemy_1: Optional[PieceMov] = square_empty_1.is_attacked(substitute_clase= self.piece.clase)
        
        if square_empty_1.piece != None or not mov_enemy_1 is None:
            return
        
        square_empty_2: Optional["Square"] = board.get_square(self.piece.coord.move((0, 2)))
        
        if square_empty_2 == None:
            return
        
        mov_enemy_2: Optional[PieceMov] = square_empty_2.is_attacked(substitute_clase= self.piece.clase)
                
        if square_empty_2.piece != None or not mov_enemy_2 is None:
            return
        
        self.handle_register_empty(square_empty_2)
    
    
    def execute(self, square_obj: "Square", is_kiler_mov: bool) -> None:
        board: "Board" = self.piece.board
        square_rook: Optional["Square"] = board.get_square(self.piece.coord.move((0, 3)))
        square_empty_1: Optional["Square"] = board.get_square(self.piece.coord.move((0, 1)))
        
        if square_rook is None or square_empty_1 is None:
            return
        
        self.piece.square.deliver_piece(square_obj)
        square_rook.deliver_piece(square_empty_1)
        
        self.piece.army.active_short_castling = False
        self.piece.army.active_long_castling = False



class LongCastlingMov(ShortMov):
    
    def __init__(self, piece: "PieceChess") -> None:
        super().__init__(piece, (0, -3))
    
    
    def register(self) -> None:
        board: "Board" = self.piece.board
        
        if not self.piece.army.active_long_castling:
            return
        
        self.clear_register()
        
        if self.piece.in_hacke:
            return
        
        square_rook: Optional["Square"] = board.get_square(self.piece.coord.move((0, -4)))
        
        if square_rook == None:
            return
        
        rook: Optional[PieceChess] = square_rook.piece
        
        if rook is None or rook.id != IdPiece.ROOK:
            self.piece.army.active_long_castling = False
            return
        
        square_empty_1: Optional["Square"]= board.get_square(self.piece.coord.move((0, -1)))
        
        if square_empty_1 == None:
            return
        
        mov_enemy_1: Optional[PieceMov] = square_empty_1.is_attacked(substitute_clase= self.piece.clase)
        
        if square_empty_1.piece != None or not mov_enemy_1 is None:
            return
        
        square_empty_2: Optional["Square"] = board.get_square(self.piece.coord.move((0, -2)))
        
        if square_empty_2 == None:
            return
        
        mov_enemy_2: Optional[PieceMov] = square_empty_2.is_attacked(substitute_clase= self.piece.clase)
        
        if square_empty_2.piece != None or not mov_enemy_2 is None:
            return
        
        square_empty_3: Optional["Square"] = board.get_square(self.piece.coord.move((0, -3)))
        if square_empty_3 == None:
            return
        
        mov_enemy_3: Optional[PieceMov] = square_empty_3.is_attacked(substitute_clase= self.piece.clase)
        
        if square_empty_3.piece != None or not mov_enemy_3 is None:
            return
        
        self.handle_register_empty(square_empty_3)
    
    
    def execute(self, square_obj: "Square", is_kiler_mov: bool) -> None:
        board: "Board" = self.piece.board
        
        square_torre:  Optional["Square"] = board.get_square(self.piece.coord.move((0, -4)))
        square_empty_2:  Optional["Square"]= board.get_square(self.piece.coord.move((0, -2)))
        
        if square_torre is None or square_empty_2 is None:
            return
        
        self.piece.square.deliver_piece(square_obj)
        square_torre.deliver_piece(square_empty_2)
        
        self.piece.army.active_short_castling = False
        self.piece.army.active_long_castling = False
