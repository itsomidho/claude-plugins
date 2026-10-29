"""clawd-git through one session, 200 columns with the panel docked: Claude
changes two files (marked ✦), then the panel is walked through: Files, Changes,
a diff, This turn, Commits, Restore. Frames go to frames/git.json."""
import json
import re
import time
from pathlib import Path

from rec import Session

HERE = Path(__file__).parent
DEMO = Path.home() / 'Projects/clawd-demo-shop'
PROMPT = ('Add a SPRING15 coupon (15 percent) to src/discounts.js, and a line to README.md saying coupon codes '
          'are not case-sensitive. Keep your answer to one line.')

s = Session('clawdrec', DEMO, cols=200, rows=50)
time.sleep(12)
frames = []


def film(sec, every=0.6):
    s.film(sec, frames, every=every)


def press(label, after=None, pause=2.5, dx=2):
    """Clicks the first `label` on the panel's side of the screen."""
    for i, line in enumerate(s.text().split('\n')):
        at = line.find(label, 105)
        if at >= 0 and (after is None or after in line):
            s.click(i + 1, len(line[:at].encode('utf-16-le')) // 2 + 1 + dx, wait=0.3)
            film(pause)
            return True
    print('not found:', label)
    return False


s.type('/git-pane files', wait=3)
film(2)
s.type(PROMPT, wait=0.5)
start = time.time()
while time.time() - start < 180:
    frames.append((s.snap(), 700))
    if re.search(r'for \d+(m \d+)?s · done', s.text()) and time.time() - start > 8:
        break
    time.sleep(0.7)
film(2)
# Files: open src, where Claude's file is marked.
press(' src', after='│')
press('Changes', after='Files')
press('discounts.js', after='+')
s.keys('h', wait=0.3); film(2)
s.keys('t', wait=0.3); film(3)
s.keys('h', wait=0.3); film(1.5)
press('Commits', after='Files')
press('Restore', after='Files', pause=3)
press('before “', pause=3)
s.keys('h', wait=0.3); film(2)
(HERE / 'frames').mkdir(exist_ok=True)
(HERE / 'frames/git.json').write_text(json.dumps(frames))
print(len(frames), 'frames')
print('\n'.join(line[105:] for line in s.text().split('\n')[:30]))
s.close()
