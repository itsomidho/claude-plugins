# itsomidho plugins for Claude Code

A [Claude Code](https://claude.com/claude-code) plugin marketplace. Each plugin lives in its own repository and works on its own: install any of them, or all.

| Plugin | |
|---|---|
| [**clawd-statusbar**](https://github.com/itsomidho/clawd-statusbar) | A framed status bar under the prompt: model, context, usage limits with reset times, git state, MR/PR pipeline status, and Clawd frying an egg while Claude works |
| [**clawd-tasks**](https://github.com/itsomidho/clawd-tasks) | A live task board: Claude's plan, and under each task the steps it took, how long it ran, the files it changed and the agents it started |
| [**clawd-guard**](https://github.com/itsomidho/clawd-guard) | A safety net: blocks or asks before `rm -rf` outside the project, force-pushes to main, discarding uncommitted work, `DROP TABLE` and `chmod 777`, protects `.env` and key files, and catches leaked secrets in writes and commits |

### clawd-statusbar

![clawd-statusbar through one turn: the model, context and usage limits, the project's git state, and Clawd frying an egg while Claude thinks, reads, edits, runs and browses](https://raw.githubusercontent.com/itsomidho/clawd-statusbar/main/docs/clawd.gif)

### clawd-tasks

![clawd-tasks through one plan: four tasks, each tool call filed under the task in progress, a failed test run, then all four done](https://raw.githubusercontent.com/itsomidho/clawd-tasks/main/docs/board.gif)

### clawd-guard

![clawd-guard through one turn: a force-push to main blocked, a write to .env blocked, and a git reset --hard over uncommitted work put to the person, who declines; the band above the prompt counts each catch](https://raw.githubusercontent.com/itsomidho/clawd-guard/main/docs/guard.gif)

Before Claude runs a shell command or writes a file, clawd-guard checks it: a risky call is blocked or put to you for approval, with a one-line reason, a toast and a counter above the prompt. Rules are set per user (`~/.claude/clawd-guard.json`) or per project (`.claude/clawd-guard.json`); `/guard` shows what's in effect.

## Install

In Claude Code, type:

```
/plugin install clawd-statusbar --marketplace itsomidho/claude-plugins
/plugin install clawd-tasks --marketplace itsomidho/claude-plugins
/plugin install clawd-guard --marketplace itsomidho/claude-plugins
```

Answer `y` to add the marketplace the first time, then choose a scope. Once it is added, `/plugin install <plugin>@itsomidho` is enough.

From a shell:

```
claude plugin install clawd-statusbar --marketplace itsomidho/claude-plugins
claude plugin install clawd-tasks --marketplace itsomidho/claude-plugins
claude plugin install clawd-guard --marketplace itsomidho/claude-plugins
```

In the desktop app: click + next to the prompt box, then Plugins, Add marketplace with `itsomidho/claude-plugins`, then Add plugin.

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
