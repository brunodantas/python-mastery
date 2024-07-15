from collections.abc import Sequence
import csv
from sys import intern
from typing import Dict


def read_csv_as_dicts(filename, coltypes):
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        return [{k: f(v) for k, v, f in zip(headers, row, coltypes)} for row in rows]


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


if __name__ == "__main__":
    import tracemalloc

    tracemalloc.start()
    read_csv_as_dicts("Data/ctabus.csv", (intern, intern, str, int))
    print(tracemalloc.get_traced_memory())
    # (14699, 126713964)
    tracemalloc.stop()
    tracemalloc.start()
    read_csv_as_columns("Data/ctabus.csv", (str, str, str, int))
    print(tracemalloc.get_traced_memory())
    # (675, 96199800)
    tracemalloc.stop()
    tracemalloc.start()
    read_csv_as_columns("Data/ctabus.csv", (intern, intern, str, int))
    print(tracemalloc.get_traced_memory())
    # (1922483, 36431988)
