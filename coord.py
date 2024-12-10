class AbstractCoord:
    def __init__(self, y: int, x: int) -> None:
        self.y = y
        self.x = x

        self.value: tuple[int, int] = (y, x)

    def __str__(self) -> tuple:
        return self.value
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other: "AbstractCoord") -> bool:
        if  issubclass(type(other), AbstractCoord):
            return self.value == other.value
        
        else: return False

    def __iter__(self):
        return iter(self.value)



class Coord(AbstractCoord):
    def __init__(self, y: int, x: int) -> None:
        super().__init__(y, x)

    def __sub__(self, other):
        if not issubclass(type(other), AbstractCoord):
            return NotImplemented
        
        return Coord(self.y - other.y, self.x - other.x)
    
    def __add__(self, other):
        if not issubclass(type(other), AbstractCoord):
            return NotImplemented
        
        return Coord(self.y + other.y, self.x + other.x)
    
    def indexMax(self):
        y, x = self.value
        result: int = None

        if y > x:
            result = 0
        
        elif y < x:
            result = 1
        
        return result

    #Funciones Abs
    def absData(self):
        return (abs(self.y), abs(self.x))
    
    def GetAbsoluteCoord(self):
        absY, absX = self.absData()
        return Coord(absY, absX)
    
    def Absolute(self):
        absY, absX = self.absData()
        self.value = (absY, absX)

    def copy(self):
        return Coord(self.y, self.x)