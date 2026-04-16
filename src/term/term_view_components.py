from typing import TYPE_CHECKING, Optional

from rich.text import Text
from src.core.types import ObjetiveChess

if TYPE_CHECKING:
    from src.core.piece import PieceChess
    from src.core.board import Board
    from src.core.square import Square
    from src.core.coordinate import Coord

def get_view_term_board(board:"Board") -> Text:
        index: int = 8
        view: Text = Text()
        view.append("____________________________\n")
        view.append("|          Board            |\n")
        view.append("|___________________________|\n\n")
        view.append("   A  B  C  D  E  F  G  H  \n\n")
        
        
        for column in board.content:
            view.append(f"{index}  ")
            
            for square in column:
                piece: Optional["PieceChess"] = square.piece
                
                if piece == None:
                    view.append("Ｘ ")
                    continue
                
                view.append(f"{piece.char_view}  ", style=f"bold {piece.str_color}")
                
            
            view.append(f" {index}\n")
            index -= 1 
        
        view.append("\n   A  B  C  D  E  F  G  H  \n")
        
        return view


def get_view_term_piece(piece: "PieceChess") -> Text:
        result: Text = Text("\n")
        
        result.append(f"{piece.__class__.__name__}({piece.char_view} )".center(27), f"bold {piece.str_color}")
        result.append("\n\n")
        result.append(f"{f"   Clase: {piece.clase}"}\n")
        result.append(f"{f"   In Hacke: {piece.in_hacke}"}\n")
        result.append(f"{f"   In still: {piece.in_still}".ljust(27)}\n")
        
        if piece.in_still:
            allowed_mov_str: str = ""
            
            for mov in piece.allowed_movs:
                allowed_mov_str += f"{str(mov.value)}, "
            
            result.append(f"{f" Allowed movs: [{allowed_mov_str}]".ljust(27)}\n")
        
        result.append("\n")
        
        board_str: list[list[Text | str]] = [["Ｘ " for _ in range(8)] for _ in range(8)] 
        
        y, x = piece.coord
        board_str[y][x] = Text(f"{piece.char_view}  ", f"bold {piece.str_color}")
        
        for coord, objetive in piece.get_coords_objetive():
            color: str
            
            if objetive == ObjetiveChess.EMPTY: color = "green"
            elif objetive == ObjetiveChess.ENEMY: color = "red"
            elif objetive == ObjetiveChess.INVALID: color = piece.str_color
            else: color = "white"
            
            y, x = coord
            board_str[y][x] = Text("Ｘ ", f"bold {color}")
        
        for column in board_str:
            result.append("   ")
            
            for data in column: 
                result.append(data)
                
            result.append(" \n")
        
        return result


def get_view_term_square(square: "Square") -> Text:
        coord_str: str = f"  Coord: ({square.coord.y}, {square.coord.x})"
        board_str: list[list[Text | str]] = [["Ｘ " for _ in range(8)] for _ in range(8)] 
        
        piece_str: Text | str =  "  None"
        class_str: Text | str  = ""
        simbol_str: Text | str  = "@  "
        
        if square.piece != None:
            piece_str = f"  {square.piece.__class__.__name__}({square.piece.char_view} )"
            piece_str = Text(piece_str, style= f"bold {square.piece.str_color}\n")
            
            class_str = f"  class: {square.piece.clase}"
            class_str = Text(class_str, style= f"bold {square.piece.str_color}\n")
            
            simbol_str = Text("@  ", f"bold {square.piece.str_color}")
        
        result: Text = Text("\n")
        
        result.append("          Scuare           \n\n")
        result.append(f"{coord_str}\n")
        result.append(piece_str)   
        result.append(class_str)
        result.append("\n\n")
        
        board_str[square.coord.y][square.coord.x] = simbol_str
        
        for mov in square.movs_on_prowl:
            if mov.is_offensive:   
                ficha: "PieceChess" = mov.piece
                coord: "Coord" = ficha.coord
                board_str[coord.y][coord.x] =  Text(f"{ficha.char_view}  ", f"bold {ficha.str_color}")
        
        for column in board_str:
            result.append("  ")
            
            for data in column: 
                result.append(data)
            
            result.append(" \n")
        
        result.append("\n")
        
        for mov in square.movs_on_prowl:
            if mov.is_offensive:
                
                result.append(f"{mov.piece.__class__.__name__}({mov.piece.char_view} ): {mov.piece.clase}".center(27) , f"bold {mov.piece.str_color}")
                result.append("\n")
        
        return result
