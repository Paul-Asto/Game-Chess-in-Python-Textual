from typing import TYPE_CHECKING

from coord import Coord
from piece import PieceChess, EntityChess, EmptyChess
from board import Board

from admin_armys import AdminArmys, admin_armys
from scuare import Scuare


if TYPE_CHECKING:
    from chessApp import ChessApp, GroupBlocks
    


class ChessGame:
    def __init__(self) -> None:
        self.tablero: Board = Board()
        self.adminFichas: AdminArmys =  admin_armys

        self.turno: str = self.adminFichas.claseA

        self.previous_ficha: EntityChess = EmptyChess()
        self.selected_ficha: EntityChess = EmptyChess()

        self.init()

    
    # Funcions Starts
    def init(self) -> None:
        self.tablero.set_fichas(self.adminFichas.fichas)
        self.adminFichas.init_influence(self.tablero)


    def restart_data(self):
        self.adminFichas.reStartArmys()
        self.tablero.refresh_content()

        self.turno = self.adminFichas.claseA

        self.previous_ficha = EmptyChess()
        self.selected_ficha = EmptyChess()

    
    def restart_game(self):
        self.restart_data()
        self.init()
    

    def iteration(self, app: "ChessApp")-> None:
        self.update_turno()
        app.update_view_turno(self.turno)

        if not(isinstance(self.previous_ficha, PieceChess)):
            return
        
        # Evento de finalizacion del programa
        if admin_armys.get_enemy_army_for_class(self.previous_ficha.clase).in_hacke_mate:
            app.exit_app()


    # Turno Funcions
    def update_turno(self) -> None: 
        self.turno = self.adminFichas.get_enemy_for_class(self.turno)


    def is_equals_turno(self, turno: str) -> str:
        return self.turno == turno


    # SelectedFicha Funcions
    def getSelectedFicha(self) -> EntityChess:
        return self.selected_ficha

    def set_selected_ficha(self, value: EntityChess) -> None:
        self.previous_ficha = self.selected_ficha
        self.selected_ficha = value


    # tablero Funcions
    def get_scuare(self, coord: tuple) -> Scuare:
        return self.tablero.get_scuare(coord)
    

    def get_ficha(self, coord: Coord) -> EntityChess | None:
        return self.tablero.get_ficha(coord)


    def trade_ficha(self, ficha_A: EntityChess, ficha_B: EntityChess) -> None:
        ficha_A.clear_influence(self.tablero)
        ficha_B.clear_influence(self.tablero)

        scuareA:Scuare = ficha_A.scuare
        scuareB:Scuare = ficha_B.scuare

        scuareA.ficha = ficha_B
        scuareB.ficha = ficha_A

        scuareA.ficha.spread_influence(self.tablero)
        scuareB.ficha.spread_influence(self.tablero)

        self.adminFichas.get_enemy_army_for_class(ficha_A.clase).update_influence_rey(self.tablero)


    def fusion_ficha(self, ficha_A: EntityChess, ficha_B: EntityChess, app: "ChessApp") -> None:
        ficha_A.clear_influence(self)
        ficha_B.clear_influence(self)

        scuareA:Scuare = ficha_A.scuare
        scuareB:Scuare = ficha_B.scuare

        ficha_B.scuare = scuareA
        scuareA.ficha = EmptyChess()
        scuareB.ficha = ficha_A

        scuareA.ficha.spread_influence(self.tablero)
        scuareB.ficha.spread_influence(self.tablero)

        self.adminFichas.get_enemy_army_for_class(ficha_A.clase).update_influence_rey(self.tablero)

        app.save_view_kill(ficha_B)


    def accion_game(self, group_blocks: "GroupBlocks") -> None:
        if isinstance(self.previous_ficha, PieceChess):
            group_blocks.clearRegisterBlock(self.previous_ficha.get_coords_objetive())

        match (self.previous_ficha, self.selected_ficha):

            case (EmptyChess(), EmptyChess()):
                pass    

            case (EmptyChess(), PieceChess()):
                if self.is_equals_turno(self.selected_ficha.clase):
                    group_blocks.addRegisterBlock(self.selected_ficha.get_coords_objetive())
                    return

                self.set_selected_ficha(EmptyChess())

            case (PieceChess(), EmptyChess()):
                if self.previous_ficha.coord_is_objetive(self.selected_ficha.coord, "empty"):
                    self.trade_ficha(self.previous_ficha, self.selected_ficha)
                    group_blocks.update_view_block_off_coord(self.previous_ficha.coord, self.selected_ficha.coord)

                    self.iteration(group_blocks.app)
                    

            case (PieceChess(), PieceChess()):
                if self.previous_ficha == self.selected_ficha:
                    self.set_selected_ficha(EmptyChess())
                    return

                if self.previous_ficha.coord_is_objetive(self.selected_ficha.coord, "enemy"):
                    self.fusion_ficha(self.previous_ficha, self.selected_ficha, group_blocks.app)
                    group_blocks.update_view_block_off_coord(self.previous_ficha.coord, self.selected_ficha.coord)
                    self.set_selected_ficha(EmptyChess())

                    self.iteration(group_blocks.app)  
                    return

                if self.is_equals_turno(self.selected_ficha.clase):
                    group_blocks.addRegisterBlock(self.selected_ficha.get_coords_objetive())
                    return
                
                self.set_selected_ficha(EmptyChess())


chess_game: ChessGame = ChessGame()