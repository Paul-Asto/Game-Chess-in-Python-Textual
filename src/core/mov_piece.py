from src.core.coordinate import CardinalPair, Coord
from typing import TYPE_CHECKING
from src.core.chess_constant import OBJ_EMPTY, OBJ_ENEMY, OBJ_INVALID
from src.core.chess_utilities import trade_pieces


if TYPE_CHECKING:
    from src.core.pieces import Peon, Rey
    from src.core.board import Board
    from src.core.coordinate import Coord
    from src.core.piece import PieceChess
    from src.core.square import Square



class MovPiece(CardinalPair):
    is_spreadable: bool = False
    is_offensive: bool = True
    is_occupiable: bool = True

    def __init__(self, ficha: "PieceChess", mov: tuple) -> None:
        super().__init__(mov[0], mov[1])
        self.ficha: "PieceChess" = ficha


    def GetOpuesto(self) -> "MovPiece":
        return MovPiece(
            self.ficha,
            self.value,
        )
    
    def copy(self, op_new_piece: "PieceChess" = None) :
        new_piece: "PieceChess" = self.ficha if op_new_piece ==  None else op_new_piece
        return self.__class__(new_piece, self.value)
    

    def register(self, board: "Board") -> None:
        coord: Coord = self.ficha.coord + self
        square: "Square" = board.get_scuare(coord)

        if square == None:
            return
        
        if square.piece == None:
            self.handle_register_empty(square)
            return

        self.handle_register_piece(square)

        

    def handle_register_piece(self, square: "Square") -> None:
        condition: bool = not self.ficha.is_equals_class(square.piece.clase)
        tipo: str = OBJ_ENEMY if condition else OBJ_INVALID

        self.ficha.add_coord_objetive(self, square.coord, tipo)
        square.add_mov_prowl(self)


    def handle_register_empty(self, square: "Square") -> None:
        tipo = OBJ_EMPTY

        self.ficha.add_coord_objetive(self, square.coord, tipo)
        square.add_mov_prowl(self)


    def clear_register(self, board: "Board[Square]") -> None:
        for coord in self.ficha.square.admin_objetives.get_coords_off_mov(self):
            board.get_scuare(coord).deleted_mov_prowl(self)

        self.ficha.square.admin_objetives.clear_store_off_mov(self)


    def execute(self, board: "Board", square_obj: "Square", is_kiler_mov: bool) -> None:
        trade_pieces(self.ficha.square, square_obj, board)



class MovPieceSpreadable(MovPiece):
    is_spreadable: bool = True
    
    def __init__(self, ficha: "PieceChess", mov: tuple) -> None:
        super().__init__(ficha, mov)


    def register(self, board: "Board") -> None:
        coord_current: Coord = self.ficha.coord + self
        square: "Square"

        while True:
            square = board.get_scuare(coord_current)

            if square is None:
                return
            
            if square.piece != None:
                self.handle_register_piece(square)
                break

            self.handle_register_empty(square)
            coord_current += self


    def execute(self, board: "Board", square_obj: "Square", is_kiler_mov: bool) -> None:
        super().execute(board, square_obj, is_kiler_mov)



class MovPiecePeon(MovPiece):
    ficha: "Peon"

    def __init__(self, ficha: "Peon", mov: tuple) -> None:
        super().__init__(ficha, mov)


    def handle_register_piece(self, square: "Square") -> None:
        condition: bool = self.is_offensive and not self.ficha.is_equals_class(square.piece.clase)
        tipo: str = OBJ_ENEMY if condition else OBJ_INVALID

        self.ficha.add_coord_objetive(self, square.coord, tipo)
        square.add_mov_prowl(self)


    def handle_register_empty(self, square: "Square") -> None:
        condition: bool = self.is_occupiable
        tipo: str = OBJ_EMPTY if condition else OBJ_INVALID

        self.ficha.add_coord_objetive(self, square.coord, tipo)
        square.add_mov_prowl(self)
    

    def execute(self, board: "Board", square_obj: "Square", is_kiler_mov: bool) -> None:
        self.ficha.double_frontal_mov.is_active = False
        super().execute(board, square_obj, is_kiler_mov)



class MovPeonFrontal(MovPiecePeon):

    def __init__(self, ficha: "Peon", mov: tuple):
        super().__init__(ficha, mov)

        self.is_offensive = False


    def register(self, board: "Board") -> None:
        coord: Coord = self.ficha.coord + self
        square: "Square" = board.get_scuare(coord)

        if square is None:
            return

        if square.piece == None:
            self.handle_register_empty(square)

            if self.ficha.double_frontal_mov.is_active:
                self.ficha.double_frontal_mov.register(board)
            return

        self.handle_register_piece(square)
        self.ficha.double_frontal_mov.clear_register(board)





