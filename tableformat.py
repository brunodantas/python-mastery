from abc import ABC, abstractmethod
import sys


class ColumnFormatMixin:
    formats = []

    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)


class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError()

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(" ".join("%10s" % h for h in headers))
        print(("-" * 10 + " ") * len(headers))

    def row(self, rowdata):
        print(" ".join("%10s" % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join(headers))

    def row(self, rowdata):
        print(",".join(str(value) for value in rowdata))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print("<tr>  " + " ".join(f"<th>{value}</th>" for value in headers) + " </tr>")

    def row(self, rowdata):
        print("<tr>  " + " ".join(f"<td>{value}</td>" for value in rowdata) + " </tr>")


def create_formatter(format="text", column_formats=None, upper_headers=False):
    cls = {
        "text": TextTableFormatter,
        "csv": CSVTableFormatter,
        "html": HTMLTableFormatter,
    }[format]
    mixins = ([ColumnFormatMixin] if column_formats else []) + (
        [UpperHeadersMixin] if upper_headers else []
    )

    class NewFormatter(*mixins, cls):
        formats = column_formats

    return NewFormatter()


class redirect_stdout:
    def __init__(self, out_file):
        self.out_file = out_file

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self.out_file
        return self.out_file

    def __exit__(self, ty, val, tb):
        sys.stdout = self.stdout


def print_table(objects, attr_names, formatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError("Expected a TableFormatter")
    formatter.headings(attr_names)
    for r in objects:
        rowdata = [getattr(r, attr_name) for attr_name in attr_names]
        formatter.row(rowdata)

    # header_fmt = len(attr_names) * "%10s "
    # print(header_fmt % attr_names)
    # print(("-" * 10 + " ") * len(attr_names))
    # row_fmt = "%10s " * len(attr_names)
    # for obj in objects:
    #     print(row_fmt % tuple(getattr(obj, name) for name in attr_names))
