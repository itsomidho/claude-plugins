"""clawd-rtl in the demo shop, 100 columns: a prompt in Persian and Claude's
Persian reply, both drawn right to left. Frames go to frames/rtl.json."""
import json
import re
import time
from pathlib import Path

from rec import Session

HERE = Path(__file__).parent
DEMO = Path.home() / 'Projects/clawd-demo-shop'
PROMPT = (
    'فایل src/cart.js را بخوان و به فارسی و کوتاه توضیح بده: '
    'یک جملهٔ کوتاه، یک فهرست سه‌موردی از کارهایش، و یک جدول کوچک از تابع‌ها با ستون‌های «تابع» و «کار». '
    'هیچ فایلی را تغییر نده.'
)

# CLAWD_RTL_DIR records a working copy (claude --plugin-dir) instead of the installed one.
import os
CMD = f"claude --plugin-dir {os.environ['CLAWD_RTL_DIR']}" if os.environ.get('CLAWD_RTL_DIR') else 'claude'
s = Session('clawdrec', DEMO, cmd=CMD, cols=100, rows=40)
time.sleep(10)
if 'trust this folder' in s.text():
    s.keys('Down', 'Enter', wait=1)
    time.sleep(8)
s.type('/git-pane close', wait=3)
frames = []
s.film(2, frames, every=1.0)
s.type(PROMPT, wait=0.5)
start = time.time()
while time.time() - start < 300:
    frames.append((s.snap(), 400))
    if re.search(r'for \d+(m \d+)?s · done', s.text()) and time.time() - start > 10:
        break
    time.sleep(0.4)
s.film(3, frames, every=1.0)
(HERE / 'frames').mkdir(exist_ok=True)
(HERE / 'frames/rtl.json').write_text(json.dumps(frames))
print(len(frames), 'frames', int(time.time() - start), 's')
print(s.text())
s.close()
