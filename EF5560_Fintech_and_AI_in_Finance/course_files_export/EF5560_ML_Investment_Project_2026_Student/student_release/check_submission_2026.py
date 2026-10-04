"""Check a weight CSV. Uses only Python's standard library.

python check_submission_2026.py EF5560_12345678.csv
"""
import argparse
import csv
import math
from pathlib import Path

TOLERANCE = 1e-6
WEIGHT_CAP = 0.10
TEMPLATE = Path(__file__).resolve().with_name("submission_template_2026.csv")


def read_rows(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.reader(stream))


def load_and_validate(path, template_path=TEMPLATE):
    expected, actual = read_rows(template_path), read_rows(path)
    if not actual or actual[0] != expected[0]:
        raise ValueError("Column names and order must match the official template.")
    if len(actual) != len(expected):
        raise ValueError(f"Expected {len(expected) - 1} weekly rows.")
    weights = []
    for line, (row, reference) in enumerate(zip(actual[1:], expected[1:]), 2):
        if len(row) != len(expected[0]):
            raise ValueError(f"Line {line}: wrong number of columns.")
        if row[0] != reference[0]:
            raise ValueError(f"Line {line}: date or date order differs from the template.")
        try:
            values = [float(value) for value in row[1:]]
        except ValueError:
            raise ValueError(f"Line {line}: missing or nonnumeric weight.") from None
        if not all(math.isfinite(value) for value in values):
            raise ValueError(f"Line {line}: weights must be finite.")
        if min(values) < -TOLERANCE or max(values) > WEIGHT_CAP + TOLERANCE:
            raise ValueError(f"Line {line}: weights must be between 0 and 0.10.")
        if abs(math.fsum(values) - 1) > TOLERANCE:
            raise ValueError(f"Line {line}: weights do not sum to 1 within 1e-6.")
        weights.append(values)
    return expected[0], [row[0] for row in actual[1:]], weights


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path)
    args = parser.parse_args()
    try:
        header, dates, weights = load_and_validate(args.submission)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Invalid submission: {error}\n")
    print(f"Valid file: {len(dates)} dates, {len(header) - 1} stocks; all weight constraints satisfied.")
    print("This check does not evaluate investment performance.")


if __name__ == "__main__":
    main()
