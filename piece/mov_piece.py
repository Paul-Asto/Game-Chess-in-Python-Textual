from coord import AbstractCoord
from typing import TYPE_CHECKING
from constant import OBJ_EMPTY, OBJ_ENEMY, OBJ_INVALID


if TYPE_CHECKING:
    from peon import Peon
    from board import Board
    from coord import Coord
    from piece.piece import PieceChess, EntityChess, EmptyChess



class MovPiece(AbstractCoord):
    is_spreadable: bool = False
    is_offensive: bool = True
    is_occupiable: bool = True

    def __init__(self, ficha: "PieceChess", mov: tuple) -> None:
        super().__init__(mov[0], mov[1])
        self.ficha: PieceChess = ficha


    def GetOpuesto(self) -> "MovPiece":
        return MovPiece(
            self.ficha,
            (-(self.y), -(self.x)),
            )
    

    def register(self, board: "Board") -> None:
        coord: Coord = self.ficha.coord + self
        ficha: EntityChess = board.get_ficha(coord)

        if ficha is None:
            return
        
        from piece.piece import PieceChess, EntityChess, EmptyChess

        if isinstance(ficha, PieceChess):
            self.handle_register_piece(ficha)

        elif isinstance(ficha, EmptyChess):
            self.handle_register_empty(ficha)
        

    def handle_register_piece(self, ficha: "PieceChess") -> None:
        condition: bool = not self.ficha.is_equals_class(ficha.clase)
        tipo: str = OBJ_ENEMY if condition else OBJ_INVALID

        self.ficha.add_coord_objetive(self, ficha.coord, tipo)
        ficha.add_mov_prowl(self)


    def handle_register_empty(self, ficha: "EmptyChess") -> None:
        tipo = OBJ_EMPTY

        self.ficha.add_coord_objetive(self, ficha.coord, tipo)
        ficha.add_mov_prowl(self)


    def clear_register(self, board: "Board") -> None:
        for coord in self.ficha.admin_obj.get_coords_off_mov(self):
            board.get_scuare(coord).deleted_mov_prowl(self)

        self.ficha.admin_obj.clear_store_off_mov(self)


    def execute(self, board: "Board", ficha_enemy: "EntityChess", is_kiler_mov: bool) -> None:
        board.trade_fichas(self.ficha, ficha_enemy, is_kiler_mov)



class MovPieceSpreadable(MovPiece):
    
    def __init__(self, ficha: "PieceChess", mov: tuple) -> None:
        super().__init__(ficha, mov)
        
        self.is_spreadable = True


    def register(self, board: "Board") -> None:
        coord_current: Coord = self.ficha.coord + self
        ficha: "EntityChess"

        while True:
            ficha = board.get_ficha(coord_current)

            if ficha is None:
                return
            
            from piece.piece import PieceChess, EntityChess, EmptyChess

            if isinstance(ficha, PieceChess):
                self.handle_register_piece(ficha)
                return

            elif isinstance(ficha, EmptyChess):
                self.handle_register_empty(ficha)

            coord_current += self


    def execute(self, board: "Board", ficha_enemy: "EntityChess", is_kiler_mov: bool) -> None:
        super().execute(board, ficha_enemy, is_kiler_mov)



class MovPiecePeon(MovPiece):
    ficha: "Peon"

    def __init__(self, ficha: "Peon", mov: tuple) -> None:
        super().__init__(ficha, mov)


    def handle_register_piece(self, ficha: "PieceChess") -> None:
        condition: bool = self.is_offensive and not self.ficha.is_equals_class(ficha.clase)
        tipo: str = OBJ_ENEMY if condition else OBJ_INVALID

        self.ficha.add_coord_objetive(self, ficha.coord, tipo)
        ficha.add_mov_prowl(self)


    def handle_register_empty(self, ficha: "EmptyChess") -> None:
        condition: bool = self.is_occupiable
        tipo: str = OBJ_EMPTY if condition else OBJ_INVALID

        self.ficha.add_coord_objetive(self, ficha.coord, tipo)
        ficha.add_mov_prowl(self)
    

    def execute(self, board: "Board", ficha_enemy: "EntityChess", is_kiler_mov: bool) -> None:
        self.ficha.double_frontal_mov.is_active = False
        super().execute(board, ficha_enemy, is_kiler_mov)



