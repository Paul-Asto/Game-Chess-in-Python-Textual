from typing import TYPE_CHECKING

from src.coordinate import Coord
from src.core.piece import PieceChess, EntityChess, EmptyChess

if TYPE_CHECKING:
    from src.ui.chessApp import ChessApp, GroupBlocks
    from src.core.army import Army
    from src.core.board import Board
    


class ChessGame:
    number_off_middle_movs: int = 0
    number_off_movs: int = 1

    def __init__(self, army_white: "Army", army_black: "Army", board: "Board") -> None:
        self.board: "Board" = board

        self.army_white: "Army" = army_white
        self.army_black: "Army" = army_black

        self.turn: str = self.army_white.id

        self.previous_piece: EntityChess = EmptyChess()
        self.selected_piece: EntityChess = EmptyChess()

        self.init()

    
    @property
    def notation_forsyth_edwards(self) -> str:
        turn: str = "w" if self.turn == self.army_white.id else "b"

        enrroque_w: str = self.army_white.notation_FE_enrroque().upper()
        enrroque_b: str = self.army_black.notation_FE_enrroque().lower()

        enrroque_fen: str = enrroque_w + enrroque_b
        enrroque_fen = enrroque_fen if enrroque_fen != "--" else "-"

        coord_mov_passant: str = "-"

        return \
            f"{self.board.notation_forsyth_edwards} {turn} " +\
            f"{enrroque_fen} {coord_mov_passant} " +\
            f"{self.number_off_middle_movs} {self.number_off_movs}"


    # Funcions Starts
    def init(self) -> None:
        self.board.set_fichas(self.army_white.pieces)
        self.board.set_fichas(self.army_black.pieces)

        self.army_white.init_influence(self.board)
        self.army_black.init_influence(self.board)


    def restart_data(self):
        self.army_white.restart()
        self.army_black.restart()

        self.board.refresh_content()
        self.turn = self.army_white.id

        self.set_selected_ficha(EmptyChess())
    

    def restart_game(self):
        self.restart_data()
        self.init()
    

    # Turno Funcions
    def update_turno(self) -> None: 
        self.turn = self.get_enemy_army_for_class(self.turn).id


    def is_equals_turno(self, turno: str) -> str:
        return self.turn == turno


    # tablero Funcions
    def get_ficha(self, coord: Coord) -> EntityChess | None:
        return self.board.get_ficha(coord)


    def get_enemy_army_for_class(self, id: str) -> "Army":
        if id == self.army_white.id:
            return self.army_black
        
        elif id == self.army_black.id:
            return self.army_white


    def iteration(self, app: "ChessApp")-> None:
        army_next: "Army" = self.get_enemy_army_for_class(self.previous_piece.clase)

        army_next.update_influence_rey(self.board)
        army_next.delete_peon_passant(self.board, app)
        app.tablero.update_view_blocks()
        
        self.update_turno()

        app.update_view_turno(self.turn)

        self.number_off_movs += 1

        if not(isinstance(self.previous_piece, PieceChess)):
            return
        
        # Evento de finalizacion del programa
        if army_next.in_hacke_mate:
            app.exit_app()


    def set_selected_ficha(self, value: EntityChess) -> None:
        self.previous_piece = self.selected_piece
        self.selected_piece = value


    async def accion_game(self, group_blocks: "GroupBlocks") -> None:
        coord_end: Coord = self.selected_piece.coord

        if isinstance(self.previous_piece, EmptyChess):
            if not isinstance(self.selected_piece, PieceChess):
                return

            # Si es el turno de la ficha seleccionada, entonces renderiza los objetivos
            if self.is_equals_turno(self.selected_piece.clase):
                group_blocks.add_ultimate_coord_selected(coord_end)
                group_blocks.addRegisterBlock(self.selected_piece.get_coords_objetive())
                return 

        elif isinstance(self.previous_piece, PieceChess):
            group_blocks.clearRegisterBlock(self.previous_piece.get_coords_objetive())

            # Verifica que  la ficha previa tenga la misma clase que la ficha seleccionada
            if self.previous_piece.is_equals_class(self.selected_piece.clase):
                # Si la ficha previa es diferente de la ficha seleccionada, entonces renderiza
                if self.previous_piece != self.selected_piece:
                    group_blocks.deleted_ultimate_ultimate_coord_selected()
                    group_blocks.add_ultimate_coord_selected(coord_end)
                    group_blocks.addRegisterBlock(self.selected_piece.get_coords_objetive())
                    return
                
                group_blocks.deleted_ultimate_ultimate_coord_selected()
            
            # En caso de que la ficha previa sea de diferente clase que la ficha seleccionada,
            # se sabe que la ficha seleccionada puede ser un empty o una ficha enemiga,
            #  entonces realiza un movimiento
            else:
                movement_performed, is_objetive_enemy = self.previous_piece.make_mov(self.selected_piece, self.board)

                if movement_performed:
                    group_blocks.deleted_parcial_ultimate_coord_selected()
                    group_blocks.add_ultimate_coord_selected(coord_end)
                    group_blocks.update_view_block_off_coord(self.previous_piece.coord, self.selected_piece.coord)
                    app: "ChessApp" = group_blocks.app

                    if is_objetive_enemy:
                        app.save_view_kill(self.selected_piece)
                    
                    self.iteration(app) 
                
                else:
                    group_blocks.deleted_ultimate_ultimate_coord_selected()

        # Se setea la ficha seleccionada para que en una futura accion la previous_ficha siempre sea empty
        self.set_selected_ficha(EmptyChess())
