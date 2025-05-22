from typing import TYPE_CHECKING, Generic

from src.core.pieces import Peon
from src.core.chess_exceptions import IlegalMovChessError, ChessGameNotRunningError
from src.core.types_chess import T_Square
from src.core.chess_constant import (
    OBJ_EMPTY,
    OBJ_ENEMY,
)

if TYPE_CHECKING:
    from src.core.army import Army
    from src.core.board import Board
    from src.core.square import Square
    from src.core.coordinate import Coord
    from src.core.mov_piece import MovPiece
    from src.core.format_uci import FormatUCI
    from src.core.piece import PieceChess



class ChessGame(Generic[T_Square]):

    def __init__(self, army_white: "Army", army_black: "Army", board: "Board[T_Square]") -> None:
        self.number_off_middle_movs: int = 0
        self.number_off_movs: int = 1

        self.in_running_game: bool = False

        self.board: "Board[Square]" = board

        self.army_white: "Army" = army_white
        self.army_black: "Army" = army_black

        self.id_army_in_turn: str = self.army_white.id


    @property
    def notation_forsyth_edwards(self) -> str:
        turn: str = "w" if self.id_army_in_turn == self.army_white.id else "b"

        enrroque_w: str = self.army_white.notation_FEN_enrroque().upper()
        enrroque_b: str = self.army_black.notation_FEN_enrroque().lower()

        enrroque_fen: str = enrroque_w + enrroque_b
        enrroque_fen = enrroque_fen if enrroque_fen != "--" else "-"

        coord_mov_passant: str = "-"

        fen_board: str = ""

        for column in self.board.content:
            n_emptys: int = 0

            for scuare in column:
                piece: "PieceChess" = scuare.piece

                if piece == None:
                    n_emptys += 1
                    continue

                if n_emptys != 0:
                    fen_board += str(n_emptys)
                    n_emptys = 0
                
                piece_fen: str = ""
                if piece.clase == self.army_white.id:
                    piece_fen = piece.char_fen.upper() 
                else:
                    piece_fen = piece.char_fen.lower()

                fen_board += piece_fen
            
            if n_emptys != 0:
                fen_board += str(n_emptys)
    
            fen_board += "/"

        fen_board = fen_board[: -1]

        return \
            f"{fen_board} {turn} "+\
            f"{enrroque_fen} {coord_mov_passant} "          +\
            f"{self.number_off_middle_movs} {self.number_off_movs}"


    @property
    def army_in_turn(self) -> "Army":
        return self.army_white \
            if self.is_equals_turn(self.army_white.id)\
            else self.army_black

    @property
    def army_not_in_turn(self) -> "Army":
        return self.army_black \
            if self.is_equals_turn(self.army_white.id)\
            else self.army_white


    # Funcions Starts
    def init(self) -> None:
        self.board.set_fichas(self.army_white.pieces)
        self.board.set_fichas(self.army_black.pieces)

        self.army_white.init_influence(self.board)
        self.army_black.init_influence(self.board)

        self.in_running_game = True


    def restart_data(self) -> None:
        self.army_white.restart()
        self.army_black.restart()

        self.board.reset_content()
        self.id_army_in_turn = self.army_white.id


    def restart_game(self) -> None:
        self.restart_data()
        self.init()


    def is_equals_turn(self, turno: str) -> str:
        return self.id_army_in_turn == turno
    

    def get_square(self, coord: "Coord") -> "Square":
        return self.board.get_scuare(coord)


    def iteration(self) -> None:
        if not self.in_running_game:
            raise ChessGameNotRunningError()
        
        self.army_not_in_turn.update_influence_rey(self.board)
        self.army_not_in_turn.reset_coords_priority()
        self.army_not_in_turn.delete_peon_passant(self.board)

        self.number_off_movs += 1

        self.id_army_in_turn = self.army_not_in_turn.id

        if self.army_in_turn.in_hacke_mate:
            self.in_running_game = False 


    def make_mov(self, format_uci: "FormatUCI") -> None:
        if not self.in_running_game:
            raise ChessGameNotRunningError()

        coord_start, coord_end = format_uci.coords

        square_start: "Square" = self.get_square(coord_start)
        square_end: "Square" = self.get_square(coord_end)

        piece_start: "PieceChess" = square_start.piece
        piece_end: "PieceChess" = square_end.piece

        piece_end_not_is_none: bool = piece_end != None

        type_objetive: str = OBJ_ENEMY if piece_end_not_is_none else OBJ_EMPTY

        if piece_start == None:
            raise IlegalMovChessError("El square donde se  genera el movimiento, no tiene una ficha")
        
        if piece_start.clase != self.id_army_in_turn:
            raise IlegalMovChessError("No es el turno de la pieza que genera el movimiento ")
        
        if piece_end_not_is_none and piece_start.clase == piece_end.clase:
            raise IlegalMovChessError("La pieza intenta hacer un movimiento a una pieza aliada")
        

        if not piece_start.coord_is_objetive(coord_end, type_objetive):
            raise IlegalMovChessError("La pieza intenta realizar un movimiento que no esta dentro de sus movimientos legales posibles")

        if piece_end_not_is_none:
            piece_end.send_to_cemetery()

        mov: "MovPiece" = square_end.get_mov_on_prowl_to_piece(piece_start)
        mov.execute(self.board, square_end, type_objetive)

        if format_uci.is_promotion:
            if isinstance(piece_start, Peon):
                piece_start.clear_influence(self.board)
                piece_start.promote_to(format_uci.class_promotion())
                piece_start.update_influence(self.board)

        self.iteration()
