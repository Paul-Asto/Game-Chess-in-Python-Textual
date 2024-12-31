from typing import TYPE_CHECKING
from constant import OBJ_INVALID, OBJ_EMPTY, OBJ_ENEMY, CHAR_VIEW_REY

from coord import Coord
from piece.mov_piece import MovPieceRey, MovReyEnrroqueCorto, MovReyEnrroqueLargo
from piece.piece import PieceChess, EmptyChess, EntityChess

if TYPE_CHECKING:
    from mov_piece import MovPiece  
    from scuare import Scuare
    from board import Board
    from army import Army



class Rey(PieceChess):
    def __init__(self, army: "Army" = None):
        super().__init__(army)

        self.char = CHAR_VIEW_REY

        self.admin_obj.add_movs(
            MovPieceRey(self, (0, 1)),
            MovPieceRey(self, (0, -1)),
            MovPieceRey(self, (-1, 0)),
            MovPieceRey(self, (1, 0)),
            MovPieceRey(self, (-1, -1)),
            MovPieceRey(self, (-1, 1)),
            MovPieceRey(self, (1, -1)),
            MovPieceRey(self, (1, 1)),

            MovReyEnrroqueCorto(self),
            MovReyEnrroqueLargo(self),
        )


    def spread_influence(self, board: "Board") -> None:
        # Cambiar estado de fichas defensivas anteriores
        for ficha in self.army.pieces_defending:
            ficha.in_still = False
        
        self.army.pieces_defending.clear()

        # Verificar Hacke 
        self.army.in_hacke = False

        in_hacke, mov_causes_hacke = self.scuare.is_attacked()

        if in_hacke:
            self.army.in_hacke = True

            coords_prioridad: list[tuple] = [(mov_causes_hacke.ficha.coord, OBJ_ENEMY)] + mov_causes_hacke.ficha.admin_obj.get_data_off_mov(mov_causes_hacke)
            self.army.coords_priority = coords_prioridad

        # llamada a la funcion de la superclase
        super().spread_influence(board)

        # se sobre esribe el registro de coordenada de la parte trasera de la ficha como invalida en caso de un mov_causes_hacke spreadable
        if in_hacke:
            coord = self.coord + mov_causes_hacke

            if  mov_causes_hacke.is_offensive and mov_causes_hacke.is_spreadable and board.is_valid_coord(coord):  
                self.admin_obj.add_coord_off_mov(mov_causes_hacke, coord, OBJ_INVALID)

        # Verificar Hacke Mate
        if self.in_hacke:
            coords_disp: list[tuple[Coord, str]] = []

            for _, ficha in self.army.fichas:
                coords_disp += ficha.get_coords_objetive()
            
            result: bool = True

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