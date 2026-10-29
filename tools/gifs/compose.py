"""Turns recorded snaps into a finished README GIF: the terminal crop in a
window (title bar, padding, rounded corners) on a quiet margin, a caption strip
that says what is happening, paced so waits are short and the moments that
matter hold, all on one palette.

    from compose import compose
    compose(frames, box, 'out.gif', title='clawd-git', captions=[(r'Restore points', 'A restore point …')])

Captions: each rule is (regex, text), matched against a frame's text; the
latest rule that matches names the frame, and the caption never goes back to
an earlier one, so it reads as steps.
"""
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import rec

SANS_PATH = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
SANS = ImageFont.truetype(SANS_PATH, 17)
# For what Noto Sans lacks (✓, ×, arrows).
SANS_FALLBACK = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)


def say(d, xy, text, fill):
    """Draws text in Noto Sans, each character it lacks in DejaVu Sans."""
    x, y = xy
    for ch in text:
        font = SANS if rec.has(SANS_PATH, ch) or ch == ' ' else SANS_FALLBACK
        d.text((x, y + (0 if font is SANS else 2)), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font)
SANS_BOLD = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf', 15)
TITLE = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 14)

MARGIN = 26
PAD = 14
TITLE_H = 34
CAPTION_H = 52
RADIUS = 11
CANVAS = (17, 19, 24)
WINDOW = rec.BG
CHROME = (40, 44, 52)
EDGE = (58, 63, 74)
ACCENT = (217, 119, 87)
CAPTION_FG = (205, 209, 216)
DOTS = [(255, 95, 87), (254, 188, 46), (40, 200, 64)]


def text_of(snap):
    return re.sub(r'\x1b\[[0-9;:]*m', '', rec.scrub(snap))


def window(term, title, caption, step):
    """The terminal image inside its window, and the caption under it."""
    w = term.width + 2 * PAD
    h = TITLE_H + term.height + 2 * PAD
    W = w + 2 * MARGIN
    H = h + 2 * MARGIN + CAPTION_H
    im = Image.new('RGB', (W, H), CANVAS)
    d = ImageDraw.Draw(im)
    x0, y0 = MARGIN, MARGIN
    # The window: its frame, then the title bar's lower corners squared off.
    d.rounded_rectangle([x0, y0, x0 + w - 1, y0 + h - 1], radius=RADIUS, fill=WINDOW, outline=EDGE)
    d.rounded_rectangle([x0, y0, x0 + w - 1, y0 + TITLE_H], radius=RADIUS, fill=CHROME, outline=EDGE)
    d.rectangle([x0 + 1, y0 + TITLE_H - RADIUS, x0 + w - 2, y0 + TITLE_H], fill=CHROME)
    d.line([x0, y0 + TITLE_H, x0 + w - 1, y0 + TITLE_H], fill=EDGE)
    for i, color in enumerate(DOTS):
        cx, cy = x0 + 20 + i * 20, y0 + TITLE_H // 2
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)
    tw = d.textlength(title, font=TITLE)
    d.text((x0 + (w - tw) / 2, y0 + (TITLE_H - 18) / 2), title, font=TITLE, fill=(150, 156, 168))
    im.paste(term, (x0 + PAD, y0 + TITLE_H + PAD))
    # The caption: a numbered step in the accent, then what happens.
    if caption:
        cy = y0 + h + (CAPTION_H + MARGIN) // 2 - 4
        label = str(step)
        r = 13
        d.ellipse([x0, cy - r, x0 + 2 * r, cy + r], fill=ACCENT)
        lw = d.textlength(label, font=SANS_BOLD)
        d.text((x0 + r - lw / 2, cy - 10), label, font=SANS_BOLD, fill=(24, 26, 31))
        say(d, (x0 + 2 * r + 12, cy - 12), caption, CAPTION_FG)
    return im


def caption_steps(texts, rules):
    """The caption index of each frame: the latest matching rule, never going back."""
    out, at = [], -1
    for text in texts:
        hit = max((i for i, (pattern, _) in enumerate(rules) if re.search(pattern, text, re.S)), default=-1)
        at = max(at, hit)
        out.append(at)
    return out


def compose(frames, box, out, title, captions=(), cap_ms=900, hold_ms=1800, end_ms=3500, target_s=20, scale=None,
            start=None, until=None):
    """frames: [(snap, ms)]. Writes `out`; returns (bytes, frames, seconds).

    `start`/`until`: regexes; the GIF begins at the first frame matching
    `start` and ends at the last matching `until`, so it ends on its moment."""
    texts = [text_of(snap) for snap, _ in frames]
    if until:
        last = max((i for i, t in enumerate(texts) if re.search(until, t, re.S)), default=len(texts) - 1)
        frames, texts = frames[:last + 1], texts[:last + 1]
    if start:
        first = next((i for i, t in enumerate(texts) if re.search(start, t, re.S)), 0)
        frames, texts = frames[first:], texts[first:]
    steps = caption_steps(texts, list(captions))
    images, durations = [], []
    last_key = None
    for (snap, ms), text, step in zip(frames, texts, steps):
        key = (text, step, snap)
        if key == last_key:
            durations[-1] += ms
            continue
        last_key = key
        term = rec.draw(rec.scrub(snap), box)
        caption = captions[step][1] if step >= 0 else ''
        images.append(window(term, title, caption, step + 1))
        durations.append(ms)
    # Pacing: no frame waits longer than cap_ms; the first frame of each step
    # holds so its caption can be read; the last one holds before the loop.
    step_of = []
    last_key = None
    for (snap, ms), text, step in zip(frames, texts, steps):
        key = (text, step, snap)
        if key != last_key:
            step_of.append(step)
            last_key = key
    paced = []
    for i, ms in enumerate(durations):
        is_new_step = i == 0 or step_of[i] != step_of[i - 1]
        paced.append(max(hold_ms, min(ms, cap_ms)) if is_new_step else min(ms, cap_ms))
    paced[-1] = end_ms
    # Too long overall: the in-between frames speed up, the holds stay.
    total = sum(paced)
    fixed = sum(p for i, p in enumerate(paced) if i == 0 or i == len(paced) - 1 or step_of[i] != step_of[i - 1])
    if total > target_s * 1000 and total > fixed:
        k = max(0.15, (target_s * 1000 - fixed) / (total - fixed))
        paced = [p if (i == 0 or i == len(paced) - 1 or step_of[i] != step_of[i - 1]) else max(90, int(p * k)) for i, p in enumerate(paced)]
    if scale:
        images = [im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS) for im in images]
    # One palette for every frame, from a sample of them, without dithering.
    sample = images[:: max(1, len(images) // 12)][:12]
    strip = Image.new('RGB', (sample[0].width, sample[0].height * len(sample)))
    for i, one in enumerate(sample):
        strip.paste(one, (0, i * one.height))
    palette = strip.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    pal = [one.quantize(palette=palette, dither=Image.Dither.NONE) for one in images]
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=paced, loop=0, optimize=True, disposal=1)
    return Path(out).stat().st_size, len(pal), round(sum(paced) / 1000, 1)