class MovPeonFrontal(MovPiecePeon):

    def __init__(self, ficha: "Peon", mov: tuple):
        super().__init__(ficha, mov)

        self.is_offensive = False


    def register(self, board: "Board") -> None:
        coord: Coord = self.ficha.coord + self
        ficha: EntityChess = board.get_ficha(coord)

        if ficha is None:
            return
        
        from piece.piece import PieceChess, EntityChess, EmptyChess

        if isinstance(ficha, PieceChess):
            self.handle_register_piece(ficha)
            self.ficha.double_frontal_mov.clear_register(board)

        elif isinstance(ficha, EmptyChess):
            self.handle_register_empty(ficha)

            if self.ficha.double_frontal_mov.is_active:
                self.ficha.double_frontal_mov.register(board)



class MovPeonDoubleFrontal(MovPiecePeon):
    is_active: bool

    def __init__(self, ficha: "Peon", mov: tuple):
        super().__init__(ficha, mov)

        self.is_active = True
        self.is_offensive = False


    def register(self, board: "Board") -> None:
        if not self.is_active:
            return
        
        ficha: EntityChess = board.get_ficha(self.ficha.coord + self.ficha.frontal_mov)

        from piece.piece import PieceChess, EntityChess

        if isinstance(ficha, PieceChess):
            return

        super().register(board)

    
    def execute(self, board: "Board", ficha_enemy: "PieceChess", is_kiler_mov: bool) -> None:
        self.ficha.is_passant = True
        self.ficha.army.set_peon_passant(self.ficha)
        
        super().execute(board, ficha_enemy, is_kiler_mov)




class MovPeonPassant(MovPiecePeon):
    mov_off_final_position: "MovPeonDiagonal"

    def __init__(self, ficha: "PieceChess", mov: tuple) -> None:
        super().__init__(ficha, mov)

    
    def register(self, board: "Board") -> None:
        coord: Coord = self.ficha.coord + self
        ficha: EntityChess = board.get_ficha(coord)

        if ficha is None:
            return
        
        self.ficha.add_coord_objetive(self, ficha.coord, OBJ_INVALID)
        ficha.add_mov_prowl(self)
        
        from piece.peon import Peon

        if isinstance(ficha, Peon):
            if ficha.is_passant:
                ficha_in_final_passant: EntityChess = board.get_ficha(self.ficha.coord + self.mov_off_final_position)
            
                self.ficha.add_coord_objetive(self.mov_off_final_position, ficha_in_final_passant.coord, OBJ_EMPTY)
                ficha_in_final_passant.add_mov_prowl(self.mov_off_final_position)
            
            else:
                self.mov_off_final_position.register(board)



class MovPeonDiagonal(MovPiecePeon):
    mov_off_passant: "MovPeonPassant"

    def __init__(self, ficha: "PieceChess", mov: tuple) -> None:
        super().__init__(ficha, mov)
        
        self.is_occupiable = False

    def execute(self, board: "Board", ficha_enemy: "EntityChess", is_kiler_mov: bool) -> None:
        if is_kiler_mov:
            super().execute(board, ficha_enemy, is_kiler_mov)
        
        else:
            ficha_in_passant: EntityChess = board.get_ficha(self.ficha.coord + self.mov_off_passant)
            self.mov_off_passant.execute(board, ficha_in_passant, True)

            ficha_in_final_passant: EntityChess = board.get_ficha(self.ficha.coord + self.ficha.frontal_mov)
            self.ficha.frontal_mov.execute(board, ficha_in_final_passant, False)




class MovPieceRey(MovPiece):

    def __init__(self, ficha, mov):
        super().__init__(ficha, mov)
    
    def register(self):
        pass

    def execute(self):
        pass



class MovPieceReyEnrroque(MovPiece):

    def __init__(self, ficha, mov):
        super().__init__(ficha, mov)
    
    def register(self):
        pass

    def execute(self):
        pass