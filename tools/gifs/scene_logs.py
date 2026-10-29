"""clawd-logs, 124 columns: a PHP fatal error lands in the demo site's
debug.log (three times), the band shows it grouped, and Fix hands it to Claude,
which adds the missing function. Frames go to frames/logs.json."""
import json
import re
import time
from pathlib import Path

from rec import Session

HERE = Path(__file__).parent
DEMO = Path.home() / 'Projects/clawd-demo-shop'
LOG = DEMO / 'wp-content/debug.log'
CART = DEMO / 'wp-content/plugins/shop/cart.php'
FATAL = ("[29-Oct-2026 15:42:0N UTC] PHP Fatal error:  Uncaught Error: Call to undefined function shop_cart_items() "
         f"in {CART}:12\nStack trace:\n#0 {DEMO}/wp-content/themes/shop/cart-page.php(8): shop_render_cart()\n#1 {{main}}\n"
         f"  thrown in {CART} on line 12\n")

LOG.write_text('')
s = Session('clawdrec', DEMO, cols=100, rows=32)
time.sleep(12)
s.type('/git-pane close', wait=3)
frames = []
s.film(2, frames, every=1.0)
for n in range(3):
    with LOG.open('a') as f:
        f.write(FATAL.replace('0N UTC', f'0{n} UTC'))
    s.film(1.5, frames, every=0.5)
s.film(4, frames, every=0.7)
# Fix: the error and its stack trace go to Claude.
for i, line in enumerate(s.text().split('\n')):
    at = line.find(' Fix ')
    if at >= 0:
        s.click(i + 1, len(line[:at].encode('utf-16-le')) // 2 + 3, wait=0.3)
        break
start = time.time()
while time.time() - start < 180:
    frames.append((s.snap(), 400))
    if re.search(r'for \d+(m \d+)?s · done', s.text()) and time.time() - start > 8:
        break
    time.sleep(0.4)
s.film(3, frames, every=1.0)
(HERE / 'frames').mkdir(exist_ok=True)
(HERE / 'frames/logs.json').write_text(json.dumps(frames))
print(len(frames), 'frames')
print(s.text()[-3500:])
s.close()
