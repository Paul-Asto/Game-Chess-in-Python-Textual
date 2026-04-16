from typing import Optional

from src.core.types import ArmyClass
from src.core.square import Square
from src.core.coordinate import Coord
from src.core.piece import PieceChess



class Board:
    
    '''
    Class Board:
    
    
    ((Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare), \n
    (Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare), \n
    (Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare), \n
    (Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare), \n
    (Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare), \n
    (Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare), \n
    (Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare), \n
    (Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare, Scuare)) \n
    
    
    
    > La clase Board es una representacion de un tablero de ajedrez que esta conformado 
    por una matriz 2D de 8 x 8 de clases "Scuare"
    
    > La matriz es inmutable, las clases "Scuare" nunca cambiaran de posicion, ni se modificara 
    ni se agregara mas elementos
    
    > Cada clase "Scuare contiene informacion de su coordenada actual en la matriz, ademas de que 
    puede poseer dentro de si una clase derivada de "EntityChess"("EmptyChess or PieceChess). 
    
    > Al crear una instancia, todos los "Scuares tendran una instancia de la clase "EmptyChess" 
    como ficha por defecto.
    
    Scuare(
        coord = Coord(posicion_y, posicion_x), # Coordenada en la matriz
        ficha = EmptyChess()        # por defecto al instanciar la clase "Board"
    )
    
    > Las objetos "Scuare", si pueden cambiar la ficha que llevan dentro de si, por cualquier 
    objeto de clase "EmptyChess o derivadas de PieceChess como "Peon", "Rey", "Caballo", etc
    
    > La mayoria de las funciones que realizan busquedas dentro de la matriz utilizan objetos "Coord" 
    como parametro
    
    
    - ATRIBUTOS: \n
    
    - size_y (int):                       Numero de elementos de eje y de la matriz \n
    - size_x (int):                       Numero de elementos de eje y de la matriz \n
    
    - content (tuple[tuple[Scuare]] ):    Contenido de la matriz de "Scuare" \n
    '''
    
    def __init__(self, size_y: int, size_x: int) -> None:
        self.__size_y: int = size_y
        self.__size_x: int = size_x
        
        self.__content: tuple[tuple[Square, ...], ...] = tuple([
                tuple([
                    Square(Coord(y, x), self) 
                    for x in range(self.size_x)
                ])
                for y in range(self.size_y)
            ])
    
    
    @property
    def size_y(self) -> int:
        '''
        Propiedad que devuelve el tamaño del tablero en la coordenada y
        '''
        return self.__size_y
    
    @property
    def size_x(self) -> int:
        '''
        Propiedad que devuelve el tamaño del tablero en la coordenada x
        '''
        return self.__size_x
    
    
    @property
    def content(self) -> tuple[tuple[Square, ...], ...] :
        '''
        Propiedad que devuelve el contenido en matriz de todas las casillas
        '''
        return self.__content
    
    
    @property
    def notation_forsyth_edwards(self) -> str:
        '''
        Propiedad que devuelve la notacion FEN que representa 
        la posicion de las piezas en el tablero
        '''
        fen_board: str = ""
        
        for column in self.__content:
            n_emptys: int = 0
            
            for scuare in column:
                piece: PieceChess | None = scuare.piece
                
                if piece is None:
                    n_emptys += 1
                    continue
                
                if n_emptys != 0:
                    fen_board += str(n_emptys)
                    n_emptys = 0
                
                piece_fen: str = \
                    piece.character_fen.value.upper() \
                    if piece.clase == ArmyClass.WHITE.value else \
                    piece.character_fen.value.lower()
                
                fen_board += piece_fen
            
            if n_emptys != 0:
                fen_board += str(n_emptys)
            
            fen_board += "/"
        
        return fen_board[: -1]
    
    
    def clear_content(self) -> None:
        '''
        Funcion que limpia todas las casillas de piezas e influencias de movimientos
        '''
        for column in self.__content:
            for square in column:
                square.delete_piece()
    
    
    def is_valid_coord(self, coord: Coord) -> bool:
        '''
        Verifica que la coordenada pasada como parametro sea una cordenada valida, 
        si es una coordenada valida retorna True de lo contrario False
        
        El numero que representa la posicion de los ejes "Y" y "X" no deben ser negativos
        y deben ser menores del tamaño del tablero
        '''
        
        return  (self.size_y > coord.y >= 0) and (self.size_x > coord.x >= 0)
    
    
    # Funcions gets
    def get_piece(self, coord: Coord) -> PieceChess | None:
        '''
        Retorna la ficha dentro del "Scuare" en la posicion de la coordenada pasada como parametro,
        primero verifica si es una coordenada valida usando la funcion "is_valid_coord".
        
        Si es una coordenada valida retorna la ficha del "scuare" de lo contrario retorna None
        '''
        
        square: Optional["Square"] = self.get_square(coord)
        
        if square is None:
            return None
        
        return square.piece 
    
    
    def get_square(self, coord: Coord) -> Square | None:
        '''
        Retorna el "Scuare" en la posicion de la coordenada pasada como parametro,
        primero verifica si es una coordenada valida usando la funcion "is_valid_coord".
        
        Si es una coordenada valida retorna el "scuare" de lo contrario retorna None
        '''
        
        return self.__content[coord.y][coord.x] if self.is_valid_coord(coord) else None
    
    
    # Funcions set Fichas
    def set_piece(self, piece: PieceChess, coord: Coord) -> None:
        '''
        Setea la ficha pasada como parametro en el "Scuare" 
        de la posicion de la coordenada pasada como parametro
        '''
        
        square: Optional["Square"] = self.get_square(coord)
        
        if square is None:
            raise Exception("Fallo al setear Fichas al Tablero")
        
        square.receive_piece(piece)
    
    
    def set_pieces(self, pieces: list[tuple[Coord, PieceChess]]) -> None:
        '''
        Setea varias fichas en varios Scuares
        
        Toma como parametro una lista de datos emparejados de coordenada y ficha y realiza 
        un seteo por cada uno de los datos de la lista usando la funcion "set_ficha"
        '''
        
        for coord, ficha in pieces:
            self.set_piece(ficha, coord)


    def get_movs_of_dead_pieces(self) -> dict[str, list[tuple[int, int]]]:
        movs: dict[str, list[tuple[int, int]]] = {}
        for column in self.content:
            for square in column:
                for mov in square.movs_on_prowl:
                    piece = mov.piece
                    army = piece.army
                    if piece in army.pieces_in_cementery:
                        if movs.get(f"{piece.id.value} {piece.clase}") is None:
                            movs[f"{piece.id.value} {piece.clase}"] = [square.coord.value]
                        
                        else:
                            movs[f"{piece.id.value} {piece.clase}"].append(square.coord.value)

        return movs

