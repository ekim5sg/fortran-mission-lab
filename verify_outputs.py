"""Validate actual program output, allowing Fortran's field spacing and decimal point."""
from decimal import Decimal
from pathlib import Path
import re
import sys

expected = [(day, Decimal(24000 * 24 * day)) for day in range(1, 6)]
for filename in sys.argv[1:]:
    text = Path(filename).read_text()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines or lines[0] != 'MISSION DISTANCE REPORT':
        raise SystemExit(f'{filename}: missing mission header')
    actual = []
    for line in lines[1:]:
        match = re.fullmatch(r'Day\s+(\d+):\s+([\d.]+)\s+km', line)
        if not match:
            raise SystemExit(f'{filename}: unexpected report line: {line!r}')
        actual.append((int(match[1]), Decimal(match[2])))
    if actual != expected:
        raise SystemExit(f'{filename}: distance mismatch: {actual!r}')
    print(f'PASS: {filename}: all five distances match; day 5 = 2,880,000 km')
if len(sys.argv) != 3:
    raise SystemExit('Expected exactly two output files')
