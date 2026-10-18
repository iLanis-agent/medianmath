#!/usr/bin/env python3
# Median Math oracle - mirrors engine.js.
import json, math

def _list(lst):
    if not isinstance(lst, list) or len(lst) < 1 or len(lst) > 30:
        raise ValueError("need 1 to 30 numbers")
    out = []
    for x in lst:
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0 or x > 1000000:
            raise ValueError("each number must be between 0 and 1000000")
        out.append(math.floor(x * 100 + 0.5))
    return sorted(out)

def _fmt(h):
    whole, frac = divmod(h, 100)
    if frac == 0:
        return str(whole)
    f = f"{frac:02d}"
    if f[1] == "0":
        f = f[0]
    return f"{whole}.{f}"

def _div(n, d):
    return (2 * n + d) // (2 * d)

def _mean(s):
    return _div(sum(s), len(s))

def _median(s):
    n = len(s); m = n // 2
    if n % 2 == 1:
        return s[m]
    return (s[m - 1] + s[m] + 1) // 2

def _modes(s):
    best = 1; vals = []; i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        c = j - i
        if c > best:
            best = c; vals = [s[i]]
        elif c == best and c > 1:
            vals.append(s[i])
        i = j
    return best, vals

def _and(vals):
    t = [_fmt(v) for v in vals]
    if len(t) == 1:
        return t[0]
    return ", ".join(t[:-1]) + " and " + t[-1]

def center_truth(lst):
    s = _list(lst)
    count, vals = _modes(s)
    if len(vals) == 0:
        mode = "no mode, since no value repeats"
    elif len(vals) == 1:
        mode = f"mode {_and(vals)} ({count} times)"
    else:
        mode = f"modes {_and(vals)} ({count} times each)"
    return f"Mean {_fmt(_mean(s))}, median {_fmt(_median(s))}, {mode}."

def spread_truth(lst):
    s = _list(lst)
    n = len(s); tot = sum(s)
    d = sum(abs(n * x - tot) for x in s)
    dev = _div(d, n * n)
    return f"Range {_fmt(s[-1] - s[0])} (from {_fmt(s[0])} to {_fmt(s[-1])}). On average the numbers sit {_fmt(dev)} from the mean."

def extra_truth(lst, extra):
    s = _list(lst)
    if isinstance(extra, bool) or not isinstance(extra, (int, float)) or not math.isfinite(extra) or extra < 0 or extra > 1000000:
        raise ValueError("extra number must be between 0 and 1000000")
    e = math.floor(extra * 100 + 0.5)
    t = sorted(s + [e])
    m0, m1, d0, d1 = _mean(s), _mean(t), _median(s), _median(t)
    a = f"leaves the mean at {_fmt(m0)}" if m0 == m1 else f"moves the mean from {_fmt(m0)} to {_fmt(m1)}"
    b = f"leaves the median at {_fmt(d0)}" if d0 == d1 else f"moves the median from {_fmt(d0)} to {_fmt(d1)}"
    return f"Adding {_fmt(e)} {a} and {b}."

FNS = {"centerTruth": center_truth, "spreadTruth": spread_truth, "extraTruth": extra_truth}

CASES = [
    ("centerTruth", [[3, 5, 3, 9, 1]]), ("centerTruth", [[1, 2, 3, 4]]), ("centerTruth", [[5]]), ("centerTruth", [[2, 2, 5, 5, 9]]),
    ("centerTruth", [[1, 1, 2, 2, 3, 3]]), ("centerTruth", [[4, 4, 4]]), ("centerTruth", [[1, 2, 3]]), ("centerTruth", [[0.5, 0.5, 1]]),
    ("centerTruth", [[1, 2]]), ("centerTruth", [[0.01, 0.02]]), ("centerTruth", [[10, 20, 20, 30, 30, 30]]),
    ("centerTruth", [[1000000, 0, 1000000]]), ("centerTruth", [[]]), ("centerTruth", [[1] * 31]), ("centerTruth", [[1] * 30]),
    ("centerTruth", [[1, -1]]), ("centerTruth", [[1, 1000001]]), ("centerTruth", [[1, 2.345, 2.345]]),
    ("spreadTruth", [[3, 5, 3, 9, 1]]), ("spreadTruth", [[5]]), ("spreadTruth", [[4, 4, 4]]), ("spreadTruth", [[1, 2]]),
    ("spreadTruth", [[0, 10]]), ("spreadTruth", [[1, 10]]), ("spreadTruth", [[0.01, 0.02, 0.04]]), ("spreadTruth", [[]]),
    ("spreadTruth", [[2, -3]]), ("spreadTruth", [[1000000, 0, 0, 0]]),
    ("extraTruth", [[3, 5, 3, 9, 1], 100]), ("extraTruth", [[3, 5, 3, 9, 1], 4.2]), ("extraTruth", [[1, 2, 3], 2]),
    ("extraTruth", [[1, 2, 3, 4], 2.5]), ("extraTruth", [[10], 20]), ("extraTruth", [[1, 2, 3], 0]), ("extraTruth", [[1, 2, 3], 1000000]),
    ("extraTruth", [[1, 2, 3], -1]), ("extraTruth", [[1, 2, 3], 1000001]), ("extraTruth", [[], 5]), ("extraTruth", [[1] * 30, 5]),
    ("extraTruth", [[5, 6], 5.5]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
