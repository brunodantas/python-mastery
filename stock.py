import csv


class Stock:
    __slots__ = ("name", "_shares", "_price")
    _types = (str, int, float)

    def __init__(self, name, shares, price) -> None:
        self.name = name
        self._shares = shares
        self._price = price

    def __repr__(self) -> str:
        return f"Stock({self.name}, {self.shares}, {self.price})"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Stock) and (self.name, self.shares, self.price) == (
            value.name,
            value.shares,
            value.price,
        )

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, self._types[1]):
            raise TypeError(f"Expected a {self._types[1]}")
        elif value < 0:
            raise ValueError("shares must be >= 0")
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f"Expected a {self._types[2]}")
        elif value < 0:
            raise ValueError("price must be >= 0")
        self._price = value

    @classmethod
    def from_row(cls, row):
        values = [f(val) for f, val in zip(cls._types, row)]
        return cls(*values)

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


def read_portfolio(filename="Data/portfolio.csv"):
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        return [Stock.from_row(row) for row in rows]


def print_portfolio(portfolio):
    print("%10s %10s %10s" % ("name", "shares", "price"))
    print(("-" * 10 + " ") * 3)
    for stock in portfolio:
        print("%10s %10d %10.2f" % (stock.name, stock.shares, stock.price))
