from abc import ABC, abstractmethod
from collections.abc import Sequence
import csv
from sys import intern
from typing import Dict


class CSVParser(ABC):
    def parse(self, filename):
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            return [self.make_record(headers, row) for row in rows]

    @abstractmethod
    def make_record(self, headers, row):
        pass


class DictCSVParser(CSVParser):
    def __init__(self, types) -> None:
        self.types = types

    def make_record(self, headers, row):
        return {name: f(v) for name, f, v in zip(headers, self.types, row)}


class InstanceCSVParser(CSVParser):
    def __init__(self, cls) -> None:
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)


class DataCollection(Sequence):
    def __init__(self, headers, coltypes) -> None:
        self.headers = headers
        self.coltypes = coltypes
        self.columns = [[] for _ in range(len(headers))]

    def __len__(self) -> int:
        return len(self.columns[0])

    def __getitem__(self, index) -> Dict:
        return {
            k: f(v)
            for k, f, v in zip(
                self.headers, self.coltypes, (col[index] for col in self.columns)
            )
        }

    def append(self, item) -> None:
        for i, (f, e) in enumerate(zip(self.coltypes, item)):
            self.columns[i].append(f(e))


def read_csv_as_columns(filename, coltypes):
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        data = DataCollection(headers, coltypes)
        for row in rows:
            data.append(row)
    return data


def read_csv_as_dicts(filename, coltypes):
    parser = DictCSVParser(coltypes)
    return parser.parse(filename)


def read_csv_as_instances(filename, cls):
    """Read a CSV file into a list of instances"""
    parser = InstanceCSVParser(cls)
    return parser.parse(filename)


if __name__ == "__main__":
    import tracemalloc

    tracemalloc.start()
    d = read_csv_as_dicts("Data/ctabus.csv", (intern, intern, str, int))
    print(tracemalloc.get_traced_memory())
    # (126682845, 126713516)
    tracemalloc.stop()
    tracemalloc.start()
    d = read_csv_as_columns("Data/ctabus.csv", (str, str, str, int))
    print(tracemalloc.get_traced_memory())
    # (96169695, 96199984)
    tracemalloc.stop()
    tracemalloc.start()
    d = read_csv_as_columns("Data/ctabus.csv", (intern, intern, str, int))
    print(tracemalloc.get_traced_memory())
    # (36401949, 36432340)
