"""clawd-debug, 200 columns: a harness of test cases runs (one fails), a
breakpoint goes in cart.js, the failing case reruns alone and stops there, and
stepping shows how its total turns into NaN. No Claude turn needed.
Frames go to frames/debug.json."""
import json
import time
from pathlib import Path

from rec import Session

HERE = Path(__file__).parent
DEMO = Path.home() / 'Projects/clawd-demo-shop'

s = Session('clawdrec', DEMO, cols=200, rows=50)
time.sleep(12)
frames = []


def film(sec, every=0.6):
    s.film(sec, frames, every=every)


def press(label, after=None, pause=2.5, dx=1):
    for i, line in enumerate(s.text().split('\n')):
        at = line.find(label, 105)
        if at >= 0 and (after is None or after in line):
            s.click(i + 1, len(line[:at].encode('utf-16-le')) // 2 + 1 + dx, wait=0.3)
            film(pause)
            return True
    print('not found:', label)
    return False


s.type('/dbg .clawd-debug/check_cart.js', wait=3)
film(2)
press('run', after='test data', pause=6)
s.type('/dbg break src/cart.js:5', wait=2)
film(2.5)
press('rerun failing', pause=5)
for _ in range(4):
    s.keys('n', wait=0.2)
    film(2.2)
s.keys('q', wait=0.2)
film(2)
(HERE / 'frames').mkdir(exist_ok=True)
(HERE / 'frames/debug.json').write_text(json.dumps(frames))
print(len(frames), 'frames')
print('\n'.join(line[105:] for line in s.text().split('\n')[:46]))
s.close()
