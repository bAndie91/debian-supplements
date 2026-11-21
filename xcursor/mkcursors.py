#!/usr/bin/env python3
# Core X cursor shapes -> Xcursor theme with extra sizes.
# Staircase edges are rebuilt as true straight lines, rasterized without anti-aliasing;
# the white outline stays 1 px at every size, only the shapes are enlarged.
import sys, os, math, struct, zlib, subprocess

SIZES = [16, 24, 32, 48, 64, 72, 96]   # 16 = native glyphs, copied pixel for pixel
BASE = 16.0                            # nominal size of the native glyphs

NAMES = """X_cursor arrow based_arrow_down based_arrow_up boat bogosity
bottom_left_corner bottom_right_corner bottom_side bottom_tee box_spiral
center_ptr circle clock coffee_mug cross cross_reverse crosshair diamond_cross
dot dotbox double_arrow draft_large draft_small draped_box exchange fleur
gobbler gumby hand1 hand2 heart icon iron_cross left_ptr left_side left_tee
leftbutton ll_angle lr_angle man middlebutton mouse pencil pirate plus
question_arrow right_ptr right_side right_tee rightbutton rtl_logo sailboat
sb_down_arrow sb_h_double_arrow sb_left_arrow sb_right_arrow sb_up_arrow
sb_v_double_arrow shuttle sizing spider spraycan star target tcross
top_left_arrow top_left_corner top_right_corner top_side top_tee trek ul_angle
umbrella ur_angle watch xterm""".split()

ALIASES = {
    'default': 'left_ptr', 'text': 'xterm', 'ibeam': 'xterm',
    'pointer': 'hand2', 'hand': 'hand2', 'move': 'fleur', 'all-scroll': 'fleur',
    'grab': 'hand1', 'grabbing': 'fleur',
    'wait': 'watch', 'progress': 'watch', 'left_ptr_watch': 'watch',
    'help': 'question_arrow', 'cross': 'crosshair',
    'col-resize': 'sb_h_double_arrow', 'row-resize': 'sb_v_double_arrow',
    'ew-resize': 'sb_h_double_arrow', 'ns-resize': 'sb_v_double_arrow',
    'size_hor': 'sb_h_double_arrow', 'size_ver': 'sb_v_double_arrow',
    'n-resize': 'top_side', 's-resize': 'bottom_side',
    'w-resize': 'left_side', 'e-resize': 'right_side',
    'nw-resize': 'top_left_corner', 'ne-resize': 'top_right_corner',
    'sw-resize': 'bottom_left_corner', 'se-resize': 'bottom_right_corner',
}

def parse_bdf(path):
    glyphs, cur, bm = {}, None, False
    for line in open(path):
        w = line.split()
        if not w: continue
        k = w[0]
        if k == 'STARTCHAR': cur, bm = {'rows': []}, False
        elif k == 'ENCODING': cur['enc'] = int(w[1])
        elif k == 'BBX': cur['bbx'] = tuple(int(x) for x in w[1:5])
        elif k == 'BITMAP': bm = True
        elif k == 'ENDCHAR': glyphs[cur['enc']] = cur; bm = False
        elif bm: cur['rows'].append(w[0])
    return glyphs

def pixels(g):
    w, h, xo, yo = g['bbx']
    s = set()
    for r, hx in enumerate(g['rows']):
        v, nb = int(hx, 16), len(hx) * 4
        for c in range(w):
            if (v >> (nb - 1 - c)) & 1:
                s.add((xo + c, yo + h - 1 - r))   # origin-relative, y up
    return s

N8 = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
N4 = [(0, -1), (-1, 0), (1, 0), (0, 1)]

def layers(src, mask):
    """black body S, core C (= silhouette without its 1 px white outline), silhouette U"""
    S = pixels(src)
    U = S | pixels(mask)
    O = {p for p in U - S if any((p[0] + dx, p[1] + dy) not in U for dx, dy in N8)}
    return S, U - O, U

def sgn(v): return (v > 0) - (v < 0)

