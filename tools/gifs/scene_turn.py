"""One real turn in the demo shop, 124 columns: a plan of three tasks
(clawd-tasks) and Claude at work (clawd-statusbar's Clawd).
Frames go to frames/turn.json for the crops."""
import json
import re
import time
from pathlib import Path

from rec import Session

HERE = Path(__file__).parent
DEMO = Path.home() / 'Projects/clawd-demo-shop'
PROMPT = (
    'Make a plan with three tasks and work through them one at a time: '
    '(1) read src/cart.js and src/discounts.js; '
    '(2) add applyCoupon(total, code) to src/discounts.js: it uses findCoupon and returns the total less the coupon, rounded to cents, or the total unchanged for an unknown code; '
    '(3) add a test for it to tests/cart.test.js and run `node --test tests/`. '
    'Keep your answers short.'
)

s = Session('clawdrec', DEMO, cols=124, rows=40)
time.sleep(10)
if 'trust this folder' in s.text():
    s.keys('Down', 'Enter', wait=1)
    time.sleep(8)
# The git panel has a recording of its own: keep this one to the prompt.
s.type('/git-pane close', wait=3)
frames = []
s.film(3, frames, every=1.0)
s.type(PROMPT, wait=0.5)
start = time.time()
# Until the turn ends: Claude Code's "… for 1m 2s · done" line.
while time.time() - start < 420:
    frames.append((s.snap(), 700))
    if re.search(r'for \d+(m \d+)?s · done', s.text()) and time.time() - start > 20:
        break
    time.sleep(0.7)
s.film(4, frames, every=1.0)
(HERE / 'frames').mkdir(exist_ok=True)
(HERE / 'frames/turn.json').write_text(json.dumps(frames))
print(len(frames), 'frames', int(time.time() - start), 's')
print(s.text()[-3000:])
