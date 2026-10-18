# itsomidho plugins for Claude Code

A [Claude Code](https://claude.com/claude-code) plugin marketplace. Each plugin lives in its own repository and works on its own: install any of them, or all.

| Plugin | Release | |
|---|---|---|
| [**clawd-statusbar**](https://github.com/itsomidho/clawd-statusbar) | [![clawd-statusbar release](https://img.shields.io/github/v/release/itsomidho/clawd-statusbar?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-statusbar/releases) | A framed status bar under the prompt: model, context, usage limits with reset times, git state, MR/PR pipeline status, and Clawd frying an egg while Claude works |
| [**clawd-tasks**](https://github.com/itsomidho/clawd-tasks) | [![clawd-tasks release](https://img.shields.io/github/v/release/itsomidho/clawd-tasks?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-tasks/releases) | A live task board: Claude's plan, and under each task the steps it took, how long it ran, the files it changed and the agents it started |
| [**clawd-guard**](https://github.com/itsomidho/clawd-guard) | [![clawd-guard release](https://img.shields.io/github/v/release/itsomidho/clawd-guard?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-guard/releases) | A safety net: blocks or asks before `rm -rf` outside the project, force-pushes to main, discarding uncommitted work, `DROP TABLE` and `chmod 777`, protects `.env` and key files, and catches leaked secrets in writes and commits |
| [**clawd-notify**](https://github.com/itsomidho/clawd-notify) | [![clawd-notify release](https://img.shields.io/github/v/release/itsomidho/clawd-notify?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-notify/releases) | Tells you when Claude is done or needs your approval: a desktop notification, a chime, and optionally a push to your phone through ntfy |
| [**clawd-git**](https://github.com/itsomidho/clawd-git) | [![clawd-git release](https://img.shields.io/github/v/release/itsomidho/clawd-git?label=&color=7fbeb3)](https://github.com/itsomidho/clawd-git/releases) | A live git panel beside the conversation: the file tree, changes, colored diffs and the commit graph; marks the files Claude changed, stages and commits, and asks Claude to review a diff |

### clawd-statusbar

![clawd-statusbar through one turn: the model, context and usage limits, the project's git state, and Clawd frying an egg while Claude thinks, reads, edits, runs and browses](https://raw.githubusercontent.com/itsomidho/clawd-statusbar/main/docs/clawd.gif)

### clawd-tasks

![clawd-tasks through one plan: four tasks, each tool call filed under the task in progress, a failed test run, then all four done](https://raw.githubusercontent.com/itsomidho/clawd-tasks/main/docs/board.gif)

### clawd-guard

![clawd-guard through one turn: a force-push to main blocked, a write to .env blocked, and a git reset --hard over uncommitted work put to the person, who declines; the band above the prompt counts each catch](https://raw.githubusercontent.com/itsomidho/clawd-guard/main/docs/guard.gif)

Before Claude runs a shell command or writes a file, clawd-guard checks it: a risky call is blocked or put to you for approval, with a one-line reason, a toast and a counter above the prompt. Rules are set per user (`~/.claude/clawd-guard.json`) or per project (`.claude/clawd-guard.json`); `/guard` shows what's in effect.

### clawd-notify

![clawd-notify while you're away: a long turn ends with a desktop notification, a chime and a push to the phone; then a deploy waits on approval, and the desktop and the phone say so](https://raw.githubusercontent.com/itsomidho/clawd-notify/main/docs/notify.gif)

Only turns that ran a while notify, so quick answers you watched stay quiet. `/notify test` tries every channel; settings are under `/config`.

### clawd-git

![clawd-git through one session: Claude's edits marked, the By Claude filter, a diff with Review, staging, a drafted commit message and the commit graph](https://raw.githubusercontent.com/itsomidho/clawd-git/main/docs/demo.gif)

One panel docked beside the conversation, styled like clawd-statusbar, with tabs for the file tree (with search), the changes and the commit graph; a diff opens in place. Files Claude changes are marked, and **By Claude** narrows the list to them. Stage, unstage, discard and commit from the panel (it drafts the commit message), or send a diff to Claude for review. `/git-pane` shows or hides it. Pairs with clawd-tasks: the plan under the prompt, the files beside it.

## Install

In Claude Code, type:

```
/plugin install clawd-statusbar --marketplace itsomidho/claude-plugins
/plugin install clawd-tasks --marketplace itsomidho/claude-plugins
/plugin install clawd-guard --marketplace itsomidho/claude-plugins
/plugin install clawd-notify --marketplace itsomidho/claude-plugins
/plugin install clawd-git --marketplace itsomidho/claude-plugins
```

Answer `y` to add the marketplace the first time, then choose a scope. Once it is added, `/plugin install <plugin>@itsomidho` is enough.

From a shell:

```
claude plugin install clawd-statusbar --marketplace itsomidho/claude-plugins
claude plugin install clawd-tasks --marketplace itsomidho/claude-plugins
claude plugin install clawd-guard --marketplace itsomidho/claude-plugins
claude plugin install clawd-notify --marketplace itsomidho/claude-plugins
claude plugin install clawd-git --marketplace itsomidho/claude-plugins
```

In the desktop app: click + next to the prompt box, then Plugins, Add marketplace with `itsomidho/claude-plugins`, then Add plugin.

## Updating

```
claude plugin marketplace update itsomidho
claude plugin update <plugin>@itsomidho
```

Then `/reload-plugins`. What changed in each version is in the plugin's releases: [clawd-statusbar](https://github.com/itsomidho/clawd-statusbar/releases), [clawd-tasks](https://github.com/itsomidho/clawd-tasks/releases), [clawd-guard](https://github.com/itsomidho/clawd-guard/releases), [clawd-notify](https://github.com/itsomidho/clawd-notify/releases), [clawd-git](https://github.com/itsomidho/clawd-git/releases).

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

## License

MIT
