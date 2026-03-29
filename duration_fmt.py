#!/usr/bin/env python3
"""duration_fmt - Parse and format human-readable durations (1h30m, 2d5h, etc)."""
import sys, re

UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

def parse_duration(s):
    total = 0
    for match in re.finditer(r"(\d+\.?\d*)\s*([smhdw])", s.lower()):
        val, unit = float(match.group(1)), match.group(2)
        total += val * UNITS[unit]
    if total == 0:
        try: return float(s)
        except: pass
    return int(total) if total == int(total) else total

def format_duration(seconds, short=True):
    if seconds < 0: return "-" + format_duration(-seconds, short)
    parts = []
    for unit, secs in [("w",604800),("d",86400),("h",3600),("m",60),("s",1)]:
        if seconds >= secs:
            count = int(seconds // secs)
            seconds -= count * secs
            if short:
                parts.append(f"{count}{unit}")
            else:
                name = {"w":"week","d":"day","h":"hour","m":"minute","s":"second"}[unit]
                parts.append(f"{count} {name}{'s' if count!=1 else ''}")
    return " ".join(parts) if parts else ("0s" if short else "0 seconds")

def test():
    assert parse_duration("1h30m") == 5400
    assert parse_duration("2d") == 172800
    assert parse_duration("1w2d3h") == 788400
    assert parse_duration("90s") == 90
    assert format_duration(5400) == "1h 30m"
    assert format_duration(90) == "1m 30s"
    assert format_duration(0) == "0s"
    assert format_duration(86400) == "1d"
    assert "day" in format_duration(86400, short=False)
    assert format_duration(3661) == "1h 1m 1s"
    print("duration_fmt: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: duration_fmt.py --test")
