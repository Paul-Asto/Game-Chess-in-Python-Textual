
class UCI_SintaxisError(Exception):

    def __init__(self):
        super().__init__("Texto en formato incompatible al formato UCI")



class IlegalMovChessError(Exception):
    
    def __init__(self, arg: str):
        super().__init__(arg)


class ChessGameNotRunningError(Exception):
    
    def __init__(self):
        super().__init__("El juego no ha iniciado o a terminado, no se pueden realizar jugadas, reiniciar el juego")