def boundary_loops(pix):
    """outlines of a pixel set as lattice-vertex loops (interior on the left, y up);
    pixels touching only at a corner count as connected"""
    out = {}
    def add(a, b): out.setdefault(a, []).append(b)
    for x, y in pix:
        if (x, y - 1) not in pix: add((x, y), (x + 1, y))
        if (x + 1, y) not in pix: add((x + 1, y), (x + 1, y + 1))
        if (x, y + 1) not in pix: add((x + 1, y + 1), (x, y + 1))
        if (x - 1, y) not in pix: add((x, y + 1), (x, y))
    loops = []
    while out:
        a0 = next(iter(out)); b0 = out[a0].pop()
        if not out[a0]: del out[a0]
        path, cur, din = [a0], b0, (b0[0] - a0[0], b0[1] - a0[1])
        while True:
            cands = list(out.get(cur, []))
            if cur == a0: cands.append(b0)
            nxt = min(cands, key=lambda c: din[0] * (c[1] - cur[1]) - din[1] * (c[0] - cur[0]))  # rightmost turn
            if cur == a0 and nxt == b0: break
            path.append(cur)
            out[cur].remove(nxt)
            if not out[cur]: del out[cur]
            din, cur = (nxt[0] - cur[0], nxt[1] - cur[1]), nxt
        m = len(path)   # drop vertices on straight runs
        loops.append([path[i] for i in range(m)
                      if (sgn(path[i][0] - path[i-1][0]), sgn(path[i][1] - path[i-1][1])) !=
                         (sgn(path[(i+1) % m][0] - path[i][0]), sgn(path[(i+1) % m][1] - path[i][1]))])
    return loops

DEV = 0.6   # how far (source px) a staircase corner may stray from its straight line

def straighten(V):
    """Replace digital straight staircases (unit steps, any slope) by true straight lines.
    Right angles, thin strokes and everything that is not a regular staircase stay as they are."""
    m = len(V)
    plain = [(float(x), float(y)) for x, y in V]
    if m < 8: return plain
    cross = lambda a, b: a[0] * b[1] - a[1] * b[0]
    D = [(sgn(V[(k+1) % m][0] - V[k][0]), sgn(V[(k+1) % m][1] - V[k][1])) for k in range(m)]
    T = [1 if cross(D[k-1], D[k]) > 0 else -1 for k in range(m)]   # turn at vertex k
    s = next((k for k in range(m) if T[k] == T[k-1]), None)
    if s is None: return plain
    P = [V[(i + s) % m] for i in range(m + 1)]          # rotated vertices; edge i = P[i] -> P[i+1]
    Tr = [T[(i + s) % m] for i in range(m)]
    L = [abs(P[i+1][0] - P[i][0]) + abs(P[i+1][1] - P[i][1]) for i in range(m)]
    mid = lambda i: ((P[i][0] + P[i+1][0]) / 2.0, (P[i][1] + P[i+1][1]) / 2.0)

    def fit(k, b):
        pts = [mid(j) for j in range(k + 1, b)]
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        sxx = sum((p[0] - cx) ** 2 for p in pts); syy = sum((p[1] - cy) ** 2 for p in pts)
        sxy = sum((p[0] - cx) * (p[1] - cy) for p in pts)
        a = 0.5 * math.atan2(2 * sxy, sxx - syy)
        return (cx, cy), (math.cos(a), math.sin(a))

    def valid(k, b):
        c = b - k + 1
        if c < 4: return False
        Ls = L[k:b + 1]
        for par in (0, 1):                 # which alternate edges are the unit "risers"
            if any(Ls[i] != 1 for i in range(par, c, 2)): continue
            maj = [i for i in range(c) if i % 2 != par]
            inner = [Ls[i] for i in maj if 0 < i < c - 1]
            ends = [Ls[i] for i in maj if i in (0, c - 1)]
            if inner and (max(inner) - min(inner) > 1 or any(e > max(inner) for e in ends)): continue
            cen, d = fit(k, b)
            if max(abs(cross(d, (P[j][0] - cen[0], P[j][1] - cen[1]))) for j in range(k, b + 2)) <= DEV:
                return True
        return False

    def longest(k):
        bmax = k
        while bmax + 1 < m and (bmax + 1 < k + 2 or Tr[bmax + 1] != Tr[bmax]): bmax += 1
        for b in range(bmax, k + 2, -1):
            if valid(k, b): return b
        return None

    segs = []       # (first edge, last edge, point, direction, is_chain)
    i = 0
    while i < m:
        b = None
        if segs and segs[-1][4] and segs[-1][1] == i - 1:      # may share one edge with the previous chain
            b = longest(i - 1)
            if b is not None and b > i - 1: k = i - 1
            else: b = None
        if b is None:
            b = longest(i); k = i
        if b is None:
            segs.append((i, i, P[i], D[(i + s) % m], False)); i += 1
        else:
            cen, d = fit(k, b)
            segs.append((k, b, cen, d, True)); i = b + 1
    out = []
    for n in range(len(segs)):
        a, c = segs[n], segs[(n + 1) % len(segs)]
        if c[0] <= a[1] and c[4] and a[4]:        # chains sharing an edge
            anchor = mid(a[1])
        else:
            anchor = (float(P[c[0]][0]), float(P[c[0]][1]))
        cr = cross(a[3], c[3])
        pt = anchor
        if abs(cr) > 0.2:
            t = cross((c[2][0] - a[2][0], c[2][1] - a[2][1]), c[3]) / cr
            cand = (a[2][0] + t * a[3][0], a[2][1] + t * a[3][1])
            if math.hypot(cand[0] - anchor[0], cand[1] - anchor[1]) <= 2.0: pt = cand
        out.append(pt)
    return out

