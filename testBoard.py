
class Cycle:
    def __init__(self, start: int, end: int, index_default: int = 0, reverse: bool = False, increment: int = 1) -> None:
        self.increment: int = increment
        self.reverse: bool = reverse
        self.index_start: int = start
        self.index_end: int = end
        self.index_max: int = self.index_end if reverse == False else self.index_start
        self.index: int = index_default


    def iteration(self) -> None:
        new_value: int = self.index + self.increment

        if self.reverse:
            if new_value < self.index_start:
                new_value = self.index_end

        else:
            if new_value > self.index_end:
                new_value = self.index_start

        self.index = new_value


class Alien:

    def __init__(self, value_initial: int = 8) -> None:
        self.life_cycle = Cycle(0, 6, value_initial, True, -1)

    def growl(self) -> None:
        self.life_cycle.iteration()

    def reproduced(self) -> bool:
        return self.value == 0
    
    @property
    def value(self) -> int:
        return self.life_cycle.index


class Poblacion:

    def __init__(self, *initil_aliens: Alien) -> None:
        self.poblacion: list[Alien] = list(initil_aliens)
        self.next_generation: list[Alien] = []

    
    def iteration(self) -> None:
        poblacion_analize: list[Alien] = self.poblacion.copy()
        self.poblacion += self.next_generation
        self.next_generation.clear()

        for alien in poblacion_analize:
            alien.growl()

            if alien.reproduced():
                self.add_alien()


    def add_alien(self) -> None:
        self.next_generation.append(Alien())

    def get_data_poblacion(self) -> list[int]:
        return [alien.value for alien in self.poblacion]
    

entrada: list[int] = [3, 4, 3, 1, 2]
aliens: list[Alien] = [Alien(value) for value in entrada]
n_dias: int = 81


poblacion = Poblacion(*aliens)


for n_dia in range(n_dias):
    data = poblacion.get_data_poblacion()
    print(f"Dia {n_dia}: N Aliens: {len(data)} Poblacion: {", ".join([str(value) for value in data])}")
    poblacion.iteration()