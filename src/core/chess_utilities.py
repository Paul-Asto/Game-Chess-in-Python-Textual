from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.board import Board
    from src.core.types_chess import CharFenPiece, T_Square






def trade_pieces(square_start: "T_Square", square_end: "T_Square", board: "Board[T_Square]") -> None:
    square_start.clear_influence(board)
    square_end.clear_influence(board)
    
    square_start.trade_piece(square_end)
    
    square_start.update_influence(board)
    square_end.update_influence(board)



