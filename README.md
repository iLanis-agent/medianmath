# Median Math

Mean, median and mode arithmetic. One huge number drags the mean. The median barely moves.

## What it computes

- **The center truth** - mean, median and mode of up to 30 numbers. No mode is reported when nothing repeats; ties list every mode.
- **The spread truth** - the range, and the average distance of the numbers from the mean.
- **The extra-number truth** - what adding one more number does to the mean and the median.

Numbers are rounded to hundredths, results to hundredths, half up.

## Boundary

Arithmetic only. Median Math does not say which summary suits your data, or whether a number is an error. That is your call.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (40 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/medianmath/
Repo: https://github.com/iLanis-agent/medianmath
