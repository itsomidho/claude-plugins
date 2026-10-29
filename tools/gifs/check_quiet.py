"""Checks clawd-statusbar's working copy: a normal turn still streams, and a
turn whose API requests keep failing shows Clawd waiting ("no reply")."""
import re
import time
from pathlib import Path

from rec import Session

DEMO = Path.home() / 'Projects/clawd-demo-shop'
PLUGIN = Path.home() / 'Projects/clawd-statusbar'


def status(s):
    return '\n'.join(s.text().split('\n')[-5:])


# 1. A normal turn.
s = Session('clawdchk', DEMO, cmd=f'claude --plugin-dir {PLUGIN}', cols=124, rows=40)
time.sleep(12)
s.type('/git-pane close', wait=3)
s.type('Reply with exactly: hello from the demo shop', wait=1)
start = time.time()
while time.time() - start < 90 and not re.search(r'for \d+(m \d+)?s · done', s.text()):
    time.sleep(1)
print('NORMAL TURN answered:', 'hello from the demo shop' in s.text().lower())
print(status(s))
s.close()

# 2. Every request fails (a closed port): the API error is retried.
s = Session('clawdchk', DEMO, cmd=f'ANTHROPIC_BASE_URL=http://127.0.0.1:9 claude --plugin-dir {PLUGIN}', cols=124, rows=40)
time.sleep(12)
s.type('/git-pane close', wait=3)
s.type('Reply with one word.', wait=1)
for at in (5, 22):
    time.sleep(at - (5 if at == 22 else 0))
    print(f'--- {at}s after sending')
    print('\n'.join(line for line in s.text().split('\n')[-14:] if line.strip()))
s.keys('Escape', wait=1)
s.close()
