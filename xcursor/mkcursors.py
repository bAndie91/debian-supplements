#!/usr/bin/env python3
import sys, os, math, struct, zlib, subprocess

SIZES = [16, 24, 32, 48, 64, 72, 96]   # 16 = native glyphs; drop it if you don't want it
BASE = 16.0   # nominal size of the native glyphs; size N is scaled by N/BASE
SS = 4        # supersampling per axis (anti-aliasing for non-integer scales)

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
    allp = S | M
    minx = min(x for x, y in allp); maxx = max(x for x, y in allp)
    miny = min(y for x, y in allp); maxy = max(y for x, y in allp)
    W, H = maxx - minx + 1, maxy - miny + 1
    grid = [[0] * W for _ in range(H)]
    for (x, y) in M: grid[maxy - y][x - minx] = 1      # white outline
    for (x, y) in S: grid[maxy - y][x - minx] = 2      # black body
    # X core hotspot = glyph origin
    return grid, W, H, -minx, maxy + 1

def scale(grid, W, H, f):
    tw, th = max(1, math.ceil(W * f)), max(1, math.ceil(H * f))
    n = SS * SS
    rows = []
    for ty in range(th):
        yi = [int((ty + (j + .5) / SS) / f) for j in range(SS)]
        row = bytearray()
        for tx in range(tw):
            xi = [int((tx + (j + .5) / SS) / f) for j in range(SS)]
            white = black = 0
            for sy in yi:
                if sy >= H: continue
                gr = grid[sy]
                for sx in xi:
                    if sx >= W: continue
                    v = gr[sx]
                    if v == 1: white += 1
                    elif v == 2: black += 1
            a = white + black
            if a:
                row += bytes((round(255 * white / a),) * 3 + (round(255 * a / n),))
            else:
                row += bytes(4)
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
        grid, W, H, hx, hy = compose(src, mask)
        cfg = []
        for size in SIZES:
            f = size / BASE
            png = os.path.abspath(os.path.join(work, '%s-%d.png' % (name, size)))
            tw, th, rows = scale(grid, W, H, f)
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
