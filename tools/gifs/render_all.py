"""Draws every README GIF from the recorded frames (frames/*.json) into out/.

    python3 render_all.py [name…]     # clawd board guard logs demo debug
"""
import json
import sys
from pathlib import Path

from compose import compose

HERE = Path(__file__).parent
BAR = r'◆ Opus[^\n]*'
PANE = (111, 1, 200, 42)

GIFS = {
    'clawd': dict(frames='status', box=(0, -18, 100, 0), title='clawd-statusbar · Claude Code', target_s=16, until=BAR + r'✓', captions=[
        (BAR + r'(thinking|cooking)', 'Claude starts: Clawd puts an egg in the hot pan'),
        (BAR + r'reading', 'The word beside him says what Claude does: reading,'),
        (BAR + r'editing', 'editing (the bar counts the files it changes),'),
        (BAR + r'running', 'running the tests'),
        (BAR + r'✓', 'Done: the pan comes off the heat and the egg is served ✓'),
    ]),
    'board': dict(frames='turn', box=(0, -16, 100, 0), title='clawd-tasks · Claude Code', target_s=18, start=r'Plan ·', until=r'Plan ·', captions=[
        (r'Plan · 0/', 'Claude makes a plan: the board lists its tasks under the prompt'),
        (r'│ ● [^\n]*\n[^\n]*│   │ ', 'Each tool call is filed under the task in progress, timed'),
        (r'failed', 'A step that fails shows in red'),
        (r'Plan · 3/3', 'All three done: the board leaves when the plan is finished'),
    ]),
    'guard': dict(frames='guard', box=(0, 6, 100, 32), title='clawd-guard · Claude Code', target_s=18, start=r'Set up local config', captions=[
        (r'Set up local config', 'Claude is asked to write .env, then throw away an uncommitted edit'),
        (r'BLOCKED', "Claude's Write to .env is blocked outright"),
        (r'Do you want to proceed', 'git checkout -- . over the uncommitted edit asks you first'),
        (r'ASKED YOU', 'You decline: the band says what it caught and keeps count'),
    ]),
    'logs': dict(frames='logs', box=(0, 6, 100, 27), title='clawd-logs · Claude Code', target_s=14, until=r'Fix this error[\s\S]*\n● ', captions=[
        (r'Git panel hidden', "A fatal error lands in the site's debug.log, three times"),
        (r'FATAL[\s\S]*×3', 'clawd-logs shows it above the prompt: grouped ×3, with its file and line'),
        (r'Fix this error', 'Fix hands it to Claude, stack trace included'),
    ]),
    'demo': dict(frames='git', box=PANE, title='clawd-git · Claude Code', target_s=20, captions=[
        (r'Git', 'The git panel, docked beside the conversation'),
        (r'●\d+ changed', 'Claude edits two files: they show up in the tree as it works'),
        (r'CHANGES', 'Changes lists them, with what each added and removed'),
        (r'modified · unstaged', 'A diff opens in place'),
        (r'History', 'The commit graph, all branches'),
        (r'Restore points', "A restore point was kept before Claude's turn"),
        (r'Restoring changes', 'Its preview: what a restore would put back'),
    ]),
    'debug': dict(frames='debug', box=PANE, title='clawd-debug · Claude Code', target_s=18, captions=[
        (r'FAILED', 'Five test cases run: four pass, one fails'),
        (r'PAUSED', 'The failing case reruns alone and stops at the breakpoint'),
        (r'subtotal = NaN', 'Each line shows what it set: the subtotal turns into NaN'),
    ]),
}

if __name__ == '__main__':
    (HERE / 'out').mkdir(exist_ok=True)
    for name in sys.argv[1:] or GIFS:
        spec = dict(GIFS[name])
        frames = json.loads((HERE / 'frames' / f"{spec.pop('frames')}.json").read_text())
        box = spec.pop('box')
        title = spec.pop('title')
        print(name, compose(frames, box, str(HERE / 'out' / f'{name}.gif'), title, **spec))
