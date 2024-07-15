from decimal import Decimal


def portfolio_cost(filename):
    total_cost = Decimal(0)
    with open(filename) as f:
        while values := f.readline().split():
            # Number of shares times prices
            try:
                total_cost += int(values[1]) * Decimal(values[2])
            except ValueError as e:
                print(f"Could not parse line: {values}")
                print(f"Reason: {e}")
    return total_cost


if __name__ == "__main__":
    print("Total cost: " + str(portfolio_cost("Data/portfolio.dat")))
