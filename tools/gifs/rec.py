"""Records the clawd plugins in a real Claude Code session and renders GIFs.

A scene drives a throwaway Claude Code in its own tmux server (keys, mouse
clicks, prompts), snapping the screen with its colours (`capture-pane -e`);
`gif()` crops the snaps and draws them with the terminal's fonts.

    from rec import Session, gif
"""
import re
import subprocess
import time
import unicodedata
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONTS = Path.home() / '.local/share/fonts/JetBrainsMonoNerdFont'
REGULAR = ImageFont.truetype(str(FONTS / 'JetBrainsMonoNerdFontMono-Regular.ttf'), 15)
BOLD = ImageFont.truetype(str(FONTS / 'JetBrainsMonoNerdFontMono-Bold.ttf'), 15)
ITALIC = ImageFont.truetype(str(FONTS / 'JetBrainsMonoNerdFontMono-Italic.ttf'), 15)
FALLBACK = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 14)
MAIN = str(FONTS / 'JetBrainsMonoNerdFontMono-Regular.ttf')
# Where a character the main font lacks is drawn from, in order.
CHAIN = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
    '/usr/share/fonts/truetype/noto/NotoSansSymbols-Regular.ttf',
    '/usr/share/fonts/truetype/noto/NotoSansSymbols2-Regular.ttf',
]
# The quadrant blocks Clawd is drawn with: which quarters each fills (UL, UR, LL, LR).
QUADS = {'▘': (1, 0, 0, 0), '▝': (0, 1, 0, 0), '▖': (0, 0, 1, 0), '▗': (0, 0, 0, 1), '▀': (1, 1, 0, 0), '▄': (0, 0, 1, 1),
         '▌': (1, 0, 1, 0), '▐': (0, 1, 0, 1), '█': (1, 1, 1, 1), '▙': (1, 0, 1, 1), '▛': (1, 1, 1, 0), '▜': (1, 1, 0, 1),
         '▟': (0, 1, 1, 1), '▚': (1, 0, 0, 1), '▞': (0, 1, 1, 0)}
CELL_W, CELL_H = 9, 19
BG = (29, 32, 38)
FG = (215, 218, 224)

# The terminal's 16 colours (One Dark), for the basic SGR codes.
BASIC = ['#282c34', '#e06c75', '#98c379', '#e5c07b', '#61afef', '#c678dd', '#56b6c2', '#abb2bf',
         '#5c6370', '#ff7b86', '#b5e890', '#f5d58a', '#7cc4ff', '#de8ef0', '#6fd3e0', '#ffffff']


