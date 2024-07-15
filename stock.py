class Stock:
    def __init__(self, name, shares, price) -> None:
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price
