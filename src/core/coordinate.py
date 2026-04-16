from typing import Iterator



class CardinalPair:
    def __init__(self, y: int, x: int) -> None:
        self.y: int = y
        self.x: int = x
        
        self.value: tuple[int, int] = (y, x)
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def __eq__(self, other: object) -> bool:
        if  isinstance(other, CardinalPair):
            return self.value == other.value
        
        else: return False
    
    def __iter__(self) -> Iterator[int]:
        return iter(self.value)



class Coord(CardinalPair):
    def __init__(self, y: int, x: int) -> None:
        super().__init__(y, x)
    
    def __sub__(self, other: object) -> "Coord":
        if not isinstance(other, CardinalPair):
            raise Exception("Error en la suma de coords")
        
        return Coord(self.y - other.y, self.x - other.x)
    
    
    def __add__(self, other: object) -> "Coord":
        if not isinstance(other, CardinalPair):
            raise Exception("Error en la resta de coords")
        
        return Coord(self.y + other.y, self.x + other.x)
    
    
    def move(self, mov: tuple[int, int]) -> "Coord":
        return Coord(self.y + mov[0], self.x + mov[1])
    
    
    def copy(self) -> "Coord":
        return Coord(self.y, self.x)
