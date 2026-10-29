"""Checks clawd-logs' working copy: at 100 columns the band takes two rows,
the message across the first, the file and line with the buttons on the second."""
import time
from pathlib import Path

from rec import Session

DEMO = Path.home() / 'Projects/clawd-demo-shop'
LOG = DEMO / 'wp-content/debug.log'
CART = DEMO / 'wp-content/plugins/shop/cart.php'
LINE = (f'[29-Oct-2026 15:42:00 UTC] PHP Fatal error:  Uncaught Error: Call to undefined function shop_cart_items() '
        f'in {CART}:12\nStack trace:\n#0 {{main}}\n  thrown in {CART} on line 12\n')

for cols in (100, 160):
    LOG.write_text('')
    s = Session('clawdchk', DEMO, cmd=f'claude --plugin-dir {Path.home()}/Projects/clawd-logs', cols=cols, rows=30)
    time.sleep(12)
    s.type('/git-pane close', wait=2)
    for _ in range(3):
        with LOG.open('a') as f:
            f.write(LINE)
        time.sleep(1)
    time.sleep(3)
    print(f'--- {cols} columns')
    print('\n'.join(line for line in s.text().split('\n') if 'FATAL' in line or 'cart.php' in line or '╭' in line or '╰' in line and 'Dismiss' not in line)[:2000])
    s.close()
LOG.write_text('')
