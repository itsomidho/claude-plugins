#!/usr/bin/env python3
"""Builds the GitHub wiki of every clawd-* plugin from its own sources.

Each wiki gets the same pages: Home, Installation, Usage, Settings, How it
works, Troubleshooting, Development and Changelog (when the plugin has the
material), plus _Sidebar and _Footer. The text comes from the plugin's README
(split by its sections), its settings from .claude-plugin/plugin.json, and the
Changelog from its GitHub releases, so a rebuild after a release keeps the
wiki true.

    python3 tools/wiki/build.py [plugin…]   # writes ~/Projects/clawd-wikis/<plugin>/*.md

The plugins' checkouts sit beside this repository (~/Projects/<plugin>), and
each ~/Projects/clawd-wikis/<plugin>/ is a clone of
github.com/itsomidho/<plugin>.wiki.git (branch master): after a build, commit
and push in that folder. CLAWD_WIKIS sets another folder for the clones.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import os

HERE = Path(__file__).resolve().parent
# This repository is ~/Projects/claude-plugins; the plugins sit beside it.
MARKET_DIR = HERE.parent.parent
PROJECTS = MARKET_DIR.parent
WIKIS = Path(os.environ.get('CLAWD_WIKIS', PROJECTS / 'clawd-wikis'))
OWNER = 'itsomidho'
MARKET = 'itsomidho/claude-plugins'
PLUGINS = ['clawd-statusbar', 'clawd-tasks', 'clawd-guard', 'clawd-notify', 'clawd-git', 'clawd-logs', 'clawd-debug']

# Which README sections make up each page, in order. Sections a plugin does not
# have are skipped; a page with no section is not written (Settings is always,
# from plugin.json). "intro" is the README's text before its first section.
PAGES = {
    'clawd-statusbar': {'Usage': ['What it shows'], 'Requirements': ['Requirements'], 'Settings': ['Settings'],
                        'How it works': ['How it works'], 'Troubleshooting': ['Troubleshooting'], 'Development': ['Development']},
    'clawd-tasks': {'Usage': ['What it shows', 'Commands'], 'Requirements': ['Requirements'], 'Settings': ['Settings'],
                    'How it works': ['How it works'], 'Troubleshooting': ['Troubleshooting'], 'Development': ['Development']},
    'clawd-guard': {'Usage': ['Rules', 'Commands'], 'Settings': ['Configure'], 'Troubleshooting': ['Good to know']},
    'clawd-notify': {'Usage': ['Commands'], 'Settings': ['Settings'], 'Troubleshooting': ['Good to know']},
    'clawd-git': {'Usage': ['What it shows', 'Use'], 'Settings': ['Settings'], 'Development': ['Development']},
    'clawd-logs': {'Usage': ['The band', 'Commands', 'wpdev'], 'Settings': ['Settings', 'Config file'], 'Troubleshooting': ['Good to know']},
    'clawd-debug': {'Usage': ['How you use it', 'Test cases', 'Keys', 'What each language needs'], 'Settings': ['Settings'],
                    'How it works': ['How it works'], 'Development': ['Development']},
}
ORDER = ['Home', 'Installation', 'Usage', 'Settings', 'How it works', 'Troubleshooting', 'Development', 'Changelog']


def slug(page):
    return page.replace(' ', '-')


def wiki_url(plugin, page='Home', anchor=''):
    return f'https://github.com/{OWNER}/{plugin}/wiki/{"" if page == "Home" else slug(page)}{anchor}'


def sections(md):
    """The README as (intro, {title: body}) by its '## ' sections; ### stay inside."""
    out, title, lines, intro = {}, None, [], []
    for line in md.split('\n'):
        m = re.match(r'^## (.+?)\s*$', line)
        if m:
            if title is None:
                intro = lines
            else:
                out[title] = '\n'.join(lines).strip('\n')
            title, lines = m.group(1), []
            continue
        lines.append(line)
    if title is None:
        intro = lines
    else:
        out[title] = '\n'.join(lines).strip('\n')
    return '\n'.join(intro).strip('\n'), out


def fix_links(text, plugin, anchors):
    """README links made to work from the wiki: images from raw, files from the repo, #anchors to their page."""
    raw = f'https://raw.githubusercontent.com/{OWNER}/{plugin}/main/'
    blob = f'https://github.com/{OWNER}/{plugin}/blob/main/'

    def image(m):
        return f'![{m.group(1)}]({m.group(2) if m.group(2).startswith("http") else raw + m.group(2)})'

    def link(m):
        target = m.group(2)
        if target.startswith('#'):
            page = anchors.get(target[1:])
            return f'[{m.group(1)}]({wiki_url(plugin, page, target) if page else target})'
        return f'[{m.group(1)}]({blob + target})'

    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', image, text)
    return re.sub(r'(?<!!)\[([^\]]+)\]\((?!https?:|mailto:)([^)]+)\)', link, text)


