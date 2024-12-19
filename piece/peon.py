from typing import TYPE_CHECKING, Generator
from constant import CHAR_VIEW_PEON, OBJ_ENEMY

from piece.piece import PieceChess
from piece.mov_piece import MovPiece
from coord import Coord

if TYPE_CHECKING:
    from piece.piece import EntityChess
    from board import Board
    from army import Army
    


class Peon(PieceChess):
    orientacion: int
    initial_double_mov: MovPiece

    def __init__(self, orientacion: int , army: "Army" = None):
        super().__init__(army)
        
        self.char = CHAR_VIEW_PEON
        self.orientacion = orientacion
        self.initial_double_mov = MovPiece(self, (self.orientacion * 2, 0), is_offensive = False)
    
        self.admin_obj.add_movs(
            MovPiece(self, (self.orientacion, -1), is_occupiable = False),
            MovPiece(self, (self.orientacion, 0), is_offensive = False), 
            MovPiece(self, (self.orientacion, 1), is_occupiable = False),
            self.initial_double_mov,
        )


    def fun_generator_mov(self) -> Generator[tuple[bool, bool], tuple["EntityChess", bool, "Board"], None]:
        ficha_final, is_objetive_enemy, tablero = yield

        tablero.trade_fichas(self, ficha_final, is_objetive_enemy)

        self.clear_influence_off_mov(tablero, self.initial_double_mov)
        self.admin_obj.deleted_movs(self.initial_double_mov)

        yield from super().fun_generator_mov()


    def spread_influence(self, board: "Board") -> None:
        super().spread_influence(board)

        ficha_front:EntityChess = board.get_ficha(self.coord + Coord(self.orientacion, 0))

        if isinstance(ficha_front, PieceChess):
            self.clear_influence_off_mov(board, self.initial_double_mov) 


    def update_presence_off_mov(self, board, mov) -> None:
        super().update_presence_off_mov(board, mov)
    
        if mov.value != (self.orientacion, 0):
            return
        
        if self.initial_double_mov not in self.admin_obj.list_movs:
            return
        
        ficha_frontal: EntityChess = board.get_ficha(self.coord + mov)

        if  isinstance(ficha_frontal, PieceChess):
            self.clear_influence_off_mov(board, self.initial_double_mov) 
        
        else:
            self.add_objetives(board, self.initial_double_mov)
        
        

    