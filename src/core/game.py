from typing import TYPE_CHECKING, Optional

from src.core.chess_exceptions import IlegalMovChessError, ChessGameNotRunningError
from src.core.types import IdPiece, ObjetiveChess

if TYPE_CHECKING:
    from src.core.square import Square
    from src.core.army import Army
    from src.core.board import Board
    from src.core.coordinate import Coord
    from src.core.movs.piece_mov import PieceMov
    from src.core.protocol_uci import FormatUCI
    from src.core.piece import PieceChess



class ChessGame:
    
    def __init__(self, army_white: "Army", army_black: "Army", board: "Board") -> None:
        self.__halfmoves_clocks: int = 0
        self.__number_off_movs: int = 1
        
        self.__in_running_game: bool = False
        
        self.__board: "Board" = board
        
        self.__army_white: "Army" = army_white
        self.__army_black: "Army" = army_black
        
        self.__ultimate_piece_moved: Optional["PieceChess" ]= None
        
        self.__id_army_in_turn: str = self.__army_white.clase
    
    
    @property
    def halfmoves_clocks(self) -> int:
        return self.__halfmoves_clocks
    
    
    @property
    def number_off_movs(self) -> int:
        return self.__number_off_movs
    
    
    @property
    def in_running_game(self) -> bool:
        return self.__in_running_game
    
    
    @property
    def board(self) -> "Board":
        return self.__board
    
    
    @property
    def army_white(self) -> "Army":
        return self.__army_white
    
    
    @property
    def army_black(self) -> "Army":
        return self.__army_black
    
    @property
    def ultimate_piece_moved(self) -> "PieceChess": 
        if self.__ultimate_piece_moved is None:
            raise Exception("no se movio ninguna pieza")
        return self.__ultimate_piece_moved
    
    @property
    def notation_forsyth_edwards(self) -> str:
        turn: str = "w" if self.__id_army_in_turn == self.__army_white.clase else "b"
        
        enrroque_w: str = self.__army_white.notation_FEN_enrroque.upper()
        enrroque_b: str = self.__army_black.notation_FEN_enrroque.lower()
        
        enrroque_fen: str = enrroque_w + enrroque_b
        enrroque_fen = enrroque_fen if enrroque_fen != "--" else "-"
        
        coord_mov_passant: str = self.army_not_in_turn.notation_FEN_passant
        
        return \
            f"{self.__board.notation_forsyth_edwards} {turn} " +\
            f"{enrroque_fen} {coord_mov_passant} " +\
            f"{self.__halfmoves_clocks} {self.__number_off_movs}"
    
    
    @property
    def army_in_turn(self) -> "Army":
        return self.__army_white \
            if self.is_equals_turn(self.__army_white.clase)\
            else self.__army_black
    
    
    @property
    def army_not_in_turn(self) -> "Army":
        return self.__army_black \
            if self.is_equals_turn(self.__army_white.clase)\
            else self.__army_white
    
    
    # Funcions Starts
    def init(self) -> None:
        self.__board.set_pieces(self.__army_white.pieces)
        self.__board.set_pieces(self.__army_black.pieces)
        
        self.__army_white.init_influence()
        self.__army_black.init_influence()
        
        self.__in_running_game = True
    
    
    def restart_data(self) -> None:
        self.__army_white.restart()
        self.__army_black.restart()
    
        self.__board.clear_content()
        self.__id_army_in_turn = self.__army_white.clase
        self.__number_off_movs = 0
        self.__halfmoves_clocks = 0
    
    
    def restart_game(self) -> None:
        self.restart_data()
        self.init()
    
    
    def is_equals_turn(self, id_army_in_turn: str) -> bool:
        return self.__id_army_in_turn == id_army_in_turn
    
    
    def get_safe_square(self, coord: "Coord") -> "Square":
        square: Optional["Square"] = self.__board.get_square(coord)
        
        if square is None:
            raise Exception("Error en la obtencion del square")
        
        return square
    
    
    def get_square(self, coord: "Coord")  -> Optional["Square"]:
        return self.__board.get_square(coord)
    
    
    def iteration(self) -> None:
        if not self.__in_running_game:
            raise ChessGameNotRunningError()
        
        self.army_not_in_turn.update_influence_king()
        self.army_not_in_turn.delete_data_passant()
        
        self.__number_off_movs += 1
        self.__halfmoves_clocks += 1
        
        self.__id_army_in_turn = self.army_not_in_turn.clase
        
        if self.army_in_turn.in_hacke_mate:
            self.__in_running_game = False 
        
        if self.__halfmoves_clocks >= 100:
            self.__in_running_game = False
    
    
    def make_mov(self, format_uci: "FormatUCI") -> None:
        if not self.__in_running_game:
            raise ChessGameNotRunningError()
        
        coord_start, coord_end = format_uci.coords
        
        square_start: Optional["Square"] = self.get_square(coord_start)
        square_end: Optional["Square"] = self.get_square(coord_end)
        
        if square_start is None or square_end is None:
            return
        
        piece_start: Optional["PieceChess"]= square_start.piece
        piece_end: Optional["PieceChess"]= square_end.piece
        
        piece_end_not_is_none: bool = piece_end != None
        
        type_objetive: ObjetiveChess = ObjetiveChess.ENEMY if piece_end_not_is_none else ObjetiveChess.EMPTY
        is_killer_mov: bool = True if type_objetive == ObjetiveChess.ENEMY else False
        
        if piece_start == None:
            raise IlegalMovChessError("El square donde se  genera el movimiento, no tiene una ficha")
        
        if piece_start.clase != self.__id_army_in_turn:
            raise IlegalMovChessError("No es el turno de la pieza que genera el movimiento ")
        
        if piece_end_not_is_none and piece_start.clase == piece_end.clase:
            raise IlegalMovChessError("La pieza intenta hacer un movimiento a una pieza aliada")
        
        if not piece_start.coord_is_objetive(coord_end, type_objetive):
            raise IlegalMovChessError("La pieza intenta realizar un movimiento que no esta dentro de sus movimientos legales posibles")
        
        if piece_end_not_is_none:
            piece_end.send_to_cemetery()
        
        mov: Optional["PieceMov"] = square_end.get_mov_on_prowl_to_piece(piece_start)
        
        if mov is None:
            return
        
        mov.execute( square_end, is_killer_mov)  
        
        self.__ultimate_piece_moved = piece_start
        
        if format_uci.is_promotion and piece_start.id == IdPiece.PAWN:
            from src.builder import BuilderChess
            
            new_piece: "PieceChess" = BuilderChess.build_promotion_piece(format_uci.promotion_id)
            piece_start.clear_influence()
            piece_start.promote_to(new_piece)
            piece_start.update_influence()
        
        self.iteration()
        
        if piece_start.id == IdPiece.PAWN or is_killer_mov:
            self.__halfmoves_clocks = 0
