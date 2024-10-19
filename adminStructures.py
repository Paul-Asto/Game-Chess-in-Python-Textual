from dataEstructures import Coord, Mov, Direction, Distance
from typing import Callable

# CLASS ADMIN STRUCTURES
class Guide:
    Top: Direction = Direction(-1, 0)
    Bot: Direction = Direction(1, 0)
    Left: Direction = Direction(0, -1)
    Right: Direction = Direction(0, 1)

    TopLeft: Direction = Direction(-1, -1)
    TopRight: Direction = Direction(-1, 1)
    BotLeft: Direction = Direction(1, -1)
    BotRight: Direction = Direction(1, 1)

    NoneDirection: Direction = Direction(0, 0)

    listDirectionSimple: list[Direction] = [Top, Bot, Left, Right]
    listDirectionComplex: list[Direction] = [TopLeft, TopRight,BotLeft, BotRight]
    listDirections: list[Direction] =  [Top, Bot, Left, Right,TopLeft, TopRight,BotLeft, BotRight]

    @classmethod
    def GetDirectionOffDistance(cls, distance: Distance):
        modifyEje: Callable[[int], int] = lambda eje: 0 if eje == 0 else 1 if  eje > 0 else -1
        y, x = distance

        return Direction(modifyEje(y), modifyEje(x))
    
    @classmethod
    def GetListDireccionSimple(cls):
        return cls.listDirectionSimple.copy()
    
    @classmethod
    def GetListDireccionComplex(cls):
        return cls.listDirectionComplex.copy()

class Movement:   

    Top: Mov = Mov(-1, 0)
    Bot: Mov = Mov(1, 0)
    Left: Mov = Mov(0, -1)
    Right: Mov = Mov(0, 1)

    Top_Left: Mov = Mov(-1, 1)
    Bot_Left: Mov = Mov(1, 1)
    Top_Right: Mov = Mov(-1, -1)
    Bot_Right: Mov = Mov(1, -1)

    listMov_Rect: list[Mov] = [Top, Bot, Left, Right]
    listMov_Diagonal: list[Mov] = [Top_Left, Bot_Left, Top_Right, Bot_Right]
    listMov_Total: list[Mov] = listMov_Rect + listMov_Diagonal



    @classmethod
    def GetListMovs_Rect(cls) -> list[Mov]:
        return cls.listMov_Rect.copy()
    
    @classmethod
    def GetListMovs_Diagonal(cls) -> list[Mov]:
        return cls.listMov_Diagonal.copy()
    
    @classmethod
    def GetListMovs_Total(cls) -> list[Mov]:
        return cls.listMov_Total .copy()
    
