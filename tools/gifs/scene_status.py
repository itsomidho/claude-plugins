"""clawd-statusbar through one real turn, 100 columns, the task board hidden:
Clawd cooks while Claude reads, edits and runs the tests, the bar counts the
changed files, and the egg is served. Frames go to frames/status.json."""
import json
import re
import time
from pathlib import Path

from rec import Session

HERE = Path(__file__).parent
DEMO = Path.home() / 'Projects/clawd-demo-shop'
PROMPT = ('Read src/discounts.js, add a SPRING15 coupon (15 percent) to it, then run '
          "node --test 'tests/*.test.js'. No plan, no summary: one short line at the end.")

s = Session('clawdrec', DEMO, cols=100, rows=30)
time.sleep(12)
s.type('/git-pane close', wait=2)
s.type('/board close', wait=2)
s.keys('C-l', wait=1)
frames = []
s.film(2.5, frames, every=0.5)
s.type(PROMPT, wait=0.3)
start = time.time()
while time.time() - start < 240:
    frames.append((s.snap(), 350))
    if re.search(r'for \d+(m \d+)?s · done', s.text()) and time.time() - start > 8:
        break
    time.sleep(0.35)
s.film(5, frames, every=0.5)
(HERE / 'frames').mkdir(exist_ok=True)
(HERE / 'frames/status.json').write_text(json.dumps(frames))
print(len(frames), 'frames')
print('\n'.join(s.text().split('\n')[-12:]))
s.close()
