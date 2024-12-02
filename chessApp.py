from textual.app import App, on
from textual.widget import Widget
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button


from coord import Coord
from chessGame import chess_game

from piece import PieceChess



def secuence_class_widget():
    x = 0; y = 0
    while True:
        if y % 8  == 0: x += 1
        yield "negro" if x % 2 == 0 else "blanco"
        x += 1; y += 1

generator_class_widget = secuence_class_widget()


def secuence_coord_widget():
    for y in range(8):
        for x in range(8):
            yield Coord(y, x)

generator_coord_widget = secuence_coord_widget()



class Block(Widget):
    def __init__(self, classes: str , coord: Coord) -> None:
        super().__init__(classes=classes)
    
        self.coord: Coord = coord
        self.ficha: PieceChess = chess_game.get_ficha(self.coord)
        
        self.view: Static = Static(self.ficha.char, classes = self.ficha.clase)   
        self._add_child(self.view) 
    
    # Funcion Update View
    def update_ficha(self) -> None:
        self.ficha = chess_game.get_ficha(self.coord)

        self.view.set_classes(self.ficha.clase)
        self.view.update(self.ficha.char)

    # Event Click
    def on_click(self) -> None:
        chess_game.set_selected_ficha(self.ficha)




class GroupBlocks(Vertical):
    def __init__(self, children: list[Block]) -> None:
        super().__init__()
    
        self.dict_blocks: dict[Coord, Block] = {}

        for block in children:
            self.dict_blocks[block.coord] = block
            self._add_child(block)


    # Funcions UpdateViewBlock
    def update_view_block_off_coord(self, *list_coord: list[Coord]) -> None:
        for coord in list_coord:
            self.dict_blocks[coord].update_ficha()

    def update_view_blocks(self):
        for block in self.dict_blocks.values():
            block.update_ficha()

    
    # Funcions RegisterBlock
    def addRegisterBlock(self, list_data: list[tuple, str]) -> None:
        for coord, key in list_data:
            self.dict_blocks[coord].add_class(key) 

    def clearRegisterBlock(self, list_data: list[tuple, str]) -> None:
        for coord, key in list_data:
            self.dict_blocks[coord].remove_class(key) 


    def on_click(self) -> None:
        chess_game.accion_game(self)



class ChessApp(App):
    CSS_PATH = "style.tcss"

    def compose(self):
        with Vertical():
            with Widget(classes= "content"):
                yield Static("AJEDREZ vs IA")

            with Widget(classes= "content"):
                self.turno = Static("Turno de los azules", classes="turno-azul")
                yield self.turno

            with Horizontal():
                self.killFichasAzules = Widget(classes= "fichas azules")
                yield self.killFichasAzules

                self.tablero = GroupBlocks(
                    children = [
                        Block(
                            classes= next(generator_class_widget),
                            coord = next(generator_coord_widget),
                        ) for _ in range(8 * 8)]
                )

                yield self.tablero

                self.killFichasRojas = Widget(classes= "fichas rojas")
                yield self.killFichasRojas

            with Widget(classes= "content"):
                yield Button("REINICIAR", id="btn-reiniciar")

            with Widget(classes= "content"):
                yield Button("SALIR", id="btn-salir")


    @on(Button.Pressed, "#btn-reiniciar")
    def restart_app(self):
        if isinstance(chess_game.selected_ficha, PieceChess):
            self.tablero.clearRegisterBlock(chess_game.selected_ficha.get_coords_objetive())

        chess_game.restart_game()

        self.tablero.update_view_blocks()
        self.update_view_turno(chess_game.turno)
        self.clear_view_kill()

        
    @on(Button.Pressed, "#btn-salir")
    def exit_app(self):
        self.exit()


    def update_view_turno(self, turno: str):
        turno:str
        
        if turno == "armyWhite":
            turno = "azules" 
            self.turno.add_class("turno-azul") 
            self.turno.remove_class("turno-rojo")      

        else:
            turno = "rojos"
            self.turno.add_class("turno-rojo")
            self.turno.remove_class("turno-azul") 
        
        self.turno.update(f"Turno de los {turno}")


    def save_view_kill(self, ficha: PieceChess):
        if ficha.clase == "armyBlack":
            self.killFichasRojas.mount(Static(ficha.char))
    
        else:
            self.killFichasAzules.mount(Static(ficha.char))
    
    def clear_view_kill(self):
        self.killFichasAzules.remove_children(Static)
        self.killFichasRojas.remove_children(Static)
            

