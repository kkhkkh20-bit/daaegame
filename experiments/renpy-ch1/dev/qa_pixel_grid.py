"""Measure the on-screen pixel grid of a region of a 1280x720 game screenshot (0.18.93).

    python3 dev/qa_pixel_grid.py SHOT.png x0 y0 x1 y1 [--alpha-from-bg]

For every row and column of the region the positions where the colour changes are collected.
For each candidate block size k (1..8) and offset o, the share of change positions that fall on
the grid o + n*k is counted. A region drawn with whole k-pixel blocks scores 1.00 at k; a
non-integer resample spreads the changes over every offset. Colour steps of 8 or less per
channel are ignored (texture blending noise). Prints the best k per axis, its
share, and the run-length histogram (lengths of equal-colour runs)."""
import collections, json, sys

import numpy as np
from PIL import Image


TOL = 8   # colour steps up to this size are shading noise (texture blending), not a cell edge


def changes(a, axis):
    d = np.any(np.abs(np.diff(a, axis=axis)) > TOL, axis=2)   # pixel i+1 differs from pixel i
    return np.nonzero(d)[axis] + 1                     # column index for axis 1, row index for axis 0


def grid_score(pos, kmax=8):
    out = {}
    for k in range(2, kmax + 1):
        counts = np.bincount(pos % k, minlength=k)
        out[k] = round(float(counts.max()) / max(1, len(pos)), 3)
    return out


def best(score, need=0.95):
    """Largest block size whose grid holds at least `need` of the changes (a 4-px grid also
    scores on 2); otherwise the best-scoring size."""
    ok = [k for k, v in score.items() if v >= need]
    return max(ok) if ok else max(score, key=lambda k: (score[k], k))


def runs(a, axis, limit=12):
    hist = collections.Counter()
    lines = a if axis == 1 else a.transpose(1, 0, 2)
    for line in lines:
        same = np.all(np.abs(line[1:] - line[:-1]) <= TOL, axis=1)
        n = 1
        for s in same:
            if s:
                n += 1
            else:
                hist[min(n, limit)] += 1
                n = 1
        hist[min(n, limit)] += 1
    total = sum(hist.values())
    return {k: round(v / total, 3) for k, v in sorted(hist.items())}


def probe(path, box):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)[box[1]:box[3], box[0]:box[2]]
    xs = changes(a, 1)
    ys = changes(a, 0)
    gx, gy = grid_score(xs), grid_score(ys)
    return {"region": box, "x_grid": gx, "y_grid": gy,
            "best_x": best(gx), "best_y": best(gy),
            "x_runs": runs(a, 1), "y_runs": runs(a, 0)}


if __name__ == "__main__":
    path = sys.argv[1]
    box = [int(v) for v in sys.argv[2:6]]
    print(json.dumps(probe(path, box), ensure_ascii=False))
