from typing import TYPE_CHECKING
from constant import OBJ_INVALID, OBJ_EMPTY, OBJ_ENEMY

from coord import Coord
from piece.mov_piece import MovPiece
from piece.piece import PieceChess, EmptyChess, EntityChess

if TYPE_CHECKING:
    from scuare import Scuare
    from board import Board
    from army import Army



class Rey(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.char = chr(9812)

        self.admin_obj.add_movs(
            MovPiece(self, (0, 1)),
            MovPiece(self, (0, -1)),
            MovPiece(self, (-1, 0)),
            MovPiece(self, (1, 0)),
            MovPiece(self, (-1, -1)),
            MovPiece(self, (-1, 1)),
            MovPiece(self, (1, -1)),
            MovPiece(self, (1, 1)),
        )


    def add_objetives(self, board: "Board", mov: MovPiece):
        in_first_scuare: bool = True
        registered_defender: bool = False

        ficha_defender: PieceChess = None
        coord_actual: Coord = self.coord.copy()

        while True:
            coord_actual += mov
            ficha_actual: EntityChess = board.get_ficha(coord_actual)

            match ficha_actual:
                case PieceChess():
                    # se ejeuta si es el primer movimiento
                    if in_first_scuare:
                        if not ficha_actual.is_equals_class(self.clase):
                            self.add_coord_objetive(mov, coord_actual, OBJ_ENEMY)
                            ficha_actual.add_mov_prowl(mov)
                            return

                        self.add_coord_objetive(mov, coord_actual, OBJ_INVALID)
                        ficha_actual.add_mov_prowl(mov)

                        ficha_defender = ficha_actual
                        registered_defender = True

                        in_first_scuare = False
                        continue

                    # se ejecuta para buscar la ficha defensiva
                    if not registered_defender:
                        if not ficha_actual.is_equals_class(self.clase):
                            break

                        ficha_defender = ficha_actual
                        registered_defender = True
                        continue

                    # se ejecuta para buscar la ficha enemiga
                    if ficha_actual.is_equals_class(self.clase):
                        break

                    for movEnemy in ficha_actual.admin_obj.get_movs():
                        if mov.GetOpuesto() == movEnemy and movEnemy.is_spreadable:
                            self.army.pieces_defending.append(ficha_defender)

                            ficha_defender.in_still = True
                            ficha_defender.allowed_movs = [mov, movEnemy]
                            break


                case EmptyChess():
                    if in_first_scuare:
                        self.add_coord_objetive(mov, coord_actual, OBJ_EMPTY)
                        ficha_actual.add_mov_prowl(mov)
                        in_first_scuare = False


                case None:
                    return 
                

    def spread_influence(self, board: "Board") -> None:
        
        # Cambiar estado de fichas defensivas anteriores
        for ficha in self.army.pieces_defending:
            ficha.in_still = False
        
        self.army.pieces_defending.clear()

        # Cambiamos el estado hacke anterior
        self.army.in_hacke = False

        # llamada a la funcion de la superclase
        super().spread_influence(board)

        # Descartar opciones de coordenadas en amenaza
        for mov in self.admin_obj.get_movs():
            coords = self.admin_obj.get_coords_off_mov(mov)

            if len(coords) == 0:
                continue

            coord: Coord = coords[0]
            scuare: "Scuare" = board.get_scuare(coord)

            for mov_prowl in scuare.movs_on_prowl:
                if (mov_prowl.ficha.clase != self.clase) and mov_prowl.is_offensive:
                    self.add_coord_objetive(mov, coord, OBJ_INVALID)
                    break

        # Verificar Hacke 
        for mov in self.scuare.movs_on_prowl:
            if self.is_equals_class(mov.ficha.clase):
                continue

            self.army.in_hacke = True

            coords_prioridad: list[tuple] = [(mov.ficha.coord, OBJ_ENEMY)] + mov.ficha.admin_obj.get_data_off_mov(mov)
            self.army.coords_priority = coords_prioridad


            coord = self.coord + mov

            if mov.is_offensive and mov.is_spreadable and board.is_valid_coord(coord):
                self.admin_obj.add_coord_off_mov(mov, coord, OBJ_INVALID)
            break


        # Verificar Hacke Mate
        if self.in_hacke:
            result: bool = True

            coords_disp: list[tuple[Coord, str]] = []

            for _, ficha in self.army.fichas:
                coords_disp += ficha.get_coords_objetive()
            
            for _, tipo in coords_disp:
                if tipo != OBJ_INVALID:
                    result = False
                    break
            
            if result:
                self.army.in_hacke_mate = True



    def coord_is_objetive(self, coord: Coord, value: str) -> bool:
        return self.admin_obj.coord_in_store(coord, value)
    

    def get_coords_objetive(self):
        return self.admin_obj.get_data()
    