def trace(pix):
    return [straighten(lp) for lp in boundary_loops(pix)] if pix else []

def fill(polys, ox, oy, f, tw, th):
    """hard (even-odd, pixel-center) rasterization of polygons scaled by f; image y runs down"""
    img = [bytearray(tw) for _ in range(th)]
    edges = []
    for poly in polys:
        pts = [((x + ox) * f, (oy - y) * f) for x, y in poly]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
            if y1 != y2: edges.append((x1, y1, x2, y2))
    for ty in range(th):
        yc = ty + 0.5
        xs = sorted(x1 + (yc - y1) * (x2 - x1) / (y2 - y1)
                    for x1, y1, x2, y2 in edges if (y1 <= yc < y2) or (y2 <= yc < y1))
        for a, b in zip(xs[0::2], xs[1::2]):
            for tx in range(max(0, math.ceil(a - 0.5)), min(tw, math.ceil(b - 0.5))):
                img[ty][tx] = 1
    return img

def render(S, C, U, polys, size, bb):
    """-> (width, height, rgba rows, hotspot x, hotspot y)"""
    minx, maxx, miny, maxy = bb
    f = size / BASE
    ox, oy = -minx, maxy + 1                  # glyph origin (= hotspot) inside the unscaled box
    if f == 1.0:                              # native size: the original pixels, untouched
        tw, th = maxx - minx + 1, maxy - miny + 1
        def raster(pix):
            img = [bytearray(tw) for _ in range(th)]
            for x, y in pix: img[maxy - y][x - minx] = 1
            return img
        black, core, sil = raster(S), raster(C), raster(U)
    else:
        tw, th = math.ceil((maxx - minx + 1) * f), math.ceil((maxy - miny + 1) * f)
        black, core, sil = (fill(p, ox, oy, f, tw, th) for p in polys)
    occ = [bytearray(a | b for a, b in zip(rb, rc)) for rb, rc in zip(black, core)]
    rows = []
    for y in range(th):
        row = bytearray()
        for x in range(tw):
            if black[y][x]:
                row += b'\x00\x00\x00\xff'                               # black
            elif occ[y][x]:
                row += b'\xff\xff\xff\xff'                               # white inside the shape
            elif sil[y][x] and (f == 1.0 or any(                          # the 1 px white outline:
                    0 <= x + dx < tw and 0 <= y + dy < th and occ[y + dy][x + dx]
                    for dx, dy in N4)):                                   # touching the shape, inside the silhouette
                row += b'\xff\xff\xff\xff'
            else:
                row += b'\x00\x00\x00\x00'                               # transparent
        rows.append(bytes(row))
    return tw, th, rows, round(ox * f), round(oy * f)

def write_png(path, w, h, rows):
    raw = b''.join(b'\0' + r for r in rows)
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    with open(path, 'wb') as fh:
        fh.write(b'\x89PNG\r\n\x1a\n'
                 + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
                 + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))

def main(bdf, outdir, only=None):
    glyphs = parse_bdf(bdf)
    cdir = os.path.join(outdir, 'cursors')
    work = os.path.join(outdir, '.work')
    os.makedirs(cdir, exist_ok=True); os.makedirs(work, exist_ok=True)
    for i, name in enumerate(NAMES):
        if only and name not in only: continue
        print(name)
        src, mask = glyphs.get(2 * i), glyphs.get(2 * i + 1)
        if not src or not mask or not (pixels(src) | pixels(mask)):
            print('skip', name); continue
        S, C, U = layers(src, mask)
        xs = [x for x, y in U]; ys = [y for x, y in U]
        bb = (min(xs) - 2, max(xs) + 2, min(ys) - 2, max(ys) + 2)   # margin for polygon overshoot
        polys = (trace(S), trace(C), trace(U))
        cfg = []
        for size in SIZES:
            png = os.path.abspath(os.path.join(work, '%s-%d.png' % (name, size)))
            tw, th, rows, xh, yh = render(S, C, U, polys, size, bb)
            write_png(png, tw, th, rows)
            cfg.append('%d %d %d %s' % (size, min(xh, tw - 1), min(yh, th - 1), png))
        cfgfile = os.path.join(work, name + '.cfg')
        open(cfgfile, 'w').write('\n'.join(cfg) + '\n')
        subprocess.run(['xcursorgen', cfgfile, os.path.join(cdir, name)], check=True)
    for alias, target in ALIASES.items():
        p = os.path.join(cdir, alias)
        if os.path.lexists(p): os.remove(p)
        os.symlink(target, p)
    with open(os.path.join(outdir, 'index.theme'), 'w') as fh:
        fh.write('[Icon Theme]\nName=xcore-large\nComment=X core cursors at larger sizes\n')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3:] or None)
