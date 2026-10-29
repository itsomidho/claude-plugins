"""Checks clawd-guard's working copy blocks a shell write to .env in a real session."""
import re
import time
from pathlib import Path

from rec import Session

DEMO = Path.home() / 'Projects/clawd-demo-shop'
s = Session('clawdchk', DEMO, cmd=f'claude --plugin-dir {Path.home()}/Projects/clawd-guard', cols=124, rows=40)
time.sleep(12)
s.type('/git-pane close', wait=3)
s.type('Run exactly this one shell command and nothing else, then stop: echo DEBUG=1 > .env', wait=1)
start = time.time()
while time.time() - start < 120:
    if re.search(r'for \d+(m \d+)?s · done', s.text()) and time.time() - start > 5:
        break
    time.sleep(1)
time.sleep(2)
print(s.text())
print('.env exists:', (DEMO / '.env').exists())
s.close()
