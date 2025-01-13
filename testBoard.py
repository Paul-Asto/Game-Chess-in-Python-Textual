from board import Board
from piece.torre import Torre
from piece.alfil import Alfil
from piece.caballo import Caballo
from piece.reina import Reina
from piece.rey import Rey
from piece.peon import Peon

from coord import Coord




tablero = Board()

p1 = Peon(1)
p1.clase = "a"
p1.console_color = "blue"

p2 = Torre()
p2.clase = "b"
p2.console_color = "green"



tablero.set_ficha(p1, Coord(4, 4))
tablero.set_ficha(p2, Coord(5, 2))

p1.spread_influence(tablero)
p2.spread_influence(tablero)

space = tablero.get_ficha(Coord(5, 4))

print(tablero)
print(p1)
print(p2)

print("+++++++++++++++++++++++++++++++++++++++++++++++")

p1.make_mov(space, tablero)

print(tablero)
print(p1)
print(str(p2))





'''
def max_value_off_string(data: str) -> int:
    max_value: int = 0
    len_data: int = len(data)

    for index in range(len_data):
        n_count_left: int = data.count("0", 0, index)
        n_count_right: int = data.count("1", index, len_data)

        value_actual: int = n_count_left + n_count_right
        
        max_value = max(max_value, value_actual)

    return max_value


entrada: str = "011101"

print(max_value_off_string(entrada))'''