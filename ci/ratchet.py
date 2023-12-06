import sys
import re
from typing import Dict, Tuple, Optional, List, TextIO

report: Dict[str, List[Optional[float]]] = {}

extract_line = re.compile(
    r"^\|\s+(?P<module>[^\s]*)\s+\|\s+(?P<percent>\d\d?\.\d\d)% imprecise \|"
)


def load(idx: int, fp: TextIO):
    global report
    for line in fp:
        if r := extract_line.match(line):
            module: str = r.group("module")
            percent: float = float(r.group("percent"))

            if module not in report:
                report[module] = [None, None]
            report[module][idx] = percent


with open(f"{sys.argv[1]}/base/index.txt") as fp:
    load(0, fp)
with open(f"{sys.argv[1]}/head/index.txt") as fp:
    load(1, fp)

good: List[Tuple[str, float, float]] = []
bad: List[Tuple[str, float, float]] = []

for module, values in report.items():
    base: Optional[float] = values[0]
    head: Optional[float] = values[1]

    if base is not None and head is not None:
        if base > head:
            good.append((module, base, head))
        elif base < head:
            bad.append((module, base, head))

if bad:
    print("Imprecision went up:")
    for module, base, head in bad:
        print(f"{module}:\t\t{base} -> {head}")

if good:
    print("Imprecision went down:")
    for module, base, head in good:
        print(f"{module}:\t\t{base} -> {head}")

if bad:
    sys.exit(1)
