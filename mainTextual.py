from textual.app import App, on
from textual.widget import Widget
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button

from dataEstructures import Coord

from tablero import Tablero
from ficha import Ficha, EmptyChess, EntityChees
from army import  ArmyBlack, ArmyWhite, adminArmys
from app import ChessGame



def generatorSecuenceClassWhidget():
    x = 0; y = 0
    while True:
        if y % 8  == 0: x += 1
        yield "negro" if x % 2 == 0 else "blanco"
        x += 1; y += 1


SIZE_X: int = 8
SIZE_Y: int = 8

generatorClassWidget = generatorSecuenceClassWhidget()

tablero : Tablero = Tablero((SIZE_Y, SIZE_X))
game: ChessGame = ChessGame(tablero, adminArmys)


class Block(Widget):
    def __init__(self, classes: str , coord: Coord) -> None:
        super().__init__(classes=classes)
    
        self.coord: Coord = coord
        self.ficha: Ficha = game.getFicha(self.coord)
        self.view: Static = Static(self.ficha.char, classes = self.ficha.getClase()) 
        self._add_child(self.view) 


    def getCoord(self) -> Coord:
        return self.coord.value 
    
    # Funcion Update View
    def updateFicha(self) -> None:
        self.ficha = game.getFicha(self.coord)

        self.view.set_classes(self.ficha.getClase())
        self.view.update(self.ficha.char)

    # Event Click
    def on_click(self) -> None:
        game.setPreviousFicha(game.getSelectedFicha())
        game.setSelectedFicha(self.ficha)



class GroupBlocks(Vertical):
    def __init__(self, children: list[Block], app) -> None:
        super().__init__()

        self.front = app

        self.dicBlock: dict[tuple, Block] = {}
        for block in children:
            self.dicBlock[block.getCoord()] = block
            self._add_child(block)


    # Funcions UpdateViewBlock
    def updateViewBlock(self, *fichas: EntityChees) -> None:
        for ficha in fichas:
            self.dicBlock[ficha.getCoord().value].updateFicha()

    def updateViewBlocksGlobal(self):
        for block in self.dicBlock.values():
            block.updateFicha()


    # Funcions RegisterBlock
    def addRegisterBlock(self, ficha: Ficha) -> None:
        for coord, key in ficha.getCoordsObjetives():
            self.dicBlock[coord].add_class(key) 

    def clearRegisterBlock(self, ficha: Ficha) -> None:
        for coord, key in ficha.getCoordsObjetives():
            self.dicBlock[coord].remove_class(key) 


    def on_click(self) -> None:
        previousFicha: EntityChees = game.getPreviousFicha()
        actualFicha: EntityChees = game.getSelectedFicha() 

        if isinstance(previousFicha, Ficha):
            self.clearRegisterBlock(previousFicha)

        match (previousFicha, actualFicha):

            case (EmptyChess(), EmptyChess()):
                pass    

            case (EmptyChess(), Ficha()):
                if game.isEqualClassTurno(actualFicha.getClase()):
                    self.addRegisterBlock(actualFicha)
                    return

                game.setSelectedFicha(EmptyChess())

            case (Ficha(), EmptyChess()):
                if previousFicha.coordInObjetivo(actualFicha.getCoord(), "empty"):
                    game.tradeFicha(previousFicha, actualFicha)
                    self.updateViewBlock(previousFicha, actualFicha)

                    game.iteration(self.front)
                    

            case (Ficha(), Ficha()):
                if previousFicha == actualFicha:
                    game.setSelectedFicha(EmptyChess())
                    return

                if previousFicha.coordInObjetivo(actualFicha.getCoord(), "enemy"):
                    game.fusionFicha(previousFicha, actualFicha, self.front)
                    self.updateViewBlock(previousFicha, actualFicha)
                    game.setSelectedFicha(EmptyChess())

                    game.iteration(self.front)  
                    

                else:
                    if game.isEqualClassTurno(actualFicha.getClase()):
                        self.addRegisterBlock(actualFicha)
                        return
                    
                    game.setSelectedFicha(EmptyChess())



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
                            classes= next(generatorClassWidget),
                            coord = game.generatorView(),

                        ) for _ in range(SIZE_Y * SIZE_X)],

                    app = self
                )

                yield self.tablero

                self.killFichasRojas = Widget(classes= "fichas rojas")
                yield self.killFichasRojas

            with Widget(classes= "content"):
                yield Button("REINICIAR", id="btn-reiniciar")

            with Widget(classes= "content"):
                yield Button("SALIR", id="btn-salir")


    @on(Button.Pressed, "#btn-reiniciar")
    def reStartProgram(self):
        if isinstance(game.selectedFicha, Ficha):
            self.tablero.clearRegisterBlock(game.selectedFicha)

        game.reStartGame()

        self.tablero.updateViewBlocksGlobal()
        self.updateTurno(game.turno)
        self.clearKillFicha()


        
    @on(Button.Pressed, "#btn-salir")
    def exitProgram(self):
        self.exit()



    def updateTurno(self, gameTurno: str):
        turno:str
        
        if gameTurno == "armyWhite":
            turno = "azules" 
            self.turno.add_class("turno-azul") 
            self.turno.remove_class("turno-rojo")      

        else:
            turno = "rojos"
            self.turno.add_class("turno-rojo")
            self.turno.remove_class("turno-azul") 
        
        self.turno.update(f"Turno de los {turno}")


    def saveKillFicha(self, ficha: Ficha):
        if ficha.getClase() == "armyBlack":
            self.killFichasRojas.mount(Static(ficha.char))
    
        else:
            self.killFichasAzules.mount(Static(ficha.char))
    
    def clearKillFicha(self):
        self.killFichasAzules.remove_children(Static)
        self.killFichasRojas.remove_children(Static)
            
        
        

if __name__ == "__main__":
    app = ChessApp()
    app.run()



