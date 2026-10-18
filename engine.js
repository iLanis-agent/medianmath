// Median Math engine - mean, median and mode; range and average distance from the mean; the effect of one extra number.
// Mirrored by oracle.py; keep the op order identical.
// Numbers are rounded to hundredths on the way in; results come out to hundredths, half up.

function _list(list) {
  if (!Array.isArray(list) || list.length < 1 || list.length > 30) throw new Error("need 1 to 30 numbers");
  var out = [];
  for (var i = 0; i < list.length; i++) {
    var x = list[i];
    if (typeof x !== "number" || !isFinite(x) || x < 0 || x > 1000000) throw new Error("each number must be between 0 and 1000000");
    out.push(Math.floor(x * 100 + 0.5));
  }
  return out.sort(function (a, b) { return a - b; });
}

function _fmt(h) {
  var whole = Math.floor(h / 100), frac = h % 100;
  if (frac === 0) return String(whole);
  var f = (frac < 10 ? "0" : "") + frac;
  if (f.charAt(1) === "0") f = f.charAt(0);
  return whole + "." + f;
}

function _div(n, d) {
  return Math.floor((2 * n + d) / (2 * d));
}

function _mean(s) {
  var sum = 0;
  for (var i = 0; i < s.length; i++) sum += s[i];
  return _div(sum, s.length);
}

function _median(s) {
  var n = s.length, m = Math.floor(n / 2);
  if (n % 2 === 1) return s[m];
  return Math.floor((s[m - 1] + s[m] + 1) / 2);
}

function _modes(s) {
  var best = 1, vals = [], i = 0;
  while (i < s.length) {
    var j = i;
    while (j < s.length && s[j] === s[i]) j++;
    var c = j - i;
    if (c > best) { best = c; vals = [s[i]]; }
    else if (c === best && c > 1) vals.push(s[i]);
    i = j;
  }
  return { count: best, values: vals };
}

function _and(vals) {
  var t = vals.map(_fmt);
  if (t.length === 1) return t[0];
  return t.slice(0, -1).join(", ") + " and " + t[t.length - 1];
}

// The center truth: mean, median and mode.
function centerTruth(list) {
  var s = _list(list);
  var m = _modes(s);
  var mode;
  if (m.values.length === 0) mode = "no mode, since no value repeats";
  else if (m.values.length === 1) mode = "mode " + _and(m.values) + " (" + m.count + " times)";
  else mode = "modes " + _and(m.values) + " (" + m.count + " times each)";
  return "Mean " + _fmt(_mean(s)) + ", median " + _fmt(_median(s)) + ", " + mode + ".";
}

// The spread truth: range, and the average distance from the mean.
function spreadTruth(list) {
  var s = _list(list);
  var n = s.length, sum = 0, i;
  for (i = 0; i < n; i++) sum += s[i];
  var d = 0;
  for (i = 0; i < n; i++) d += Math.abs(n * s[i] - sum);
  var dev = _div(d, n * n);
  return "Range " + _fmt(s[n - 1] - s[0]) + " (from " + _fmt(s[0]) + " to " + _fmt(s[n - 1]) + "). On average the numbers sit " + _fmt(dev) + " from the mean.";
}

// The extra truth: what one more number does to the mean and the median.
function extraTruth(list, extra) {
  var s = _list(list);
  if (typeof extra !== "number" || !isFinite(extra) || extra < 0 || extra > 1000000) throw new Error("extra number must be between 0 and 1000000");
  var e = Math.floor(extra * 100 + 0.5);
  var t = s.concat([e]).sort(function (a, b) { return a - b; });
  var m0 = _mean(s), m1 = _mean(t), d0 = _median(s), d1 = _median(t);
  var a = m0 === m1 ? "leaves the mean at " + _fmt(m0) : "moves the mean from " + _fmt(m0) + " to " + _fmt(m1);
  var b = d0 === d1 ? "leaves the median at " + _fmt(d0) : "moves the median from " + _fmt(d0) + " to " + _fmt(d1);
  return "Adding " + _fmt(e) + " " + a + " and " + b + ".";
}