class MovPeonDoubleFrontal(MovPiecePeon):
    is_active: bool

    def __init__(self, ficha: "Peon", mov: tuple) -> None:
        super().__init__(ficha, mov)

        self.is_active = True
        self.is_offensive = False


    def register(self, board: "Board") -> None:
        if not self.is_active:
            return
        
        square: "Square" = board.get_scuare(self.ficha.coord + self)

        if square == None:
            return
        
        if square.piece != None:
            return
        
        self.handle_register_empty(square)

    
    def execute(self, board: "Board", square_obj: "Square", is_kiler_mov: bool) -> None:
        self.ficha.is_passant = True
        self.ficha.army.set_peon_passant(self.ficha)
        
        super().execute(board, square_obj, is_kiler_mov)



class MovPeonPassant(MovPiecePeon):
    mov_off_final_position: "MovPeonDiagonal"

    def __init__(self, ficha: "PieceChess", mov: tuple) -> None:
        super().__init__(ficha, mov)
        self.is_offensive = False

    
    def register(self, board: "Board") -> None:
        coord: Coord = self.ficha.coord + self
        square: "Square" = board.get_scuare(coord)

        if square is None:
            return
        
        self.ficha.add_coord_objetive(self, square.coord, OBJ_INVALID)
        square.add_mov_prowl(self)
        
        from src.core.pieces import Peon
        ficha: "PieceChess" = square.piece

        if isinstance(ficha, Peon):
            if ficha.is_passant:
                square_in_final_passant: "Square" = board.get_scuare(self.ficha.coord + self.mov_off_final_position)

                if square_in_final_passant == None:
                    return
                
                if square_in_final_passant.piece != None:
                    return

                self.ficha.add_coord_objetive(self.mov_off_final_position, square_in_final_passant.coord, OBJ_EMPTY)
                square_in_final_passant.add_mov_prowl(self.mov_off_final_position)

            else:
                self.mov_off_final_position.register(board)



class MovPeonDiagonal(MovPiecePeon):
    mov_off_passant: "MovPeonPassant"

    def __init__(self, ficha: "PieceChess", mov: tuple) -> None:
        super().__init__(ficha, mov)
        
        self.is_occupiable = False

    def execute(self, board: "Board", square_obj: "Square", is_kiler_mov: bool) -> None:
        if is_kiler_mov:
            super().execute(board, square_obj, is_kiler_mov)
        
        else:
            square_in_passant: "Square" = board.get_scuare(self.ficha.coord + self.mov_off_passant)
            ficha_in_passant = square_in_passant.piece

            if ficha_in_passant != None:
                self.mov_off_passant.execute(board, square_in_passant, True)

            square_in_final_passant: "Square" = board.get_scuare(self.ficha.coord + self.ficha.frontal_mov)
            ficha_in_final_passant = square_in_final_passant.piece

            if ficha_in_final_passant == None:
                self.ficha.frontal_mov.execute(board, square_in_final_passant, False)



class MovPieceRey(MovPiece):

    def __init__(self, ficha: "Rey", mov):
        super().__init__(ficha, mov)
    
    def register(self, board: "Board") -> None:
        coord: Coord = self.ficha.coord + self
        square: "Square" = board.get_scuare(coord)

        if square == None:
            return
        
        ficha = square.piece

        if ficha == None:
            self.handle_register_empty(square)
            
        else:
            self.handle_register_piece(square)

        # Descartar opciones de coordenadas en amenaza
        for mov in square.movs_on_prowl:
            if self.ficha.is_equals_class(mov.ficha.clase):
                continue
            
            if mov.is_offensive:
                self.ficha.add_coord_objetive(self, square.coord, OBJ_INVALID)
                break
        

        ficha_defender: "PieceChess" = None

        current_coord: Coord = coord
        current_square: "Square" = square
        current_ficha: "PieceChess" = square.piece

        # search ficha defender
        while True:
            if current_square == None:
                break
            
            if current_ficha == None:
                current_coord += self
                current_square = board.get_scuare(current_coord)
                current_ficha = current_square.piece if current_square != None else None
                continue

            if self.ficha.is_equals_class(current_ficha.clase):
                ficha_defender = current_ficha

            break

        if ficha_defender == None:
            return
        

        current_coord += self
        current_square = board.get_scuare(current_coord)
        current_ficha = current_square.piece if current_square != None else None

        # search ficha enemiga
        while True:
            if current_square == None:
                break
            
            if current_ficha == None:
                current_coord += self
                current_square = board.get_scuare(current_coord)
                current_ficha = current_square.piece if current_square != None else None
                continue

            if not self.ficha.is_equals_class(current_ficha.clase):
                for mov_enemy in current_ficha.movs:
                    if self.GetOpuesto() == mov_enemy and mov_enemy.is_spreadable:
                        self.ficha.army.add_piece_defending(ficha_defender, [self, mov_enemy])
                        break
            break
    

    def execute(self, board: "Board", square_obj: "Square", is_kiler_mov: bool) -> None:
        super().execute(board, square_obj, is_kiler_mov)

        self.ficha.army.active_enrroque_corto = False
        self.ficha.army.active_enrroque_largo = False



