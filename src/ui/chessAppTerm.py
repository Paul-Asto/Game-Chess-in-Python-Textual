from typing import TYPE_CHECKING

from rich.text import Text
from rich.console import Console
from rich.layout import Layout


if TYPE_CHECKING:
    from src.chessGame import ChessGame
    from src.core.square import Square
    from src.core.piece import PieceChess, EmptyChess

class ChessAppTerm:

    def __init__(self, game: "ChessGame"):
        self.console: Console = Console()
        self.game: "ChessGame" = game
        

    @property
    def view_board(self) -> Text:
        index: int = 8
        view: Text = Text()
        view.append("____________________________\n")
        view.append("|          Board            |\n")
        view.append("|___________________________|\n\n")
        view.append("   A  B  C  D  E  F  G  H  \n\n")

        for column in self.game.board.content:
            view.append(f"{index}  ")

            for scuare in column:
                ficha = scuare.ficha
                
                if isinstance(ficha, "EmptyChess"):
                    view.append("Ｘ ")
                    continue
                    
                if isinstance(ficha, "PieceChess"):
                    view.append(f"{ficha.char}  ", style=f"bold {ficha.console_color}")
                    continue

            view.append(f" {index}\n")
            index -= 1 

        view.append("\n   A  B  C  D  E  F  G  H  \n")

        return view


    def view_square(self, square: "Square") -> Text:
        pass


    def view_piece(self, piece: "PieceChess") -> Text:
        pass


    def run(self):
        pass



if __name__ == "__main__":
    pass

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

# Crear una consola
console = Console()


# Crear el diseño principal
layout = Layout()

# Dividir el diseño en una columna superior y una inferior
layout.split_column(
    Layout(name="superior"),
    Layout(name="inferior")
)

# Dividir la sección inferior en dos columnas
layout["inferior"].split_row(
    Layout(name="izquierda"),
    Layout(name="derecha")
)

# Asignar contenido a cada sección
layout["superior"].update(Panel("Encabezado", title="Sección Superior"))
layout["izquierda"].update(Panel("Contenido Izquierdo", title="Sección Izquierda"))
layout["derecha"].update(Panel("Contenido Derecho", title="Sección Derecha"))

# Imprimir el diseño en la consola
console.print(layout)

