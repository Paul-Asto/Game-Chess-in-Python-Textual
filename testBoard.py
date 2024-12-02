from board import Board
from torre import Torre
from coord import Coord



tablero = Board()

torre = Torre()
torre.clase = "blanco"
tablero.set_ficha(torre, Coord(0, 0))
torre.spread_influence(tablero)


'''torre = Torre()
torre.clase = "negro"
tablero.set_ficha(torre, Coord(0, 0))
torre.spread_influence(tablero)
'''
