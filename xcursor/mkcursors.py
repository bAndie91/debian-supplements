#!/usr/bin/env python3
import sys, os, math, struct, zlib, subprocess

SIZES = [16, 24, 32, 48, 64, 72, 96]   # 16 = native glyphs; drop it if you don't want it
BASE = 16.0   # nominal size of the native glyphs; size N is scaled by N/BASE
SIGMA = 0.55   # smoothing radius in source pixels: larger = straighter diagonals, rounder corners
THRESH = 0.5   # lower = fatter shapes, higher = thinner
PAD = 2        # empty margin in source pixels, so the outer contour gets smoothed too

# cursorfont.h names, in glyph order: glyph 2*i is the shape, 2*i+1 its mask
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

# modern / CSS-style names -> core names
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

def compose(src, mask):
    S, M = pixels(src), pixels(mask)
    U = S | M
    minx = min(x for x, y in U) - PAD; maxx = max(x for x, y in U) + PAD
    miny = min(y for x, y in U) - PAD; maxy = max(y for x, y in U) + PAD
    W, H = maxx - minx + 1, maxy - miny + 1
    shape = [[0] * W for _ in range(H)]   # whole silhouette (outline + body)
    body = [[0] * W for _ in range(H)]    # black part only
    for (x, y) in U: shape[maxy - y][x - minx] = 1
    for (x, y) in S: body[maxy - y][x - minx] = 1
    return shape, body, W, H, -minx, maxy + 1   # hotspot = glyph origin

def weights(n_out, f):
    # for each output pixel: [(source index, gaussian weight)] around its center in source space
    R = int(math.ceil(3 * SIGMA))
    res = []
    for t in range(n_out):
        c = (t + 0.5) / f - 0.5
        i0 = int(math.floor(c))
        raw = [(i, math.exp(-((i - c) ** 2) / (2 * SIGMA ** 2)))
               for i in range(i0 - R, i0 + R + 2)]
        tot = sum(w for _, w in raw)
        res.append([(i, w / tot) for i, w in raw])
    return res

def blur(grid, W, H, wx, wy, tw, th):
    # separable: horizontal pass on source rows, then vertical pass
    tmp = []
    for j in range(H):
        row = grid[j]
        tmp.append([sum(w * row[i] for i, w in wx[tx] if 0 <= i < W) for tx in range(tw)])
    return [[sum(w * tmp[j][tx] for j, w in wy[ty] if 0 <= j < H) for tx in range(tw)]
            for ty in range(th)]

def scale(shape, body, W, H, f):
    tw, th = max(1, math.ceil(W * f)), max(1, math.ceil(H * f))
    if f == 1.0:                       # native size: keep the original pixels untouched
        Sh, B = shape, body
    else:
        wx, wy = weights(tw, f), weights(th, f)
        Sh = blur(shape, W, H, wx, wy, tw, th)
        B = blur(body, W, H, wx, wy, tw, th)
    rows = []
    for ty in range(th):
        row = bytearray()
        for tx in range(tw):
            if B[ty][tx] >= THRESH:    row += b'\x00\x00\x00\xff'   # black
            elif Sh[ty][tx] >= THRESH: row += b'\xff\xff\xff\xff'   # white outline
            else:                      row += b'\x00\x00\x00\x00'   # transparent
        rows.append(bytes(row))
    return tw, th, rows

def write_png(path, w, h, rows):
    raw = b''.join(b'\0' + r for r in rows)
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    with open(path, 'wb') as fh:
        fh.write(b'\x89PNG\r\n\x1a\n'
                 + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
                 + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))

def main(bdf, outdir):
    glyphs = parse_bdf(bdf)
    cdir = os.path.join(outdir, 'cursors')
    work = os.path.join(outdir, '.work')
    os.makedirs(cdir, exist_ok=True); os.makedirs(work, exist_ok=True)
    for i, name in enumerate(NAMES):
        src, mask = glyphs.get(2 * i), glyphs.get(2 * i + 1)
        if not src or not mask or not (pixels(src) | pixels(mask)):
            print('skip', name); continue
        shape, body, W, H, hx, hy = compose(src, mask)
        cfg = []
        for size in SIZES:
            f = size / BASE
            png = os.path.abspath(os.path.join(work, '%s-%d.png' % (name, size)))
            tw, th, rows = scale(shape, body, W, H, f)
            write_png(png, tw, th, rows)
            xh = max(0, min(tw - 1, round(hx * f)))
            yh = max(0, min(th - 1, round(hy * f)))
            cfg.append('%d %d %d %s' % (size, xh, yh, png))
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
    main(sys.argv[1], sys.argv[2])
