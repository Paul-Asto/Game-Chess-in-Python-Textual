from coord import AbstractCoord
from typing import TYPE_CHECKING
from constant import OBJ_EMPTY, OBJ_ENEMY, OBJ_INVALID


if TYPE_CHECKING:
    from peon import Peon
    from board import Board
    from coord import Coord
    from piece.piece import PieceChess, EntityChess, EmptyChess



class MovPiece(AbstractCoord):

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


    def execute(self, board: "Board", ficha_enemy: "EntityChess", is_kiler_mov: bool) -> None:
        board.trade_fichas(self.ficha, ficha_enemy, is_kiler_mov)



class MovPieceSpreadable(MovPiece):

    def __init__(self, ficha: "PieceChess", mov: tuple) -> None:
        super().__init__(ficha, mov)


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

    def __init__(self, ficha: "Peon", mov: tuple, is_occupiable: bool = True, is_offensive: bool = True) -> None:
        super().__init__(ficha, mov)

        self.is_occupiable: bool = is_occupiable
        self.is_offensive: bool = is_offensive


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
        self.ficha.initial_double_mov.is_active = False
        super().execute(board, ficha_enemy, is_kiler_mov)



class MovPiecePeonFrontal(MovPiecePeon):

    def __init__(self, ficha: "Peon", mov: tuple, is_occupiable: bool = True, is_offensive: bool = True):
        super().__init__(ficha, mov, is_occupiable, is_offensive)


    def register(self, board: "Board") -> None:
        coord: Coord = self.ficha.coord + self
        ficha: EntityChess = board.get_ficha(coord)

        if ficha is None:
            return
        
        from piece.piece import PieceChess, EntityChess, EmptyChess

        if isinstance(ficha, PieceChess):
            self.handle_register_piece(ficha)
            self.ficha.clear_influence_off_mov(board, self.ficha.initial_double_mov)

        elif isinstance(ficha, EmptyChess):
            self.handle_register_empty(ficha)

            if self.ficha.initial_double_mov.is_active:
                self.ficha.initial_double_mov.register(board)



class MovPiecePeonDoubleFrontal(MovPiecePeon):

    def __init__(self, ficha: "Peon", mov: tuple, is_occupiable: bool = True, is_offensive: bool = True):
        super().__init__(ficha, mov, is_occupiable, is_offensive)

        self.is_active: bool = True


    def register(self, board: "Board") -> None:
        if not self.is_active:
            return
        
        ficha: EntityChess = board.get_ficha(self.ficha.coord + self.ficha.frontal_mov)

        from piece.piece import PieceChess, EntityChess

        if isinstance(ficha, PieceChess):
            return

        super().register(board)



class MovPiecePassant(MovPiece):
    def __init__(self, ficha, mov):
        super().__init__(ficha, mov)



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