def heading_slug(title):
    return re.sub(r'[^\w\- ]', '', title.lower()).strip().replace(' ', '-')


def drop_shared(body):
    """Install problems every plugin shares live on Installation: leave them out here."""
    blocks = re.split(r'\n(?=\*\*)', body)
    kept = [b for b in blocks if not re.match(r'\*\*(`Host key verification failed`|`/[a-z-]+` is listed twice)', b)]
    return '\n'.join(kept).strip('\n')


def settings_table(manifest):
    options = manifest.get('userConfig') or {}
    if not options:
        return ''
    rows = ['| Setting | Key | Default | What it does |', '|---|---|---|---|']
    for key, one in options.items():
        default = one.get('default')
        shown = '' if default in (None, '') else f'`{json.dumps(default) if not isinstance(default, str) else default}`'
        choices = f' One of: {", ".join(f"`{c}`" for c in one["options"])}.' if one.get('options') else ''
        text = (one.get('description') or '').replace('|', '\\|').replace('\n', ' ')
        rows.append(f'| {one.get("title", key)} | `{key}` | {shown} | {text}{choices} |')
    return '\n'.join(rows)


def releases(plugin):
    out = subprocess.run(['gh', 'api', f'repos/{OWNER}/{plugin}/releases?per_page=100'], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def changelog(plugin):
    parts = [f'Every release of {plugin}, newest first, as published on [GitHub](https://github.com/{OWNER}/{plugin}/releases).', '']
    for one in releases(plugin):
        date = (one.get('published_at') or '')[:10]
        body = (one.get('body') or '').strip() or '_No notes._'
        parts += [f'## {one["tag_name"]} · {date}', '', body, '']
    return '\n'.join(parts).strip() + '\n'


def installation(plugin, extra):
    text = f'''## Install

In Claude Code, type:

```
/plugin install {plugin} --marketplace {MARKET}
```

Answer `y` to add the marketplace if asked, then choose a scope. From a shell:

```
claude plugin install {plugin} --marketplace {MARKET}
```

In the desktop app, where `/plugin` does not run: click **+** next to the prompt box, then **Plugins**, **Add marketplace** with `{MARKET}`, then **Add plugin**.

The [`itsomidho` marketplace](https://github.com/{MARKET}) lists every [clawd plugin](#the-clawd-family); each works on its own.
'''
    if extra.strip():
        text += f'\n## Requirements\n\n{extra.strip()}\n'
    text += f'''
## Update

```
claude plugin marketplace update itsomidho
claude plugin update {plugin}@itsomidho
```

Then run `/reload-plugins`, or restart Claude Code.

## Uninstall

```
claude plugin uninstall {plugin}@itsomidho
```

## Run a working copy

Start Claude Code with `claude --plugin-dir /path/to/{plugin}` to run a checkout instead of the installed copy; edits reload when a turn ends. Disable the installed copy with `/plugin` meanwhile, or both load.

## Install problems

**`Host key verification failed` on install or update.** Claude Code fetched the plugin from GitHub over SSH, and this machine has no SSH key for GitHub. Either add one (`ssh-keygen -t ed25519`, add it to your GitHub account, then `ssh -T git@github.com` once to accept GitHub's host key), or have git use HTTPS for GitHub:

```
git config --global url."https://github.com/".insteadOf git@github.com:
```

Installing from a shell (`claude plugin install …`) also falls back to HTTPS by itself; updating does not.

**A command is listed twice, or something draws twice.** Two copies of the plugin are loaded, such as the installed one and a working copy started with `--plugin-dir`. Run one: start Claude Code without `--plugin-dir`, or disable the installed copy with `/plugin` while you work on yours.

## The clawd family
'''
    return text + family_table() + '\n'


def family_table():
    market = json.loads((MARKET_DIR / '.claude-plugin/marketplace.json').read_text())
    about = {p['name']: p.get('description', '') for p in market['plugins']}
    rows = ['| Plugin | |', '|---|---|']
    rows += [f'| [{p}]({wiki_url(p)}) | {about.get(p, "")} |' for p in PLUGINS]
    return '\n'.join(rows)


def development(plugin, body):
    text = (body.strip() + '\n\n') if body.strip() else ''
    return text + f'''## Releasing

A release is a version bump in `.claude-plugin/plugin.json` pushed to `main`: the repository's `release` workflow then tags it `vX.Y.Z` and publishes a GitHub release whose notes are the commit's message (less its first line). A version tagged by hand is left alone.

1. Bump `version` in `.claude-plugin/plugin.json`; update the README when behaviour changed.
2. `claude plugin validate .` and `claude plugin test .`
3. Commit to `main` as `{plugin} X.Y.Z: <what changed>`, with the notes as bullets in the body, and push.

Installed copies pick it up with `claude plugin update {plugin}@itsomidho`.

## Source

[github.com/{OWNER}/{plugin}](https://github.com/{OWNER}/{plugin}) · [issues](https://github.com/{OWNER}/{plugin}/issues) · MIT
'''


def build(plugin):
    repo = PROJECTS / plugin
    readme = (repo / 'README.md').read_text()
    manifest = json.loads((repo / '.claude-plugin/plugin.json').read_text())
    intro, parts = sections(readme)
    plan = PAGES[plugin]

    # Where each README heading lands, for its #anchor links.
    anchors = {}
    for page, titles in plan.items():
        for title in titles:
            if title in parts:
                anchors[heading_slug(title)] = 'Installation' if page == 'Requirements' else page
                for sub in re.findall(r'^### (.+)$', parts[title], re.M):
                    anchors[heading_slug(sub)] = page
    fix = lambda text: fix_links(text, plugin, anchors)

    pages = {}
    # Home: what it is (the README's opening, without its title and badge), then the pages.
    opening = '\n'.join(line for line in intro.split('\n') if not line.startswith('# ') and not line.startswith('[![')).strip()
    home = [fix(opening), '', '## In this wiki', '']
    pages['Home'] = home
    pages['Installation'] = installation(plugin, fix('\n\n'.join(parts[t] for t in plan.get('Requirements', []) if t in parts)))

    for page in ['Usage', 'How it works', 'Troubleshooting']:
        chosen = [t for t in plan.get(page, []) if t in parts]
        if not chosen:
            continue
        body = []
        for title in chosen:
            text = parts[title]
            if page == 'Troubleshooting':
                text = drop_shared(text)
            # One section on its own page needs no heading of its own.
            body.append(fix(text) if len(chosen) == 1 else f'## {title}\n\n{fix(text)}')
        pages[page] = '\n\n'.join(body).strip() + '\n'

    settings = [fix(parts[t]) if len(plan.get('Settings', [])) == 1 else f'## {t}\n\n{fix(parts[t])}' for t in plan.get('Settings', []) if t in parts]
    table = settings_table(manifest)
    if table:
        settings.append(f'## Every option\n\nAs `{plugin}` declares them; set them in `/plugin` (or `/config`), or from a shell with `claude plugin configure {plugin}@itsomidho`.\n\n{table}')
    pages['Settings'] = '\n\n'.join(settings).strip() + '\n'

    dev = '\n\n'.join(fix(parts[t]) for t in plan.get('Development', []) if t in parts)
    pages['Development'] = development(plugin, dev)
    pages['Changelog'] = changelog(plugin)

    names = [p for p in ORDER if p in pages]
    about = {
        'Installation': 'install, update, uninstall, and install problems',
        'Usage': 'what it shows and how to use it',
        'Settings': 'every option',
        'How it works': 'what runs, and where',
        'Troubleshooting': 'when something does not look right',
        'Development': 'tests, working copies and releases',
        'Changelog': 'every release',
    }
    home += [f'- [{p}]({wiki_url(plugin, p)}): {about[p]}' for p in names if p != 'Home']
    home += ['', '## The clawd family', '', family_table(), '']
    pages['Home'] = '\n'.join(home)

    out = WIKIS / plugin
    out.mkdir(parents=True, exist_ok=True)
    for page, text in pages.items():
        (out / f'{slug(page)}.md').write_text(text if text.endswith('\n') else text + '\n')
    sidebar = [f'**[{plugin}]({wiki_url(plugin)})** {manifest["version"]}', '']
    sidebar += [f'- [{p}]({wiki_url(plugin, p)})' for p in names if p != 'Home']
    sidebar += ['', '**The clawd family**', ''] + [f'- [{p}]({wiki_url(p)})' for p in PLUGINS]
    (out / '_Sidebar.md').write_text('\n'.join(sidebar) + '\n')
    (out / '_Footer.md').write_text(
        f'[{plugin}](https://github.com/{OWNER}/{plugin}) · [releases](https://github.com/{OWNER}/{plugin}/releases) · '
        f'part of the [clawd family]({wiki_url(plugin, "Installation", "#the-clawd-family")}) · MIT\n')
    return names


if __name__ == '__main__':
    for one in (sys.argv[1:] or PLUGINS):
        print(one, ', '.join(build(one)))
