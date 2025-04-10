from typing import TYPE_CHECKING
from rich.text import Text

from src.coordinate import Coord
from src.core.piece import EntityChess, EmptyChess, PieceChess

    
if TYPE_CHECKING:
    from src.core.mov_piece import MovPiece



class Square:
    '''
    Class Scuare:  \n
    
    Coord: (n, m) \n
    ___________________  \n
    |     Scuare       |  \n
    |__________________|  \n
    |  Piece or Empty  |  <----    Movs on Prowl: list[MovFicha] = [Mov, Mov, Mov]  \n
    |__________________|  \n

    > La clase Scuare representa una casilla del tablero,  \n
    en el Board hay en total 64 (8 x 8) clases Scuare,  \n
    estas estan hechas para quedarse siempre en su posicion en la matriz.  \n

    > Las clases scuare contienen siempre una ficha o un empty,  \n
    esta ficha puede ser reemplazada por otra muchas veces,   \n
    al obtener una nueva ficha la ficha tambien guarda   \n
    la referencia del scuare en su atributo scuare  \n

    > La lista de movs_on_prowl contiene los movimientos   \n
    de fichas que tienen como objetivo este scuare, esto   \n
    quiere decir que estas fichas tienen la capacidad de trasladarse a este scuare.  \n

    > Los movPieces son almacenados como llaves con valor None, 
    estos se diferencian entre si con su atributo value que es una tupla 
    de 2 int que representan la direccion de movimiento, ejemplo: \n
    
    - up -> (-1, 0)\n
    - down -> (1, 0)\n
    - left -> (0, -1)\n
    - right -> (0, 1)\n
    
    > pueden existir 2 movsPieces con un  mismo valor
    
    - Atributos:  \n
    - coord (Coord):                              coordenada  inmutable  \n
    - ficha (EntityChess)                         ficha contenida actualmente en el scuare, el scuare puede cambiar de ficha  \n
    - movs_on_prowl (dict["MovPiece", None])        lista de movimientos de fichas que tienen como objetivo este Scuare  \n
    '''

    sealed_ficha: EntityChess

    def __init__(self, coord: Coord, ficha: EntityChess) -> None      :
        self.coord: Coord = coord
        self.ficha = ficha

        self.__movs_on_prowl: dict["MovPiece", None] = {}


    @property
    def view(self) -> Text:
        coord_str: str = f"Coord: ({self.coord.y}, {self.coord.x})"
        clase_str: str = f" class: {self.ficha.clase}".ljust(20)
        tablero_str: list[list[str]] = [["Ｘ " for _ in range(8)] for _ in range(8)] 
        ficha_str: str = ""

        if isinstance(self.ficha, PieceChess):
            ficha_str = f"{self.ficha.__class__.__name__}({self.ficha.char} )".center(20)

        elif isinstance(self.ficha, EmptyChess):
            ficha_str= self.ficha.__class__.__name__.center(20)
        
        result: Text = Text("____________________________\n")
        
        result.append("|          Scuare           |\n")
        result.append(f"|{coord_str.center(27)}|\n")
        result.append("|  _____________________    |\n")
        result.append("|  |                    |   |\n")

        result.append(f"|  |")
        result.append(ficha_str, style= f"bold {self.ficha.console_color}")
        result.append("|   |\n")
        
        result.append(f"|  |")
        result.append(clase_str, style= f"bold {self.ficha.console_color}")
        result.append("|   |\n")

        result.append("|  |____________________|   |\n")
        result.append("|                           |\n")

        tablero_str[self.coord.y][self.coord.x] = Text("@  ", f"bold {self.ficha.console_color}")

        for mov in self.movs_on_prowl:
            if mov.is_offensive:   
                ficha: PieceChess = mov.ficha
                coord: Coord = ficha.coord

                tablero_str[coord.y][coord.x] =  Text(f"{ficha.char}  ", f"bold {ficha.console_color}")

        for column in tablero_str:
            result.append("|  ")

            for data in column: 
                result.append(data)

            result.append(" |\n")
        
        result.append("|                           |\n")

        for mov in self.movs_on_prowl:
            if mov.is_offensive:
                result.append("|")
                result.append(f"{mov.ficha.__class__.__name__}({mov.ficha.char} ): {mov.ficha.clase}".center(27) , f"bold {mov.ficha.console_color}")
                result.append("|\n")

        result.append("|___________________________|\n")

        return result


    # propiedad Ficha
    @property
    def ficha(self) -> EntityChess: 
        return self.sealed_ficha
    
    @ficha.setter
    def ficha(self, value: EntityChess) -> None: 
        self.sealed_ficha = value
        self.sealed_ficha.scuare = self


    # Propiedad movs_prowl
    @property
    def movs_on_prowl(self) -> list["MovPiece"]:
        return list(self.__movs_on_prowl.keys())


    def add_mov_prowl(self, mov: "MovPiece") -> None: 
        '''
        Añade una clase "MovPiece" al diccionario movs_on_prowl
        '''
        self.__movs_on_prowl[mov] = None

    
    def deleted_mov_prowl(self, mov: "MovPiece")-> None: 
        '''
        Elimina una clase "MovPiece" al diccionario movs_on_prowl
        '''
        self.__movs_on_prowl.pop(mov)

    
    def is_attacked(self, clase: str = None ) -> tuple[bool, "MovPiece"]:
        '''
        Devuelve True si el scuare esta siendo atacado por alguna ficha
        que tenga diferente clase que la clase de la ficha del scuare y 
        si el movimiento es ofensivo
        '''

        clase_attacked: str

        if clase == None:
            clase_attacked = self.ficha.clase
        
        else:
            clase_attacked = clase

        for mov in self.movs_on_prowl:
            if clase_attacked == mov.ficha.clase:
                continue

            if mov.is_offensive:
                return (True, mov)

        return (False, None)