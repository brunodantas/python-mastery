from collections import Counter, namedtuple
from collections.abc import Sequence
import csv


RowTuple = namedtuple("RowTuple", ["route", "date", "daytype", "rides"])


class RowClass:
    __slots__ = ["route", "date", "daytype", "rides"]

    def __init__(self, route, date, daytype, rides) -> None:
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


class RideData(Sequence):
    def __init__(self):
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self) -> int:
        return len(self.routes)

    def __getitem__(self, index):
        if isinstance(index, int):
            return {
                "route": self.routes[index],
                "date": self.dates[index],
                "daytype": self.daytypes[index],
                "rides": self.numrides[index],
            }
        elif isinstance(index, slice):
            ride_data = RideData()
            for i in range(index.start, index.stop, index.step or 1):
                ride_data.append(self[i])
            return ride_data

    def append(self, d):
        self.routes.append(d["route"])
        self.dates.append(d["date"])
        self.daytypes.append(d["daytype"])
        self.numrides.append(d["rides"])


def read_rides_as_tuples(filename):
    """Read the bus ride data as a list of tuples"""
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        records = [(row[0], row[1], row[2], int(row[3])) for row in rows]
    return records


def read_rides_as_dicts(filename):
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        records = [
            {
                k: v
                for k, v in zip(
                    ("route", "date", "daytype", "rides"), (v for v in row[:4])
                )
            }
            for row in rows
        ]
    return records


def read_rides_as_ridedata(filename):
    records = RideData()  # <--- CHANGE THIS
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {"route": route, "date": date, "daytype": daytype, "rides": rides}
            records.append(record)
    return records


def read_rides_as_namedtuples(filename):
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        records = [RowTuple(row[0], row[1], row[2], int(row[3])) for row in rows]
    return records


def read_rides_as_classes_slots(filename):
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        records = [RowClass(row[0], row[1], row[2], int(row[3])) for row in rows]
    return records


def read_rides_as_columns(filename):
    """
    Read the bus ride data into 4 lists, representing columns
    """
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)


def count_routes_chicago(filename="Data/ctabus.csv", fn=read_rides_as_dicts):
    rows = fn(filename)
    return len({row["route"] for row in rows})


def count_passengers(
    filename="Data/ctabus.csv", route="22", date="02/02/2011", fn=read_rides_as_dicts
):
    rows = fn(filename)
    return sum(
        int(row["rides"])
        for row in rows
        if row["date"] == date and row["route"] == route
    )


def count_route_rides(filename="Data/ctabus.csv", fn=read_rides_as_dicts):
    rows = fn(filename)
    counter = Counter()
    for row in rows:
        counter[row["route"]] += int(row["rides"])
    return counter


def get_top_ten_year_increase(filename="Data/ctabus.csv", fn=read_rides_as_dicts):
    rows = fn(filename)
    ridership_2001, ridership_2011 = Counter(), Counter()
    for row in rows:
        if "2001" in row["date"]:
            ridership_2001[row["route"]] += int(row["rides"])
        elif "2011" in row["date"]:
            ridership_2011[row["route"]] += int(row["rides"])
    return (ridership_2011 - ridership_2001).most_common(5)


if __name__ == "__main__":
    import tracemalloc

    for name, funct in (
        ("Tuples", read_rides_as_tuples),
        ("Dicts", read_rides_as_dicts),
        ("NamedTuples", read_rides_as_namedtuples),
        ("Classes w/ slots", read_rides_as_classes_slots),
        ("Columns", read_rides_as_columns),
        ("RideData", read_rides_as_ridedata),
    ):
        tracemalloc.start()
        rows = funct("Data/ctabus.csv")
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{name} memory use: Current {current}, Peak {peak}")
        # Tuples memory use: Current 123687990, Peak 123718640
        # Dicts memory use: Current 203661924, Peak 203547391
        # NamedTuples memory use: Current 128324433, Peak 128339432
        # Classes w/ slots memory use: Current 119069436, Peak 119098520
        # Columns memory use: Current 96169970, Peak 96199072
        # RideData memory use: Current 96169158, Peak 96199672
