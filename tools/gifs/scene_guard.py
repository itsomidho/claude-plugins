"""clawd-guard through one turn, 124 columns: a write to .env is blocked, then
`git checkout -- .` over an uncommitted change is put to the person, who
declines. Frames go to frames/guard.json."""
import json
import re
import time
from pathlib import Path

from rec import Session

HERE = Path(__file__).parent
DEMO = Path.home() / 'Projects/clawd-demo-shop'
PROMPT = ('Set up local config in two separate steps. First, create the file .env containing DEBUG=1 '
          'with your Write tool (not the shell). Second, in its own shell command, throw away my '
          'uncommitted README edit with `git checkout -- .`. Keep your answers short.')

# An uncommitted change for the checkout to throw away.
(DEMO / 'README.md').write_text((DEMO / 'README.md').read_text() + '\nRun the tests with `node --test`.\n')
s = Session('clawdrec', DEMO, cols=124, rows=40)
time.sleep(10)
s.type('/git-pane close', wait=3)
frames = []
s.film(2, frames, every=1.0)
s.type(PROMPT, wait=0.5)
start = time.time()
asked = False
while time.time() - start < 240:
    frames.append((s.snap(), 700))
    text = s.text()
    if not asked and 'Do you want to proceed?' in text:
        # Let the question show, then decline it.
        s.film(3, frames, every=1.0, ms=1000)
        s.keys('Escape', wait=1.5)
        asked = True
    if re.search(r'for \d+(m \d+)?s · done', text) and time.time() - start > 10:
        break
    time.sleep(0.7)
s.film(4, frames, every=1.0)
(HERE / 'frames').mkdir(exist_ok=True)
(HERE / 'frames/guard.json').write_text(json.dumps(frames))
print(len(frames), 'frames', int(time.time() - start), 's', 'asked' if asked else 'never asked')
print(s.text()[-2500:])
s.close()
