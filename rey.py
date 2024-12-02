from typing import TYPE_CHECKING

from coord import Coord
from mov_piece import MovPiece
from piece import PieceChess, AdminObjetives, EmptyChess, EntityChess


if TYPE_CHECKING:
    from scuare import Scuare
    from chessGame import ChessGame



class Rey(PieceChess):
    def __init__(self, army = None):
        super().__init__(army)

        self.char = chr(9812)
        self.pieces_defending: list[PieceChess] = []

        self.admin_obj = AdminObjetives(
            MovPiece(self, (0, 1)),
            MovPiece(self, (0, -1)),
            MovPiece(self, (-1, 0)),
            MovPiece(self, (1, 0)),
            MovPiece(self, (-1, -1)),
            MovPiece(self, (-1, 1)),
            MovPiece(self, (1, -1)),
            MovPiece(self, (1, 1)),
        )


    def registrarObjectives(self, game: "ChessGame", mov: MovPiece):
        fichaDefender: PieceChess  = None
        directRegistrado: bool = False

        def registerRecursive(coord: Coord):
            nonlocal fichaDefender
            nonlocal directRegistrado

            ficha: EntityChess = game.get_ficha(coord)

            match ficha:
                case PieceChess():
                    if fichaDefender == None:
                        if (ficha.clase != self.clase):
                            if not directRegistrado:
                                self.add_coord_objetive(mov, coord, "enemy")
                                ficha.add_mov_prowl(mov)
                            return

                        else:
                            self.add_coord_objetive(mov, coord, "invalid")
                            fichaDefender = ficha
                            ficha.add_mov_prowl(mov)

                            for movEnemy in ficha.admin_obj.get_movs():
                                if mov.GetOpuesto() == movEnemy and movEnemy.is_spreadable:
                                    fichaDefender.in_defense = True
                                    self.pieces_defending.append(fichaDefender)
                                    fichaDefender.movs_defending = [mov, movEnemy]
                                    break
                        return
                    

                case EmptyChess():
                    if not directRegistrado:
                        self.add_coord_objetive(mov, coord, "empty")
                        ficha.add_mov_prowl(mov)
                        

                case None:
                    return 
                
            directRegistrado = True
                        
            
            registerRecursive(coord + mov)

        registerRecursive(self.coord + mov)


    def spread_influence(self, app: "ChessGame") -> None:     
        # Cambiar estado de fichas defensivas anteriores
        for ficha in self.pieces_defending:
            ficha.in_defense = False
        
        self.movs_defending.clear()

        # Cambiamos el estado hacke anterior
        self.army.in_hacke = False

        # llamada a la funcion de la superclase
        super().spread_influence(app)

        # Descartar opciones de coordenadas en amenaza
        for mov in self.admin_obj.get_movs():
            coords = self.admin_obj.get_coords_off_mov(mov)

            if len(coords) == 0:
                continue

            coord: Coord = coords[0]
            scuare: "Scuare" = app.get_scuare(coord)

            for mov_prowl in scuare.movs_on_prowl:
                if (mov_prowl.ficha.clase != self.clase) and mov_prowl.is_ofensive:
                    self.add_coord_objetive(mov, coord, "invalid")
                    break

        # Verificar Hacke 
        for mov in self.scuare.movs_on_prowl:
            if self.is_equals_class(mov.ficha.clase):
                continue

            self.army.in_hacke = True

            coords_prioridad: list[tuple] = [(mov.ficha.coord, "enemy")] + mov.ficha.admin_obj.get_data_off_mov(mov)
            self.army.coords_priority = coords_prioridad


            coord = self.coord + mov

            if mov.is_ofensive and mov.is_spreadable and app.tablero.is_valid_coord(coord):
                self.admin_obj.add_coord_off_mov(mov, coord, "invalid")
            break


        # Verificar Hacke Mate
        if self.in_hacke:
            result: bool = True

            coords_disp: list[tuple[Coord, str]] = []

            for _, ficha in self.army.fichas:
                coords_disp += ficha.get_coords_objetive()
            
            for _, tipo in coords_disp:
                if tipo != "invalid":
                    result = False
                    break
            
            if result:
                self.army.in_hacke_mate = True





    def coord_is_objetive(self, coord: Coord, value: str) -> bool:
        return self.admin_obj.coord_in_store(coord, value)
    

    def get_coords_objetive(self):
        return self.admin_obj.get_data()
    


