# itsomidho plugins for Claude Code

A [Claude Code](https://claude.com/claude-code) plugin marketplace. Each plugin lives in its own repository and works on its own: install any of them, or all.

| Plugin | Release | |
|---|---|---|
| [**clawd-statusbar**](https://github.com/itsomidho/clawd-statusbar) | [![clawd-statusbar release](https://img.shields.io/github/v/release/itsomidho/clawd-statusbar?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-statusbar/releases) | A framed status bar under the prompt: model, context, usage limits with reset times, git state, MR/PR pipeline status, and Clawd frying an egg while Claude works |
| [**clawd-tasks**](https://github.com/itsomidho/clawd-tasks) | [![clawd-tasks release](https://img.shields.io/github/v/release/itsomidho/clawd-tasks?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-tasks/releases) | A live task board: Claude's plan, and under each task the steps it took, how long it ran, the files it changed and the agents it started |
| [**clawd-guard**](https://github.com/itsomidho/clawd-guard) | [![clawd-guard release](https://img.shields.io/github/v/release/itsomidho/clawd-guard?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-guard/releases) | A safety net: blocks or asks before `rm -rf` outside the project, force-pushes to main, discarding uncommitted work, `DROP TABLE` and `chmod 777`, protects `.env` and key files, and catches leaked secrets in writes and commits |
| [**clawd-notify**](https://github.com/itsomidho/clawd-notify) | [![clawd-notify release](https://img.shields.io/github/v/release/itsomidho/clawd-notify?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-notify/releases) | Tells you when Claude is done or needs your approval: a desktop notification, a chime, and optionally a push to your phone through ntfy |
| [**clawd-git**](https://github.com/itsomidho/clawd-git) | [![clawd-git release](https://img.shields.io/github/v/release/itsomidho/clawd-git?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-git/releases) | A live git panel beside the conversation: the file tree, changes, colored diffs and the commit graph; marks the files Claude changed, stages and commits, and asks Claude to review a diff |
| [**clawd-logs**](https://github.com/itsomidho/clawd-logs) | [![clawd-logs release](https://img.shields.io/github/v/release/itsomidho/clawd-logs?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-logs/releases) | Watches your project's error logs (WordPress `debug.log`, nginx, any log file): new errors above the prompt, grouped, with a Fix button, and Claude hears about the ones its own work caused |
| [**clawd-debug**](https://github.com/itsomidho/clawd-debug) | [![clawd-debug release](https://img.shields.io/github/v/release/itsomidho/clawd-debug?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-debug/releases) | A step debugger pane: set a breakpoint, let Claude run the code with test data, and step line by line with every variable and what each line set shown next to the code (Python, Node, PHP with Xdebug) |

### clawd-statusbar

![clawd-statusbar through one real turn: the model, context and usage limits, the branch as a chip, and Clawd frying an egg and saying what Claude is doing while it works](https://raw.githubusercontent.com/itsomidho/clawd-statusbar/main/docs/clawd.gif)

A framed bar under the prompt: the model, how full the context is, the 5-hour and weekly limits with their reset times, then the project's folder, branch, uncommitted files, ahead/behind, stashes, a git operation in progress, and the branch's open MR or PR with its pipeline. On the right, Clawd fries an egg while Claude works and says what it is doing. `/statusbar` turns it off and on.

[Wiki](https://github.com/itsomidho/clawd-statusbar/wiki) · [Releases](https://github.com/itsomidho/clawd-statusbar/releases)

### clawd-tasks

![The task board through one real plan: three tasks, each tool call filed under the task in progress, a failed test run that is retried, then all three done](https://raw.githubusercontent.com/itsomidho/clawd-tasks/main/docs/board.gif)

When Claude makes a plan, the board lists its tasks under the prompt with a progress bar, and under the task in progress the steps Claude takes: each tool call, what it worked on, how long it ran, and the lines it changed. It leaves when the plan is done. `/board export` copies the plan as Markdown, for an MR description.

[Wiki](https://github.com/itsomidho/clawd-tasks/wiki) · [Releases](https://github.com/itsomidho/clawd-tasks/releases)

### clawd-guard

![clawd-guard through one real turn: a write to .env is blocked, then git checkout -- . over uncommitted work is put to the person, who declines; the band above the prompt shows each catch and counts them](https://raw.githubusercontent.com/itsomidho/clawd-guard/main/docs/guard.gif)

Before Claude runs a shell command or writes a file, clawd-guard checks it: a risky call is blocked or put to you for approval, with a one-line reason, a toast and a counter above the prompt. Rules are set per user (`~/.claude/clawd-guard.json`) or per project (`.claude/clawd-guard.json`); `/guard` shows what's in effect.

[Wiki](https://github.com/itsomidho/clawd-guard/wiki) · [Releases](https://github.com/itsomidho/clawd-guard/releases)

### clawd-notify

![clawd-notify while you're away: a long turn ends with a desktop notification, a chime and a push to the phone; then a deploy waits on approval, and the desktop and the phone say so](https://raw.githubusercontent.com/itsomidho/clawd-notify/main/docs/notify.gif)

Only turns that ran a while notify, so quick answers you watched stay quiet. `/notify test` tries every channel; settings are under `/config`.

[Wiki](https://github.com/itsomidho/clawd-notify/wiki) · [Releases](https://github.com/itsomidho/clawd-notify/releases)

### clawd-git

![The panel through one real session: Claude changes two files, marked ✦ in Files and Changes; a diff, the commit graph, and the turn's restore point](https://raw.githubusercontent.com/itsomidho/clawd-git/main/docs/demo.gif)

One panel docked beside the conversation, drawn like clawd-debug's: a header with the branch and a key bar, and tabs for the file tree (with search), the changes, the commit graph and **restore points**. Files Claude changes are marked, and **By Claude** narrows the list to them; **This turn** shows exactly what Claude changed since your last message. Stage, unstage, discard and commit from the panel (it drafts the message), write review notes on diff lines and send them to Claude. Before each of Claude's turns it keeps a restore point, and **Restore** puts every file back, shell changes included, kept apart from your history. `/git-pane` shows or hides it.

[Wiki](https://github.com/itsomidho/clawd-git/wiki) · [Releases](https://github.com/itsomidho/clawd-git/releases)

### clawd-logs

![clawd-logs in a real session: a PHP fatal error lands in debug.log three times, the band above the prompt shows it once with ×3, and Fix hands it to Claude](https://raw.githubusercontent.com/itsomidho/clawd-logs/main/docs/logs.gif)

New errors in the project's logs show above the prompt, grouped with a count, with **Fix** (send it to Claude), **Debug** (open the file and line in clawd-debug, when installed) and **Dismiss**. It finds WordPress's `debug.log` (and Bedrock's, Laravel's, and a wpdev stack's nginx log) by itself; add other files in `.claude/clawd-logs.json`. When an error appears while Claude works, Claude reads it, stack trace included, right after the tool call that caused it. `/logs` lists the session's errors.

[Wiki](https://github.com/itsomidho/clawd-logs/wiki) · [Releases](https://github.com/itsomidho/clawd-logs/releases)

### clawd-debug

![clawd-debug in a real session: five test cases run and one fails; a breakpoint goes in cart.js, the failing case reruns alone, and stepping shows its total turn into NaN](https://raw.githubusercontent.com/itsomidho/clawd-debug/main/docs/debug.gif)

A debugger beside the conversation, no editor needed. `/dbg <file>` shows the file; press `b` for a breakpoint and `t`, and Claude writes test cases with the results they should give, runs them and shows a ✓/✗ table; a failing case reruns alone, stopping at your breakpoints. Step with `n` `s` `o` `c` while every value shows next to its line; add watches, conditional breakpoints, and explore objects in place. Python (debugpy, `/dbg setup`), Node (built in) and PHP with Xdebug, also inside a Docker container, with WordPress loaded through WP-CLI. clawd-git's ▷ and clawd-logs' **Debug** open files here.

[Wiki](https://github.com/itsomidho/clawd-debug/wiki) · [Releases](https://github.com/itsomidho/clawd-debug/releases)

## Install

In Claude Code, type:

```
/plugin install clawd-statusbar --marketplace itsomidho/claude-plugins
/plugin install clawd-tasks --marketplace itsomidho/claude-plugins
/plugin install clawd-guard --marketplace itsomidho/claude-plugins
/plugin install clawd-notify --marketplace itsomidho/claude-plugins
/plugin install clawd-git --marketplace itsomidho/claude-plugins
/plugin install clawd-logs --marketplace itsomidho/claude-plugins
/plugin install clawd-debug --marketplace itsomidho/claude-plugins
```

Answer `y` to add the marketplace the first time, then choose a scope. Once it is added, `/plugin install <plugin>@itsomidho` is enough.

From a shell:

```
claude plugin install clawd-statusbar --marketplace itsomidho/claude-plugins
claude plugin install clawd-tasks --marketplace itsomidho/claude-plugins
claude plugin install clawd-guard --marketplace itsomidho/claude-plugins
claude plugin install clawd-notify --marketplace itsomidho/claude-plugins
claude plugin install clawd-git --marketplace itsomidho/claude-plugins
claude plugin install clawd-logs --marketplace itsomidho/claude-plugins
claude plugin install clawd-debug --marketplace itsomidho/claude-plugins
```

In the desktop app: click + next to the prompt box, then Plugins, Add marketplace with `itsomidho/claude-plugins`, then Add plugin.

## Updating

```
claude plugin marketplace update itsomidho
claude plugin update <plugin>@itsomidho
```

Then `/reload-plugins`. What changed in each version is in the plugin's releases: [clawd-statusbar](https://github.com/itsomidho/clawd-statusbar/releases), [clawd-tasks](https://github.com/itsomidho/clawd-tasks/releases), [clawd-guard](https://github.com/itsomidho/clawd-guard/releases), [clawd-notify](https://github.com/itsomidho/clawd-notify/releases), [clawd-git](https://github.com/itsomidho/clawd-git/releases), [clawd-logs](https://github.com/itsomidho/clawd-logs/releases), [clawd-debug](https://github.com/itsomidho/clawd-debug/releases).

## Troubleshooting

**`Host key verification failed` on install or update.** Claude Code fetched a plugin from GitHub over SSH, and this machine has no SSH key for GitHub. Either add one (`ssh-keygen -t ed25519`, add it to your GitHub account, then `ssh -T git@github.com` once to accept GitHub's host key), or have git use HTTPS for GitHub:

```
git config --global url."https://github.com/".insteadOf git@github.com:
```

Installing from a shell (`claude plugin install …`) also falls back to HTTPS by itself; updating does not.

**A plugin is not found, or a new version doesn't show.** Your copy of the marketplace is older than this repository. Refresh it, then install or update again:

```
claude plugin marketplace update itsomidho
```

**You added `itsomidho` from `itsomidho/clawd-statusbar` before.** That older marketplace lists only clawd-statusbar, and two marketplaces can't share a name. Switch to this one (removing the old marketplace may uninstall clawd-statusbar; installing puts it back):

```
/plugin marketplace remove itsomidho
/plugin install clawd-statusbar --marketplace itsomidho/claude-plugins
```

**A plugin is installed but misbehaves.** Each plugin's README has its own troubleshooting: [clawd-statusbar](https://github.com/itsomidho/clawd-statusbar#troubleshooting), [clawd-tasks](https://github.com/itsomidho/clawd-tasks#troubleshooting).

## Adding a plugin

Add an entry to `.claude-plugin/marketplace.json` whose `source` names the plugin's repository, then check it:

```
claude plugin validate .
```

## Tools

[`tools/`](tools) keeps the docs current: `tools/wiki/build.py` rebuilds every plugin's GitHub wiki from its README, settings and releases, and `tools/gifs/` records the README GIFs from real Claude Code sessions. See [tools/README.md](tools/README.md).

## License

MIT
