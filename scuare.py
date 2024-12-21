from termcolor import colored

from coord import Coord
from piece.piece import EntityChess, EmptyChess, PieceChess
from piece.mov_piece import MovPiece
    



class Scuare:
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
    - movs_on_prowl (dict[MovPiece, None])        lista de movimientos de fichas que tienen como objetivo este Scuare  \n
    '''

    coord: Coord
    __ficha: EntityChess
    __movs_on_prowl: dict[MovPiece, None]

    def __init__(self, coord: Coord, ficha: EntityChess) -> None      :
        self.coord = coord
        self.ficha = ficha
        self.__movs_on_prowl = {}


    def __str__(self) -> str:
        coord_str: str = f"Coord: ({self.coord.y}, {self.coord.x})"
        clase_str: str = colored(f" class: {self.ficha.clase}".ljust(20), self.ficha.console_color)
        tablero_str: list[list[str]] = [["Ｘ " for _ in range(8)] for _ in range(8)] 
        ficha_str: str

        if isinstance(self.ficha, PieceChess):
            ficha_str = f"{colored(f"{self.ficha.__class__.__name__}({self.ficha.char} )".center(20), self.ficha.console_color)}"

        elif isinstance(self.ficha, EmptyChess):
            ficha_str = self.ficha.__class__.__name__.center(20)
        
        result: str = "____________________________\n"
        
        result += "|          Scuare           |\n"
        result += f"|{coord_str.center(27)}|\n"
        result += "|  _____________________    |\n"
        result += "|  |                    |   |\n"
        result += f"|  |{ficha_str}|   |\n"
        result += f"|  |{clase_str}|   |\n"
        result += "|  |____________________|   |\n"
        result += "|                           |\n"

        tablero_str[self.coord.y][self.coord.x] = colored("◎  ", self.ficha.console_color)

        for mov in self.movs_on_prowl:
        
            ficha: PieceChess = mov.ficha
            coord: Coord = ficha.coord

            tablero_str[coord.y][coord.x] =  f"{colored(ficha.char, ficha.console_color)}  "

        for column in tablero_str:
            result += "|  "

            for data in column: 
                result += data

            result += " |\n"
        
        result += "|                           |\n"

        for mov in self.movs_on_prowl:
            result += "|"
            result += colored(f"{mov.ficha.__class__.__name__}({mov.ficha.char} ): {mov.ficha.clase}".center(27) , mov.ficha.console_color)
            result += "|\n"

        result += "|___________________________|\n"

        return result


    # propiedad Ficha
    @property
    def ficha(self) -> EntityChess: 
        return self.__ficha
    
    @ficha.setter
    def ficha(self, value: EntityChess) -> None: 
        self.__ficha = value
        self.__ficha.scuare = self


    # Propiedad movs_prowl
    @property
    def movs_on_prowl(self) -> list[MovPiece]:
        return list(self.__movs_on_prowl.keys())


    def add_mov_prowl(self, mov: MovPiece) -> None: 
        '''
        Añade una clase MovPiece al diccionario movs_on_prowl
        '''
        self.__movs_on_prowl[mov] = None

    
    def deleted__mov_prowl(self, mov: MovPiece)-> None: 
        '''
        Elimina una clase MovPiece al diccionario movs_on_prowl
        '''
        self.__movs_on_prowl.pop(mov)