class MovReyEnrroqueCorto(MovPiece):

    def __init__(self, ficha: "PieceChess"):
        super().__init__(ficha, (0, 2))
    
    def register(self, board: "Board") -> None:
        if not self.ficha.army.active_enrroque_corto:
            return
        
        self.clear_register(board)
        
        if self.ficha.in_hacke:
            return
        
        square_torre: "Square" = board.get_scuare(self.ficha.coord.move((0, 3)))

        if square_torre == None:
            return

        torre = square_torre.piece

        from src.core.pieces import Torre
        if not isinstance(torre, Torre):
            self.ficha.army.active_enrroque_corto = False
            return
        
        square_empty_1: "Square" = board.get_scuare(self.ficha.coord.move((0, 1)))

        if square_empty_1 == None:
            return
        
        is_atacked, _ = square_empty_1.is_attacked(self.ficha.clase)

        if square_empty_1.piece != None or is_atacked:
            return

        square_empty_2: "Square" = board.get_scuare(self.ficha.coord.move((0, 2)))

        if square_empty_2 == None:
            return
        
        is_atacked, _ = square_empty_2.is_attacked(self.ficha.clase)
                
        if square_empty_2.piece != None or is_atacked:
            return
    
        self.handle_register_empty(square_empty_2)

        
    def execute(self, board: "Board", square_obj: "Square", is_kiler_mov: bool) -> None:
        square_torre: "Square" = board.get_scuare(self.ficha.coord.move((0, 3)))
        square_empty_1: "Square" = board.get_scuare(self.ficha.coord.move((0, 1)))

        trade_pieces(self.ficha.square, square_obj, board)
        trade_pieces(square_torre, square_empty_1, board)

        self.ficha.army.active_enrroque_corto = False
        self.ficha.army.active_enrroque_largo = False



class MovReyEnrroqueLargo(MovPiece):

    def __init__(self, ficha: "PieceChess"):
        super().__init__(ficha, (0, -3))
    
    def register(self, board: "Board") -> None:
        if not self.ficha.army.active_enrroque_largo:
            return
        
        self.clear_register(board)
        
        if self.ficha.in_hacke:
            return
        
        square_torre: "Square" = board.get_scuare(self.ficha.coord.move((0, -4)))

        if square_torre == None:
            return
    
        torre = square_torre.piece
        from src.core.pieces import Torre

        if not isinstance(torre, Torre):
            self.ficha.army.active_enrroque_largo = False
            return
        
        square_empty_1: "Square" = board.get_scuare(self.ficha.coord.move((0, -1)))

        if square_empty_1 == None:
            return
        
        is_atacked, _ = square_empty_1.is_attacked(self.ficha.clase)

        if square_empty_1.piece != None or is_atacked:
            return
        
        square_empty_2: "Square" = board.get_scuare(self.ficha.coord.move((0, -2)))

        if square_empty_2 == None:
            return
        
        is_atacked, _ = square_empty_2.is_attacked(self.ficha.clase)

        if square_empty_2.piece != None or is_atacked:
            return
        
        square_empty_3: "Square" = board.get_scuare(self.ficha.coord.move((0, -3)))
        if square_empty_3 == None:
            return
        
        is_atacked, _ = square_empty_3.is_attacked(self.ficha.clase)

        if square_empty_3.piece != None or is_atacked:
            return

        self.handle_register_empty(square_empty_3)
        
    
    def execute(self, board: "Board[Square]", square_obj: "Square", is_kiler_mov: bool) -> None:
        square_torre: "Square" = board.get_scuare(self.ficha.coord.move((0, -4)))
        square_empty_2: "Square" = board.get_scuare(self.ficha.coord.move((0, -2)))

        trade_pieces(self.ficha.square, square_obj, board)
        trade_pieces(square_torre, square_empty_2, board)
        

        self.ficha.army.active_enrroque_largo = False
        self.ficha.army.active_enrroque_corto = False
