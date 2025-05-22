from typing import TYPE_CHECKING

from rich.text import Text
from src.core.types_chess import ColorPiece
from src.core.chess_constant import EObjetiveChess

if TYPE_CHECKING:
    from src.core.piece import PieceChess
    from src.core.board import Board
    from src.core.square import Square
    from src.core.coordinate import Coord

def get_view_term_board(board:"Board[Square]") -> Text:
        index: int = 8
        view: Text = Text()
        view.append("____________________________\n")
        view.append("|          Board            |\n")
        view.append("|___________________________|\n\n")
        view.append("   A  B  C  D  E  F  G  H  \n\n")
        

        for column in board.content:
            view.append(f"{index}  ")

            for scuare in column:
                ficha = scuare.piece
                
                if ficha == None:
                    view.append("Ｘ ")
                    continue
                
                view.append(f"{ficha.char_view}  ", style=f"bold {ficha.console_color}")
                

            view.append(f" {index}\n")
            index -= 1 

        view.append("\n   A  B  C  D  E  F  G  H  \n")

        return view


def get_view_term_piece(piece: "PieceChess") -> Text:
        result: Text = Text("\n")

        result.append(f"{piece.__class__.__name__}({piece.char_view} )".center(27), f"bold {piece.console_color}")
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

        tablero_str: list[list[str]] = [["Ｘ " for _ in range(8)] for _ in range(8)] 

        y, x = piece.coord
        tablero_str[y][x] = Text(f"{piece.char_view}  ", f"bold {piece.console_color}")

        for coord, tipo in piece.get_coords_objetive():
            color: ColorPiece 

            if tipo == EObjetiveChess.EMPTY.value: color = "green"
            elif tipo == EObjetiveChess.ENEMY.value: color = "red"
            elif tipo == EObjetiveChess.INVALID.value: color = piece.console_color

            y, x = coord
            tablero_str[y][x] = Text("Ｘ ", f"bold {color}")

        for column in tablero_str:
            result.append("   ")

            for data in column: 
                result.append(data)
                
            result.append(" \n")
    
        return result


def get_view_term_square(square: "Square") -> Text:
        coord_str: str = f"  Coord: ({square.coord.y}, {square.coord.x})"
        tablero_str: list[list[str]] = [["Ｘ " for _ in range(8)] for _ in range(8)] 

        ficha_str = "  None"
        clase_str = ""
        simbolo_str = "@  "
        
        if square.piece != None:
            ficha_str = f"  {square.piece.__class__.__name__}({square.piece.char_view} )"
            ficha_str = Text(ficha_str, style= f"bold {square.piece.console_color}\n")

            clase_str = f"  class: {square.piece.clase}"
            clase_str = Text(clase_str, style= f"bold {square.piece.console_color}\n")

            simbolo_str = Text("@  ", f"bold {square.piece.console_color}")
        
        result: Text = Text("\n")
        
        result.append("          Scuare           \n\n")
        result.append(f"{coord_str}\n")
        result.append(ficha_str)   
        result.append(clase_str)
        result.append("\n\n")

        tablero_str[square.coord.y][square.coord.x] = simbolo_str

        for mov in square.movs_on_prowl:
            if mov.is_offensive:   
                ficha: "PieceChess" = mov.ficha
                coord: "Coord" = ficha.coord

                tablero_str[coord.y][coord.x] =  Text(f"{ficha.char_view}  ", f"bold {ficha.console_color}")

        for column in tablero_str:
            result.append("  ")

            for data in column: 
                result.append(data)

            result.append(" \n")
        
        result.append("\n")

        for mov in square.movs_on_prowl:
            if mov.is_offensive:
                
                result.append(f"{mov.ficha.__class__.__name__}({mov.ficha.char_view} ): {mov.ficha.clase}".center(27) , f"bold {mov.ficha.console_color}")
                result.append("\n")

        return result