def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def c256(n):
    if n < 16:
        return hexrgb(BASIC[n])
    if n < 232:
        n -= 16
        f = lambda v: 0 if v == 0 else 55 + v * 40
        return (f(n // 36), f((n // 6) % 6), f(n % 6))
    v = 8 + (n - 232) * 10
    return (v, v, v)


def width(ch):
    if unicodedata.combining(ch):
        return 0
    return 2 if unicodedata.east_asian_width(ch) in 'WF' else 1


def parse(line):
    """One captured line → cells: (char, fg, bg, bold, dim, italic, inverse), one per column."""
    st = dict(fg=None, bg=None, b=False, d=False, i=False, inv=False)
    cells = []
    for m in re.finditer(r'\x1b\[([0-9;:]*)m|([^\x1b]+)', line):
        if m.group(2) is not None:
            for ch in m.group(2):
                w = width(ch)
                if w == 0:
                    continue
                cells.append((ch, dict(st)))
                if w == 2:
                    cells.append(('', dict(st)))
            continue
        codes = [int(x) if x else 0 for x in re.split('[;:]', m.group(1) or '0')]
        k = 0
        while k < len(codes):
            c = codes[k]
            if c == 0: st = dict(fg=None, bg=None, b=False, d=False, i=False, inv=False)
            elif c == 1: st['b'] = True
            elif c == 2: st['d'] = True
            elif c == 3: st['i'] = True
            elif c == 7: st['inv'] = True
            elif c == 22: st['b'] = st['d'] = False
            elif c == 23: st['i'] = False
            elif c == 27: st['inv'] = False
            elif 30 <= c <= 37: st['fg'] = hexrgb(BASIC[c - 30])
            elif 90 <= c <= 97: st['fg'] = hexrgb(BASIC[c - 90 + 8])
            elif 40 <= c <= 47: st['bg'] = hexrgb(BASIC[c - 40])
            elif 100 <= c <= 107: st['bg'] = hexrgb(BASIC[c - 100 + 8])
            elif c == 39: st['fg'] = None
            elif c == 49: st['bg'] = None
            elif c in (38, 48):
                key = 'fg' if c == 38 else 'bg'
                if k + 1 < len(codes) and codes[k + 1] == 2 and k + 4 < len(codes):
                    st[key] = tuple(codes[k + 2:k + 5]); k += 4
                elif k + 1 < len(codes) and codes[k + 1] == 5 and k + 2 < len(codes):
                    st[key] = c256(codes[k + 2]); k += 2
            k += 1
    return cells


_cmaps = {}
_fallbacks = {}


def has(path, ch):
    if path not in _cmaps:
        from fontTools.ttLib import TTFont
        _cmaps[path] = set(TTFont(path, fontNumber=0).getBestCmap() or {})
    return ord(ch) in _cmaps[path]


def font_for(ch, st):
    if has(MAIN, ch):
        return BOLD if st['b'] else ITALIC if st['i'] else REGULAR
    for path in CHAIN:
        if has(path, ch):
            if path not in _fallbacks:
                _fallbacks[path] = ImageFont.truetype(path, 14)
            return _fallbacks[path]
    return FALLBACK


def draw(snap, box):
    """A snap's text, cropped to box = (col0, row0, col1, row1), as an image."""
    c0, r0, c1, r1 = box
    lines = snap.split('\n')[r0:r1]
    im = Image.new('RGB', ((c1 - c0) * CELL_W, (r1 - r0) * CELL_H), BG)
    d = ImageDraw.Draw(im)
    for y, line in enumerate(lines):
        cells = parse(line)[c0:c1]
        for x, (ch, st) in enumerate(cells):
            fg, bg = st['fg'] or FG, st['bg']
            if st['inv']:
                fg, bg = (bg or BG), (st['fg'] or FG)
            if st['d']:
                base = bg or BG
                fg = tuple(int(a * 0.55 + b * 0.45) for a, b in zip(fg, base))
            px, py = x * CELL_W, y * CELL_H
            if bg:
                d.rectangle([px, py, px + CELL_W - 1, py + CELL_H - 1], fill=bg)
            if ch and ch != ' ':
                # Box drawing fills its cell, so lines join.
                if '─' <= ch <= '╿':
                    box_char(d, ch, px, py, fg)
                elif ch in QUADS:
                    hw, hh = CELL_W // 2, CELL_H // 2
                    parts = [(0, 0, hw, hh), (hw, 0, CELL_W - hw, hh), (0, hh, hw, CELL_H - hh), (hw, hh, CELL_W - hw, CELL_H - hh)]
                    for on, (qx, qy, qw, qh) in zip(QUADS[ch], parts):
                        if on:
                            d.rectangle([px + qx, py + qy, px + qx + qw - 1, py + qy + qh - 1], fill=fg)
                else:
                    d.text((px, py + 1), ch, font=font_for(ch, st), fill=fg)
    return im


def box_char(d, ch, px, py, fg):
    cx, cy = px + CELL_W // 2, py + CELL_H // 2
    heavy = ch in '┃━┏┓┗┛'
    w = 2 if heavy else 1
    name = unicodedata.name(ch, '')
    left = 'LEFT' in name or 'HORIZONTAL' in name or ch in '─━┐┘┤┴┬┼╮╯┓┛'
    right = 'RIGHT' in name or 'HORIZONTAL' in name or ch in '─━┌└├┴┬┼╭╰┏┗'
    up = 'UP' in name or 'VERTICAL' in name or ch in '│┃└┘├┤┴┼╰╯┗┛'
    down = 'DOWN' in name or 'VERTICAL' in name or ch in '│┃┌┐├┤┬┼╭╮┏┓'
    if ch in '╭╮╰╯':
        # Rounded corners: a quarter arc.
        r = min(CELL_W, CELL_H) // 2
        if ch == '╭': d.arc([cx, cy, cx + 2 * r, cy + 2 * r], 180, 270, fill=fg, width=w); d.line([cx + r, cy, px + CELL_W, cy], fill=fg, width=w); d.line([cx, cy + r, cx, py + CELL_H], fill=fg, width=w)
        if ch == '╮': d.arc([cx - 2 * r, cy, cx, cy + 2 * r], 270, 360, fill=fg, width=w); d.line([px, cy, cx - r, cy], fill=fg, width=w); d.line([cx, cy + r, cx, py + CELL_H], fill=fg, width=w)
        if ch == '╰': d.arc([cx, cy - 2 * r, cx + 2 * r, cy], 90, 180, fill=fg, width=w); d.line([cx + r, cy, px + CELL_W, cy], fill=fg, width=w); d.line([cx, py, cx, cy - r], fill=fg, width=w)
        if ch == '╯': d.arc([cx - 2 * r, cy - 2 * r, cx, cy], 0, 90, fill=fg, width=w); d.line([px, cy, cx - r, cy], fill=fg, width=w); d.line([cx, py, cx, cy - r], fill=fg, width=w)
        return
    if ch in '╌┄┈':
        for x in range(px, px + CELL_W, 3):
            d.point((x, cy), fill=fg)
        return
    if left: d.line([px, cy, cx, cy], fill=fg, width=w)
    if right: d.line([cx, cy, px + CELL_W, cy], fill=fg, width=w)
    if up: d.line([cx, py, cx, cy], fill=fg, width=w)
    if down: d.line([cx, cy, cx, py + CELL_H], fill=fg, width=w)
    if not (left or right or up or down):
        d.text((px, py + 1), ch, font=FALLBACK, fill=fg)


# Text that is not the plugin's to show: the session's title on the prompt's border.
SCRUB = ['Clawd-debug: language-agnostic breakpoint debugger plugin']


def scrub(snap):
    # Hyperlinks (OSC 8) and other OSC sequences are not text.
    snap = re.sub(r'\x1b\][^\x07\x1b]*(\x07|\x1b\\)', '', snap)
    for text in SCRUB:
        snap = snap.replace(f' {text} ', '─' * (len(text) + 2))
    # Home folders as ~, as the plugins themselves write them.
    snap = re.sub(r'/home/[a-z][a-z0-9_-]*/', '~/', snap)
    return snap


def gif(frames, box, out, scale=1.0):
    """frames: [(snap, ms)]; same snaps in a row merge. Writes out, returns its size."""
    merged = []
    for snap, ms in frames:
        snap = scrub(snap)
        if merged and merged[-1][0] == snap:
            merged[-1] = (snap, merged[-1][1] + ms)
        else:
            merged.append((snap, ms))
    images = [draw(snap, box) for snap, _ in merged]
    if scale != 1.0:
        images = [im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS) for im in images]
    pal = [im.convert('P', palette=Image.ADAPTIVE, colors=128) for im in images]
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=[ms for _, ms in merged], loop=0, optimize=True, disposal=1)
    return Path(out).stat().st_size, len(merged)


