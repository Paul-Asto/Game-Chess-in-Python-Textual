from typing import Generic, TYPE_CHECKING
from src.core.types_chess import T_Square
from src.core.coordinate import Coord
from src.core.piece import PieceChess

if TYPE_CHECKING:
    from src.core.square import Square
    

class Board(Generic[T_Square]):
    
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
    
    
    
    def __init__(self, size_y: int, size_x: int, type_square: type[T_Square]) -> None:
        '''
        Al inicializar se llama a la funcion "refresh_content" para guardar en el atributo content
        la matriz de "Scuare"
        '''
        self.type_square: type[T_Square] = type_square
        
        self.size_y: int = size_y
        self.size_x: int = size_x
        
        self.content: tuple[tuple[T_Square, ...], ...] = tuple([
                tuple([
                    self.type_square(Coord(y, x)) 
                    for x in range(self.size_x)
                ])
                for y in range(self.size_y)
            ])
    
    
    def reset_content(self) -> None:
        for column in self.content:
            for square in column:
                square.reset(self)

    
    def is_valid_coord(self, coord: Coord) -> bool:
        '''
        Verifica que la coordenada pasada como parametro sea una cordenada valida, 
        si es una coordenada valida retorna True de lo contrario False
        
        El numero que representa la posicion de los ejes "Y" y "X" no deben ser negativos
        y deben ser menores del tamaño del tablero
        '''
        
        return  (self.size_y > coord.y >= 0) and (self.size_x > coord.x >= 0)
    
    
    # Funcions gets
    def get_ficha(self, coord: Coord) -> PieceChess | None:
        '''
        Retorna la ficha dentro del "Scuare" en la posicion de la coordenada pasada como parametro,
        primero verifica si es una coordenada valida usando la funcion "is_valid_coord".
        
        Si es una coordenada valida retorna la ficha del "scuare" de lo contrario retorna None
        '''
        
        return self.get_scuare(coord).piece if self.is_valid_coord(coord) else None
    
    
    def get_scuare(self, coord: Coord) -> T_Square | None:
        '''
        Retorna el "Scuare" en la posicion de la coordenada pasada como parametro,
        primero verifica si es una coordenada valida usando la funcion "is_valid_coord".
        
        Si es una coordenada valida retorna el "scuare" de lo contrario retorna None
        '''
        
        return self.content[coord.y][coord.x] if self.is_valid_coord(coord) else None
    
    
    # Funcions set Fichas
    def set_ficha(self, ficha: PieceChess, coord: Coord) -> None:
        '''
        Setea la ficha pasada como parametro en el "Scuare" 
        de la posicion de la coordenada pasada como parametro
        '''
        
        square = self.get_scuare(coord)
        square.piece = ficha
        ficha.square = square
    
    
    def set_fichas(self, fichas: list[tuple[Coord, PieceChess]]) -> None:
        '''
        Setea varias fichas en varios Scuares
        
        Toma como parametro una lista de datos emparejados de coordenada y ficha y realiza 
        un seteo por cada uno de los datos de la lista usando la funcion "set_ficha"
        '''
        
        for coord, ficha in fichas:
            self.set_ficha(ficha, coord)
    
