from collections import defaultdict, Counter
from dataclasses import dataclass

class Dice:
    def distribution():
        raise NotImplementedError()


@dataclass(frozen=True)
class D(Dice):
    n: int

    def distribution(self):
        return {i: 1/self.n for i in range(1, self.n + 1)}
    
    def __rmul__(self, other):
        assert type(other) is int
        return LinearD([self] * other)
    
    def __add__(self, other):
        if type(other) is int:
            return LinearD([self], other)
        if type(other) is D:
            return LinearD([self, other])
        if type(other) is LinearD:
            return LinearD([self, *other.dice], other.offset)
        raise TypeError(f'add not implemented for {type(self)} + {type(other)}')
    
    def __str__(self) -> str:
        return f'd{self.n}'


@dataclass(frozen=True)
class LinearD(Dice):
    dice: list[Dice]
    offset: int = 0

    def distribution(self):
        out = defaultdict(lambda: 0)
        for d in self.dice:
            if not out:
                out = d.distribution()
                continue
            
            new = defaultdict(lambda: 0)
            for x,y in d.distribution().items():
                for a,b in out.items():
                    new[x + a] += y * b
            out = new
        return {(k + self.offset): v for k,v in out.items()}
    
    def __add__(self, other):
        if type(other) is int:
            return LinearD(self.dice, self.offset + other)
        if type(other) is D:
            return LinearD([*self.dice, other], self.offset)
        if type(other) is LinearD:
            return LinearD([*self.dice, *other.dice], self.offset + other.offset)
        raise TypeError(f'add not implemented for {type(self)} + {type(other)}')

    def __str__(self) -> str:
        counted = Counter(self.dice).items()
        base = ' + '.join(f'{n}{d}' if n != 1 else str(d) for d, n in counted)
        return f'{base} + {self.offset}' if self.offset else base




def __main__():
    print(D(6))
    print(D(6).distribution())

    print((3 * D(4)).distribution())


if __name__ == '__main__':
    __main__()
