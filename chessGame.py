from typing import TYPE_CHECKING
from constant import OBJ_EMPTY, OBJ_ENEMY

from coord import Coord
from piece.piece import PieceChess, EntityChess, EmptyChess
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
    

    # Turno Funcions
    def update_turno(self) -> None: 
        self.turno = self.adminFichas.get_enemy_for_class(self.turno)


    def is_equals_turno(self, turno: str) -> str:
        return self.turno == turno


    # tablero Funcions
    def get_ficha(self, coord: Coord) -> EntityChess | None:
        return self.tablero.get_ficha(coord)


    def iteration(self, app: "ChessApp")-> None:
        army_next = self.adminFichas.get_enemy_army_for_class(self.previous_ficha.clase)

        army_next.update_influence_rey(self.tablero)
        army_next.delete_peon_passant(self.tablero, app)
        
        self.update_turno()
        app.update_view_turno(self.turno)

        if not(isinstance(self.previous_ficha, PieceChess)):
            return
        
        # Evento de finalizacion del programa
        if admin_armys.get_enemy_army_for_class(self.previous_ficha.clase).in_hacke_mate:
            app.exit_app()


    def set_selected_ficha(self, value: EntityChess) -> None:
        self.previous_ficha = self.selected_ficha
        self.selected_ficha = value


    def accion_game(self, group_blocks: "GroupBlocks") -> None:
        if isinstance(self.previous_ficha, EmptyChess):
            if not isinstance(self.selected_ficha, PieceChess):
                return

            # Si es el turno de la ficha seleccionada, entonces renderiza los objetivos
            if self.is_equals_turno(self.selected_ficha.clase):
                group_blocks.addRegisterBlock(self.selected_ficha.get_coords_objetive())
                return 


        elif isinstance(self.previous_ficha, PieceChess):
            group_blocks.clearRegisterBlock(self.previous_ficha.get_coords_objetive())

            # Verifica que  la ficha previa tenga la misma clase que la ficha seleccionada
            if self.previous_ficha.is_equals_class(self.selected_ficha.clase):
                # Si la ficha previa es diferente de la ficha seleccionada, entonces renderiza
                if self.previous_ficha != self.selected_ficha:
                    group_blocks.addRegisterBlock(self.selected_ficha.get_coords_objetive())
                    return
            
            # En caso de que la ficha previa sea de diferente clase que la ficha seleccionada,
            # se sabe que la ficha seleccionada puede ser un empty o una ficha enemiga,
            #  entonces realiza un movimiento
            else:
                movement_performed, is_objetive_enemy = self.previous_ficha.make_mov(self.selected_ficha, self.tablero)

                if movement_performed:
                    group_blocks.update_view_block_off_coord(self.previous_ficha.coord, self.selected_ficha.coord)
                    app: "ChessApp" = group_blocks.app

                    if is_objetive_enemy:
                        app.save_view_kill(self.selected_ficha)
                    
                    self.iteration(app)  


        # Se setea la ficha seleccionada para que en una futura accion la previous_ficha siempre sea empty
        self.set_selected_ficha(EmptyChess())



chess_game: ChessGame = ChessGame()