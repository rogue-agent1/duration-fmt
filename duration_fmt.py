#!/usr/bin/env python3
"""Duration parser and formatter."""
import re

def parse_duration(s):
    s = s.strip()
    # ISO 8601: P[nY][nM][nD][T[nH][nM][nS]]
    m = re.match(r'P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$', s)
    if m:
        years, months, days = int(m.group(1) or 0), int(m.group(2) or 0), int(m.group(3) or 0)
        hours, mins, secs = int(m.group(4) or 0), int(m.group(5) or 0), float(m.group(6) or 0)
        total = ((years*365 + months*30 + days) * 86400 + hours*3600 + mins*60 + secs)
        return total
    # Human: 1h30m, 2d, 45s, etc.
    total = 0
    for val, unit in re.findall(r'(\d+(?:\.\d+)?)\s*(ms|d|h|m|s)', s.lower()):
        val = float(val)
        if unit == 'd': total += val * 86400
        elif unit == 'h': total += val * 3600
        elif unit == 'm': total += val * 60
        elif unit == 's': total += val
        elif unit == 'ms': total += val / 1000
    return total

def format_duration(seconds, style="human"):
    if style == "iso":
        parts = []
        d = int(seconds // 86400); seconds %= 86400
        h = int(seconds // 3600); seconds %= 3600
        m = int(seconds // 60); s = seconds % 60
        date_part = f"{'%dD' % d if d else ''}"
        time_part = f"{'%dH' % h if h else ''}{'%dM' % m if m else ''}{'%gS' % s if s else ''}"
        return f"P{date_part}{'T' + time_part if time_part else ''}" or "PT0S"
    # Human
    parts = []
    d = int(seconds // 86400); seconds %= 86400
    h = int(seconds // 3600); seconds %= 3600
    m = int(seconds // 60); s = int(seconds % 60)
    if d: parts.append(f"{d}d")
    if h: parts.append(f"{h}h")
    if m: parts.append(f"{m}m")
    if s or not parts: parts.append(f"{s}s")
    return " ".join(parts)

if __name__ == "__main__":
    import sys
    s = " ".join(sys.argv[1:]) or "1h30m"
    secs = parse_duration(s)
    print(f"Parsed: {secs}s = {format_duration(secs)}")

def test():
    assert parse_duration("PT1H30M") == 5400
    assert parse_duration("P1D") == 86400
    assert parse_duration("P1DT2H3M4S") == 93784
    assert parse_duration("1h30m") == 5400
    assert parse_duration("2d 5h") == 2*86400 + 5*3600
    assert parse_duration("45s") == 45
    assert parse_duration("500ms") == 0.5
    assert format_duration(3661) == "1h 1m 1s"
    assert format_duration(86400) == "1d"
    assert format_duration(0) == "0s"
    iso = format_duration(3661, "iso")
    assert "1H" in iso and "1M" in iso and "1S" in iso
    print("  duration_fmt: ALL TESTS PASSED")