class Session:
    """A Claude Code in its own tmux server, `cols` × `rows`."""

    def __init__(self, name, cwd, cmd='claude', cols=200, rows=50):
        self.name = name
        self.t = ['tmux', '-L', name]
        subprocess.run(self.t + ['kill-server'], capture_output=True)
        time.sleep(0.5)
        subprocess.run(self.t + ['new-session', '-d', '-s', 't', '-x', str(cols), '-y', str(rows), f'cd {cwd} && {cmd}; sleep 5'], check=True)

    def keys(self, *keys, wait=0.4):
        for k in keys:
            subprocess.run(self.t + ['send-keys', '-t', 't', k])
            time.sleep(wait)

    def type(self, text, enter=True, wait=1.0):
        subprocess.run(self.t + ['send-keys', '-t', 't', '-l', text])
        time.sleep(0.6)
        if enter:
            subprocess.run(self.t + ['send-keys', '-t', 't', 'Enter'])
        time.sleep(wait)

    def raw(self, seq):
        subprocess.run(self.t + ['send-keys', '-t', 't', '-l', seq])

    def click(self, row, col, wait=1.0):
        """1-based screen row and column."""
        self.raw(f'\x1b[<0;{col};{row}M'); time.sleep(0.15); self.raw(f'\x1b[<0;{col};{row}m'); time.sleep(wait)

    def wheel(self, row, col, down=True, n=1, wait=0.4):
        for _ in range(n):
            self.raw(f'\x1b[<{65 if down else 64};{col};{row}M'); time.sleep(wait)

    def snap(self):
        return subprocess.run(self.t + ['capture-pane', '-e', '-p', '-t', 't'], capture_output=True, text=True).stdout

    def text(self):
        return subprocess.run(self.t + ['capture-pane', '-p', '-t', 't'], capture_output=True, text=True).stdout

    def find(self, needle, after=None):
        """(row, col), 1-based, of the first `needle` on screen (in a line holding `after`)."""
        for i, line in enumerate(self.text().split('\n')):
            if needle in line and (after is None or after in line):
                pre = line[:line.index(needle)]
                return i + 1, sum(width(c) for c in pre) + 1
        return None

    def wait_for(self, needle, timeout=60, every=0.5, frames=None, ms=None):
        """Until `needle` shows; snaps every `every` s into `frames` meanwhile."""
        end = time.time() + timeout
        while time.time() < end:
            if frames is not None:
                frames.append((self.snap(), ms or int(every * 1000)))
            if needle in self.text():
                return True
            time.sleep(every)
        return False

    def film(self, seconds, frames, every=0.5, ms=None):
        end = time.time() + seconds
        while time.time() < end:
            frames.append((self.snap(), ms or int(every * 1000)))
            time.sleep(every)

    def close(self):
        subprocess.run(self.t + ['kill-server'], capture_output=True)
