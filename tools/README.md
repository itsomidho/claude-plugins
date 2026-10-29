# Tools

What keeps the clawd plugins' docs current. Neither is needed to install or run a plugin.

## wiki: the GitHub wikis

`wiki/build.py` writes every clawd plugin's wiki from its own sources: the README (split by its sections into Usage, Settings, How it works and Troubleshooting), the settings `.claude-plugin/plugin.json` declares, and the GitHub releases (the Changelog). Each wiki gets Home, Installation, Usage, Settings, Development and Changelog, plus How it works and Troubleshooting where the README has them, a sidebar and a footer.

It expects the plugins checked out beside this repository (`~/Projects/clawd-git` …) and each wiki cloned under `~/Projects/clawd-wikis/<plugin>` (or the folder `CLAWD_WIKIS` names):

```
git clone https://github.com/itsomidho/clawd-git.wiki.git ~/Projects/clawd-wikis/clawd-git
```

After a release:

```
python3 tools/wiki/build.py clawd-git        # or no name: all seven
cd ~/Projects/clawd-wikis/clawd-git && git add -A && git commit -m "Wiki rebuilt" && git push
```

Edit the README, not a wiki page: the next build writes the page again.

## gifs: the README GIFs

The GIFs in each plugin's README are recordings of real Claude Code sessions in a made-up project (`~/Projects/clawd-demo-shop`), never real work: they are public.

- `gifs/rec.py` drives a throwaway Claude Code in its own tmux server (prompts, keys, mouse clicks and the wheel), snaps the screen with its colours, and draws the snaps as a GIF with the terminal's fonts (JetBrains Mono Nerd Font, with DejaVu and Noto Symbols for what it lacks). It leaves out hyperlink codes and the session's title, and writes home folders as `~`.
- `gifs/scene_*.py` record one plugin each into `gifs/frames/` (kept out of git), so a GIF can be cropped or drawn again without recording again; `gifs/check_*.py` replay a fix in a real session.

Needs tmux, Python 3 with Pillow and fontTools, and the fonts above.
